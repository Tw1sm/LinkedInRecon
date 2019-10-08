#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
import argparse


def flags():
    parser = argparse.ArgumentParser(description="Gathers a given company's employees from LinkedIn", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-c", "--company", type=str, dest="company", help="Target company", required=True)
    parser.add_argument("-p", "--pages", type=int, dest="pages", default=5, help="Number of result pages to iterate through (100 per page)", required=False)
    parser.add_argument("-o", "--output", type=str, dest="output", default="output.csv", help="name and path of output csv", required=False)
    
    return parser.parse_args()


def request(company, start):
    ua = UserAgent()
    url = 'https://www.google.com/search'
    params = {
        'nl': 'en',
        'q': f'site:linkedin.com/in "{company}"'.encode('utf8'),
        'start': start,
        'num': 100
    }
    headers = {'User-Agent': ua.random}
    
    r = requests.get(url, headers=headers, params=params)
    return r.text


def check_comma(text):
    if ',' in text:
        return f'"{text}"'
    else:
        return text


def main():
    args = flags()
    company = args.company
    pages = args.pages
    output = args.output
   
    emps = [] # holds resulting employee dictionaries

    print('[*] Googling...')
    for pagenum in range(0, pages):
        start = 100 * pagenum
        html = request(company, start)

        soup =  BeautifulSoup(html, 'html.parser')
        divs = soup.findAll("div", attrs={"class": "g"})
        results_div = soup.find("div", attrs={"id": "resultStats"})
        
        if pagenum == 0:
            print(f'[+] {results_div.text}')

        print(f'[*] Processing page {pagenum + 1}...')
        for li in divs:
            a = li.find("a")
            if a is not None:

                # init empty dict
                emp = {
                    'Name': '',
                    'Title': '',
                    'Company': ''
                }

                name = a.text.strip()
                split_name = name.split('-')

                if len(split_name) > 2:
                    emp['Company'] = check_comma(split_name[2])

                if len(split_name) > 1:
                    emp['Title'] = check_comma(split_name[1])
                
                emp['Name'] = check_comma(split_name[0])
                emps.append(emp)


    # write output CSV
    print('[*] Writing to CSV file...')
    with open(output, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Title', 'Company'])
        writer.writeheader()

        for emp in emps:
            writer.writerow(emp)

    print('[+] Done!')
    

if __name__ == '__main__':
    main()

