import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
import tkinter.filedialog as filedialog


def save_output():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("File di testo", "*.txt")])    
    with open(filepath, "w") as f:
        f.write(result_label.cget("text"))

def create_study_plan():
    try:
        study_hours = float(study_hours_entry.get())
        num_pages = num_pages_entry.get()
        
        if study_hours > 24:
            raise ValueError("Il limite massimo di studio giornaliero è 24 ore.")
        
        if not num_pages.isdigit():
            raise ValueError("Il valore inserito per il numero di pagine deve essere numerico")
        total_pages = int(num_pages)

        subject = subject_entry.get()

        complexity = complexity_var.get().capitalize()

        exam_date = exam_date_entry.get()

        # Calcola il numero di giorni disponibili per lo studio
        
        today = datetime.now()
        exam_date_obj = datetime.strptime(exam_date, '%d/%m/%Y')
        days_available = (exam_date_obj - today).days
        if days_available < 1:
            raise ValueError("Data esame non valida.")

        # Calcola il piano di studio personalizzato
        
        plan = generate_study_plan(study_hours, total_pages, subject, complexity, exam_date, days_available)
        if 'pages_per_hour' not in plan:
            raise ValueError("Piano di studio non valido")
        pages_per_hour = plan['pages_per_hour']
        
        study_hours_per_day = plan['total_hours'] / days_available

        result_label.config(text=f"Devi studiare {total_pages} pagine di {subject} in {study_hours} ore al giorno per arrivare preparato all'esame del {exam_date}.")
        result_label.config(text=result_label.cget("text") + f"\n\nPiano di studio personalizzato:\n- Ore totali di studio necessarie: {plan['total_hours']:.2f}\n- Data di fine studio: {plan['end_date']}\n- Pagine da studiare ogni giorno: {plan['pages_per_day']:.2f}\n- Ore di studio necessarie al giorno: {study_hours_per_day:.2f}\n- Numero di pagine che puoi studiare in un'ora: {pages_per_hour:.2f}")

        # Cancella eventuali messaggi di errore precedenti
        
        error_label.config(text="")

    except ValueError as e:
        
        # Visualizza il messaggio di errore
        error_label.config(text=str(e))

        # Crea un label widget per visualizzare il messaggio di errore
        error_label.pack()

def create_study_plan_wrapper(complexity):
    create_study_plan()

def generate_study_plan(study_hours, total_pages, subject, complexity, exam_date, days_available):

    # Calcola il numero di pagine per ora in base alla complessità della materia
    
    if complexity == "Facile":
        pages_per_hour = 2.5
    elif complexity == "Intermedio":
        pages_per_hour = 2.0
    else:
        pages_per_hour = 1.5

    pages_per_day = total_pages / days_available

    total_hours = total_pages / pages_per_hour
    
    end_date = datetime.now() + timedelta(days=days_available)

    # Restituisci il piano di studio
    
    return {
        "total_hours": total_hours,
        "end_date": end_date.strftime("%d/%m/%Y"),
        "pages_per_day": pages_per_day,
        "pages_per_hour": pages_per_hour,
    }


# Crea una GUI

window = tk.Tk()
window.title("Crea il tuo piano di studio")

# Crea etichette e campi di inserimento

study_hours_label = tk.Label(window, text="Quante ore studi al giorno?")
study_hours_label.pack()
study_hours_entry = tk.Entry(window)
study_hours_entry.pack()

num_pages_label = tk.Label(window, text="Quante pagine devi studiare?")
num_pages_label.pack()
num_pages_entry = tk.Entry(window)
num_pages_entry.pack()

subject_label = tk.Label(window, text="Di quale materia?")
subject_label.pack()
subject_entry = tk.Entry(window)
subject_entry.pack()

complexity_label = tk.Label(window, text="Quanto è complessa la materia?")
complexity_label.pack()

complexity_var = tk.StringVar(value="facile")
complexity_menu = tk.OptionMenu(window, complexity_var, "facile", "intermedio", "difficile", command=create_study_plan_wrapper)
complexity_menu.pack()

exam_date_label = tk.Label(window, text="Entro quale data hai l'esame? (gg/mm/aaaa)")
exam_date_label.pack()
exam_date_entry = tk.Entry(window)
exam_date_entry.pack()

# Aggiungi un controllo sulle stringhe di input alle domande "Quante ore studi al giorno?" e "Quante pagine devi studiare?"

def check_numeric_input(input):
    if not input.isnumeric():
        messagebox.showerror("Errore", "Inserisci solo numeri.")
        return False
    return True

def check_study_hours_input():
    if not check_numeric_input(study_hours_entry.get()):
        if study_hours_entry.get() == "":
            return
        study_hours_entry.delete(0, tk.END)

def check_num_pages_input():
    if not check_numeric_input(num_pages_entry.get()):
        if num_pages_entry.get() == "":
            return
        num_pages_entry.delete(0, tk.END)

study_hours_entry.bind("<FocusOut>", lambda event: check_study_hours_input())
num_pages_entry.bind("<FocusOut>", lambda event: check_num_pages_input())

# Aggiungi un controllo sulle stringhe di input alla domanda "Di quale materia?"

def check_subject_input():
    if not subject_entry.get().isalpha():
        messagebox.showerror("Errore", "Inserisci solo caratteri alfabetici.")
        subject_entry.delete(0, tk.END)

subject_entry.bind("<FocusOut>", lambda event: check_subject_input())

create_plan_button = tk.Button(window, text="Genera piano di studio",
command=create_study_plan)
create_plan_button.pack()

create_plan_button.pack()
create_plan_button.config(command=create_study_plan)

# Crea una label per visualizzare il risultato

result_label = tk.Label(window, text="")
result_label.pack()

# Etichetta per visualizzare eventuali messaggi di errore

error_label = tk.Label(text="", fg="red")
error_label.pack()

save_button = tk.Button(window, text="Salva output", command=save_output)
save_button.pack()

exit_button = tk.Button(window, text="Esci", command=window.quit)
exit_button.pack()

window.mainloop()
# Coded by Gianmarco Benedetti with ❤️
