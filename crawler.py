#!/usr/bin/env python

import urllib
import re

class Entry:
    def __init__(self, _type, href, filename, d):
        self.type = _type 
        self.href = href 
        self.date = d 
        self.filename = filename

    def is_folder(self):
        if self.type == '[DIR]':
            return True
        return False

class Crawler:
    def __init__(self):
        pass

    def crawl(self, url):
        entries = self.__get_entries(url) 
        for entry in entries:
            if entry.is_folder(): 
                print "Crawling entry: %s" % (entry.href)
                self.crawl(entry.href) 
            else:
                print "Downloading file %s ..." % (entry.filename)
                self.__download(entry) 

    def __download(self, entry):
        file_content = urllib.urlopen(entry.href).read()
        with open(entry.filename, 'w') as f:
            f.write(file_content) 

    def __get_entries(self, url):
        content = self.__get_content(url)
        pattern = re.compile('<img src="(.*?)" alt="(.*?)"></td><td><a href="(.*?)">(.*?)</a></td><td align="right">(.*?)</td><td align="right">')
        m = pattern.findall(content)

        entries = []
       
        for element in m: 
            _type = element[1]
            href = element[3]
            d = element[4]
            
            entry = Entry(_type, url + href, href, d) 
            entries.append(entry)

        return entries

    def __get_content(self, url):
        return urllib.urlopen(url).read() 

def main():
    crawler = Crawler()
    crawler.crawl("http://domain-to-crawl.com/") 

if __name__ == "__main__":
    main() 
