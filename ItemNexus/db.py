import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="guilda",
        user="postgres",
        password="marianesobral123",
        host="localhost"
        )

