# WebRL

## Requirement
python3, Selenium, torch, Levenshtein, BeautifulSoup, torchvision, PIL

## Run WebRL

python main.py -t <test_case> -o <old_url>  -n <new_url> -m <match_strategy> -c <chromedriver_path>

example:
python main.py -t yahoo_search -o http://web.archive.org/web/20200107001908/https://www.yahoo.com/  -n http://web.archive.org/web/20220221000940/https://www.yahoo.com/ -m Hyb -c /Users/Desktop/chromedriver

Explanation: The parameter -t represents the script is named as yahoo_search.py (need in the directory webTestScript), the parameter -m represents the repair strategy to apply (Hyb, CNN and COLOR).



