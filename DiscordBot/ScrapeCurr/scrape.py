import requests
from bs4 import BeautifulSoup

class Scrape:
    def __init__(self, url):
        self.url = url
        
    def get_soup(self):
        source = requests.get(self.url).text
        soup = BeautifulSoup(source, 'lxml')
        return soup

    def get_curr_data(self, soup, curr_data):

        curr_meta = []
        curr_meta.append(soup.find("a", { "id" : curr_data.get("dollar",None) }).text.split("\n"))
        curr_meta.append(soup.find("a", { "id" : curr_data.get("euro",None) }).text.split("\n"))
        curr_meta.append(soup.find("a", { "id" : curr_data.get("bitcoin",None) }).text.split("\n"))

        curr_meta = self.clear_list(curr_meta)

        return curr_meta

    @staticmethod
    def clear_list(lst):
        formatted_list = []
        for item in lst:
            temp = []
            for i in item:
                if i:
                    temp.append(i)
            formatted_list.append(temp)
        return formatted_list