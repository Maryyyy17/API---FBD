import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="ITEMNEXUS",
        user="postgres",
        password="marianesobral123",
        host="localhost"
        )

