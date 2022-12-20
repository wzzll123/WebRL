# WebRL
WebRL is a tool for repairing broken UI test scripts automatically.
## Getting Started with WebRL
### Prerequisites
python3, Selenium, torch, Levenshtein, BeautifulSoup, torchvision, PIL

### Running WebRL
```
usage: python main.py [-t test_case] [-o old_url] [-n new_url] [-m strategy] [-c chromedriver_path]
- optional arguments:
  -t test_case          the name of a test script
  -m strategy           the repair strategy to apply (Hyb, COLOR and CNN)
  -o old_url            
  -n new_url         
  -c chromedriver_path   
```
### Example
```
python main.py -t yahoo_search -o http://web.archive.org/web/20200107001908/https://www.yahoo.com/  -n http://web.archive.org/web/20220221000940/https://www.yahoo.com/ -m Hyb -c /Users/Desktop/chromedriver
```
The original yahoo_search.py can be found in webTestScript/, the repaired script can be found in WebRL_output/yahoo_search.



