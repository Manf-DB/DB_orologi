import sqlite3
import os

db_path = os.path.join("..\instance\gestione_orologi.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ottieni i nomi delle colonne della tabella
cursor.execute("PRAGMA table_info(orologio);")
columns = cursor.fetchall()
conn.close()

print("Colonne nella tabella orologio:")
for column in columns:
    print(column[1])  # Il secondo elemento contiene il nome della colonna

