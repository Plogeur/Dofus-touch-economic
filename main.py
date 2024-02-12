from API_touch import parse_object_page
from API_touch import connect_integer_SQL

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
        connect_integer_SQL(object_list)

if __name__ == "__main__":
    main()