import psycopg2 # type: ignore

# Параметры подключения
conn = psycopg2.connect(
    host="5.104.75.180",
    port=5432,
    dbname="neurodb",
    user="neurouser",
    password="neurosecret"
)

# Путь к SQL-файлу
sql_file_path = "show.sql"

with open(sql_file_path, "r", encoding="utf-8") as f:
    sql = f.read()

with conn:
    with conn.cursor() as curs:
        curs.execute(sql)
        rows = curs.fetchall()
        print("Таблицы в public-схеме PostgreSQL:")
        for row in rows:
            print(f"- {row[0]}")

conn.close()