# Ai-Mysql-Tool
这是一个LLM辅助MySQL查询的项目，It is a project by using LLM to assist user do search in MySQL
# AI-Assisted MySQL Interactive Tool

Welcome to the **AI-Assisted MySQL Interactive Tool**! This project aims to create an intuitive and powerful SQL assistant capable of interacting with a MySQL database via natural language commands. It integrates advanced AI capabilities with a friendly user interface, allowing users to query databases, explore data structures, and manipulate records without needing to remember complex SQL syntax.

## 🌟 Key Features

- **Natural Language to SQL Conversion**: Enter your questions in natural language, and the tool will generate and execute the appropriate SQL queries for you.
- **Interactive Shell**: Provides an interactive MySQL Shell, where users can type natural language questions and receive both SQL commands and results.
- **Rich GUI Input**: Includes a full graphical user interface (GUI) for connecting to databases. Input your credentials easily, and let the tool handle the rest.
- **AI-Assisted Results Interpretation**: After executing a query, the tool generates a natural language interpretation of the results, making data exploration more understandable.
- **Automatic Database Structure Detection**: The AI model is aware of the table structure and can adapt queries based on database metadata and actual data samples.

## 💻 Project Architecture

The project is organized into several modules, each with a specific responsibility to ensure code maintainability and extensibility.

```
mysql_ai_tool_project/
├── main.py                  # Main entry point of the application
├── config.py                # Global configuration (API keys, model settings, etc.)
├── db/
│   ├── __init__.py         # Makes db a Python package
│   ├── connection.py      # Manages database connections
│   ├── utils.py           # Database utility functions (e.g., table structure)
├── gui/
│   ├── __init__.py         # Makes gui a Python package
│   ├── credentials_gui.py # GUI for user credential input
├── ai/
│   ├── __init__.py         # Makes ai a Python package
│   ├── llm_interaction.py # Manages interaction with the AI language model
├── utils/
│   ├── __init__.py         # Makes utils a Python package
│   ├── prompts.py         # Prompt templates for the language model
├── requirements.txt       # Project dependencies
```

### Module Overview

1. **`main.py`**:  
   The main entry point of the application. It contains the logic for displaying the menu and handling different modes (e.g., interactive shell, AI-assisted shell).

2. **`config.py`**:  
   Stores configuration values such as API keys for the AI model, base URLs, and model names.

3. **`db/connection.py`**:  
   Manages the MySQL database connection, including functions to establish or close connections securely.

4. **`db/utils.py`**:  
   Provides utility functions to work with the database, such as displaying the structure of tables and generating sample data for AI context enhancement.

5. **`gui/credentials_gui.py`**:  
   Implements a GUI using Tkinter to accept user credentials for connecting to the MySQL database. This keeps the setup user-friendly.

6. **`ai/llm_interaction.py`**:  
   Manages communication with the AI language model, including generating SQL from user queries and interpreting the results. Supports streaming output for real-time response.

7. **`utils/prompts.py`**:  
   Stores prompt templates used by the AI to ensure that queries and responses are appropriately formatted.

## 🚀 How It Works
# 🚀 How It Works

1. **Connect to Your Database**: Launch the tool using `main.py`. The GUI will prompt you to enter your MySQL credentials, including the username, password, host, and port. You can also specify a particular database.

2. **Choose an Interaction Mode**:

   - **Interactive Shell**: You can directly type SQL commands or use natural language queries.

   - **AI-Assisted Shell**: Input questions like "What are the details of employees older than 30?" and let the tool generate the SQL query, execute it, and provide a summary.

3. **Database Structure Awareness**: To accurately generate SQL, the AI needs knowledge of the database schema. The application automatically gathers:

   - **Table Names and Fields**: Collected from the database using `SHOW TABLES` and `DESCRIBE` commands.
   - **Random Data Samples**: The AI also receives a few rows of data to understand the content types and distribution. This is especially useful when a field is ambiguous, e.g., gender represented by `M/F` instead of full strings like `Male/Female`.

   For instance, if the database contains a table called `employees`, the system will generate a structure similar to this:

   ```
   表名：employees
   字段：
     - id (INT, NOT NULL, PRIMARY KEY)
     - name (VARCHAR(50), NOT NULL)
     - age (INT, NOT NULL)
     - department_id (INT, NULLABLE)
   样本数据：
   +----+----------+-----+--------------+
   | id | name     | age | department_id|
   +----+----------+-----+--------------+
   |  1 | John Doe |  45 | 2            |
   |  2 | Jane Doe |  32 | NULL         |
   +----+----------+-----+--------------+
   ```

4. **Clarification Phase by the AI (LLM)**: After gathering the database structure, the tool uses an AI language model (LLM) to understand and clarify the user's input:

   - **Prompt Construction**: The system constructs a prompt that includes the user query, table structure, and sample data. This helps the AI clarify what kind of SQL should be generated.
   - **Clarification with Context**: For instance, for the input "Show me all employees over the age of 30," the LLM uses the database structure to determine that `employees` is the appropriate table and `age` is the relevant field.

5. **SQL Query Generation**: The AI generates an SQL query based on the clarified information. In this step:

   - **LLM SQL Generation**: The AI, with all the context provided, creates an appropriate SQL statement. For example:

     ```sql
     SELECT * FROM employees WHERE age > 30;
     ```

   - **Extracting Pure SQL**: If the AI generates more information (e.g., explanations or comments), a post-processing step extracts just the SQL command for execution.

6. **Executing the SQL Query**: Once the SQL command is ready, it is passed to the database interaction module:

   - **Database Connection**: Using the established connection (from `db/connection.py`), the SQL is executed against the connected MySQL instance.
   - **Result Handling**: The results are fetched, and any potential errors are caught and handled gracefully.

   For the example query, the execution might return:

   ```
   +----+----------+-----+--------------+
   | id | name     | age | department_id|
   +----+----------+-----+--------------+
   |  1 | John Doe |  45 | 2            |
   |  3 | Alice    |  50 | 1            |
   +----+----------+-----+--------------+
   ```

7. **Natural Language Result Interpretation**: After executing the SQL query, the tool then uses the AI to interpret and present the results in an understandable format:

   - **Prompt for Explanation**: A new prompt is created with the query results to generate a natural language explanation.
   - **LLM Generates Explanation**: The AI uses the query results to generate an answer like:

     ```
     AI 生成的回答：
     所有年龄大于 30 岁的员工包括：
     1. John Doe, 45 岁
     2. Alice, 50 岁
     ```

   This step helps users, especially those who may not be well-versed in interpreting raw data, to quickly understand the meaning behind the results.

8. **Streaming Output for Real-Time Interaction**: To enhance the interactivity of the tool:

   - **Real-Time Streaming**: When generating natural language explanations, the AI provides streaming output so that users get feedback immediately, even as the final answer is being formed.
   - **Seamless Interaction**: This ensures that users feel they are in a conversational environment rather than waiting for a batch process to complete.
## 📦 Installation and Setup

### Prerequisites
- Python 3.8 or later
- MySQL server running locally or remotely

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/mysql_ai_tool_project.git
   cd mysql_ai_tool_project
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**:
   - Open `config.py` and add your OpenAI API key or other model settings.

5. **Run the Application**:
   ```bash
   python main.py
   ```

## 📖 Example Use Case

Imagine you are a data analyst who wants to extract insights from a database. Instead of manually writing complex SQL, you simply input:

```
ai-mysql> What are the names of employees whose age is greater than 25?
```

The tool will generate the appropriate SQL command, execute it, and provide both the raw results and a natural-language summary like:

```
AI 生成的回答：
所有年龄大于 25 岁的员工包括：
1. John Doe, 28 岁
2. Jane Smith, 30 岁
...
```

## 📋 Project Features in Detail

### 1. Natural Language to SQL Conversion
- Utilizes powerful AI models to convert ambiguous natural language into precise SQL commands.
- Handles common database interactions like `SELECT`, `INSERT`, and `UPDATE` statements.

### 2. Real-Time Streaming Responses
- **Streaming Output**: The AI provides real-time feedback when generating results, making the experience more interactive and fast-paced.

### 3. Interactive Shell Modes
- **Interactive SQL Shell**: Directly type and execute SQL.
- **AI-Assisted Mode**: Type questions in natural language; see the equivalent SQL query and results.

### 4. Enhanced Data Context Understanding
- The AI gains better accuracy by examining both the database structure and a few sample rows.
- Sample rows help clarify data types (e.g., gender stored as "M" or "F" instead of full names).

## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a Pull Request.

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🛠️ Technologies Used
- **Python**: Core programming language.
- **MySQL**: Database for data storage and retrieval.
- **OpenAI API**: For generating SQL and summarizing results.
- **Tkinter**: GUI for database connection setup.
- **Tabulate**: Formatting SQL results into readable tables.

## 📝 Future Enhancements
- **User Authentication**: Adding different levels of user access for enhanced security.
- **Improved Language Model Integration**: Supporting more advanced prompts to handle ambiguous or complex questions.
- **Support for Additional Databases**: Adding compatibility for PostgreSQL, SQLite, etc.

## 🌟 Get Started Today!
Try out the AI-Assisted MySQL Interactive Tool today and experience a seamless blend of natural language processing and database interaction. With a few clicks and a simple question, you can retrieve valuable data insights without needing SQL expertise.

If you have any questions or run into issues, feel free to open an issue on [GitHub](https://github.com/your_username/mysql_ai_tool_project/issues).

Happy querying! 🚀

## 📞 Contact Information
- **GitHub**: [https://github.com/guangxiangdebizi/](https://github.com/guangxiangdebizi/)
- **Email**: [guangxiangdebizi@gmail.com](mailto:guangxiangdebizi@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/%E6%98%9F%E5%AE%87-%E9%99%88-b5b3b0313/](https://www.linkedin.com/in/%E6%98%9F%E5%AE%87-%E9%99%88-b5b3b0313/)

