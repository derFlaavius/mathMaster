from tkinter import messagebox


def check(ergebnis, operatorwert, zahlen):
    if ergebnis == "":
        messagebox.showerror("Fehlende Eingabe", "Bitte gib etwas ein!")
        return False, False
    for c in ergebnis:
        if c.isdigit() == False:
            messagebox.showerror("Falsche Eingabe", "Bitte gib nur Zahlen ein!")
            return False, False
    ergebnis = int(ergebnis)
    if operatorwert == 1:
        if ergebnis == zahlen.ergebnis_plus:
            return True, True
        else:
            return True, False # 1.True = Aufgabe wurde bearbeitet, 2.False = Aufgabe nicht richtig beantwortet
    elif operatorwert == 2: # Minus
        if ergebnis == zahlen.ergebnis_minus:
            return True, True
        else:
            return True, False
    else:
        print("Fataler Fehler: check")
        return False, False
    
def farben(farbe):
    if farbe == "green":
        return "#3CFF00"
    elif farbe == "red":
        return "#FF0000"
    elif farbe == "yellow":
        return "#EEFF00"
    else:
        return "#FFFFFF"