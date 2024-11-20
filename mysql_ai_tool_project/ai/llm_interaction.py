from openai import OpenAI
from mysql_ai_tool_project.config import API_KEY, BASE_URL, MODEL_NAME
from mysql_ai_tool_project.utils.prompts import sql_prompt, extract_sql_prompt, clarify_prompt, answer_prompt
from tabulate import tabulate
import mysql.connector
from mysql_ai_tool_project.db.utils import get_database_structure_with_samples

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_sql(user_question, conversation_history=None, connection=None):
    """
    生成 SQL 查询并通过澄清提示优化。
    Args:
        user_question: 用户当前问题。
        conversation_history: 对话历史。
        connection: 数据库连接对象。

    Returns:
        str: 生成的 SQL 查询。
    """
    if conversation_history is None:
        conversation_history = []
    if connection is None:
        raise ValueError("Connection must be provided to generate database structure.")

    # 获取包含随机样本数据的数据库结构
    database_structure = get_database_structure_with_samples(connection)

    # 构造对话历史
    history_prompt = "\n".join(
        [f"用户：{entry['user']}\nLLM：{entry['response']}" for entry in conversation_history]
    )

    # 构造澄清提示
    clarify_prompt_text = clarify_prompt.format(
        conversation_history=history_prompt,
        database_structure=database_structure,
        user_question=user_question,
    )

    # 调用 LLM 进行澄清
    clarification_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": clarify_prompt_text}],
        temperature=0.7,
    )
    clarified_user_question = clarification_completion.choices[0].message.content

    print(f"\n[DEBUG] LLM Clarification Output:\n{clarified_user_question}")

    # 构造 SQL 生成提示
    full_prompt = f"{history_prompt}\n用户：{clarified_user_question}"
    prompt = sql_prompt.format(user_question=full_prompt)

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    llm_output = completion.choices[0].message.content

    print(f"\n[DEBUG] LLM SQL Generation Output:\n{llm_output}")

    # 提取有效 SQL 查询
    extract_prompt_text = extract_sql_prompt.format(llm_output=llm_output)
    extraction_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": extract_prompt_text}],
        temperature=0.3,
    )
    sql_query = extraction_completion.choices[0].message.content

    print(f"\n[DEBUG] LLM SQL Extraction Output:\n{sql_query}")

    # 清理并返回最终 SQL
    sql_query = sql_query.strip().replace("```sql", "").replace("```", "").splitlines()
    sql_query = " ".join(line for line in sql_query if not line.strip().startswith("--"))
    return sql_query

def generate_answer(user_question, query_results):
    """
    Generates a natural language answer based on the user's question and query results.
    Outputs the response in a streaming fashion for real-time updates.

    Args:
        user_question (str): The user's input question.
        query_results (list): The results from the database query.

    Returns:
        str: The final generated response.
    """
    prompt = answer_prompt.format(user_question=user_question, query_results=query_results)
    print("\n[DEBUG] Sending prompt to LLM for answer generation:")
    print(prompt)  # 输出发送给 LLM 的完整 Prompt

    # 初始化生成结果
    answer = ""

    # 调用 OpenAI 接口并开启流式输出
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            stream=True
        )

        print("\nAI 正在生成回答...")  # 提示生成开始

        # 逐步接收流式输出
        for chunk in response:
            print(chunk.choices[0].delta.content,end="")
            delta=chunk.choices[0].delta.content
            answer += delta
            # if 'choices' in chunk:
            #     delta = chunk['choices'][0]['delta']
            #     if 'content' in delta:
            #         content = delta['content']
            #         print(content, end="", flush=True)  # 实时输出到控制台
            #         answer += content  # 累积生成的内容

        print("\n\n[DEBUG] Final Generated Answer:\n", answer)  # 输出完整回答
        return answer

    except Exception as e:
        print("\n[ERROR] LLM 流式输出过程中发生错误：", e)
        return "回答生成失败。"


def ai_interactive_shell(connection):
    """
    AI 辅助的 MySQL Shell 模式，支持通过自然语言生成 SQL 并执行。
    """
    conversation_history = []  # 用于存储用户的对话历史
    try:
        while True:
            user_question = input("ai-mysql> ").strip()
            if user_question.lower() in ['exit', 'quit']:
                print("退出 AI 辅助的 MySQL Shell 模式")
                break

            try:
                # 获取数据库结构和样本数据
                database_structure = get_database_structure_with_samples(connection)
                print(f"\n[DEBUG] Database Structure and Samples:\n{database_structure}")

                # 调用 SQL 生成逻辑
                sql_query = generate_sql(user_question, conversation_history, connection=connection)
                print(f"\n[DEBUG] Final SQL Query for Execution:\n{sql_query}")

                # 执行 SQL 查询
                cursor = connection.cursor()
                cursor.execute(sql_query)
                if sql_query.lower().startswith("select") or sql_query.lower().startswith("show") or sql_query.lower().startswith("describe"):
                    rows = cursor.fetchall()
                    headers = [desc[0] for desc in cursor.description]
                    print(tabulate(rows, headers=headers, tablefmt="grid"))

                    # 调用回答生成逻辑
                    query_results = [dict(zip(headers, row)) for row in rows]
                    answer = generate_answer(user_question, query_results)
                    print("\nAI 生成的回答：", answer)
                else:
                    while cursor.nextset():
                        pass
                    connection.commit()
                    print("执行成功！")

                # 保存对话到历史
                conversation_history.append({"user": user_question, "response": sql_query})
            except mysql.connector.Error as e:
                print(f"SQL 错误：{e}")
            except Exception as e:
                print(f"未知错误：{e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
