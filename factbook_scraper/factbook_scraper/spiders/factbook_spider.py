import scrapy
import time
import re

class FactbookSpider(scrapy.Spider):
    name = 'FactbookSpider'
    start_urls = ['https://www.cia.gov/the-world-factbook/africa/'] 
                  
                #   'https://www.cia.gov/the-world-factbook/europe/', 'https://www.cia.gov/the-world-factbook/middle-east/' ]

    count = 0
    start_time = 0
    limit = False

    def start_requests(self):
        self.start_time = time.time()
        yield from super().start_requests()

    def parse(self, response):
        continent_name = response.css('h1.hero-title::text').get().strip()
        country_elements = response.css('a.link-button.bold')
        for element in country_elements:
            # We break the loop if we get 100 countries listed 
            if FactbookSpider.limit == True:
                if FactbookSpider.count >= 100:
                    break
            country_link = response.urljoin(element.attrib['href'])
            # For each country link, we call method "parse_country_info" and we provide variable with the continent that the country is placed on 
            yield scrapy.Request(country_link, callback=self.parse_country_info, meta={'continent_name': continent_name})
            # For Each country we increase counter by one 
            FactbookSpider.count += 1


    def parse_country_info(self, response):
        
        continent_name = response.meta['continent_name']
        country_name = response.css('h1.hero-title::text').get().strip() , ''

        # Extracting data depends if there is a response
        
        population_element = response.css('div#people-and-society>div:contains("Population")>p::text')
        if population_element:
            population_element = population_element.get().strip()
        else:
            population_element= ""

        population_growth_rate = response.css('#people-and-society>div:contains("Population growth rate")>p::text')
        if population_growth_rate:
            population_growth_rate= population_growth_rate.get().strip()
        else:
            population_growth_rate = ""

        birth_rate = response.css('#people-and-society>div:contains("Birth rate")>p::text')
        if birth_rate:
            birth_rate= birth_rate.get().strip() 
        else:
            birth_rate = ""

        death_rate= response.css('#people-and-society>div:contains("Death rate")>p::text')
        if death_rate:
            death_rate= death_rate.get().strip()
        else:
            death_rate = ""


        # Extracting data into arrays and then checking if data is present for specific values. We repeat "same" thing for each values we can get into array  
        age_structure = response.css('#people-and-society>div:contains("Age structure")>p::text').getall()
        age_0_14 = age_structure[0].strip() if age_structure else ""
        age_15_64 = age_structure[1].strip() if len(age_structure)>=2 else ""
        age_65_more = age_structure[2].strip() if len(age_structure)>=3 else ""

        median = response.css('#people-and-society>div:contains("Median age")>p::text').getall()
        total_median_age = median[0].strip() if median else ""
        male_median_age = median[1].strip() if len(median) >= 2 else ""
        female_median_age = median[2].strip() if len(median) >= 3 else ""

        life_expectancy = response.css('#people-and-society>div:contains("Life expectancy at birth")>p::text').getall()
        total_life_expectancy = life_expectancy[0].strip() if life_expectancy else ""
        male_life_expectancy = life_expectancy[1].strip() if len(life_expectancy)>=2 else ""
        female_life_expectancy = life_expectancy[2].strip() if len(life_expectancy)>=3 else ""

        sex_ratio = response.css('#people-and-society>div:contains("Sex ratio")>p::text').getall()
        total_sex_ratio = sex_ratio[len(sex_ratio)-1].strip() if sex_ratio else "";

        real_gdp = response.css('div#economy>div:contains("Real GDP (purchasing power parity)")>p::text').getall()
        gdp_2021 = ''
        gdp_2020 = ''
        gdp_2019 = ''
        if real_gdp:
            real_gdp_text = ' '.join(real_gdp)
            pattern = r'\$(.*?) \((\d{4}) est.\)'
            matches = re.findall(pattern, real_gdp_text)
            for match in matches:
                real_gdp_value, year = match 
                if year == '2021':
                    gdp_2021 = real_gdp_value
                elif year == '2020':
                    gdp_2020 = real_gdp_value
                elif year == '2019':
                    gdp_2019 = real_gdp_value


        real_gdp_growth = response.css('#economy>div:contains("Real GDP growth rate")>p::text').getall()
        gdp_growth_2021 = ''
        gdp_growth_2020 = ''
        gdp_growth_2019 = ''
        if real_gdp_growth:
            real_gdp_growth_text = ' '.join(real_gdp_growth)
            pattern = r'([\d.-]+)% \((\d{4}) est.\)'
            matches = re.findall(pattern, real_gdp_growth_text)
            year = ''
            for match in matches:
                gdp_growth_value, year = match 
                if year == '2021':
                    gdp_growth_2021 = gdp_growth_value
                elif year == '2020':
                    gdp_growth_2020 = gdp_growth_value
                elif year == '2019':
                    gdp_growth_2019 = gdp_growth_value

        real_gdp_per_capita = response.css('#economy>div:contains("Real GDP per capita")>p::text').getall()
        gdp_per_capita_2021 = ''
        gdp_per_capita_2020 = ''
        gdp_per_capita_2019 = ''
        if real_gdp_per_capita:
            real_gdp_per_capita_text = ' '.join(real_gdp_per_capita)
            pattern = r'\$(.*?) \((\d{4}) est.\)'
            matches = re.findall(pattern, real_gdp_per_capita_text)
            year = ''
            for match in matches:
                real_gdp_per_capita_value, year = match 
                if year == '2021':
                    gdp_per_capita_2021 = real_gdp_per_capita_value
                elif year == '2020':
                    gdp_per_capita_2020 = real_gdp_per_capita_value
                elif year == '2019':
                    gdp_per_capita_2019 = real_gdp_per_capita_value

        inflation_rate = response.css('#economy>div:contains("Inflation rate (consumer prices)")>p::text').getall()
        inflation_rate_2021 = ''
        inflation_rate_2020 = ''
        inflation_rate_2019 = ''
        if inflation_rate:
            infation_rate_text = ' '.join(inflation_rate)
            pattern = r'([\d.-]+)% \((\d{4}) est.\)'
            matches = re.findall(pattern, infation_rate_text)
            year =''
            for match in matches:
                inflation_value, year = match 
                if year == '2021':
                    inflation_rate_2021 = inflation_value
                elif year == '2020':
                    inflation_rate_2020 = inflation_value
                elif year == '2019':
                    inflation_rate_2019 = inflation_value

        unemployment_rate = response.css('#economy>div:contains("Unemployment rate")>p::text').getall()
        unemployment_rate_2021 = ''
        unemployment_rate_2020 = ''
        unemployment_rate_2019 = ''
        if unemployment_rate:
            # Join the list elements into a single string
            unemployment_rate_text = ' '.join(unemployment_rate)  
            pattern = r'([\d.-]+)% \((\d{4}) est.\)'
            matches = re.findall(pattern, unemployment_rate_text)
            year = ''
            for match in matches:
                unemployment_value, year = match 
                if year == '2021':
                    unemployment_rate_2021 = unemployment_value
                elif year == '2020':
                    unemployment_rate_2020 = unemployment_value
                elif year == '2019':
                    unemployment_rate_2019 = unemployment_value

        # yielding all the collected data and then we can save that to csv file 
        yield {
            'Continent': continent_name,
            'Country': country_name,
            'Population': population_element,
            'Age 0-14': age_0_14,
            'Age 15-64': age_15_64,
            'Age 65 and more': age_65_more,
            'Total Median Age': total_median_age,
            'Male Median Age': male_median_age,
            'Female Median Age': female_median_age,
            'Population Growth Rate': population_growth_rate,
            'Birth Rate': birth_rate,
            'Death Rate': death_rate,
            'Total Life Expectancy': total_life_expectancy,
            'Male Life Expectancy': male_life_expectancy,
            'Female Life Expectancy': female_life_expectancy,
            'Total Sex Ratio': total_sex_ratio,
            'GDP 2021 (bn)': gdp_2021,
            'GDP 2020 (bn)': gdp_2020,
            'GDP 2019 (bn)': gdp_2019,
            'GDP Growth Rate 2021 (%)': gdp_growth_2021,
            'GDP Growth Rate 2020 (%)': gdp_growth_2020,
            'GDP Growth Rate 2019 (%)': gdp_growth_2019,
            'GDP per capita 2021 (bn)': gdp_per_capita_2021,
            'GDP per capita 2020 (bn)': gdp_per_capita_2020,
            'GDP per capita 2019 (bn)': gdp_per_capita_2019,
            'Inflation Rate 2021 (%)': inflation_rate_2021,
            'Inflation Rate 2020 (%)': inflation_rate_2020,
            'Inflation Rate 2019 (%)': inflation_rate_2019,
            'Unemployment Rate 2021 (%)': unemployment_rate_2021,
            'Unemployment Rate 2020 (%)': unemployment_rate_2020,
            'Unemployment Rate 2019 (%)': unemployment_rate_2019
        }

    def closed(self, reason):
        running_time = time.time() - self.start_time
        print("Total running time: {:.2f} seconds".format(running_time))