# Gestione Ordini Acqua Minerale

Gestione Ordini Acqua Minerale è un'applicazione Python per la gestione degli ordini e dei vettori per il trasporto di acqua minerale in Italia. Questa applicazione consente di inserire, modificare, eliminare e monitorare gli ordini, tutto attraverso un'interfaccia grafica semplice e intuitiva.

## Funzionalità

- **Inserimento e Modifica Ordini**: Permette di inserire e modificare i dettagli degli ordini, inclusi vettore, destinazione e numero d'ordine.
- **Visualizzazione del Calendario**: Mostra gli ordini per data in un calendario integrato.
- **Gestione degli Stati degli Ordini**: Cambia lo stato degli ordini (es. "In ritardo" o "Arrivato") con un semplice clic destro.
- **Salvataggio e Caricamento Automatico**: Gli ordini vengono salvati automaticamente in un file CSV per essere caricati all'avvio successivo.
- **Verifica degli Aggiornamenti**: Controlla automaticamente se è disponibile una nuova versione del software.
- **Interfaccia Intuitiva**: Interfaccia grafica user-friendly realizzata con Tkinter.

## Installazione

1. **Clona la Repository**:
    ```bash
    git clone https://github.com/tuoutente/gestione-ordini-acqua-minerale.git
    cd gestione-ordini-acqua-minerale
    ```

2. **Installa le Dipendenze**:
    Assicurati di avere Python 3.7+ installato. Poi installa le dipendenze necessarie:
    ```bash
    pip install -r requirements.txt
    ```

3. **Esegui l'Applicazione**:
    ```bash
    python vector.py
    ```

## Utilizzo

1. **Inserimento Ordini**: Inserisci i dettagli del vettore, la destinazione, il numero d'ordine e la data di inserimento. Premi "Salva Ordine" per aggiungere l'ordine.
2. **Modifica/Eliminazione Ordini**: Clicca su un ordine esistente e scegli "Modifica" o "Elimina" per gestire l'ordine.
3. **Monitoraggio dello Stato**: Clicca con il tasto destro su un ordine per cambiarne lo stato in "In ritardo" o "Arrivato".
4. **Verifica degli Aggiornamenti**: All'avvio, l'applicazione controllerà se è disponibile una nuova versione e ti avviserà se è necessario aggiornare.

## Aggiornamenti

L'applicazione controlla automaticamente se sono disponibili nuovi aggiornamenti ogni volta che viene avviata. Se è disponibile una nuova versione, ti verrà chiesto di aggiornare.

## Licenza

Questo progetto è rilasciato sotto la licenza GNU General Public License v3.0. È richiesto che l'attribuzione all'autore originale, Riccardi Gaetano, sia mantenuta in tutte le versioni distribuite del software.

Per maggiori dettagli, consulta il file LICENSE.

## Contribuire

Contributi, segnalazioni di bug e richieste di funzionalità sono i benvenuti! Sentiti libero di aprire un [issue](https://github.com/tuoutente/gestione-ordini-acqua-minerale/issues) o di inviare una pull request.

## Contatti

**Autore:** Riccardi Gaetano  
**Email:** info@riccardigaetano.it
