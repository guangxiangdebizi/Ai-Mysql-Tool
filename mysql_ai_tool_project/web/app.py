from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql_ai_tool_project.ai.llm_interaction import generate_sql, generate_answer

app = Flask(__name__)

def create_connection(config):
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(
            user=config['username'],
            password=config['password'],
            host=config['host'],
            port=int(config['port']),
            database=config.get('database')
        )
        return connection
    except Exception as e:
        raise Exception(f"数据库连接失败: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    try:
        config = request.json
        connection = create_connection(config)
        
        # 获取所有数据库
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall() 
                    if db[0] not in ['information_schema', 'performance_schema', 'mysql', 'sys']]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'databases': databases
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.json
        user_question = data.get('question')
        config = data.get('config')
        
        if not config or not user_question:
            return jsonify({'error': '缺少必要参数'}), 400
            
        # 创建数据库连接
        connection = create_connection(config)
        
        # 生成SQL
        sql_query = generate_sql(user_question, connection=connection)
        
        # 执行查询
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # 生成回答
        answer = generate_answer(user_question, results)
        
        return jsonify({
            'sql': sql_query,
            'results': results,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True) 