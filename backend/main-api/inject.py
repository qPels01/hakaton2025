import psycopg2

# Параметры подключения
conn = psycopg2.connect(
    host="5.104.75.180",      # твой хост PostgreSQL
    port=5432,                # порт
    dbname="neurodb",         # имя базы
    user="neurouser",         # пользователь
    password="neurosecret"    # пароль
)

# Путь к SQL-файлу
sql_file_path = "schema.sql"

# Чтение и выполнение
with open(sql_file_path, "r", encoding="utf-8") as f:
    sql = f.read()

with conn:
    with conn.cursor() as curs:
        curs.execute(sql)
        # Если много отдельных выражений и ошибок, можно циклом:
        # for statement in sql.split(';'):
        #    if statement.strip():
        #        curs.execute(statement)
print("SQL script executed successfully")

conn.close()