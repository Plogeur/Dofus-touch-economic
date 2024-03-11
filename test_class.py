from bs4 import BeautifulSoup
import re
import string
import csv
import asyncio
import aiohttp

def generate_combinations(x):
    letters = string.ascii_lowercase
    
    # Recursive generator function to yield combinations
    def generate_combinations_rec(prefix, length):
        if length == 0:
            yield prefix
            return
        for char in letters:
            new_prefix = prefix + char
            yield from generate_combinations_rec(new_prefix, length - 1)
    
    # Loop through lengths from 1 to x
    for length in range(1, x + 1):
        yield from generate_combinations_rec('', length)

async def fetch_page(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()

async def parse_object_page(session, url, object_list):
    html = await fetch_page(session, url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table', class_='ak-table ak-responsivetable')
        if table:
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if cells:
                    name = cells[1].text.strip()
                    if name not in object_list:
                        class_name = cells[2].text.strip()
                        niveau_str = cells[3].text.strip()
                        niveau = int(re.search(r'\d+', niveau_str).group())
                        sexe = cells[4].text.strip()
                        serveur = cells[5].text.strip()
                        guild = cells[6].text.strip() if cells[6].text.strip() else None
                        
                        user_link = row.find('a', href=True)
                        user_url = user_link['href']
                        user_url = "https://www.dofus-touch.com" + user_url
                        
                        user_response = await fetch_page(session, user_url)
                        if user_response:
                            user_soup = BeautifulSoup(user_response, "html.parser")
                            
                            guild_level_tag = user_soup.find('span', class_='ak-infos-guildlevel')
                            guild_level = int(guild_level_tag.text.split()[1]) if guild_level_tag else None

                            alliance_name_tag = user_soup.find('a', class_='ak-infos-alliancename')
                            alliance_name = alliance_name_tag.text.strip() if alliance_name_tag else None

                            alignment_name_tag = user_soup.find('span', class_='ak-alignment-name')
                            alignment_name = alignment_name_tag.text.strip() if alignment_name_tag else None

                            total_xp_tag = user_soup.find('div', class_='ak-total-xp')
                            total_xp_text = total_xp_tag.find('span').text.strip() if total_xp_tag else None
                            total_xp = int(total_xp_text.replace(' ', '')) if total_xp_text else None

                            jobs = {}
                            job_elements = user_soup.find_all('div', class_=lambda value: value and value.startswith('ak-list-element ak-infos-job-'))
                            for job_element in job_elements:
                                job_name = job_element.find('div', class_='ak-title').text.strip()
                                job_level_text = job_element.find('div', class_='ak-text').text.strip()
                                job_level = int(re.search(r'\d+', job_level_text).group()) if job_level_text else None
                                jobs[job_name] = job_level

                            object_list[name] = {
                                "class_name": class_name,
                                "niveau": niveau,
                                "sexe": sexe,
                                "serveur": serveur,
                                "guild": guild,
                                "guild_level": guild_level,
                                "alliance_name": alliance_name,
                                "alignment_name": alignment_name,
                                "total_xp": total_xp,
                                "jobs": jobs if jobs else None
                            }
                            print(len(object_list))

async def main():
    object_list = {}
    base_url = "https://www.dofus-touch.com/fr/mmorpg/communaute/annuaires/pages-persos?text={}&page={}"
    string_generator = generate_combinations(2)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for name_search in string_generator:
            for page in range(1, 10):  # Adjust the range based on the number of pages you want to scrape.
                url = base_url.format(name_search, page)
                task = asyncio.ensure_future(parse_object_page(session, url, object_list))
                tasks.append(task)
        await asyncio.gather(*tasks)

    save_object_list_to_csv(object_list)
    print("fin")

def save_object_list_to_csv(object_list):
    """
    Save the object_list to a CSV file.
    """
    filename = "classe_touch.csv"
    fieldnames = ['ID', 'class_name', 'niveau', 'sexe', 'serveur', 'guild', 'guild_level',
                  'alliance_name', 'alignment_name', 'total_xp', 'jobs']

    # Write object_list to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id, caract in object_list.items():
            # Create a row dictionary with ordered keys
            row = {'ID': id}
            row.update(caract)
            # Write the row to the CSV file
            writer.writerow({key: row[key] for key in fieldnames})

if __name__ == "__main__":
    asyncio.run(main())
