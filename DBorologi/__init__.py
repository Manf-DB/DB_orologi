import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

# Configurazione database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orologi.db'
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

from .routes import init_routes  # Importa le route
# Inizializza le route
init_routes(app)