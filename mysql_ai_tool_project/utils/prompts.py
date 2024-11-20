from langchain.prompts import PromptTemplate

sql_prompt = PromptTemplate(template='''
为以下问题生成一个SQL查询：{user_question}。
请注意，你只能生成SQL语句，其余的内容一律不要给我返回！且确保你生成的SQL语句和用户输入的请求相匹配。
确保输出给我的东西里面只有sql命令的纯文本，别的都不要。不要给我这种 sql xxxx格式的东西，我只要里面的命令行''')
extract_sql_prompt = PromptTemplate(template='''
请从以下内容中提取有效的SQL查询语句：{llm_output}。
请注意，你只能生成SQL语句，其余的内容一律不要给我返回！且确保你生成的SQL语句和用户输入的请求相匹配。
确保输出给我的东西里面只有sql命令的纯文本，别的都不要。不要给我这种 sql xxxx格式的东西，我只要里面的命令行''')
clarify_prompt = PromptTemplate(template='''根据以下用户对话历史和数据库结构信息，分析并明确用户的自然语言指令：
对话历史：{conversation_history} 
数据库结构：{database_structure} 
用户当前问题：{user_question}''')
answer_prompt = PromptTemplate(template='''
根据以下用户问题和数据库查询结果生成回答：问题：{user_question} 结果：{query_results}
''')
