from mysql_ai_tool_project.gui.credentials_gui import get_credentials_via_single_gui

def connect_to_database():
    connection = get_credentials_via_single_gui()
    if not connection:
        print("连接信息未完整输入，操作已取消。")
        return None

    return connection
