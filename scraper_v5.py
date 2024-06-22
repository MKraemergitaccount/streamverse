import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_full_page_html(year):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://www.justwatch.com/de/Anbieter/netflix?release_year_from={year}&release_year_until={year}"
    driver.get(url)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'total-titles-seo'))
        WebDriverWait(driver, 60).until(element_present)
        total_titles = driver.find_element(By.CLASS_NAME, 'total-titles-seo').text.split()[0]  
        # Extrahiere die Anzahl der Titel
        print(f"Anzahl der Titel für Jahr {year}: {total_titles}")
    except Exception as e:
        print("Timeout-Fehler: ", e)

    # Scrollen bis zum Ende der Seite
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wartezeit, um das Laden von Inhalten abzuwarten
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wartezeit, um sicherzustellen, dass alle Inhalte geladen wurden
    time.sleep(5)

    # Scrapen der sichtbaren Elemente
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    df = pd.DataFrame(columns=['Title', 'Image_Link', 'Year'])

    title_count = 0
    for series in soup.select('.title-list-grid__item--link'):
        title = series['href'].split('/')[-1]
        image_source = series.select_one('.title-poster__image source')
        if image_source:
            image_url = image_source.get('data-srcset') or image_source.get('srcset')  
            # Versuche data-srcset und dann srcset
            if image_url:
                image_url = image_url.split(',')[0]  # Extrahiere nur die erste URL
        else:
            image_url = ''  # Wenn kein source-Tag gefunden wurde, leere URL setzen

        # Hinzufügen der Daten zum DataFrame
        dataframe_to_add = {'Title': [title],
                            'Image_Link': [image_url],
                            'Year': [year]}

        df = pd.concat([df, pd.DataFrame(dataframe_to_add)], ignore_index=True)
        title_count += 1
        print(f"Scraping: {title_count}/{total_titles}, Jahr: {year}", end='\r')  
        # Fortschrittsanzeige

    driver.quit()
    return df

def get_dataframe():
    # Liste der Jahre, in 1er-Schritten von 1900 bis 2024
    years = range(1900, 2025)

    # DataFrame für gesamte Daten
    full_df = pd.DataFrame(columns=['Title', 'Image_Link', 'Year'])

    # Iteriere durch die Jahre und scrape die Daten für jede Zeitperiode
    for year in years:
        df = get_full_page_html(year)
        full_df = pd.concat([full_df, df], ignore_index=True)

    # Entfernen der Doppelten Eintaege fuer "Title"
    duplicates = full_df[full_df.duplicated(subset=['Title'], keep=False)]
    if not duplicates.empty:
        print("Doppelte Titel:")
        for index, row in duplicates.iterrows():
            print(f"{row['Title']} war im Jahr {row['Year']}")

    full_df = full_df.drop_duplicates(subset='Title', keep='first')
    return full_df

