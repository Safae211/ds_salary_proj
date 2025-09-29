import requests
from bs4 import BeautifulSoup
import csv

page = requests.get('https://www.glassdoor.com/sitedirectory/data-science.html')

def main(page):
    
    src = page.content
    soup = BeautifulSoup(src,'lxml')
    print(soup)

main(page)
