from bs4 import BeautifulSoup
import requests

def get_data():
    base_url = "https://justjoin.it/"
    job_dict = {}
    
    main_response = requests.get(base_url)
    main_soup = BeautifulSoup(main_response.text, "html.parser")

    for i in range(20):
        # Extract link
        div_index = main_soup.find('div', attrs={'data-index': i})
        a_tag = div_index.find('a')

        if a_tag and 'href' in a_tag.attrs:
            offer_response = requests.get(f"https://justjoin.it{a_tag['href']}")
            offer_soup = BeautifulSoup(offer_response.text, "html.parser")

            # Extract title
            title_div = offer_soup.find('div', attrs={'class': 'css-s52zl1'})
            h1_title_tag = title_div.find('h1')

            # Extract salary
            try:
                salary = offer_soup.find("span", attrs={'class': 'css-1pavfqb'})
                salary_text = salary.text
            except:
                salary_text = "Undisclosed Salary"

            # Extract company
            company = offer_soup.find("h2", attrs={'class': 'css-77dijd'})

            # Extract location
            location = [offer_soup.find("span", attrs={'class': 'css-1o4wo1x'}).text]

            # Extract type of work (full-time, part-time etc.), job level (junior, mid, senior), operating mode (hybrid, remote etc.)
            other = [i.text for i in offer_soup.find_all("div", attrs={'class': 'css-snbmy4'})]

            # Extract skills
            skills =  [i.text for i in offer_soup.find_all("h4", attrs={'class': 'css-b849nv'})]

            # Extract description
            desc = offer_soup.find("div", attrs={'class': 'css-r1n8l8'})

            # Add all values to dict
            job_dict[i] = {
                "link": f"https://justjoin.it{a_tag['href']}",
                "title": h1_title_tag.text,
                "salary": salary_text,
                "company": company.text,
                "location": location,
                "type_of_work": other[0],
                "job_level": other[1],
                "operating_mode": other[3],
                # "desc": desc,
                "skills": skills
                }
            
            print(job_dict)
    #         offer_response.close()

    # main_response.close()

    # return job_dict

if __name__ == "__main__":
    get_data()