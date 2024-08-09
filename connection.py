import psycopg2

conn = psycopg2.connect(
    database="db_clientes",
    user="postgres",
    password="postgres",
    host="0.0.0.0"
)

cur = conn.cursor()
cur.execute()