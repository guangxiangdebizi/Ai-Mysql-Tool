import tkinter as tk
from mysql.connector import errorcode
import mysql.connector

# 添加默认配置
DEFAULT_CONFIG = {
    'user': 'root',
    'password': 'chenxingyu050115',
    'host': 'localhost',
    'port': 3306,
    'database': 'homedata'
}

def get_credentials_via_single_gui():
    """
    Opens a single GUI window to get MySQL credentials and connection details from the user.
    Returns:
        mysql.connector.connect: A MySQL connection object.
    """
    # 首先尝试使用默认配置连接
    try:
        connection = mysql.connector.connect(**DEFAULT_CONFIG)
        print("使用默认配置连接数据库成功")
        return connection
    except mysql.connector.Error as e:
        print(f"使用默认配置连接失败：{e}")
        print("启动GUI配置界面...")

    # 如果默认连接失败，则显示GUI
    root = tk.Tk()
    root.title("MySQL 连接信息输入")
    root.geometry("400x450")
    root.attributes('-topmost', True)
    
    # 确保窗口显示在屏幕中央
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 450) // 2
    root.geometry(f"400x450+{x}+{y}")

    # 强制窗口获取焦点
    root.focus_force()
    
    error_labels = {}

    def clear_error(field):
        if field in error_labels:
            error_labels[field].config(text="")

    # 创建输入框并预填充默认值
    tk.Label(root, text="用户名：").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    username_entry = tk.Entry(root)
    username_entry.insert(0, DEFAULT_CONFIG['user'])
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    error_labels['user'] = tk.Label(root, text="", fg="red")
    error_labels['user'].grid(row=0, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="密码：").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    password_entry = tk.Entry(root, show='*')
    password_entry.insert(0, DEFAULT_CONFIG['password'])
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    error_labels['password'] = tk.Label(root, text="", fg="red")
    error_labels['password'].grid(row=1, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="主机地址：").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    host_entry = tk.Entry(root)
    host_entry.insert(0, DEFAULT_CONFIG['host'])
    host_entry.grid(row=2, column=1, padx=10, pady=5)
    error_labels['host'] = tk.Label(root, text="", fg="red")
    error_labels['host'].grid(row=2, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="端口号：").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    port_entry = tk.Entry(root)
    port_entry.insert(0, str(DEFAULT_CONFIG['port']))
    port_entry.grid(row=3, column=1, padx=10, pady=5)
    error_labels['port'] = tk.Label(root, text="", fg="red")
    error_labels['port'].grid(row=3, column=2, padx=5, pady=5, sticky='w')

    tk.Label(root, text="数据库名称：").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    database_entry = tk.Entry(root)
    database_entry.insert(0, DEFAULT_CONFIG['database'])
    database_entry.grid(row=4, column=1, padx=10, pady=5)
    error_labels['database'] = tk.Label(root, text="", fg="red")
    error_labels['database'].grid(row=4, column=2, padx=5, pady=5, sticky='w')

    connection_status_label = tk.Label(root, text="", fg="blue")
    connection_status_label.grid(row=6, column=0, columnspan=3, pady=10)

    credentials = {}
    connection = None

    def on_submit():
        nonlocal connection
        # Clear previous error messages
        for field in error_labels:
            clear_error(field)
        connection_status_label.config(text="")

        # Collect the data from the entries
        credentials['user'] = username_entry.get().strip()
        credentials['password'] = password_entry.get().strip()
        credentials['host'] = host_entry.get().strip() or 'localhost'
        credentials['port'] = port_entry.get().strip() or '3306'
        credentials['database'] = database_entry.get().strip()

        has_error = False

        # Validate entries
        if not credentials['user']:
            error_labels['user'].config(text="用户名不能为空！")
            has_error = True

        if not credentials['password']:
            error_labels['password'].config(text="密码不能为空！")
            has_error = True

        try:
            credentials['port'] = int(credentials['port'])
        except ValueError:
            error_labels['port'].config(text="端口号必须是数字！")
            has_error = True

        if has_error:
            return

        # Try to connect to the database
        try:
            config = {
                'user': credentials['user'],
                'password': credentials['password'],
                'host': credentials['host'],
                'port': credentials['port']
            }
            if credentials['database']:
                config['database'] = credentials['database']

            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                connection_status_label.config(text="连接成功！", fg="green")
                root.after(1000, root.destroy)  # Close the window after 1 second
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                connection_status_label.config(text="用户名或密码错误，请重新输入！", fg="red")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                connection_status_label.config(text="数据库不存在，请重新输入！", fg="red")
            else:
                connection_status_label.config(text=f"连接失败，错误：{e}", fg="red")
        except Exception as e:
            connection_status_label.config(text=f"发生未知错误：{e}", fg="red")

    # Submit Button
    submit_button = tk.Button(root, text="提交", command=on_submit)
    submit_button.grid(row=5, column=0, columnspan=2, pady=20)

    # 添加键盘事件处理
    def on_enter(event):
        on_submit()
    root.bind('<Return>', on_enter)

    # 更新GUI
    root.update()
    
    # 运行主循环
    root.mainloop()

    if connection and connection.is_connected():
        return connection
    return None
