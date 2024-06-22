import scraper_v5
import database_interact
from datetime import date

def main():
    updated = date.today()
    cur, conn = database_interact.connect_to_database()

    # Add Scraped Dataframe content to Database;
    full_df = scraper_v5.get_dataframe()
    for index, row in full_df.iterrows():
        title = row['Title']
        image_url = row['Image_Link']
        year = row['Year']
        service = 'Netflix'
        database_interact.write_to_database(conn, cur, service, title, image_url, year, updated)


    database_interact.get_from_database(cur,range(10+1))
    conn.close()

main()

