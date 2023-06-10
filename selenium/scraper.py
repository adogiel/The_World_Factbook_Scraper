from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
import datetime
import re
import pandas as pd
import os
import csv


threshold = True
thresholdLevel = 100
counter = 0

# Method for scraping information with Selenium
def scrapeInfoSelenium(continent):
    global thresholdLevel
    global threshold
    global counter

    # Init:
    gecko_path = '/opt/homebrew/bin/geckodriver'
    ser = Service(gecko_path)
    options = webdriver.firefox.options.Options()
    options.headless = False
    driver = webdriver.Firefox(options = options, service=ser)
    url = 'https://www.cia.gov/the-world-factbook/'

    continentName = continent

    # Actual program:
    driver.implicitly_wait(20)
    driver.get(url)
    driver.implicitly_wait(20)

    # Go to the chosen continent page
    continent = driver.find_element(By.PARTIAL_LINK_TEXT, continent)
    continent.click()
    driver.implicitly_wait(20)

    # Find all countries on the continent page
    country_elements = driver.find_elements(By.TAG_NAME, 'h5')
    country_names = [element.text for element in country_elements]

    continent_results = pd.DataFrame({'Country': [], 'Population': [] ,'Age 0-14 (male/female)': [], 'Age 15-64 (male/female)': [], 'Age 65 and more (male/female)': [], 'Total Median Age': [], 'Male Median Age': [], 'Female Median Age': [], 'Population growth rate': [], 'Birth rate': [], 'Death rate': [], 'Total sex ratio': [], 'Total life expactancy': [], 'Male life expactancy': [], 'Female life expactancy': [], 'GDP 2021 (bn)': [], 'GDP 2020 (bn)': [], 'GDP 2019 (bn)': [], 'GDP growth rate 2021 (%)': [], 'GDP growth rate 2020 (%)': [], 'GDP growth rate 2019 (%)': [], 'GDP per capita 2021 (bn)': [], 'GDP per capita 2020 (bn)': [], 'GDP per capita 2019 (bn)': [], 'Inflation rate 2021 (%)': [], 'Inflation rate 2020 (%)': [], 'Inflation rate 2019 (%)': [], 'Unemployment rate 2021 (%)': [], 'Unemployment rate 2020 (%)': [], 'Unemployment rate 2019 (%)': []})

    # Go through each country and scrape chosen information
    for country in country_names[:]:
        # Condition stopping the program if the limit of pages to scrap is reached
        if (threshold and counter >= thresholdLevel):
            break
        # Go to the country page
        country_link = driver.find_element(By.PARTIAL_LINK_TEXT, country)
        country_link.click()
        driver.implicitly_wait(20)

        # Find the population element and extract the population data
        try:
            population_element = driver.find_element(By.XPATH, '//h2[text()="People and Society"]//parent::div//following-sibling::div//p').text

            if population_element:
                match = re.search(r'(?<!\()\d{1,3}(?:,\d{3})*(?![\)\d])', population_element)
                population = match.group()
        except:
            population = ""

        # Find the age structure element and extract the age structure data
        try:
            age_structure = driver.find_element(By.XPATH, '//a[text()="Age structure"]//parent::h3//following-sibling::p').text

            if age_structure:
                age_0_14_element = re.split(r'%|NA', age_structure.split("0-14 years: ")[1])[0].strip()
                if age_0_14_element != "NA":
                    age_0_14 = age_0_14_element
                else:
                    age_0_14 = ""
                age_15_64_element = re.split(r'%|NA', age_structure.split("15-64 years: ")[1])[0].strip()
                if age_15_64_element != "NA":
                    age_15_64 = age_15_64_element
                else:
                    age_15_64 = ""
                age_65_more_element = re.split(r'%|NA', age_structure.split("65 years and over: ")[1])[0].strip()
                if age_65_more_element != "NA":
                    age_65_more = age_65_more_element    
                else:
                    age_65_more = ""
        except:
            age_0_14 = ""
            age_15_64 = ""
            age_65_more = ""

        # Find the median age element and extract the median age data
        try:
            medianAge_element = driver.find_element(By.XPATH, '//a[text()="Median age"]//parent::h3//following-sibling::p').text

            if medianAge_element:
                medianAgeT = medianAge_element.split("total: ")[1].split("years")[0].strip() if medianAge_element != "NA" else ""
                medianAgeM = medianAge_element.split("male: ")[1].split("years")[0].strip() if medianAge_element != "NA" else ""
                medianAgeF = medianAge_element.split("female: ")[1].split("years")[0].strip() if medianAge_element != "NA" else ""
        except:
            medianAgeT = ""
            medianAgeM = ""
            medianAgeF = ""

        # Find the population growth rate element and extract the population growth rate data
        try:
            populationGrowth_element = driver.find_element(By.XPATH, '//a[text()="Population growth rate"]//parent::h3//following-sibling::p').text 

            if populationGrowth_element:
                populationGrowth = populationGrowth_element.split("(")[0].strip() if populationGrowth_element != "NA" else ""
        except:
            populationGrowth = ""

        # Find the birth rate element and extract the birth rate data
        try:
            birthRate_element = driver.find_element(By.XPATH, '//a[text()="Birth rate"]//parent::h3//following-sibling::p').text

            if birthRate_element:
                if re.search(r"^\(\d{4} est.\)", birthRate_element):
                    birthRate = birthRate_element.split(")")[1].split("births")[0].strip() if birthRate_element != "NA" else ""
                else:
                    birthRate = birthRate_element.split("births")[0].strip() if birthRate_element != "NA" else ""
        except:
            birthRate = ""

        # Find the death rate element and extract the death rate data
        try:
            deathRate_element = driver.find_element(By.XPATH, '//a[text()="Death rate"]//parent::h3//following-sibling::p').text

            if deathRate_element:
                if re.search(r"^\(\d{4} est.\)", deathRate_element):
                    deathRate = deathRate_element.split(")")[1].split("deaths")[0].strip() if deathRate_element != "NA" else ""
                else:
                    deathRate = deathRate_element.split("deaths")[0].strip() if deathRate_element != "NA" else ""
        except:
            deathRate = ""

        # Find the sex ratio element and extract the sex ratio data
        try:
            sexRatio_element = driver.find_element(By.XPATH, '//a[text()="Sex ratio"]//parent::h3//following-sibling::p').text

            if sexRatio_element:
                sexRatioT = sexRatio_element.split("total population: ")[1].split("male(s)")[0].strip() if sexRatio_element != "NA" else ""
        except:
            sexRatioT = ""

        # Find the life expectancy element and extract the life expectancy data
        try:
            lifeExpectancy_element = driver.find_element(By.XPATH, '//a[text()="Life expectancy at birth"]//parent::h3//following-sibling::p').text

            if lifeExpectancy_element:
                lifeExpectancyTotal = re.split(r'years|NA', lifeExpectancy_element.split("total population: ")[1])[0].strip() 
                if lifeExpectancyTotal != "NA" :
                    lifeExpectancyT = lifeExpectancyTotal
                else:
                    lifeExpectancyT = ""
                lifeExpectancyMale = re.split(r'years|NA', lifeExpectancy_element.split("male: ")[1])[0].strip()
                if lifeExpectancyMale != "NA":
                    lifeExpectancyM = lifeExpectancyMale
                else:
                    lifeExpectancyM = ""
                lifeExpectancyFemale = re.split(r'years|NA', lifeExpectancy_element.split("female: ")[1])[0].strip()
                if lifeExpectancyFemale != "NA":
                    lifeExpectancyF = lifeExpectancyFemale
                else:
                    lifeExpectancyF = ""
        except:
            lifeExpectancyT = ""
            lifeExpectancyM = ""
            lifeExpectancyF = ""

        # Find the real GDP element and extract the real GDP data
        realGDP2021 = ''
        realGDP2020 = ''
        realGDP2019 = ''
    
        try:
            GDP_element = driver.find_element(By.XPATH, '//a[text()="Real GDP (purchasing power parity)"]//parent::h3//following-sibling::p').text

            if GDP_element:
                pattern = r'\$(.*?) billion \((\d{4}) est.\)'
                matches = re.findall(pattern, GDP_element)

                for match in matches:
                    GDP_element, year = match
                    if year == '2021':
                        realGDP2021 = GDP_element if GDP_element != "NA" else ""
                    elif year == '2020':
                        realGDP2020 = GDP_element if GDP_element != "NA" else ""
                    elif year == '2019':
                        realGDP2019 = GDP_element if GDP_element != "NA" else ""
        except:
            realGDP2021 = ""
            realGDP2020 = ""
            realGDP2019 = ""

        # Find the real GDP growth element and extract the real GDP growth data
        GDPGrowth2021 = ''
        GDPGrowth2020 = ''
        GDPGrowth2019 = ''

        try:
            GDPGrowth_element = driver.find_element(By.XPATH, '//a[text()="Real GDP growth rate"]//parent::h3//following-sibling::p').text

            if GDPGrowth_element:
                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, GDPGrowth_element)

                for match in matches:
                    GDPGrowth_element, year = match
                    if year == '2021':
                        GDPGrowth2021 = GDPGrowth_element if GDPGrowth_element != "NA" else ""
                    elif year == '2020':
                        GDPGrowth2020 = GDPGrowth_element if GDPGrowth_element != "NA" else ""
                    elif year == '2019':
                        GDPGrowth2019 = GDPGrowth_element if GDPGrowth_element != "NA" else ""
        except:
            GDPGrowth2021 = ""
            GDPGrowth2020 = ""
            GDPGrowth2019 = ""

        # Find the real GDP per capita element and extract the real GDP per capita data
        GDPCapita2021 = ''
        GDPCapita2020 = ''
        GDPCapita2019 = ''

        try:
            GDPCapita_element = driver.find_element(By.XPATH, '//a[text()="Real GDP per capita"]//parent::h3//following-sibling::p').text

            if GDPCapita_element:
                pattern = r'\$(.*?) \((\d{4}) est.\)'
                matches = re.findall(pattern, GDPCapita_element)

                for match in matches:
                    GDPCapita_element, year = match
                    if year == '2021':
                        GDPCapita2021 = GDPCapita_element if GDPCapita_element != "NA" else ""
                    elif year == '2020':
                        GDPCapita2020 = GDPCapita_element if GDPCapita_element != "NA" else ""
                    elif year == '2019':
                        GDPCapita2019 = GDPCapita_element if GDPCapita_element != "NA" else ""
        except:
            GDPCapita2021 = ""
            GDPCapita2020 = ""
            GDPCapita2019 = ""

        # Find the inflation element and extract the inflation data
        inflation2021 = ''
        inflation2020 = ''
        inflation2019 = ''

        try:
            inflation_element = driver.find_element(By.XPATH, '//a[text()="Inflation rate (consumer prices)"]//parent::h3//following-sibling::p').text 

            if inflation_element:
                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, inflation_element)

                for match in matches:
                    inflation_element, year = match
                    if year == '2021':
                        inflation2021 = inflation_element if inflation_element != "NA" else ""
                    elif year == '2020':
                        inflation2020 = inflation_element if inflation_element != "NA" else ""
                    elif year == '2019':
                        inflation2019 = inflation_element if inflation_element != "NA" else ""
        except:
            inflation2021 = ""
            inflation2020 = ""
            inflation2019 = ""

        # Find the unemployment element and extract the unemployment data
        unemployment2021 = ''
        unemployment2020 = ''
        unemployment2019 = ''

        try:
            unemployment_element = driver.find_element(By.XPATH, '//a[text()="Unemployment rate"]//parent::h3//following-sibling::p').text

            if unemployment_element:
                pattern = r'([\d.-]+)% \((\d{4}) est.\)'
                matches = re.findall(pattern, unemployment_element)

                for match in matches:
                    unemployment_element, year = match
                    if year == '2021':
                        unemployment2021 = unemployment_element if unemployment_element != "NA" else ""
                    elif year == '2020':
                        unemployment2020 = unemployment_element if unemployment_element != "NA" else ""
                    elif year == '2019':
                        unemployment2019 = unemployment_element if unemployment_element != "NA" else ""
        except:
            unemployment2021 = ""
            unemployment2020 = ""
            unemployment2019 = ""

        # Storing scraped information in a dataframe
        results = {'Country': country, 'Population': population, 'Age 0-14 (male/female)': age_0_14, 'Age 15-64 (male/female)': age_15_64, 'Age 65 and more (male/female)': age_65_more, 'Total Median Age': medianAgeT, 'Male Median Age': medianAgeM, 'Female Median Age': medianAgeF, 'Population growth rate': populationGrowth, 'Birth rate': birthRate, 'Death rate': deathRate, 'Total sex ratio': sexRatioT, 'Total life expactancy': lifeExpectancyT, 'Male life expactancy': lifeExpectancyM, 'Female life expactancy': lifeExpectancyF, 'GDP 2021 (bn)': realGDP2021, 'GDP 2020 (bn)': realGDP2020, 'GDP 2019 (bn)': realGDP2019, 'GDP growth rate 2021 (%)': GDPGrowth2021, 'GDP growth rate 2020 (%)': GDPGrowth2020, 'GDP growth rate 2019 (%)': GDPGrowth2019, 'GDP per capita 2021 (bn)': GDPCapita2021, 'GDP per capita 2020 (bn)': GDPCapita2020, 'GDP per capita 2019 (bn)': GDPCapita2019, 'Inflation rate 2021 (%)': inflation2021, 'Inflation rate 2020 (%)': inflation2020, 'Inflation rate 2019 (%)': inflation2019, 'Unemployment rate 2021 (%)': unemployment2021, 'Unemployment rate 2020 (%)': unemployment2020, 'Unemployment rate 2019 (%)': unemployment2019}

        continent_results = continent_results.append(results, ignore_index = True)

        # Counting number of pages scraped
        if threshold:
            counter += 1
       
       # Go back to the continent page
        driver.back()

    # Save to CSV
    filename = continentName + '_countries.csv'
    file_path = os.path.join('/Users/natalia.roszczypala/Desktop/Webscraping/project', filename)
    continent_results.to_csv(file_path, index=False)
    print("Information saved to", file_path)  

    # Close the browser
    driver.quit()

# Method for removing commas and converting values to float
def convert_to_float(value):
    if value != '':
        value = value.strip().replace(',', '.').replace('%', '')
        return float(value)
    else:
        return(0)

def convert_to_float_pop(value):
    if value != '':
        return float(value.replace(',', ''))
    else:
        return(0)

# Method for extract data from CSV file and calculating statistics
def calculateStatistics(file, columns_list, max_columns_list):
    with open(file, 'r') as file:
        countries = csv.reader(file)

    # Reading the header row to get the column names
        header = next(countries)

        column_indices = [header.index(column) for column in columns_list]
        max_column_indices = [header.index(column) for column in max_columns_list]

        selected_values = [[] for _ in columns_list]
        max_values = [[] for _ in max_columns_list]
    
    # Iterating over each row in the CSV file and converting the values in selected columns to float
        for row in countries:
            for i, index in enumerate(column_indices[:1], start=0):
                selected_values[i].append(convert_to_float_pop(row[index]))
            for i, index in enumerate(column_indices[1:], start=1):
                selected_values[i].append(convert_to_float(row[index]))
            for i, index in enumerate(max_column_indices[:1], start=0):
                max_values[i].append(convert_to_float_pop(row[index]))
            for i, index in enumerate(max_column_indices[1:], start=1):
                max_values[i].append(convert_to_float(row[index]))
    
    # Calculating statistics for selected columns
        averages = [sum(values) / len(values) for values in selected_values if len(values) > 0]
        max_value = [max(values) for values in max_values if len(values) > 0]
    
    # Printing the results
        for column, average in zip(columns_list, averages):
            rounded_average = round(average, 4)
            print(f"Average {column}: {rounded_average}")

        for column, maximum in zip(max_columns_list, max_value):
            rounded_maximum = round(maximum, 4)
            print(f"Maximum {column}: {rounded_maximum}")

start_time = time.time()

scrapeInfoSelenium("Africa")   
scrapeInfoSelenium("Europe")

end_time = time.time()
time_taken = end_time - start_time
print("Execution time for Selenium scraper:", time_taken, "seconds")

selected_columns = ['Population', 'Population growth rate', 'Birth rate', 'Death rate', 'Total life expactancy', 'Male life expactancy', 'Female life expactancy', 'Total Median Age', 'Male Median Age', 'Female Median Age', 'Total sex ratio', 'GDP 2021 (bn)', 'GDP growth rate 2021 (%)', 'GDP per capita 2021 (bn)', 'Inflation rate 2021 (%)', 'Inflation rate 2020 (%)', 'Inflation rate 2019 (%)', 'Unemployment rate 2021 (%)', 'Unemployment rate 2020 (%)', 'Unemployment rate 2019 (%)']

max_selected_columns = ['Population', 'Population growth rate', 'Birth rate', 'Death rate', 'Total life expactancy', 'Male life expactancy', 'Female life expactancy', 'Total Median Age', 'Male Median Age', 'Female Median Age', 'Total sex ratio', 'GDP 2021 (bn)', 'GDP growth rate 2021 (%)', 'GDP per capita 2021 (bn)', 'Inflation rate 2021 (%)', 'Inflation rate 2020 (%)', 'Inflation rate 2019 (%)', 'Unemployment rate 2021 (%)', 'Unemployment rate 2020 (%)', 'Unemployment rate 2019 (%)']

calculateStatistics("Africa_countries.csv", selected_columns, max_selected_columns)
calculateStatistics("Europe_countries.csv", selected_columns, max_selected_columns)
