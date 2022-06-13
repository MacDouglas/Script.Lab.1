import requests
from bs4 import BeautifulSoup

DegreesOfSeparation = None
LinksInUse = set()

def SixDegreesOfSeparation(_currlink, _destLink, _currDepth = 0, _maxDepth = 6, path = None): 
    global DegreesOfSeparation, LinksInUse

    if (_currDepth == _maxDepth): 
        return None
    if _currlink == _destLink:
        DegreesOfSeparation = path
        return None       
    if (DegreesOfSeparation is not None):
        return None
    if path is None:
        path = []

    print(f"Link: {_currlink}")
    print(f"Depth: {_currDepth}")

    LinksInUse.add(_currlink)
    
    response = requests.get(_currlink)
    if response.reason != "OK":
        raise Exception(f"Cant get content from link {_currlink}\n")
    content = requests.get(_currlink).content
    

    bs = BeautifulSoup(content, 'html.parser')
    if bs.html["lang"] != 'en':
        return None
    
    body = bs.find(id="bodyContent")
    extractedLinks = body.find_all("a", href=True)


    articles = [
        _localLink['href'] 
        for _localLink in extractedLinks 
        if ("/wiki/" in _localLink['href']) and CheckArticleLink(_localLink['href'])
    ]
    
    links = [
        "https://en.wikipedia.org" + article 
        for article in articles
    ]
    
    if _destLink in links:
        DegreesOfSeparation = path
        return None
    
    results = [SixDegreesOfSeparation(_link,
            _destLink,
            _currDepth + 1,
            _maxDepth,
            path = path + [_currlink]) 
        for _link in links 
            if _link not in LinksInUse
    ]

    for result in results:
        if (result is not None):
            DegreesOfSeparation = result
            break

def CheckArticleLink(_link, _sortLists = False, _sortIndexes = False):
    isArticle = ":" not in _link
    
    if _sortLists:
        isArticle = isArticle and "List" not in _link
    
    if _sortIndexes:
        isArticle = isArticle and "Index" not in _link

    return isArticle

if __name__ == '__main__':    
    link_a = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
    link_b = "https://en.wikipedia.org/wiki/The_Twilight_Zone_(2019_TV_series)#Episodes"
       
    SixDegreesOfSeparation(link_a, link_b)
    
    if DegreesOfSeparation is None:
        print("Path is not found!")
    
    else:
        print(link_a, " => ".join(DegreesOfSeparation[1:]), " => ", link_b)
