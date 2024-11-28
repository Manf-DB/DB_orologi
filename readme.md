1. aprire cmd
2. andare alla cartella dove si è scaricato il repository con il comando cd <percorso>
3. eseguire comando "setup_env.bat". Installerà un ambiente virtuale all'interno del quale
   saranno installate tutte le dipendenze;
4. controllare:
   i.  avvenuta creazione della cartella <venv>
   ii. che in cmd, dopo completato l'installazione e premuto un tasto per continuare appaia
       (venv) prima del percorso
5. ATTENZIONE: ad ogni successivo avvio devi riattivare l'ambiente virtuale con il comando
   "call venv\Scripts\activate"
6. lanciare run.py da cmd con il comando "python run.py"
4. attendere l'uscita della scritta <DEBUGGER PIN .....>
5. aprire il browser alla pagina http://127.0.0.1:5000/
6. oppure pagina http://127.0.0.1:5000/vista
7. oppure pagine http://127.0.0.1:5000/insert
8. oppure pagina http://127.0.0.1:5000/filtro