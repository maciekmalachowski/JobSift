from bs4 import BeautifulSoup
import requests

def get_data():
    base_url = "https://justjoin.it/"
    job_dict = {}
    
    main_response = requests.get(base_url)
    soup = BeautifulSoup(main_response.text, "html.parser")

    for i in range(20):
        # Extract link
        div_index = soup.find('div', attrs={'data-index': i})
        a_tag = div_index.find('a')

        if a_tag and 'href' in a_tag.attrs:
            offer_response = requests.get(f"https://justjoin.it{a_tag['href']}")
            soup = BeautifulSoup(offer_response.text, "html.parser")

            # Extract title
            title_div = soup.find('div', attrs={'class': 'css-s52zl1'})
            h1_title_tag = title_div.find('h1')

            # Extract salary
            try:
                salary = soup.find("span", attrs={'class': 'css-1pavfqb'})
                salary_text = salary.text
            except:
                salary_text = "Undisclosed Salary"

            # Extract company
            company = soup.find("h2", attrs={'class': 'css-77dijd'})

            # Extract location
            location = soup.find("span", attrs={'class': 'css-1o4wo1x'})

            # Extract type of work (full-time, part-time etc.), job level (junior, mid, senior), operating mode (hybrid, remote etc.)
            other = [i.text for i in soup.find_all("div", attrs={'class': 'css-snbmy4'})]

            # Extract description
            desc = soup.find("div", attrs={'class': 'css-r1n8l8'})

            # Add all values to dict
            job_dict[i] = {
                "link": f"https://justjoin.it{a_tag['href']}",
                "title": h1_title_tag.text,
                "salary": salary_text,
                "company": company.text,
                "location": location.text,
                "type_of_work": other[0],
                "job_level": other[1],
                "operating_mode": other[3],
                "desc": desc
                }
            
            offer_response.close()

    main_response.close()

    return job_dict

if __name__ == "__main__":
    get_data()