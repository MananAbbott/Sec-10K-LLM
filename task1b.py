from openai import OpenAI
import os
import glob
import matplotlib.pyplot as plt
# from task1 import download_10k_filings
client = OpenAI(api_key='sk-proj-0KQ887k2NEPcgSX2KhUCT3BlbkFJncEuEyU0CZmRzAx0jCP6')
import re
from bs4 import BeautifulSoup

def analyze_10k_filings(company_ticker):
    if not os.path.exists(f"./sec-edgar-filings/{company_ticker}"):
        download_10k_filings([company_ticker], 1995, 2023, "./sec-edgar-filings", "mhabbott@umas.edu")
    path_pattern = f"./sec-edgar-filings/{company_ticker}/**/*.txt"
    file_paths = glob.glob(path_pattern, recursive=True)
    
    combined_text = ""
    keywords = ['assets', 'income', 'sales']  # Keywords to search for in tables
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'lxml')
                
                tables = soup.find_all('table')
                for table in tables:
                    # Extract text from the table
                    table_text = ' '.join([tr.get_text(separator=" ", strip=True) for tr in table.find_all('tr')])
                    
                    # Check if any keyword exists in the table text
                    if all(keyword in table_text.lower() for keyword in keywords):
                        combined_text += table_text + " \n\n"

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if not combined_text:
        return "No text available for analysis."
    combined_text = combined_text[:23500]
    
    insights = {}
    questions = [
        {"role": "system", "content": "You are a financial analyst who needs to extract specific financial insights from SEC 10-K filings."},
        {"role": "user", "content":combined_text}
    ]

    for key in ["Profitability", "Cash Flow", "Revenue Growth"]:
        questions.append({"role": "user", "content": f"give me an array of {key.lower()} values based on the text i provided. I do not need anything else. Just a python list with year by year value in it from 1995 to 2023 with every element as a tuple with year and the value"})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=questions,
            temperature=0.5,
            max_tokens=500
        )
        insights[key] = response.choices[0].message.content


    return insights


company_ticker = "MSFT"
insights = analyze_10k_filings(company_ticker)
for key, value in insights.items():
    # get the array from the value string
    array = re.findall(r"\((\d+),\s*(\d+(\.\d+)?)\)", value)
    if array:
        # convert the array to a list
        array = [(float(x), float(y))for x,y, _ in array]
        #seperate the first values of tuple in one list and second values of tuple in another
        x, y = zip(*array)
        #plot the graph
        plt.plot(x, y, label=key)
        plt.xlabel('Year')
        plt.ylabel(value)
        plt.title(key)
        plt.legend()
        plt.show()

    