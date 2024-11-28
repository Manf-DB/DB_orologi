@echo off
echo ==============================================
echo Configurazione dell'ambiente per il progetto
echo ==============================================

:: Verifica se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo Errore: Python non è installato. Installa Python e riprova.
    exit /b 1
)

:: Creazione di un ambiente virtuale
echo Creazione dell'ambiente virtuale "venv"...
python -m venv venv

:: Attivazione dell'ambiente virtuale
echo Attivazione dell'ambiente virtuale...
call venv\Scripts\activate

:: Aggiornamento di pip
echo Aggiornamento di pip...
python -m pip install --upgrade pip

:: Installazione delle dipendenze
if exist requirements.txt (
    echo Installazione delle dipendenze dal file requirements.txt...
    pip install -r requirements.txt
) else (
    echo Il file requirements.txt non è stato trovato. Installazione manuale delle dipendenze principali...
    pip install Flask Flask-SQLAlchemy Flask-CORS Werkzeug
)

:: Conferma del completamento
echo Tutto è pronto! Per attivare l'ambiente virtuale in futuro, esegui:
echo    call venv\Scripts\activate
echo ==============================================
pause
