import os
import sys
sys.path.append(r'C:\Users\Djgoe\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')
import babel.numbers
import csv
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from urllib.request import urlretrieve

# URL del file di versione sul server
VERSION_URL = "https://raw.githubusercontent.com/HorsemanDj/version/main/vctversion.txt"
DOWNLOAD_URL = "http://tuosito.com/nuovo_eseguibile.exe"
CURRENT_VERSION = "1.3.1"

def controlla_aggiornamenti():
    try:
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()
        if latest_version > CURRENT_VERSION:
            mostra_notifica_aggiornamento(latest_version)
    except Exception as e:
        print(f"Errore durante il controllo degli aggiornamenti: {e}")

def mostra_notifica_aggiornamento(versione):
    if messagebox.askyesno("Aggiornamento disponibile", f"È disponibile la versione {versione}. Vuoi aggiornare ora?"):
        aggiorna_programma()

def aggiorna_programma():
    try:
        # Scarica il nuovo eseguibile
        local_filename, headers = urlretrieve(DOWNLOAD_URL, "nuovo_eseguibile.exe")
        # Sostituisci l'eseguibile corrente
        os.replace(local_filename, sys.argv[0])
        messagebox.showinfo("Aggiornamento completato", "Il programma è stato aggiornato alla nuova versione.")
        # Riavvia l'applicazione aggiornata
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        messagebox.showerror("Errore durante l'aggiornamento", f"Si è verificato un errore durante l'aggiornamento: {e}")

# Funzione per leggere gli ordini da un file CSV
def leggi_ordini(file_csv):
    ordini = []
    try:
        with open(file_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Data' in row and 'Vettore' in row and 'Destinazione' in row and 'NumeroOrdine' in row and 'Stato' in row:
                    ordini.append(row)
                else:
                    print(f"Errore: la riga {row} non contiene tutte le chiavi necessarie.")
    except FileNotFoundError:
        pass
    return ordini

# Funzione per validare le date
def valida_data(data_str):
    try:
        return datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# Funzione per mostrare gli ordini di un giorno selezionato
def mostra_ordini(event=None):
    selected_date = cal.selection_get()
    selected_orders = [ordine for ordine in ordini if 'Data' in ordine and ordine['Data'] == selected_date.strftime('%Y-%m-%d')]
    ordine_list.delete(*ordine_list.get_children())  # Pulire la lista prima di aggiornare
    for ordine in selected_orders:
        tag = ordine.get('Stato', 'normal')
        ordine_list.insert("", "end", values=(ordine["Vettore"], ordine["Destinazione"], ordine["NumeroOrdine"], 'Modifica / Elimina'), tags=(tag,))
        ordine_list.insert("", "end", values=("─" * 200, "", "", ""), tags=('separator',))

# Funzione per aggiungere o modificare un ordine
def aggiungi_ordine(event=None):
    nuova_data = entry_data_inserimento.get()
    vettore = entry_vettore.get()
    destinazione = entry_destinazione.get()
    numero_ordine = entry_numero_ordine.get()
    
    if vettore or destinazione or numero_ordine:  # Permetti di salvare se almeno uno dei campi è riempito
        ordini.append({'Data': nuova_data, 'Vettore': vettore, 'Destinazione': destinazione, 'NumeroOrdine': numero_ordine, 'Stato': 'normal'})
        
        salva_ordini()
        messagebox.showinfo("Successo", "Ordine salvato con successo!")
        
        entry_vettore.delete(0, tk.END)
        entry_destinazione.delete(0, tk.END)
        entry_numero_ordine.delete(0, tk.END)
        
        aggiorna_calendario()
        mostra_ordini()
    else:
        messagebox.showwarning("Attenzione", "Inserisci almeno un campo (vettore, destinazione o numero d'ordine) prima di salvare!")

# Funzione per cancellare un ordine
def cancella_ordine(selected_item):
    values = ordine_list.item(selected_item, 'values')
    for ordine in ordini:
        if ordine['NumeroOrdine'] == values[2] and ordine['Vettore'] == values[0] and ordine['Destinazione'] == values[1]:
            ordini.remove(ordine)
            break
    
    salva_ordini()
    mostra_ordini()
    aggiorna_calendario()
    messagebox.showinfo("Successo", "Ordine cancellato con successo!")

# Funzione per aggiornare il calendario con i segni dei vettori
def aggiorna_calendario():
    cal.calevent_remove('all')
    date_con_ordini = {ordine['Data'] for ordine in ordini if 'Data' in ordine}
    for data_str in date_con_ordini:
        data_obj = valida_data(data_str)
        if data_obj:
            cal.calevent_create(data_obj, '✓', 'vettore')

# Funzione per cambiare lo stato di un ordine
def cambia_stato_ordine(nuovo_stato):
    selected_item = ordine_list.selection()
    if selected_item:
        values = ordine_list.item(selected_item, 'values')
        for ordine in ordini:
            if ordine['NumeroOrdine'] == values[2] and ordine['Vettore'] == values[0] and ordine['Destinazione'] == values[1]:
                ordine['Stato'] = nuovo_stato
                break
        salva_ordini()
        mostra_ordini()

# Funzione per mostrare la licenza
def mostra_licenza():
    licenza = (
        "Licenza Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)\n"
        "------------------------------------------------------------------------------------\n"
        "Questo software è distribuito con una licenza Creative Commons Attribution-NoDerivatives 4.0 International.\n"
        "È permesso condividere, copiare, distribuire, eseguire e mostrare questo software, a condizione che \n"
        "venga data attribuzione completa all'autore originale.\n"
        "\n"
        "Tuttavia, non è permesso alterare, trasformare o creare nuove opere basate su questo software senza il \n"
        "consenso scritto dell'autore.\n"
        "\n"
        "Autore:\n"
        "Riccardi Gaetano\n"
        "Email: info@riccardigaetano.it\n"
        "\n"
        "Per maggiori informazioni sulla licenza, visita:\n"
        "https://creativecommons.org/licenses/by-nd/4.0/"
    )
    messagebox.showinfo("Info e Licenza", licenza)

# Funzione per mostrare il changelog
def mostra_changelog():
    changelog = (
        "Versione 1.3.1\n"
        "- Risolto un bug che impediva la corretta visualizzazione degli ordini nel calendario.\n\n"
        "Versione 1.3.0\n"
        "- Aggiunta la possibilità di colorare gli ordini in base allo stato (ritardo/arrivato).\n\n"
        "Versione 1.2.0\n"
        "- Implementata una scrollbar per visualizzare tutti gli ordini quando sono troppi per la finestra.\n\n"
        "Versione 1.1.0\n"
        "- Aggiunta la colonna per il numero dell'ordine nella visualizzazione degli ordini."
    )
    messagebox.showinfo("Changelog", changelog)

# Funzione per salvare gli ordini nel file CSV
def salva_ordini():
    with open('ordini.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Data', 'Vettore', 'Destinazione', 'NumeroOrdine', 'Stato']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ordine in ordini:
            writer.writerow(ordine)

# Funzione per gestire il click su un ordine per selezionarlo
def on_select(event):
    selected_item = ordine_list.selection()
    if selected_item:
        # Rimuove il tag 'selected' da tutti gli altri elementi
        for item in ordine_list.get_children():
            ordine_list.item(item, tags=ordine_list.item(item, 'tags')[0])
        # Aggiunge il tag 'selected' all'elemento corrente
        ordine_list.item(selected_item, tags=('selected', ordine_list.item(selected_item, 'tags')[0]))

# Funzione per rimuovere la selezione
def rimuovi_selezione(event=None):
    for item in ordine_list.get_children():
        ordine_list.item(item, tags=ordine_list.item(item, 'tags')[0])

# Funzione per modificare un ordine
def modifica_ordine(selected_item):
    values = ordine_list.item(selected_item, 'values')
    for ordine in ordini:
        if ordine['NumeroOrdine'] == values[2] and ordine['Vettore'] == values[0] and ordine['Destinazione'] == values[1]:
            # Apre una finestra per modificare i dettagli
            mod_window = tk.Toplevel(root)
            mod_window.title("Modifica Ordine")
            
            # Creare e configurare campi di input per la modifica
            ttk.Label(mod_window, text="N° Ordine:").grid(row=0, column=0, padx=20, pady=5, sticky='e')
            mod_numero_ordine = ttk.Entry(mod_window)
            mod_numero_ordine.grid(row=0, column=1, padx=20, pady=5)
            mod_numero_ordine.insert(0, ordine['NumeroOrdine'])

            ttk.Label(mod_window, text="Vettore:").grid(row=1, column=0, padx=20, pady=5, sticky='e')
            mod_vettore = ttk.Entry(mod_window)
            mod_vettore.grid(row=1, column=1, padx=20, pady=5)
            mod_vettore.insert(0, ordine['Vettore'])

            ttk.Label(mod_window, text="Destinazione:").grid(row=2, column=0, padx=20, pady=5, sticky='e')
            mod_destinazione = ttk.Entry(mod_window)
            mod_destinazione.grid(row=2, column=1, padx=20, pady=5)
            mod_destinazione.insert(0, ordine['Destinazione'])

            ttk.Label(mod_window, text="Data Inserimento:").grid(row=3, column=0, padx=20, pady=5, sticky='e')
            mod_data_inserimento = DateEntry(mod_window, date_pattern='yyyy-mm-dd', locale='it_IT')
            mod_data_inserimento.grid(row=3, column=1, padx=20, pady=5)
            mod_data_inserimento.set_date(ordine['Data'])

            def salva_modifiche():
                ordine['NumeroOrdine'] = mod_numero_ordine.get()
                ordine['Vettore'] = mod_vettore.get()
                ordine['Destinazione'] = mod_destinazione.get()
                ordine['Data'] = mod_data_inserimento.get()
                
                salva_ordini()
                aggiorna_calendario()
                mostra_ordini()
                mod_window.destroy()
                messagebox.showinfo("Successo", "Ordine modificato con successo!")

            ttk.Button(mod_window, text="Salva", command=salva_modifiche).grid(row=4, column=0, columnspan=2, pady=10)

# Gestione delle azioni nella colonna "Azione"
def gestisci_azione(event):
    selected_item = ordine_list.identify_row(event.y)
    if selected_item:
        column = ordine_list.identify_column(event.x)
        if column == '#4':  # La colonna "Azione" è la quarta
            action = ordine_list.item(selected_item, 'values')[3]
            if 'Modifica' in action:
                risposta = messagebox.askyesno("Conferma Modifica", "Sei sicuro di voler modificare questo ordine?")
                if risposta:
                    modifica_ordine(selected_item)
            elif 'Elimina' in action:
                risposta = messagebox.askyesno("Conferma Eliminazione", "Sei sicuro di voler eliminare questo ordine?")
                if risposta:
                    cancella_ordine(selected_item)

# Lettura degli ordini dal file CSV
ordini = leggi_ordini('ordini.csv')

# Configurazione dell'interfaccia grafica principale
root = tk.Tk()
root.title("Gestione Ordini Acqua Minerale")
root.configure(bg="white")  # Imposta lo sfondo della finestra principale a bianco

# Aggiungi un'icona personalizzata
root.iconbitmap(r'C:\Users\Djgoe\Documents\Software\Vettori\icona.ico')

# Set the theme
style = ttk.Style()
style.theme_use('clam')

# Configura colori e font personalizzati
style.configure('TLabel', font=('Helvetica', 12), background="white")
style.configure('TButton', font=('Helvetica', 12), padding=6)
style.configure('TEntry', padding=6)
style.configure('TFrame', background="white")  # Imposta lo sfondo dei frame a bianco

# Creazione del menu
menubar = tk.Menu(root)
root.config(menu=menubar)

# Creazione del menu "File"
file_menu = tk.Menu(menubar, tearoff=0, bg="white", activebackground="lightgray")
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Chiudi", command=root.quit)

def report_bug():
    # Creazione della finestra di segnalazione bug
    bug_window = tk.Toplevel(root)
    bug_window.title("Report Bug")
    bug_window.geometry("400x300")
    bug_window.configure(bg="white")
    
    ttk.Label(bug_window, text="Se hai trovato dei bug o hai dei suggerimenti, scrivimi:", background="white").pack(pady=10)
    
    ttk.Label(bug_window, text="Il tuo messaggio:", background="white").pack(anchor="w", padx=20, pady=5)
    bug_text = tk.Text(bug_window, height=8, wrap="word")
    bug_text.pack(padx=20, pady=5, fill="x")
    
    def invia_email():
        subject = "Segnalazione Bug/Suggerimento"
        body = bug_text.get("1.0", tk.END).strip()
        recipient = "info@riccardigaetano.it"
        if body:
            webbrowser.open(f"mailto:{recipient}?subject={subject}&body={body}")
            messagebox.showinfo("Invio Segnalazione", "La segnalazione verrà inviata utilizzando il tuo client di posta.")
            bug_window.destroy()
        else:
            messagebox.showwarning("Campo vuoto", "Per favore inserisci un messaggio prima di inviare.")

    ttk.Button(bug_window, text="Invia", command=invia_email).pack(pady=10)

# Aggiungi la voce "Report Bug" nel menu "File"
file_menu.add_command(label="Report Bug", command=report_bug)

# Creazione del menu "?"
help_menu = tk.Menu(menubar, tearoff=0, bg="white", activebackground="lightgray")
menubar.add_cascade(label="?", menu=help_menu)
help_menu.add_command(label="Info e Licenza", command=mostra_licenza)
help_menu.add_command(label="Changelog", command=mostra_changelog)

# Configurazione griglia principale
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Frame per contenere il calendario e la lista degli ordini
frame_main = ttk.Frame(root, padding=(20, 10))
frame_main.grid(row=0, column=0, sticky="nsew")
frame_main.grid_columnconfigure(0, weight=1)
frame_main.grid_columnconfigure(1, weight=1)
frame_main.grid_rowconfigure(0, weight=1)

# Creazione del calendario per visualizzare gli ordini
cal = Calendar(frame_main, selectmode='day', year=2024, month=9, day=1, locale='it_IT')
cal.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="nsew")
cal.bind("<<CalendarSelected>>", mostra_ordini)

# Frame per la lista degli ordini con scrollbar
frame_ordini = ttk.Frame(frame_main)
frame_ordini.grid(row=0, column=1, rowspan=6, padx=20, pady=10, sticky="nsew")
frame_ordini.grid_rowconfigure(0, weight=1)
frame_ordini.grid_columnconfigure(0, weight=1)

# Aggiungi una scrollbar alla lista degli ordini
scrollbar = ttk.Scrollbar(frame_ordini, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")

# Lista per mostrare i vettori e le destinazioni
cols = ('Vettore', 'Destinazione', 'NumeroOrdine', 'Azione')
ordine_list = ttk.Treeview(frame_ordini, columns=cols, show='headings', height=8, yscrollcommand=scrollbar.set)
ordine_list.heading('Vettore', text='Vettore')
ordine_list.heading('Destinazione', text='Destinazione')
ordine_list.heading('NumeroOrdine', text='N° Ordine')
ordine_list.heading('Azione', text='Azione')
ordine_list.column('Azione', width=150, anchor='center')
ordine_list.grid(row=0, column=0, sticky="nsew")

scrollbar.config(command=ordine_list.yview)

# Aggiungi tag per i colori e la selezione
ordine_list.tag_configure('normal', background='white')
ordine_list.tag_configure('ritardo', background='red')
ordine_list.tag_configure('arrivato', background='green')
ordine_list.tag_configure('separator', background='white')  # Linea di separazione sottile e trasparente
ordine_list.tag_configure('selected', background='white')  # Cambia solo il bordo della riga selezionata

ordine_list.bind("<<TreeviewSelect>>", on_select)
ordine_list.bind("<Button-1>", gestisci_azione)

# Rimuove la selezione quando si clicca altrove
root.bind("<Button-1>", rimuovi_selezione)

# Aggiunta del menu contestuale (tasto destro)
menu_contestuale = tk.Menu(root, tearoff=0)
menu_contestuale.add_command(label="In ritardo", command=lambda: cambia_stato_ordine('ritardo'))
menu_contestuale.add_command(label="Arrivato", command=lambda: cambia_stato_ordine('arrivato'))

def mostra_menu_contestuale(event):
    # Seleziona l'elemento su cui è stato fatto clic con il tasto destro
    selected_item = ordine_list.identify_row(event.y)
    ordine_list.selection_set(selected_item)
    menu_contestuale.post(event.x_root, event.y_root)

ordine_list.bind("<Button-3>", mostra_menu_contestuale)

# Sezione per inserire i dettagli del nuovo ordine, centrata
frame_input = ttk.Frame(root, padding=(20, 10))
frame_input.grid(row=1, column=0, sticky="nsew")

frame_input_inner = ttk.Frame(frame_input, padding=(20, 10))
frame_input_inner.grid(row=0, column=0, sticky="")
frame_input.grid_columnconfigure(0, weight=1)
frame_input.grid_rowconfigure(0, weight=1)

frame_input_inner.grid_columnconfigure(0, weight=1)
frame_input_inner.grid_columnconfigure(1, weight=1)

ttk.Label(frame_input_inner, text="Inserisci o Modifica il Vettore").grid(row=0, column=0, columnspan=2, pady=(10, 10))

ttk.Label(frame_input_inner, text="Vettore:").grid(row=1, column=0, padx=20, pady=5, sticky='e')
entry_vettore = ttk.Entry(frame_input_inner)
entry_vettore.grid(row=1, column=1, padx=20, pady=5)

ttk.Label(frame_input_inner, text="Destinazione:").grid(row=2, column=0, padx=20, pady=5, sticky='e')
entry_destinazione = ttk.Entry(frame_input_inner)
entry_destinazione.grid(row=2, column=1, padx=20, pady=5)

ttk.Label(frame_input_inner, text="N° Ordine:").grid(row=3, column=0, padx=20, pady=5, sticky='e')
entry_numero_ordine = ttk.Entry(frame_input_inner)
entry_numero_ordine.grid(row=3, column=1, padx=20, pady=5)

# Sezione per selezionare la data di inserimento ordine
ttk.Label(frame_input_inner, text="Data Inserimento:").grid(row=4, column=0, padx=20, pady=5, sticky='e')
entry_data_inserimento = DateEntry(frame_input_inner, date_pattern='yyyy-mm-dd', locale='it_IT')
entry_data_inserimento.grid(row=4, column=1, padx=20, pady=5)

btn_add = ttk.Button(frame_input_inner, text="Salva Ordine", command=aggiungi_ordine)
btn_add.grid(row=5, column=0, columnspan=2, pady=20)

# Associa il tasto Invio al salvataggio dell'ordine
root.bind('<Return>', aggiungi_ordine)

# Variabile per tracciare l'ordine selezionato per la modifica
ordine_selezionato = {}

# Aggiorna il calendario con gli ordini caricati dal CSV
aggiorna_calendario()

# Controllo aggiornamenti all'avvio
controlla_aggiornamenti()

# Avvio dell'interfaccia grafica
root.mainloop()
