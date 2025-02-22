from langchain.prompts import PromptTemplate

sql_prompt = PromptTemplate(template='''
你是一个专业的 SQL 查询生成器。请根据以下数据库结构和用户需求生成准确的 SQL 查询语句：

数据库结构：
{database_structure}

用户需求：{user_question}

生成 SQL 时请注意：
1. 优先使用 LEFT JOIN 而不是 INNER JOIN，以避免数据丢失
2. 如果查询涉及多个表，为每个表添加别名以提高可读性
3. 使用 COALESCE 或 IFNULL 处理可能的 NULL 值
4. 对于模糊查询，使用 LIKE 语句并添加通配符
5. 如果查询结果可能为空，添加适当的错误处理
6. 确保查询性能优化，避免不必要的表连接

请直接输出 SQL 语句，不要包含任何注释或解释。
''')

extract_sql_prompt = PromptTemplate(template='''
请从以下内容中提取并优化 SQL 查询语句：

输入内容：{llm_output}

优化要求：
1. 移除所有注释和格式标记
2. 确保语句的完整性和正确性
3. 优化查询性能
4. 添加必要的错误处理
5. 使用更友好的表别名

请只返回优化后的 SQL 语句，不要包含任何其他内容。
''')

clarify_prompt = PromptTemplate(template='''
作为数据库查询专家，请分析并明确用户的查询需求：

历史对话：
{conversation_history}

数据库结构：
{database_structure}

用户问题：
{user_question}

请提供：
1. 查询目标的具体定义
2. 需要查询的表和字段
3. 查询条件和过滤要求
4. 结果排序和分组需求
5. 是否需要聚合函数
6. 是否需要分页处理
7. 可能的边界情况处理

请用专业的数据库术语描述需求，以便生成精确的 SQL。
''')

answer_prompt = PromptTemplate(template='''
你是一个友好的数据库助手，请用自然语言回答用户的问题。

用户问题：{user_question}
查询结果：{query_results}

请直接用中文回答用户的问题：
1. 使用自然、友好的语言
2. 直接回答用户的问题要点
3. 如果查询结果为空，说明可能的原因
4. 如果有结果，清晰地描述查询到的内容
5. 不要生成任何代码或技术分析
6. 不要解释数据类型或技术细节
7. 保持回答简洁明了

请直接开始回答：
''')
