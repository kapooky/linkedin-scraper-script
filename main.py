import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters


import re


# Prints out event data to the console
# @params event:EventData, case: String denoting the case(Good,Bad,Best,etc)
def printout(data,case):
    print(case)
   # print(set(other.findall(txt)))
    print(data.link)
    print(data.apply_link)
    print(data.description)
    print('-------------------------------------------------------')

def uniqueMatches(array):
    return bool(len(array))

def on_data(data: EventData):
    txt = data.description

    amazon = re.compile(r'\b(amazon|aws)\b', flags=re.I ).findall(txt)

    tools = re.compile(r'\b(terraform|docker|linux|ansible)\b', flags=re.I).findall(txt)

    language = re.compile(r'\b(node(js)?|Typescript|javascript|python|bash)\b', flags=re.I).findall(txt) 

    location = re.compile(r'\b(Canada|sponser|remote|graduated?)\b', flags=re.I).findall(txt) 

    #This matches for years of experience, see https://regex101.com/r/KwngR1/2
    years = re.compile(r"(\d+(?:-\d+)?\+?)\s*(or more|to)?(years?)", re.I).findall(txt)

    #Match only for 1-2 year of experience 
    entrylevel = re.compile(r"([3-9](?:-[3-9])?\+?)\s*(or more|to)?(years?)", re.I).findall(txt)

    #special regex 
    graduate = re.compile(r"graduated?").findall(txt)




    #This if-else is block is a bottle neck for performance. It's better to cache the results from UniqueMatches than to re-compute 
    #it everytime. I don't care about performance, so it doesn't matter to me. 
    if uniqueMatches(amazon) >= 1 and uniqueMatches(tools) >= 1  and  uniqueMatches(language) >= 1 and uniqueMatches(location) > 0 and not uniqueMatches(years):
         printout(data, "perfect case")
    elif uniqueMatches(amazon) >= 1 and uniqueMatches(tools) >= 1  and uniqueMatches(language) >= 1 and uniqueMatches(location) >= 0 and not uniqueMatches(years):
         printout(data, "Good case")
         #parse for 'graduate/graduated' token in the advert 
    elif uniqueMatches(amazon) >= 1 and uniqueMatches(tools) >= 1  and uniqueMatches(language) >= 1 and uniqueMatches(location) >= 0 and uniqueMatches(graduate):
        #Special case for university graduate jobs 
         printout(data, "graduate")
    elif uniqueMatches(amazon) >= 1 and uniqueMatches(tools) >= 1  and uniqueMatches(language) >= 1 and uniqueMatches(location) >= 0 and not uniqueMatches(entrylevel):
         printout(data,"entrylevel")


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_options=None,  # You can pass your custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests (429)' errors
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

limit = 1500
queries = [
    Query(
        query='Cloud Engineer',
        options=QueryOptions(
            locations=['Canada',"United-States"],
            optimize=False,
            limit=limit,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                experience=[ExperienceLevelFilters.INTERNSHIP, ExperienceLevelFilters.ASSOCIATE, ExperienceLevelFilters.ENTRY_LEVEL]
            )
        )
    ),
    Query(
             query='Cloud architect',
             options=QueryOptions(
                 locations=['Canada','United-States'],
                 optimize=False,
                 limit= limit,
                 filters=QueryFilters(
                     relevance=RelevanceFilters.RECENT,
                     time=TimeFilters.MONTH,
                     experience=[ExperienceLevelFilters.INTERNSHIP, ExperienceLevelFilters.ASSOCIATE, ExperienceLevelFilters.ENTRY_LEVEL]
                 )
             )
         ),
          Query(
                      query='Devops Engineer',
                      options=QueryOptions(
                          locations=['Canada','United-States'],
                          optimize=False,
                          limit=limit,
                          filters=QueryFilters(
                              relevance=RelevanceFilters.RECENT,
                              time=TimeFilters.MONTH,
                              experience=[ExperienceLevelFilters.INTERNSHIP, ExperienceLevelFilters.ASSOCIATE, ExperienceLevelFilters.ENTRY_LEVEL]
                          )
                      )
                  )
]

scraper.run(queries)