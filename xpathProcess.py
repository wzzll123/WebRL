# encoding=utf-8
import time


def generateXpathFromSeleniumElement(el,currentXpathString):
    childTag=el.tag_name
    if(childTag=="html"):
        return "/html[1]"+currentXpathString
    parentElement=el.find_element_by_xpath("..")
    childrenElements=parentElement.find_elements_by_xpath("*")
    count=0
    for childrenElement in childrenElements:
        childrenElementTag=childrenElement.tag_name
        if(childTag==childrenElementTag):
            count=count+1
        if(childrenElement==el):
            return generateXpathFromSeleniumElement(parentElement,"/" + childTag + "[" + str(count) + "]"+currentXpathString)
def addLocationToSoupAttribute(soup,el):
    soup_children = list(soup.children)
    selenium_childen = list(el.find_elements_by_xpath("*"))
    if(len(soup_children) == len(selenium_childen)):
        for i,childElement in enumerate(soup.children):
            # childTag=childElement.name
            # if(childTag==None):
            #     # print childElement
            #     continue
            # childTag=childTag.encode("utf-8")
            addLocationToSoupAttribute(childElement,selenium_childen[i])


    else:
        print(soup)
    # print(list(soup.html.children))
    # print(list(el.find_element_by_xpath("/html[1]").find_elements_by_xpath("*")))
def addXpathToSoupAttribute(soup):
    addXpathToSoupAttributeMain(soup.html,"/html[1]")
def addXpathToSoupAttributeMain(HTMLElement,currentXpathString):
    HTMLElement.attrs["xpath"]=currentXpathString
    #print currentXpathString
    # if(currentXpathString=="/html[1]/body[1]/div[5]/div[2]/div[1]/div[1]/div[2]/div[2]/a[1]"):
    #     print HTMLElement
    count = {}
    for childElement in HTMLElement.children:
        childTag=childElement.name
        if(childTag==None):
            # print childElement
            continue
        childTag=childTag.encode("utf-8")
        if(childTag not in count.keys()):
            count[childTag]=1
        else:
            count[childTag]=count[childTag]+1
        addXpathToSoupAttributeMain(childElement,currentXpathString+"/"+str(childTag, encoding = "utf-8")+"[" + str(count[childTag]) + "]")
def main():
    pass
    # driver = webdriver.Chrome(executable_path='/Users//Desktop/chromedriver')
    # driver.get('file:///Users//Desktop/webProject/w3schools2016/index.html')
    # import htmlMatch
    # hp = htmlMatch.HtmlProcess()
    # soup = hp.getRoot(open("guider_output/w3c/0/01.html"))
    # el = driver.find_element_by_xpath("/html[1]")
    # addLocationToSoupAttribute(soup.html,el)

if __name__ == '__main__':
    main()
