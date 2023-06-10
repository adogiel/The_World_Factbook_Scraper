import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import time

start_time = time.time()

def scrape_country_info(country_link):
    response = requests.get(country_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the country name
    country_name_element = soup.find('h1', class_='hero-title')
    country_name = country_name_element.text.strip() if country_name_element else ""

    # Find the population
    population_element = soup.find('div', id='people-and-society')
    if population_element:
        population_element = population_element.find('h3', class_='mt30').find_next('p').text.strip()
    else:
        population_element = ""

    #Find age structure
    age_struct_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    age_struct_section = age_struct_div.find('h3', text='Age structure')
    age_struct_paragraph = age_struct_section.find_next_sibling('p')
    age_struct_strong_tags = age_struct_paragraph.find_all('strong')

    age_0_14 = age_struct_strong_tags[0].next_sibling.strip()
    age_15_64 = age_struct_strong_tags[1].next_sibling.strip()
    age_65_more = age_struct_strong_tags[2].next_sibling.strip()

    # Find median age
    median_age_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    median_age_section = median_age_div.find('h3', text='Median age')
    median_age_paragraph = median_age_section.find_next_sibling('p') if median_age_section else None
    median_age_strong_tags = median_age_paragraph.find_all('strong') if median_age_paragraph else []

    total_median_age = median_age_strong_tags[0].next_sibling.strip() if median_age_strong_tags else ""
    male_median_age = median_age_strong_tags[1].next_sibling.strip() if len(median_age_strong_tags) >= 2 else ""
    female_median_age = median_age_strong_tags[2].next_sibling.strip() if len(median_age_strong_tags) >= 3 else ""

    #Find population growth rate
    growth_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    growth_rate_section = growth_rate_div.find('h3', text='Population growth rate')
    growth_rate_paragraph = growth_rate_section.find_next_sibling('p') if growth_rate_section else None
    growth_rate = growth_rate_paragraph.text.strip() if growth_rate_paragraph else ""


    #Birth rate
    birth_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    birth_rate_section = birth_rate_div.find('h3', text='Birth rate')
    birth_rate_paragraph = birth_rate_section.find_next_sibling('p') if birth_rate_section else None
    birth_rate = birth_rate_paragraph.text.strip() if birth_rate_paragraph else ""

    #Death rate
    death_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    death_rate_section = death_rate_div.find('h3', text='Death rate')
    death_rate_paragraph = death_rate_section.find_next_sibling('p') if death_rate_section else None
    death_rate = death_rate_paragraph.text.strip() if death_rate_paragraph else ""

    #Life expactancy
    life_expectancy_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    life_expectancy_section = life_expectancy_div.find('h3', text='Life expectancy at birth')
    life_expectancy_paragraph = life_expectancy_section.find_next_sibling('p') if life_expectancy_section else None
    life_expectancy_strong_tags = life_expectancy_paragraph.find_all('strong') if life_expectancy_paragraph else []

    total_life_expectancy = life_expectancy_strong_tags[0].next_sibling.strip() if life_expectancy_strong_tags else ""
    male_life_expectancy = life_expectancy_strong_tags[1].next_sibling.strip() if len(life_expectancy_strong_tags) >= 2 else ""
    female_life_expectancy = life_expectancy_strong_tags[2].next_sibling.strip() if len(life_expectancy_strong_tags) >= 3 else ""

    #Total_sex_ratio
    total_sex_ratio_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'people-and-society'})
    total_sex_ratio_section = total_sex_ratio_div.find('h3', text='Sex ratio')
    total_sex_ratio_paragraph = total_sex_ratio_section.find_next_sibling('p') if total_sex_ratio_section else None
    total_sex_ratio_strong_tags = total_sex_ratio_paragraph.find_all('strong') if total_sex_ratio_paragraph else []

    total_sex_ratio = total_sex_ratio_strong_tags[4].next_sibling.strip() if total_sex_ratio_strong_tags else ""

    #Real GDP
    gdp_2021 = ""
    gdp_2020 = ""
    gdp_2019 = ""

    gdp_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'economy'})
    if gdp_div:
        gdp_section = gdp_div.find('h3', text='Real GDP (purchasing power parity)')
        if gdp_section:
            gdp_paragraph = gdp_section.find_next_sibling('p')
            gdp_values = gdp_paragraph.text.strip()

            pattern = r'\$(.*?) billion \((\d{4}) est.\)'
            matches = re.findall(pattern, gdp_values)

            for match in matches:
                gdp_value, year = match
                if year == '2021':
                    gdp_2021 = gdp_value
                elif year == '2020':
                    gdp_2020 = gdp_value
                elif year == '2019':
                    gdp_2019 = gdp_value

    #Real gdp growth rate

    growth_gdp_2021 = ""
    growth_gdp_2020 = ""
    growth_gdp_2019 = ""

    real_gdp_growth_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'economy'})
    if real_gdp_growth_rate_div:
        real_gdp_growth_rate_section = real_gdp_growth_rate_div.find('h3', text='Real GDP growth rate')
        if real_gdp_growth_rate_section:
            real_gdp_growth_rate_paragraph = real_gdp_growth_rate_section.find_next_sibling('p')
            if real_gdp_growth_rate_paragraph:
                real_gdp_growth_rate_values = real_gdp_growth_rate_paragraph.text.strip()

                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, real_gdp_growth_rate_values)

                for match in matches:
                    growth_rate, year = match
                    if year == '2021':
                        growth_gdp_2021 = growth_rate
                    elif year == '2020':
                        growth_gdp_2020 = growth_rate
                    elif year == '2019':
                        growth_gdp_2019 = growth_rate

    #Real gdp per capita

    gdp_per_capita_2021 = ""
    gdp_per_capita_2020 = ""
    gdp_per_capita_2019 = ""

    gdp_per_capita_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'economy'})
    if gdp_per_capita_div:
        gdp_per_capita_section = gdp_per_capita_div.find('h3', text='Real GDP per capita')
        if gdp_per_capita_section:
            gdp_per_capita_paragraph = gdp_per_capita_section.find_next_sibling('p')
            if gdp_per_capita_paragraph:
                gdp_per_capita_values = gdp_per_capita_paragraph.text.strip()

                pattern = r'\$(.*?) \((\d{4}) est.\)'
                matches = re.findall(pattern, gdp_per_capita_values)

                for match in matches:
                    gdp_per_capita_value, year = match
                    if year == '2021':
                        gdp_per_capita_2021 = gdp_per_capita_value
                    elif year == '2020':
                        gdp_per_capita_2020 = gdp_per_capita_value
                    elif year == '2019':
                        gdp_per_capita_2019 = gdp_per_capita_value
    #Inflation rate

    inflation_2021 = ""
    inflation_2020 = ""
    inflation_2019 = ""

    inflation_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'economy'})
    if inflation_rate_div:
        inflation_rate_section = inflation_rate_div.find('h3', text='Inflation rate (consumer prices)')
        if inflation_rate_section:
            inflation_rate_paragraph = inflation_rate_section.find_next_sibling('p')
            if inflation_rate_paragraph:
                inflation_rate_values = inflation_rate_paragraph.text.strip()

                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, inflation_rate_values)

                for match in matches:
                    inflation_rate_values, year = match
                    if year == '2021':
                        inflation_2021 = inflation_rate_values
                    elif year == '2020':
                        inflation_2020 = inflation_rate_values
                    elif year == '2019':
                        inflation_2019 = inflation_rate_values

    #unemployment rate    

    unemployment_2021 = ""
    unemployment_2020 = ""
    unemployment_2019 = ""

    unemployment_rate_div = soup.find('div', {'class': 'free-form-content__content', 'id': 'economy'})
    if unemployment_rate_div:
        unemployment_rate_section = unemployment_rate_div.find('h3', text='Unemployment rate')
        if unemployment_rate_section:
            unemployment_rate_paragraph = unemployment_rate_section.find_next_sibling('p')
            if unemployment_rate_paragraph:
                unemployment_rate_values = unemployment_rate_paragraph.text.strip()

                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, unemployment_rate_values)

                for match in matches:
                    unemployment_rate_value, year = match
                    if year == '2021':
                        unemployment_2021 = unemployment_rate_value
                    elif year == '2020':
                        unemployment_2020 = unemployment_rate_value
                    elif year == '2019':
                        unemployment_2019 = unemployment_rate_value

    return country_name, population_element, total_median_age, male_median_age, female_median_age, age_0_14, age_15_64, age_65_more, growth_rate, birth_rate, death_rate, total_life_expectancy, male_life_expectancy, female_life_expectancy, total_sex_ratio, gdp_2021, gdp_2020, gdp_2019, growth_gdp_2021, growth_gdp_2020, growth_gdp_2019, gdp_per_capita_2021, gdp_per_capita_2020, gdp_per_capita_2019, inflation_2021, inflation_2020, inflation_2019, unemployment_2021, unemployment_2020, unemployment_2019     

def print_country_info(url,limit=50):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    continent_name = soup.find('h1', class_='hero-title').text.strip()
    country_elements = soup.find_all('a', class_='link-button bold')

    population_table = []
    counter = 0
    for element in country_elements:
        if counter >= limit:
            break

        country_link = 'https://www.cia.gov' + element['href']
        country_name, population, total_median_age, male_median_age, female_median_age, age_0_14, age_15_64, age_65_more, growth_rate, birth_rate, death_rate, total_life_expactancy, male_life_expactancy, female_life_expactancy, total_sex_ratio, gdp_2021, gdp_2020, gdp_2019, growth_gdp_2021, growth_gdp_2020, growth_gdp_2019, gdp_per_capita_2021, gdp_per_capita_2020, gdp_per_capita_2019, inflation_2021, inflation_2020, inflation_2019, unemployment_2021, unemployment_2020, unemployment_2019  = scrape_country_info(country_link)
        population_table.append([country_name, population, total_median_age, male_median_age, female_median_age, age_0_14, age_15_64, age_65_more, growth_rate, birth_rate, death_rate, total_life_expactancy, male_life_expactancy, female_life_expactancy, total_sex_ratio, gdp_2021, gdp_2020, gdp_2019, growth_gdp_2021, growth_gdp_2020, growth_gdp_2019, gdp_per_capita_2021, gdp_per_capita_2020, gdp_per_capita_2019, inflation_2021, inflation_2020, inflation_2019, unemployment_2021, unemployment_2020, unemployment_2019 ])
        counter += 1

    df = pd.DataFrame(population_table, columns=['Country', 'Population', 'Total Median Age', 'Male Median Age', 'Female Median Age', 'Age 0-14', 'Age 15-64', 'Age 65 and more', 'Population growth rate', 'Birth rate', 'Death rate', 'Total life expactancy', 'Male life expactancy', 'Female life expactancy', 'Total sex ratio', 'GDP 2021 (bn)', 'GDP 2020 (bn)', 'GDP 2019 (bn)', 'GDP growth rate 2021 (%)', 'GDP growth rate 2019 (%)', 'GDP growth rate 2019 (%)', 'GDP per capita 2021 (bn)', 'GDP per capita 2020 (bn)', 'GDP per capita 2019 (bn)', 'Inflation rate 2021 (%)', 'Inflation rate 2020 (%)', 'Inflation rate (%)', 'Unemployment rate 2021 (%)', 'Unemployment rate 2020 (%)', 'Unemployment rate 2019 (%)'])
    print("Information about countries in", continent_name)
    print(df.to_string(index=False))
    print()

    # Save to CSV
    filename = continent_name.lower() + '_countries.csv'
    file_path = os.path.join('/Users/oksana/Desktop/university/web_scraping/project', filename)
    df.to_csv(file_path, index=False)
    print("Information saved to", file_path)

print_country_info('https://www.cia.gov/the-world-factbook/africa/')
print_country_info('https://www.cia.gov/the-world-factbook/europe/')

# Existing code for scraping and processing data

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")   
