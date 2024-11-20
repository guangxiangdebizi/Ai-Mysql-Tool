import mysql.connector
from tabulate import tabulate
import random

def get_database_structure_with_samples(connection, sample_count=5):
    """
    获取数据库中每张表的结构信息和随机样本数据。

    Args:
        connection: 数据库连接对象。
        sample_count: 每张表提取的随机样本行数。

    Returns:
        str: 包含表结构和随机样本数据的文本描述。
    """
    cursor = connection.cursor()
    database_structure = ""

    try:
        # 获取所有表名
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            database_structure += f"表名：{table_name}\n字段：\n"

            # 获取表结构
            cursor.execute(f"DESCRIBE {table_name};")
            structure = cursor.fetchall()
            for row in structure:
                field_info = f"  - {row[0]} ({row[1]}, {'NOT NULL' if row[2] == 'NO' else 'NULLABLE'})"
                if row[3] == "PRI":
                    field_info += ", PRIMARY KEY"
                if row[4]:
                    field_info += f", DEFAULT {row[4]}"
                database_structure += field_info + "\n"

            # 获取随机样本数据
            database_structure += "样本数据：\n"
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {sample_count};")
            samples = cursor.fetchall()
            if samples:
                headers = [desc[0] for desc in cursor.description]
                table_text = tabulate(samples, headers=headers, tablefmt="grid", numalign="center")
                database_structure += table_text + "\n"
            else:
                database_structure += "  (无样本数据)\n"

            database_structure += "\n"  # 分隔不同表

    except Exception as e:
        database_structure += f"\n获取表结构或样本数据时出错：{e}\n"

    finally:
        cursor.close()

    return database_structure

def display_table_structure(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        if not tables:
            print("\n没有找到任何表。")
            return
        print("\n数据库中的表及其结构：")
        for table in tables:
            print(f"\n表名：{table[0]}")
            cursor.execute(f"DESCRIBE {table[0]};")
            structure = cursor.fetchall()
            print(tabulate(structure, headers=["字段名", "类型", "是否为空", "主键", "默认值", "额外"], tablefmt="grid"))
    except mysql.connector.Error as e:
        print(f"操作失败，错误：{e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def interactive_shell(connection):
    try:
        cursor = connection.cursor()
        print("\n欢迎进入 MySQL Shell 模式，输入 SQL 语句并按回车执行，输入 'exit' 或 'quit' 退出。\n")
        while True:
            sql = input("mysql> ").strip()
            if sql.lower() in ['exit', 'quit']:
                print("退出 MySQL Shell 模式")
                break
            try:
                cursor.execute(sql)
                if sql.lower().startswith("select") or sql.lower().startswith("show") or sql.lower().startswith("describe"):
                    rows = cursor.fetchall()
                    headers = [desc[0] for desc in cursor.description]
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    while cursor.nextset():
                        pass
                    connection.commit()
                    print("执行成功！")
            except mysql.connector.Error as e:
                print(f"SQL 错误：{e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
