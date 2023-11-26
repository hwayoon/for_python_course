from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
options=Options()
browser=webdriver.Chrome(options=options)

def get_page_count(keyword):
    base_url="https://kr.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")
    soup=BeautifulSoup(browser.page_source, "html.parser")
    pagination=soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
    if pagination==None:
        return 1
    pages=pagination.find_all("li", recursive=False)
    count=len(pages)
    if count==0:
        return count+1
    elif count!=0:
        return count

def extract_indeed_jobs(keyword):
    pages=get_page_count(keyword)
    results=[]
    for page in range(pages):
        base_url="https://kr.indeed.com/jobs"
        final_url=f"{base_url}?q={keyword}&start={page*10}"
        browser.get(final_url)
        soup=BeautifulSoup(browser.page_source, "html.parser")
        job_list=soup.find("ul",class_="eu4oa1w0")
        jobs=job_list.find_all('li',recursive=False)
        for job in jobs:
            zone=job.find("div", class_="mosaic-zone")
            if zone==None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link=anchor['href']
                company=job.find("span", attrs={"data-testid":"company-name"})
                location=job.find("div", attrs={"data-testid":"text-location"})
                job_data={
                    'link':f"https://kr.indeed.com{link}",
                    'company':company.string.replace(",", " "),
                    'location':location.string.replace(",", " "),
                    'position':title.replace(",", " ")
                }
                results.append(job_data)
        if page==4:
            soup=BeautifulSoup(browser.page_source, "html.parser")
            pagination=soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
            new_pages=pagination.find_all("li", recursive=False)
            new_count=len(new_pages)
            while new_count!=4:
                browser.get(f"{base_url}?q={keyword}&start={(page+1)*10}")
                soup=BeautifulSoup(browser.page_source, "html.parser")
                job_list=soup.find("ul",class_="eu4oa1w0")
                jobs=job_list.find_all('li',recursive=False)
                for job in jobs:
                    zone=job.find("div", class_="mosaic-zone")
                    if zone==None:
                        anchor = job.select_one("h2 a")
                        title = anchor['aria-label']
                        link=anchor['href']
                        company=job.find("span", attrs={"data-testid":"company-name"})
                        location=job.find("div", attrs={"data-testid":"text-location"})
                        job_data={
                            'link':f"https://kr.indeed.com{link}",
                            'company':company.string.replace(",", " "),
                            'location':location.string.replace(",", " "),
                            'position':title.replace(",", " ")
                        }
                        results.append(job_data)
                page=page+1
                soup=BeautifulSoup(browser.page_source, "html.parser")
                pagination=soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
                new_pages=pagination.find_all("li", recursive=False)
                new_count=len(new_pages)
    return results