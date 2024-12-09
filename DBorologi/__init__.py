import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_cors import CORS  # Importa l'estensione Flask-CORS



app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le origini

# Configurazione database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestione_orologi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('DBorologi', 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite di 16 MB per i file caricati
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Formati di immagine consentiti
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)


# Verifica che il file abbia un'estensione valida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Modello per il database
class Orologio(db.Model):
    nr_sacchetto = db.Column(db.Integer, primary_key=True)
    posizione = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modello = db.Column(db.String(100), nullable=False)
    movimento = db.Column(db.String(100), nullable=False)
    carica = db.Column(db.String(100), nullable=False)
    calibro = db.Column(db.String(100), nullable=False)
    nr_gioielli = db.Column(db.Integer, nullable=True)
    riserva_di_carica = db.Column(db.Integer, nullable=True)
    frequenza_alt_h = db.Column(db.String(100), nullable=False)
    materiale_cassa = db.Column(db.String(100), nullable=False)
    diametro_cassa = db.Column(db.String(100), nullable=False)
    fondello = db.Column(db.String(100), nullable=False)
    water_resistent = db.Column(db.String(100), nullable=False)
    sfera_ora = db.Column(db.String(100), nullable=False)
    sfera_minuti = db.Column(db.String(100), nullable=False)
    sfera_secondi = db.Column(db.String(100), nullable=False)
    cronografo = db.Column(db.String(10), nullable=False)  # Si/No
    innesto_cronografico = db.Column(db.String(100), nullable=False)
    smistamento_cronografico = db.Column(db.String(100), nullable=False)
    secondi_cronografici = db.Column(db.String(100), nullable=False)
    minuti_cronografici = db.Column(db.String(100), nullable=False)
    ore_cronografiche = db.Column(db.String(100), nullable=False)
    indicazione_data = db.Column(db.String(100), nullable=False)
    indicazione_giorno_settimana = db.Column(db.String(100), nullable=False)
    indicazione_mese = db.Column(db.String(100), nullable=False)
    indicazione_riserva_di_carica = db.Column(db.String(100), nullable=False)
    ghiera = db.Column(db.String(100), nullable=False)
    materiale_bracciale_cinturino = db.Column(db.String(100), nullable=False)
    chiusura_bracciale_cinturino = db.Column(db.String(100), nullable=False)
    ulteriori_complicazioni = db.Column(db.String(200), nullable=True)
    foto = db.Column(db.String(300), nullable=True)  # Percorso dell'immagine

#    def __repr__(self):
#       return f"<Orologio {self.nr_sacchetto} - {self.marca} {self.modello}>"

# Creazione del database
with app.app_context():
    db.create_all()

def query_database(query, params):
    conn = sqlite3.connect('gestione_orologi.db')  # mio database
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Funzione per caricare la foto
def save_photo(photo):
    if photo:
        # Costruisci il nome del file e il percorso
        filename = photo.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        return filename  # Restituisce solo il nome del file per salvarlo nel database
    return None

# Funzione per recuperare i dettagli di un orologio dal database in modo dinamico
def get_details_from_db(nr_sacchetto):
    db_path = os.path.join("instance\gestione_orologi.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Recupera i nomi delle colonne dalla tabella 'orologio'
    cursor.execute("PRAGMA table_info(orologio);")
    columns = cursor.fetchall()

    # Crea un dizionario per memorizzare i dati
    column_names = [column[1] for column in columns]  # La colonna 1 contiene i nomi delle colonne
    query = "SELECT * FROM orologio WHERE nr_sacchetto = ?"
    cursor.execute(query, (nr_sacchetto,))
    data = cursor.fetchone()

    conn.close()
    
    # Se i dati sono stati trovati, crea un dizionario con i nomi delle colonne come chiavi
    if data:
        return dict(zip(column_names, data))
    return None

def save_details_to_db(details):
    db_path = os.path.join("instance\gestione_orologi.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ottieni i nomi delle colonne
    cursor.execute("PRAGMA table_info(orologio);")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    # Aggiungi chiavi mancanti a `details` con valori predefiniti
    for col in column_names:
        if col not in details:
           details [col] = col  # O un valore predefinito, se applicabile

    # Crea una lista per i valori da aggiornare (ignora nr_sacchetto per l'aggiornamento)
    values = [details[col] for col in column_names if col != 'nr_sacchetto']
    
    # Crea la clausola SET dinamicamente
    set_clause = ", ".join([f"{col} = ?" for col in column_names if col != 'nr_sacchetto'])
    
    # Aggiungi nr_sacchetto alla lista dei valori
    values.append(details['nr_sacchetto'])
    
    # Costruisci la query dinamica
    query = f"UPDATE orologio SET {set_clause} WHERE nr_sacchetto = ?"
    
    #print("Query SQL:", query)  # DEBUG: Mostra la query generata
    print("Valori SQL:", values)  # DEBUG: Mostra i valori passati
    
    # Esegui la query di aggiornamento
    cursor.execute(query, values)
    conn.commit()
    conn.close()


from .routes import init_routes  # Importa le route
# Inizializza le route
init_routes(app)