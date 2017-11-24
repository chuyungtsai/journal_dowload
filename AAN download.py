import requests
import datetime
import urllib
from bs4 import BeautifulSoup


def download_file(download_url, filename):
    try:
        resp = requests.get(download_url)
        if resp.status_code == 200:
            response = urllib.request.urlopen(download_url)
            file = open(filename, 'wb')
            file.write(response.read())
            print(filename + " is downloaded")
            file.close()
    except Exception as e:
        return None

def doi_to_pdf(doi):
    dom = requests.get(doi).text
    soup = BeautifulSoup(dom, 'html5lib')
    pdf = soup.find('li',class_='notice full-text-pdf-view-link primary').a['href']
    print(pdf[:-5])
    final_url = "http://www.neurology.org"+pdf[:-5]
    return final_url

def main():
    print('AAN clinical reasoning')
    urlpt1 = 'http://www.neurology.org/search?submit=yes&submit=yes&andorexacttitle=and&RESULTFORMAT=1&sortspecbrief=relevance&%20Fellow%20Section=&FIRSTINDEX='
    urlpt2 = '&hits=10&title=Clinical%20Reasoning&titleabstract=&flag=&sortspec=date&andorexacttitleabs=and&displaysectionid=RESIDENT%20AND%20FELLOW%20SECTION&tocsectionid=Resident%20and%20Fellow%20Section&tocsectionid=Resident%20&andorexactfulltext=and&hitsbrief=25&fulltext='
    for i in range(0,300, 10):
        url = urlpt1 + str(i) + urlpt2
        dom = requests.get(url).text
        soup = BeautifulSoup(dom, 'html5lib')
        date_list=[]
        for ele in soup.find_all('cite'):
            paper_date = ele.find('span',class_='cit-print-date').text
            new_date = datetime.datetime.strptime(paper_date, '%B %d, %Y,  ').strftime('%Y%m%d')+" AAN clinical reasoning"
            date_list.append(new_date)
            doi =ele.a['href']

            if date_list.count(new_date)>1:
                pdfname = new_date + '-' + str(date_list.count(new_date)) + '.pdf'
            else:
                pdfname = new_date + '.pdf'
            pdfurl = doi_to_pdf(doi)
            download_file(pdfurl, pdfname)


if __name__ == '__main__':
    main()