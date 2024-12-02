import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

from DBorologi import Orologio, allowed_file, db, query_database

def init_routes(app):
    # Route principale per visualizzare e aggiungere orologi
    @app.route('/', methods=['GET', 'POST'])
    def index():
        orologi = Orologio.query.all()
        return render_template('index.html', orologi=orologi)

    # Route per aggiungere orologi
    @app.route('/insert', methods=['GET', 'POST'])
    def insert():
        if request.method == 'POST':
            # Ottenere dati dal form
            nr_sacchetto = request.form['nr_sacchetto']
            posizione = request.form['posizione']
            marca = request.form['marca']
            modello = request.form['modello']
            movimento = request.form['movimento']
            carica = request.form['carica']
            calibro = request.form['calibro']
            nr_gioielli = request.form.get('nr_gioielli', 0)
            riserva_di_carica = request.form.get('riserva_di_carica', 0)
            frequenza_alt_h = request.form['frequenza_alt_h']
            materiale_cassa = request.form['materiale_cassa']
            diametro_cassa = request.form['diametro_cassa']
            fondello = request.form['fondello']
            water_resistent = request.form['water_resistent']
            sfera_ora = request.form['sfera_ora']
            sfera_minuti = request.form['sfera_minuti']
            sfera_secondi = request.form['sfera_secondi']
            cronografo = request.form['cronografo']
            innesto_cronografico = request.form['innesto_cronografico']
            smistamento_cronografico = request.form['smistamento_cronografico']
            secondi_cronografici = request.form['secondi_cronografici']
            minuti_cronografici = request.form['minuti_cronografici']
            ore_cronografiche = request.form['ore_cronografiche']
            indicazione_data = request.form['indicazione_data']
            indicazione_giorno_settimana = request.form['indicazione_giorno_settimana']
            indicazione_mese = request.form['indicazione_mese']
            indicazione_riserva_di_carica = request.form['indicazione_riserva_di_carica']
            ghiera = request.form['ghiera']
            materiale_bracciale_cinturino = request.form['materiale_bracciale_cinturino']
            chiusura_bracciale_cinturino = request.form['chiusura_bracciale_cinturino']
            ulteriori_complicazioni = request.form.get('ulteriori_complicazioni', '')
            # Gestione del file immagine
            foto = request.files.get('foto')
            foto_filename = None

            if foto and allowed_file(foto.filename):
                # Salva l'immagine nella cartella di upload
                foto_filename = secure_filename(foto.filename)

                # Controlla e crea la directory se non esiste
                upload_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Salva l'immagine nella cartella di upload
                foto_path = os.path.join(upload_folder, foto_filename)
                foto.save(foto_path)
                print(f"Foto salvata con nome: {foto_filename} in {foto_path}")
            else:
                print("Nessun file selezionato o file non valido")

            # Creare una nuova istanza di Orologio
            nuovo_orologio = Orologio(
                nr_sacchetto=nr_sacchetto,
                posizione=posizione,
                marca=marca,
                modello=modello,
                movimento=movimento,
                carica=carica,
                calibro=calibro,
                nr_gioielli=nr_gioielli,
                riserva_di_carica=riserva_di_carica,
                frequenza_alt_h=frequenza_alt_h,
                materiale_cassa=materiale_cassa,
                diametro_cassa=diametro_cassa,
                fondello=fondello,
                water_resistent=water_resistent,
                sfera_ora=sfera_ora,
                sfera_minuti=sfera_minuti,
                sfera_secondi=sfera_secondi,
                cronografo=cronografo,
                innesto_cronografico=innesto_cronografico,
                smistamento_cronografico=smistamento_cronografico,
                secondi_cronografici=secondi_cronografici,
                minuti_cronografici=minuti_cronografici,
                ore_cronografiche=ore_cronografiche,
                indicazione_data=indicazione_data,
                indicazione_giorno_settimana=indicazione_giorno_settimana,
                indicazione_mese=indicazione_mese,
                indicazione_riserva_di_carica=indicazione_riserva_di_carica,
                ghiera=ghiera,
                materiale_bracciale_cinturino=materiale_bracciale_cinturino,
                chiusura_bracciale_cinturino=chiusura_bracciale_cinturino,
                ulteriori_complicazioni=ulteriori_complicazioni,
                foto=foto_filename,
            )

            # Salvare nel database
            db.session.add(nuovo_orologio)
            db.session.commit()
            print("Orologio aggiunto correttamente al database!")
            
            return redirect(url_for('insert'))

        # Ottenere tutti gli orologi dal database
        orologi = Orologio.query.all()
        return render_template('insert.html', orologi=orologi)

    # Route per visualizzare la pagina #vista
    @app.route('/vista')
    def vista():
        orologi = Orologio.query.all()
        return render_template('vista.html', orologi=orologi)
    
    @app.route('/filtro')
    def filtro():
        columns = [column.name for column in Orologio.__table__.columns]
        return render_template('filtro.html', columns=columns)

    @app.route('/get_column_values', methods=['POST'])
    def get_column_values():
        data = request.json
        column_name = data.get('column')
        filters = data.get('filters', [])

        # Controlla se la colonna è valida
        if column_name not in [column.name for column in Orologio.__table__.columns]:
            return jsonify({'error': 'Colonna non valida'}), 400

        try:
            # Crea una query iniziale
            query = db.session.query(Orologio)

            # Applica i filtri attivi
            for f in filters:
                col = f.get('column')
                val = f.get('value')
                if col and val and col in [column.name for column in Orologio.__table__.columns]:
                    query = query.filter(getattr(Orologio, col) == val)

            # Ottieni i valori unici della colonna selezionata
            values = query.with_entities(getattr(Orologio, column_name)).distinct().all()
            values = [value[0] for value in values if value[0] is not None]
            return jsonify(values)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            return jsonify({'error': 'Errore durante il recupero dei dati'}), 500


    @app.route('/filter', methods=['POST'])
    def filter():
        data = request.get_json()  # Usa request.get_json() per recuperare i dati JSON
        filters = data.get('filters', [])

        try:
            # Crea una query iniziale
            query = db.session.query(Orologio)

            # Applica i filtri
            for f in filters:
                column_name = f.get('column')
                value = f.get('value')
                if column_name and value and column_name in [col.name for col in Orologio.__table__.columns]:
                    query = query.filter(getattr(Orologio, column_name) == value)

            # Esegui la query
            results = query.all()

            # Serializza i risultati in formato JSON
            data = [
                {col.name: getattr(row, col.name) for col in Orologio.__table__.columns}
                for row in results
            ]
            return jsonify(data)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            return jsonify({'error': 'Errore durante il recupero dei dati'}), 500
        

    @app.route('/details/<int:nr_sacchetto>', methods=['GET'])
    def get_details(nr_sacchetto):
        # Query per selezionare il record che corrisponde al nr_sacchetto
        orologio = Orologio.query.filter_by(nr_sacchetto=nr_sacchetto).first()

        # Se il record non viene trovato, restituiamo un messaggio di errore
        if not orologio:
            return f"<h1>Nessun record trovato per nr_sacchetto: {nr_sacchetto}</h1>", 404

        # Converte l'oggetto orologio in un dizionario per passarlo al template
        result_dict = {col.name: getattr(orologio, col.name) for col in Orologio.__table__.columns}

        # Passa il dizionario dei dettagli al template HTML
        return render_template('details.html', nr_sacchetto=nr_sacchetto, details=result_dict)