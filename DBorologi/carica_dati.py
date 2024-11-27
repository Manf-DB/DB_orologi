import sqlite3

# Funzione per creare una connessione al database
def create_connection(db_file):
    """Crea una connessione al database SQLite specificato."""
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connessione al database '{db_file}' avvenuta con successo.")
        return conn
    except sqlite3.Error as e:
        print(f"Errore nella connessione: {e}")
    return None

# Funzione per creare una tabella
def create_table(conn):
    """Crea una tabella nel database."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS orologio (
        nr_sacchetto INTEGER PRIMARY KEY,
        posizione TEXT,
        marca TEXT,
        modello TEXT,
        movimento TEXT,
        carica TEXT,
        calibro TEXT,
        nr_gioielli INTEGER,
        riserva_di_carica INTEGER,
        frequenza_alt_h TEXT,
        materiale_cassa TEXT,
        diametro_cassa TEXT,
        fondello TEXT,
        water_resistent TEXT,
        sfera_ora TEXT,
        sfera_minuti TEXT,
        sfera_secondi TEXT,
        cronografo TEXT CHECK (cronografo IN ('VERO', 'FALSO')),
        innesto_cronografico TEXT,
        smistamento_cronografico TEXT,
        secondi_cronografici TEXT,
        minuti_cronografici TEXT,
        ore_cronografiche TEXT,
        indicazione_data TEXT,
        indicazione_giorno_settimana TEXT,
        indicazione_mese TEXT,
        indicazione_riserva_di_carica TEXT,
        ghiera TEXT,
        materiale_bracciale_cinturino TEXT,
        chiusura_bracciale_cinturino TEXT,
        ulteriori_complicazioni TEXT,
        foto TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        print("Tabella 'orologio' creata (se non esisteva già).")
    except sqlite3.Error as e:
        print(f"Errore nella creazione della tabella: {e}")

# Funzione per inserire dati
def insert_data(conn, data):
    """Inserisce dati nella tabella."""
    insert_sql = """
    INSERT INTO orologio (nr_sacchetto, posizione, marca, modello, movimento, carica, calibro, nr_gioielli, riserva_di_carica, frequenza_alt_h, materiale_cassa, diametro_cassa, fondello, water_resistent, sfera_ora, sfera_minuti, sfera_secondi, cronografo, innesto_cronografico, smistamento_cronografico, secondi_cronografici, minuti_cronografici, ore_cronografiche, indicazione_data, indicazione_giorno_settimana, indicazione_mese, indicazione_riserva_di_carica, ghiera, materiale_bracciale_cinturino, chiusura_bracciale_cinturino, ulteriori_complicazioni, foto)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cursor = conn.cursor()
        cursor.executemany(insert_sql, data)
        conn.commit()
        print(f"{cursor.rowcount} record inseriti con successo.")
    except sqlite3.Error as e:
        print(f"Errore nell'inserimento dei dati: {e}")

# Funzione principale
def main():
    database = "orologi.db"  # Nome del file del database
    
    # Dati da inserire (aggiungere nr_sacchetto esplicitamente per ciascun record)
    dati = [
        (1, "CN", "Panerai", "Luminor 8 DAYS GMT PAM00233 1950", "meccanico", "manuale", "Panerai P.2002", 21, 0, "28800", "acciaio", "44", "trasparente", "10 bar", "grande", "grande", "piccoli a ore 9", "FALSO", "nn", "nn", "no", "no", "no", "finestrella a ore 3", "no", "no", "lineare a ore 6", "no", "Alligatore", "ardiglione", "finestrella giorno/notte", ""),
        (2, "CN", "Cartier", "Santos 100 XL cronografo W20090X8", "meccanico", "automatica", "Cartier 8630MC", 27, 42, "28800", "acciaio", "51x41", "chiuso", "10 bar", "grande", "grande", "piccoli a ore 9", "FALSO", "", "", "grandi", "piccoli a ore 3", "piccole a ore 6", "finestrella a ore 5", "no", "no", "no", "no", "Alligatore", "deployante", "", ""),
        (3, "CN", "Omega", "Speedmaster Professional Moonwatch", "meccanico", "manuale", "Omega 1861", 18, 48, "21600", "acciaio", "42", "chiuso", "5 bar", "grande", "grande", "piccoli a ore 9", "FALSO", "laterale", "a camma", "grandi", "piccoli a ore 3", "piccole a ore 6", "no", "no", "no", "no", "scala tachimetrica", "Acciaio", "deployante", "", ""),
        (4, "CN", "Longines", "Master Collection L2.673.4.78.3", "meccanico", "automatica", "Longines L687.2", 25, 54, "28800", "acciaio", "40", "trasparente", "3 bar", "grande", "grande", "piccoli a ore 9", "FALSO", "laterale", "a ruota a colonne", "grandi", "piccoli a ore 12", "piccole a ore 6", "con lancetta centrale", "finestrella a ore 12", "finestrella a ore 12", "no", "no", "Alligatore", "deployante", "24 ore a ore 9, fasi lunari a ore 6", ""),
        (5, "CN", "Hamilton", "KHAKI AVIATION X-WIND AUTO CHRONO - H77726151", "meccanico", "automatica", "Hamilton H-21", 25, 60, "28800", "acciaio", "45", "trasparente", "10 bar", "grande", "grande", "piccoli a ore 3", "FALSO", "laterale", "a camma", "grandi", "piccoli a ore 6", "piccole a ore 12", "finestrella a ore 9", "finestrella a ore 9", "no", "no", "doppia ghiera a con scala mobile", "Acciaio", "deployante", "", ""),
        (6, "Cas", "Glycine", "Airman Base 22 Sphair Fade to Grey", "meccanico", "automatica", "Glycine GL293", 21, 42, "28800", "acciaio", "42", "trasparente", "20 bar", "24 ore", "grande", "grandi", "FALSO", "nn", "nn", "no", "no", "no", "finestrella a ore 3", "no", "no", "no", "secondo fuso", "tessuto", "ardiglione", "", ""),
        (7, "Cas", "U-Boat", "Capsoil SS 8110", "quarzo", "batteria", "Ronda 503", 0, 0, "nn", "acciaio", "45", "trasparente", "10 bar", "grande", "grande", "grandi", "FALSO", "nn", "nn", "no", "no", "no", "no", "no", "no", "no", "no", "bovino", "ardiglione", "movimento a bagno d'olio", ""),
        (8, "Cas", "Tissot", "LE LOCLE AUTOMATIC CHRONOGRAPH VALJOUX T41.1.387.51", "meccanico", "automatica", "ETA 7750", 25, 48, "28800", "acciaio", "42", "trasparente", "3 bar", "grande", "grande", "piccoli a ore 9", "FALSO", "laterale", "a camma", "grandi", "piccoli a ore 12", "piccole a ore 6", "finestrella a ore 3", "finestrella a ore 3", "no", "no", "no", "Acciaio", "deployante", "", "")
    ]
    
    # Crea connessione
    conn = create_connection(database)
    
    if conn:
        # Crea tabella
        create_table(conn)
        
        # Inserisci dati
        insert_data(conn, dati)
        
        # Chiudi connessione
        conn.close()
        print("Connessione chiusa.")

if __name__ == "__main__":
    main()
