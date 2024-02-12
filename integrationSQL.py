import mysql.connector

# Configurer la connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="yourdatabase"
)

# Créer un curseur pour exécuter des requêtes SQL
mycursor = mydb.cursor()

for object_n, object_list in objects.items():
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
