import mysql.connector
from tabulate import tabulate
import random

def get_database_structure_with_samples(connection):
    """
    获取数据库结构和示例数据，返回格式化的字符串
    """
    try:
        cursor = connection.cursor(dictionary=True)  # 使用字典游标
        
        # 获取当前数据库名称
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()['DATABASE()']
        
        # 获取所有表
        cursor.execute("SHOW TABLES")
        tables = [table[f'Tables_in_{current_db}'] for table in cursor.fetchall()]
        
        structure_parts = [f"数据库名称: {current_db}\n"]
        
        for table_name in tables:
            # 获取表结构
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table = cursor.fetchone()['Create Table']
            
            # 获取列信息
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            # 获取示例数据
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            samples = cursor.fetchall()
            
            # 格式化表信息
            table_info = [f"\n表名: {table_name}"]
            table_info.append("\n列信息:")
            for col in columns:
                col_desc = f"  - {col['Field']} ({col['Type']})"
                if col['Key'] == 'PRI':
                    col_desc += " [主键]"
                if col['Key'] == 'MUL':
                    col_desc += " [外键]"
                table_info.append(col_desc)
            
            if samples:
                table_info.append("\n示例数据:")
                for sample in samples:
                    sample_str = "  "
                    for key, value in sample.items():
                        sample_str += f"{key}: {value}, "
                    table_info.append(sample_str.rstrip(", "))
            
            structure_parts.append("\n".join(table_info))
        
        return "\n".join(structure_parts)
        
    except Exception as e:
        print(f"获取数据库结构时出错：{e}")
        return "数据库结构获取失败，请检查数据库连接"
    finally:
        if 'cursor' in locals():
            cursor.close()

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
