# encoding=utf-8
import re
import time


def normarlizaXpath(absolute_xpath: str):
    # covert /html/body to /html[1]/body[1]
    # Split the absolute XPath into individual elements
    elements = absolute_xpath.split('/')[1:]
    normalized_xpath = ""

    for i, element in enumerate(elements):
        # Extract the element name and index (if present)
        match = re.match(r"([a-zA-Z0-9\-]+)(?:\[(\d+)\])?", element)

        if match:
            tag_name = match.group(1)
            index = match.group(2)
            # Build the normalized XPath
            normalized_xpath += f"/{tag_name}[{index or 1}]"
        elif 'local-name' in element:
            normalized_xpath = normalized_xpath + '/' + element + '[1]'
        else:

            raise ValueError("Invalid absolute XPath format")
    # print(absolute_xpath, normalized_xpath)
    return normalized_xpath
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
