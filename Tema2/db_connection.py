import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='unida',
        cursorclass=pymysql.cursors.DictCursor,
        auth_plugin_map={
            "caching_sha2_password": "pymysql.auth.caching_sha2_password"
        }
    )
    return conn
