# from dbm import whichdb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import mth
import klassen


def clearwdw():
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.place_forget()

def lastscreen():
    clearwdw()
    lb_1 = tk.Label(root, text="Ende!")
    lb_2 = tk.Label(root, text=f"Richtig: {nutzer.punkte}", fg=mth.farben("green"))
    lb_3 = tk.Label(root, text=f"Falsch: {nutzer.fehler}", fg=mth.farben("red"))
    bn_bst = ttk.Button(root, text="Bestätigen", command=mainscreen)

    pic_logo.pack()
    tk.Label(root, text="")
    lb_1.pack()
    lb_2.pack()
    lb_3.pack()
    tk.Label(root, text="")
    bn_bst.pack()


def aufgabe(wert, sg):
    print(sg)
    def bestaetigen(tf_ergebnis):
        ergebnis = tf_ergebnis.get()
        r1, r2 = mth.check(ergebnis, wert, zahlen)
        if r1 == True and r2 == True:
            flag = 1
            nutzer.punkte += 1
            lb_msg = tk.Label(root, text="Richtig!", fg=mth.farben("green"))
            lb_msg.pack()
            root.after(2000, lambda:aufgabe(wert, sg))
            return
        elif r1 == True and r2 == False:
            flag = 1
            nutzer.fehler += 1
            if operator == "+":
                lb_msg = tk.Label(root, text=f"Falsch! {zahlen.ergebnis_plus} wäre richtig.", fg=mth.farben("red"))
            elif operator == "-":
                lb_msg = tk.Label(root, text=f"Falsch! {zahlen.ergebnis_minus} wäre richtig.", fg=mth.farben("red"))
            lb_msg.pack()
            root.after(2000, lambda:aufgabe(wert, sg))
            return
        elif r1 == False:
            return
        else:
            print("Fehler")

    def generieren():
        clearwdw()
        zahlen.generieren(sg)
        zahlen.result()

        # Elemente
        lb_text = tk.Label(root, text=f"Runde {nutzer.runden}")
        lb_aufgabe = tk.Label(root, text=f"{zahlen.zahl1} {operator} {zahlen.zahl2} =")
        tf_ergebnis = ttk.Entry(root)
        bn_bestaetigen = ttk.Button(root, text="Bestätigen", command=lambda:bestaetigen(tf_ergebnis))
        bn_abbruch = ttk.Button(root, text="Abbrechen", command=lastscreen)

        tf_ergebnis.bind('<Return>', lambda event: bestaetigen(tf_ergebnis))
        tf_ergebnis.focus_set()  

        pic_logo.pack()
        tk.Label(root, text="").pack()
        lb_text.pack()
        lb_aufgabe.pack()
        tf_ergebnis.pack()
        tk.Label(root, text="").pack()
        bn_bestaetigen.pack()
        tk.Label(root, text="").pack()
        bn_abbruch.pack()

    if wert == 1: # Plus
        operator = "+"
    elif wert == 2: # Minus
        operator = "-"
    else:
        print("Fataler Fehler: aufgabe/wert")

    if nutzer.runden < 10:
        nutzer.runden += 1
        print(nutzer.runden)
        generieren()
    else:
        print("ende")
        lastscreen()


def mainscreen():
    global nutzer, zahlen
    nutzer = klassen.Nutzer()
    zahlen = klassen.Zahlen()
    clearwdw()
    # Deklaration
    # Buttons
    bn_plus = ttk.Button(root, text="+", command=lambda:aufgabe(1, cb_schwgr.get()))
    bn_minus = ttk.Button(root, text="-", command=lambda:aufgabe(2, cb_schwgr.get()))

    # Label
    lb_gruss = tk.Label(root, text="Herzlich Willkommen")
    lb_info = tk.Label(root, text="Bitte wähle aus, was du machen möchtest:")

    # Combobox
    schwgr = ["Leicht", "Mittel", "Schwer"]
    cb_schwgr = ttk.Combobox(root, values=schwgr, state="readonly")
    cb_schwgr.current(0)

    # Platzierung
    pic_logo.pack()
    tk.Label(root, text="").pack()
    lb_gruss.pack()
    lb_info.pack()
    tk.Label(root, text="").pack()
    cb_schwgr.pack()
    tk.Label(root, text="").pack()
    bn_plus.pack()
    tk.Label(root, text="").pack()
    bn_minus.pack()


# Deklaration Pfade
lnk_azure = os.path.join(os.path.dirname(__file__), "themes", "azure", "azure.tcl")
lnk_logo = os.path.join(os.path.dirname(__file__), "images", "logo2.png")


# Erzeugung des Fensters
root = tk.Tk()
root.geometry("500x500")
root.title("mathMaster v1.0.0 - Du schaffst das!")

# Einstellung GUI
root.tk.call("source", lnk_azure)
root.tk.call("set_theme", "dark")

# Implementierung der Grafiken
logo = Image.open(lnk_logo)
logo = logo.resize((180, 140))
logo = ImageTk.PhotoImage(logo)
pic_logo = tk.Label(root, image=logo)

mainscreen()
root.mainloop()