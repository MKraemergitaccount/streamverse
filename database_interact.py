# Module Imports
import mariadb
import sys
import rest_api


def connect_to_database():
    try:
        conn = mariadb.connect(
            user="streamverse_scraper",
            password="Duhima32habi&",
            host="127.0.0.1",
            port=3306,
            database="scraper_db"
        )
        cur = conn.cursor()
        print("connection OK")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)
    return cur, conn


def get_from_database(cur,id):
    try:
        cur.execute(f"SELECT id, service, title, image, year, updated FROM website_data;")
        results = cur.fetchall()
        header, url = rest_api.get_header()
        for id, service, title, image, year, updated in results:
            rest_api.post_content(url, header, service, title, image, year)
        return results
    except mariadb.Error as e:
        print(f"Error reading Data: {e}")

"""
def write_to_database(conn, cur, service, title, image, year ,updated):
    try:
        cur.execute("INSERT INTO website_data  (service, title, image, year, updated) VALUES (?, ?, ?, ?, ?)",
                    (service, title, image, year, updated))
        conn.commit()
    except mariadb.Error as e:
        print(f"Error writing Data: {e}")
"""

def write_to_database(conn, cur, service, title, image, year ,updated):
    try:
        # Check if the combination already exists
        cur.execute("SELECT id FROM website_data WHERE service = ? AND title = ? AND image = ?",
                    (service, title, image))
        result = cur.fetchone()

        if result:
            # If it exists, update the record
            cur.execute("UPDATE website_data SET service = ?, title = ?, image = ?, year = ?, updated = ? WHERE id = ?",
                        (service, title, image, year, updated, result[0]))
        else:
            # If it doesn't exist, insert a new record
            cur.execute("INSERT INTO website_data  (service, title, image, year, updated) VALUES (?, ?, ?, ?, ?)",
                        (service, title, image, year, updated))

        conn.commit()
    except mariadb.Error as e:
        print(f"Error writing Data: {e}")

