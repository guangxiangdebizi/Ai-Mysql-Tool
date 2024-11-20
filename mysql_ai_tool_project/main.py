from db.connection import connect_to_database
from db.utils import display_table_structure, interactive_shell
from ai.llm_interaction import ai_interactive_shell

def show_menu():
    print("\n操作菜单：")
    print("1. 进入交互式数据库操作系统")
    print("2. 显示当前数据库的表结构")
    print("3. 进入 AI 辅助的数据库操作系统")
    print("4. 退出程序")

if __name__ == "__main__":
    try:
        connection = connect_to_database()
        if connection:
            while True:
                show_menu()
                choice = input("\n请选择操作（输入数字）：").strip()
                if choice == '1':
                    interactive_shell(connection)
                elif choice == '2':
                    display_table_structure(connection)
                elif choice == '3':
                    ai_interactive_shell(connection)
                elif choice == '4':
                    print("程序已退出")
                    break
                else:
                    print("无效选择，请重新输入！")
            if connection.is_connected():
                connection.close()
                print("连接已关闭")
        else:
            print("\n未能成功连接数据库，请检查配置并重试。")
    except Exception as e:
        print(f"\n主程序发生错误：{e}")
