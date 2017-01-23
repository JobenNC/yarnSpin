import requests
import pdb
import random
from bs4 import BeautifulSoup
#Create a "proper noun remix" of a story from fanfiction.net

#TODO:
# - What is the best way to re-use the similar usage of random array access
#   and url append?

def hasLast(tag):
    return tag.text == "Last"

try:
    url = "http://fanfiction.com"

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    #soup = BeautifulSoup(page.text, 'html.parser')
    tables = soup.find_all(id = ["gui_table1i", "gui_table2i"])
    table = tables[random.randrange(len(tables))]
    links = table.find_all("a")
    link = links[random.randrange(len(links))]["href"]
    #soup = BeautifulSoup(requests.get(url))


    soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')
    #Will only be one table
    table = soup.find_all(id="list_output")[0]
    links = table.find_all("a")
    link = links[random.randrange(len(links))]['href']

    soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')

    #TODO
    # - Crossovers will involve an extra step!!!!
    # - presence of div w/ id="list_output" means we have another selection to make
    #   same as above
    # - Otherwise look for last page

    #soup = BeautifulSoup(requests.get('https://www.fanfiction.net/crossovers/Hetalia-Axis-Powers/3616/').text, 'html.parser')

    if len(soup.find_all(id="list_output")) > 0:
        print("Selecting second item in crossover")
        table = soup.find_all(id="list_output")[0]
        links = table.find_all("a")
        link = links[random.randrange(len(links))]['href']
        soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')


    #soup = BeautifulSoup(requests.get("https://www.fanfiction.net/book/Harry-Potter").text, 'html.parser')
    #https://www.fanfiction.net/book/Harry-Potter/?p=4
    #TODO
    # - find if multi-page, if so, find last page
    # - soup.find_all(id="content_wrapper_inner")[0].center
    pageInfo = soup.find_all(id="content_wrapper_inner")[0].center
    if pageInfo is not None and pageInfo.a is not None:
        print("Multi page entry")
        last = pageInfo.find_all(hasLast)
        if len(last) > 0:
            lastPage = int(pageInfo.find_all("a")[-2]["href"].rsplit("=",1)[1])
        else:
            #TODO only multi page scenario without Last is 2 page, right?
            print("check: there should only be two pages for this category")
            lastPage = 2
        newPage = random.randrange(lastPage+1)
        newPage =  "/?p=" + str(newPage)

        aList = pageInfo.find_all("a")
        soup = BeautifulSoup(requests.get(url + link + newPage).text, 'html.parser')
    else:
        newPage = ""
        print("only single page category")

    print(url+link+newPage)
    pdb.set_trace()

except Exception as e:
    print("Exception encountered: %s" %(e))
    pdb.set_trace()
