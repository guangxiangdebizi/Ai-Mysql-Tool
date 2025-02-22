# LLM Interaction Module

## 主要功能
该模块负责与大语言模型(LLM)的交互，包括SQL生成、答案生成和交互式shell功能。

## 函数说明

### generate_sql()
将自然语言转换为SQL查询语句。

**输入参数:**
- user_question (str): 用户的自然语言问题
- conversation_history (list, optional): 对话历史记录
- connection (mysql.connector): 数据库连接对象

**输出:**
- str: 生成的SQL查询语句

**工作流程:**
1. 获取数据库结构
2. 构造对话历史
3. 使用LLM澄清用户问题
4. 生成SQL查询
5. 提取和优化SQL语句

### generate_answer()
根据查询结果生成自然语言回答。

**输入参数:**
- user_question (str): 用户的原始问题
- query_results (list): 数据库查询结果

**输出:**
- str: 生成的自然语言回答

**工作流程:**
1. 构造回答提示
2. 调用LLM生成回答
3. 流式输出回答内容

### ai_interactive_shell()
提供交互式SQL查询界面。

**输入参数:**
- connection (mysql.connector): 数据库连接对象

**工作流程:**
1. 接收用户输入
2. 生成SQL查询
3. 执行查询
4. 展示结果
5. 生成自然语言解释
6. 维护对话历史 