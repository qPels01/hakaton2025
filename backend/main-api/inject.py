import psycopg2 # type: ignore

conn = psycopg2.connect(
    host="5.104.75.180",
    port=5432,
    dbname="neurodb",
    user="postgres",
    password="123123"
)

sql_file_path = "schema.sql"

try:
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    with conn:
        with conn.cursor() as curs:
            statements = sql.split(';')
            for statement in statements:
                stmt = statement.strip()
                if not stmt:
                    continue
                
                curs.execute(stmt)

                # Если это SELECT — выводим результат
                if stmt.lower().startswith('select'):
                    rows = curs.fetchall()
                    print(f"Result of query:\n{stmt}")
                    for row in rows:
                        print(row)
                    print('-' * 40)

    print("SQL script executed successfully")

except Exception as e:
    print("Error executing SQL script:", e)

finally:
    conn.close()
