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
    if count >=5:
        return 5
    else:
        return count

print(get_page_count("react"))
print(get_page_count("python"))
print(get_page_count("django"))
print(get_page_count("nestjs"))
print(get_page_count("java"))
print(get_page_count("c#"))

range()#start point here

def extract_indeed_jobs(keyword):
    pages=get_page_count(keyword)
    base_url="https://kr.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")

    results=[]
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
                'company':company.string,
                'location':location.string,
                'position':title,
            }
            results.append(job_data)
    for result in results:
        print(result)
        print("===========================================================")