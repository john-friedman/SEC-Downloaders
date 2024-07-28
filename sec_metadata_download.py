import csv
import json

# 

basic_company_data_path = "../data/basic_company_data.json"
with open(basic_company_data_path, "r") as file:
    basic_company_data = json.load(file)

with open('../data/company_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['cik', 'ticker', 'title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for key in basic_company_data:
        cik_str = basic_company_data[key]['cik_str']
        ticker = basic_company_data[key]['ticker']
        title = basic_company_data[key]['title']
        writer.writerow({'cik': cik_str, 'ticker': ticker, 'title': title})