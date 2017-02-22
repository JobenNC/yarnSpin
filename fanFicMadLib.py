import requests
import random
from bs4 import BeautifulSoup
#from remix import remix
import nltk
import pdb
#Create a "proper noun remix" of a story from fanfiction.net

#TODO:
# - What is the best way to re-use the similar usage of random array access
#   and url append?

def hasLast(tag):
    return tag.text == "Last"



# NOTE:
# from nltk.download()
# - punkt
# - averaged_perceptron_tagger
# - maxent_ne_chunker
# - words
# pip deps
# - pip install numpy
# - pip install nltk
# - pip install beautifulsoup4
# - pip install requests

def remix(text):
    names = set()
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() == 'PERSON':
                    print(chunk)
                    name = []
                    for leaf in chunk.leaves():
                        name.append(leaf[0])
                    names.add(" ".join(name))
    return list(names)
                    #print(chunk)
            #    print(chunk.node, ' '.join(c[0] for c in chunk.leaves()))

#pdb.set_trace()

def getStory():
    try:
        url = "http://fanfiction.com"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        tables = soup.find_all(id = ["gui_table1i", "gui_table2i"])
        table = tables[random.randrange(len(tables))]
        links = table.find_all("a")
        link = links[random.randrange(len(links))]["href"]

        soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')
        #Will only be one table
        table = soup.find_all(id="list_output")[0]
        links = table.find_all("a")
        link = links[random.randrange(len(links))]['href']

        soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')
        #Handle crossovers
        if len(soup.find_all(id="list_output")) > 0:
            print("Selecting second item in crossover")
            table = soup.find_all(id="list_output")[0]
            links = table.find_all("a")
            link = links[random.randrange(len(links))]['href']
            soup = BeautifulSoup(requests.get(url + link).text, 'html.parser')

        pageInfo = soup.find_all(id="content_wrapper_inner")[0].center
        # - Handle multi-page items
        if pageInfo is not None and pageInfo.a is not None:
            print("Multi page entry")
            last = pageInfo.find_all(hasLast)
            if len(last) > 0:
                lastPage = int(pageInfo.find_all("a")[-2]["href"].rsplit("=",1)[1])
            else:
                # only multi page scenario without Last should be 2 pagers
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

        stories = soup.find_all(class_="stitle")
        if len(stories) < 1:
            raise Exception("Empty stories list")
        story = stories[random.randrange(len(stories))]['href']
        soup = BeautifulSoup(requests.get(url + story).text, 'html.parser')
        print(url + story)

        # - check if english
        isEnglish = soup.find_all(class_="xgray xcontrast_txt")[0].text.find("English")
        if isEnglish == -1:
            raise Exception("Non english story")

        # - Pull out story
        paragraphs = soup.find_all(id="storytext")[0].find_all("p")
        paragraphs = soup.find_all("p")
        story = ""
        for p in paragraphs:
            story = story + "\\n\\n" + p.text
        if story == "":
            raise Exception("Story is blank.  debug.")
        names = remix(story)
        print(names)

        print("%s names found" %(len(names)))

        #Get replacements from stdin
        #for i in range(0, len(names)):
        #    newName = input("Please input name to replace '%s'.  If it's not a real name, just re-enter the same value.: " %(names[i]))
        #    print ("%s replaceing %s" %(newName, names[i]))
        #    newStory = story.replace(names[i], newName)

        #print(story)
        return (names, story)

    except Exception as e:
        #TODO: Move on to the next story if this attempt fails
        print("!!!!-----REATTEMPT")
        return getStory()

if __name__ == "__main__":
    print(getStory())
