## script for downloading reports from https://www.bls.gov/bls/news-release/cpi.htm
## assumes you have 2 files named "May02-current" and "Jan94-Apr02"
## need to install beautifulsoup4. 


import urllib.request as ulr ## reading url's
import re ## regex
from bs4 import BeautifulSoup as bs ## scrape pages


## initialize 
root_site = 'https://www.bls.gov'
cpi_link = 'https://www.bls.gov/bls/news-release/cpi.htm'
page = ulr.urlopen(cpi_link) # open link to page
soup = bs(page, 'html.parser') # pull html


## create list of urls for all pdf reports (May 2002 - current)
urls = []
for link in soup.find_all('a', {'href': re.compile('.*[0-9]{4}\.pdf')}):
    full_url = root_site + link.get('href')
    urls.append(full_url)
    
    
## create folder names by month-year
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months.reverse()
years = list(range(2002,2019))
years.reverse()
times = []
for year in years:
    for month in months:
        times.append(str(year) + '_' + month)
 

## deletion of months that aren't available in .pdf format
## could be cleaner if we could pull the <li> elements
del times[0:7]
times.reverse()
del times[0:4]
times.reverse()


## create tuples with folder names (times) and url for each report
## read each url, save to file in "May02-current" directory
zipped_pdfs = zip(times, urls)

for time, url in zipped_pdfs:
    res = ulr.urlopen(url)
    pdf = open("May02-current/" + time + '.pdf', 'wb')
    pdf.write(res.read())
    pdf.close()


## grab urls of reports prior to May 2002. Only available in .txt format
reports94to99 = soup.find_all('a', {'href': re.compile('.*9[4-9]\.txt')})
reports00to01 = soup.find_all('a', {'href': re.compile('.*200[0-1]\.txt')})
reports02 = soup.find_all('a', {'href': re.compile('.*0[0-5]..2002\.txt')})

reports_txt = reports02 + reports00to01 + reports94to99


## function for swapping order of 2 words in a string
def string_reverse(string):
    split = string.split(' ')
    split[0],split[1] = split[1],split[0]
    split = '_'.join(split)
    return(split)


## create list of names/dates for .txt reports
dates_txt = []
for link in reports_txt:
    dates_txt.append(string_reverse(link.text))
    
    
## create list of urls for .txt reports
urls_txt = []
for link in reports_txt:
    full_url = root_site + link.get('href')
    urls_txt.append(full_url)
    
    
## read each url, save to file in "Jan94-Apr02" directory
zipped_txt = zip(dates_txt, urls_txt)

for date, url in zipped_txt:
    res = ulr.urlopen(url)
    pdf = open("Jan94-Apr02/" + date + '.txt', 'wb')
    pdf.write(res.read())
    pdf.close()    