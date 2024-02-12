import requests
from bs4 import BeautifulSoup
import mysql.connector

def connect_integer_SQL(objects) :
    # Configurer la connexion à la base de données
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="yourdatabase"
    )

    # Créer un curseur pour exécuter des requêtes SQL
    mycursor = mydb.cursor()

    for _, object_list in objects.items():
        for object_info in object_list:
            name = object_info["name"]
            type = object_info["type"]
            level = object_info["level"]

            # Exécuter une requête SQL pour insérer les données
            sql = "INSERT INTO objects (name, type, level) VALUES (%s, %s, %s)"
            val = (name, type, level)
            mycursor.execute(sql, val)

            # Valider la transaction
            mydb.commit()

            print(mycursor.rowcount, "record inserted.")

    mydb.close()

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