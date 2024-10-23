from bs4 import BeautifulSoup
import requests
from keybert import KeyBERT

def get_data():
    base_url = "https://bulldogjob.pl/companies/jobs/s/page,{}"
    job_dict = {}
    kw_model = KeyBERT()
    index = 0

    for i in range(1, 2):
        url = base_url.format(i)
        main_response = requests.get(url)
        main_soup = BeautifulSoup(main_response.text, "html.parser")
    
        # Get all links from current page
        links = main_soup.find_all("a", attrs={'class': 'JobListItem_item__M79JI'})
        for link in links:
            # Extract link
            if link and 'href' in link.attrs:
                offer_response = requests.get(link['href'])
                offer_soup = BeautifulSoup(offer_response.text, "html.parser")

                # Extract title
                title = offer_soup.find('h1', class_ = ['text-c32', 'font-medium', 'mt-3'])

                # Extract salary
                salary = offer_soup.find("p", class_ = ['text-c22', 'xl:text-2xl'])
                if salary and (salary.text == 'Packages and extras' or salary.text == 'Pakiety i dofinansowania'):
                    salary_text = "Undisclosed Salary"
                elif salary:
                    salary_text = salary.text

                # Extract company
                company = offer_soup.find("h2", class_ = ['text-c20', 'leading-6', 'font-medium', 'text-gray-500'])

                # Extract location
                parent_location = offer_soup.find('p', string=lambda x: x in ['Location', 'Lokalizacja'])
                if parent_location:
                    cities = parent_location.find_parent('div').find_all('p', class_ = ['text-md', 'xl:text-c22', 'leading-6'])
                    locations = [city.text for city in cities]
                else:
                    locations = ["Only remote"]

                # Extract type of work (full-time, part-time etc.)
                parent_type = offer_soup.find('p', string=lambda x: x in ['Employment Type', 'Typ współpracy'])
                if parent_type:
                    type_of_work = parent_type.find_parent('div').find_all('p', class_ = ['text-md', 'xl:text-c22', 'leading-6'])

                # Extract job level (junior, mid, senior)
                parent_type = offer_soup.find('p', string=lambda x: x in ['Experience', 'Doświadczenie'])
                if parent_type:
                    job_level = parent_type.find_parent('div').find_all('p', class_ = ['text-md', 'xl:text-c22', 'leading-6'])

                # # Extract operating mode (hybrid, remote etc.)
                parent_type = offer_soup.find('p', string=lambda x: x in ['Remote work', 'Praca zdalna'])
                if parent_type:
                    operating_mode = parent_type.find_parent('div').find_all('p', class_ = ['text-md', 'xl:text-c22', 'leading-6'])

                # # Extract skills
                skill_desc =  offer_soup.find("section", attrs={'id': '3-panel'})
                ul = skill_desc.find("ul")
                
                if ul:
                    keywords = kw_model.extract_keywords(ul.text)
                    skills = [skill for skill, _ in keywords]
                else:
                    skills = ["Hard to tell"]

                # Extract description
                # desc = offer_soup.find("section", attrs={'id': '1-panel'})

                # Add all values to dict
                
                job_dict[f"bulldog_jobs_{index}"] = {
                    "link": link['href'],
                    "title": title.text,
                    "salary": salary_text,
                    "company": company.text,
                    "location": locations,
                    "type_of_work": type_of_work[0].text,
                    "job_level": job_level[0].text,
                    "operating_mode": f"{operating_mode[0].text} remote",
                    # "desc": desc,
                    "skills": skills
                    }
                
                index += 1                

            offer_response.close()

    main_response.close()

    return job_dict

if __name__ == "__main__":
    get_data()