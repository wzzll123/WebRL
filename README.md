# WebRL
WebRL is a tool for repairing broken UI test scripts automatically.
## Getting Started with WebRL
### Prerequisites
python3, Selenium, torch, Levenshtein, BeautifulSoup, torchvision, PIL

### Running WebRL
```
usage: python main.py [-t test_case] [-o old_url] [-n new_url] [-m strategy] [-c chromedriver_path]
- optional arguments:
  -t test_case          the name of a test script that needed in the directory webTestScript/
  -m strategy           the repair strategy to apply (Hyb, COLOR, CNN, webEvo and SFTM)
  -o old_url            
  -n new_url         
  -c chromedriver_path   
```
### Example
```
python main.py -t yahoo_search -o http://web.archive.org/web/20200107001908/https://www.yahoo.com/  -n http://web.archive.org/web/20220221000940/https://www.yahoo.com/ -m Hyb -c /Users/Desktop/chromedriver
```
The original yahoo_search.py can be found in webTestScript/, the repaired script can be found in WebRL_output/yahoo_search.
## Experiment
Our experiment builds upon the dataset established in Similo ("Similarity-based web element localization for robust test automation". ACM Trans. Softw. Eng. Methodol. 2023). To begin, clone their repository using the command `git clone https://github.com/michelnass/Similo2.git`.

After cloning, navigate to the exp/ directory and modify the config.json file to specify the root path and the path to Similo.

Following this, execute make_website.py in the exp/ directory to generate UI test scripts and other necessary files.

Finally, run exp_similo.py to conduct the experiment and obtain the experimental results. You can customize the repair mode by modifying the repairMode variable in exp_similo.py to use different tools for the experiment.


