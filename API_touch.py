import requests
from bs4 import BeautifulSoup
import time
import random

def parse_object_page(url, object_n, object_list):
    """
    Fonction pour parser une page contenant des informations sur un type d'objet.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200 :

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('table', class_='ak-table')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells :
                    nom_index = 1
                    
                    if object_n in ["weapons", "equipment"]:
                        type_index = 3
                        niveau_index = 4
                    else:
                        type_index = 2
                        niveau_index = 3
                        
                    object_info = {
                        "name": cells[nom_index].text.strip(),
                        "type": cells[type_index].text.strip(),
                        "level": cells[niveau_index].text.strip()
                    }
                    object_list.append(object_info)
                    print(object_info)
            return True  # Indique que la page a été analysée avec succès
    else:
        print(f"Erreur lors de la requête vers la page {url}")
        return False  # Indique qu'il y a eu une erreur lors de la requête

def main():
    """
    Fonction principale pour récupérer les informations sur les objets.
    """
    base_url = "https://www.dofus-touch.com/en/mmorpg/encyclopedia"
    objects = {
        "weapons": [],
        "equipment": [],
        "consumables": [],
        "resources": []
    }

    for object_n, object_list in objects.items():
        url = f"{base_url}/{object_n}"
        parse_object_page(url, object_n, object_list)
        page = 2

        while True:
            page_url = f"{url}?page={page}"
            success = parse_object_page(page_url, object_n, object_list)
            if not success:
                break
            page += 1

if _name_ == "_main_":
    main()