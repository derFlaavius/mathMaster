# from dbm import whichdb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import klassen
import sql_befehle
import check
import key


def clearwdw():
    for widget in root.winfo_children():
        widget.place_forget()

def startprogramm(keystr):
    result = key.check(keystr)
    if result:
        mainscreen()
    else:
        messagebox.showinfo("Ungültig", "Key ist ungültig!")
        sys.exit()

def verlauf(person):
    def zurueck(tabelle):
        tabelle.destroy()
        bn_zurueck.destroy()
        mainscreen()
    
    def tabelle_erzeugen(daten):
        spalten = ("Datum", "Aura", "Grund")
        tabelle = ttk.Treeview(columns=spalten, show="headings")
        for spalte in spalten:
            tabelle.heading(spalte, text=spalte)
            tabelle.column(spalte, anchor="center", width=50)
        # Daten einfügen
        for eintrag in daten:
            tabelle.insert("", tk.END, values=eintrag)

        tabelle.pack(expand=False, fill="both")
        return tabelle

    if person.name == None:
        messagebox.showwarning("Fehlende Eingabe", "Bitte wähle einen Namen aus und bestätige mit (Auswählen)")
        return
    clearwdw()
    # Tabelle
    tk.Label(root, text=" ").pack()
    tabelle = tabelle_erzeugen(person.ereignisse)   

    # Button
    bn_zurueck = ttk.Button(root, text="Zurück", width=gui_werte.abst_buty, command=lambda:zurueck(tabelle))
    tk.Label(root, text=" ").pack()
    bn_zurueck.pack()


def person_hinzufg():
    def check_eingabe():
        eingabe = tf_name.get()
        rm = check.space(eingabe, "Name")
        if rm == False:
            return
        if eingabe == "":
            messagebox.showwarning("Fehlende Eingabe", "Bitte gib einen Namen ein.")
            return
        rm = sql_befehle.person_anlegen(eingabe)
        if rm == 1:
            messagebox.showerror("Fehler", "Dieser Name existiert bereits.")
            return
        elif rm == 2:
            messagebox.showerror("DB Fehler", "Es gab ein Problem mit der Datenbank")
            return
        messagebox.showinfo("Speicherung erfolgreich", "Der Name wurde erfolgreich gespeichert.")
        pliste, rm_pliste = sql_befehle.personen_laden() # Personen neu laden
        if rm_pliste == 1:
            messagebox.showerror("Fatal Error", "Fataler Fehler")
        mainscreen()
        
    clearwdw()
    pic_logo4.pack()

    # Label
    lb_info = tk.Label(root, text="Bitte gebe erst einen neuen Namen ein, wenn du dir\nabsolut sicher bist, dass dieser nicht existiert!\n\nEine Namensänderung erfolgt ausschließlich administrativ!", fg="yellow")
    lb_eingabe = tk.Label(root, text="Wie lautet der Name?")

    # Button
    bn_bestaetigen = ttk.Button(root, text="Bestätigen", command=check_eingabe, width=gui_werte.bnwidth)
    bn_abbrechen = ttk.Button(root, text="Abbrechen", width=gui_werte.bnwidth, command=lambda:mainscreen())

    # Entry
    tf_name = ttk.Entry(root, width=gui_werte.bnwidth + 1)

    # Platzierung
    xwert = 40
    ywert = 170

    lb_info.place(x=xwert, y=ywert)
    ywert += (gui_werte.abst_lby * 4)
    lb_eingabe.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby
    tf_name.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_bestaetigen.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_abbrechen.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty

def auswaehlen(lib_personen):
    def speichern():
        eintrag = klassen.Eintrag()
        cases1 = cases.get()
        if cases1 == 1: # Keine Auswahl
            pkt = tf_punkte.get()
            komm = tf_kommentar.get()
            if pkt != 0 and pkt != "" and komm != "":
                if check.digit(pkt, "Aura") == True and check.char50(komm, "Kommentar") == True:
                    if int(pkt) <= 5000 and int(pkt) >= -5000:
                        eintrag.pkt = pkt
                        eintrag.kommentar = komm
                    else:
                        messagebox.showwarning("Fehler Eingabe", "Eingabewert > 5000 oder < -5000")
                        return
                else:
                    return
            else:
                messagebox.showwarning("Fehlende Eingabe", "Bitte gib etwas in die Felder Aura und Kommentar ein.")
                return

        elif cases1 == 2: # LOST
            eintrag.pkt = -1000
            eintrag.kommentar = "LOST"
        elif cases1 == 3: # Labert schmarrn
            eintrag.pkt = -100
            eintrag.kommentar = "Gibt Bullshit von sich"
        elif cases1 == 4: # O-Saft getrunken
            eintrag.pkt = 50
            eintrag.kommentar = "O-Saft "
        else:
            print("Fehler")
            messagebox.showerror("Fatal Error", "Fataler Fehler aufgetreten.")

        rm = sql_befehle.person_bearbeiten(eintrag, person)
        if rm == 0:
            messagebox.showinfo("Erfolg", "Speicherung erfolgreich")
            mainscreen()
        elif rm == 1:
            messagebox.showerror("Fehler bei der Datenspeicherung")

    global person
    # Abfrage Personendaten
    #lib_personen.get()
    eintrg = lib_personen.curselection()
    if eintrg == ():
        messagebox.showwarning("Fehlende Angabe", "Bitte wähle einen Namen aus")
        return
    index = eintrg[0]
    eintrg = pliste[index]
    pid = eintrg[0]
    print(pid)
    #global person
    person, rw = sql_befehle.person_laden(pid)
    if rw == 1:
        messagebox.showwarning("Eingabe fehlt", "Bitte wähle zuvor einen Namen aus")
        return
    elif rw == 2:
        messagebox.showerror("Datenbank Fehler", "Es gab ein Problem mit der Datenverarbeitung")
        return
    
    bn_auswaehlen.config(state="disabled")
    bn_verlauf.config(state="enabled")

    # Elemente
    # Labels
    lb_pinfo = tk.Label(root, text=f"Rang: {person.rang}\nAura: {person.aura}", fg=person.rangclr)
    lb_alternativ = tk.Label(root, text="Manuelle Eingabe")
    lb_punkte = tk.Label(root, text="Aura:")
    lb_kommentar= tk.Label(root, text="Kommentar:")

    # Buttons
    bnwidth = gui_werte.bnwidth
    bn_bestaetigen = ttk.Button(root, text="Bestätigen", width=bnwidth, command=lambda:speichern())
    bn_abbruch = ttk.Button(root, text="Abbruch", width=bnwidth, command=lambda:mainscreen())

    # Radioboxen
    cases = tk.IntVar(value=1)
    rb_case1 = ttk.Radiobutton(root, text="Manuelle Eingabe (unten)", variable=cases, value=1)
    rb_case2 = ttk.Radiobutton(root, text="LOST | -1000", variable=cases, value=2)
    rb_case3 = ttk.Radiobutton(root, text="Labert Schmarrn | -100", variable=cases, value=3)
    rb_case4 = ttk.Radiobutton(root, text="O-Saft Power | +50", variable=cases, value=4)

    # Entry
    tf_punkte = ttk.Entry(root, width=bnwidth + 1)
    tf_kommentar = ttk.Entry(root, width=bnwidth + 1)

    # Platzierung
    xwert = 350
    ywert = 170
    lb_pinfo.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby + 20
    rb_case1.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_rby
    rb_case2.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_rby
    rb_case3.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_rby
    rb_case4.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_rby + 10
    lb_alternativ.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby - 5
    lb_punkte.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby
    tf_punkte.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    lb_kommentar.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby
    tf_kommentar.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_bestaetigen.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_abbruch.place(x=xwert, y=ywert)

def mainscreen():
    def listbox(liste, xwert, ywert):
        listbox_widget = tk.Listbox(root, height=6, width=24, activestyle='none')
        if liste != []:
            for item in liste:
                listbox_widget.insert(tk.END, item)
        listbox_widget.place(x=xwert, y=ywert)
        return listbox_widget

    global bn_auswaehlen, bn_verlauf, pliste # Da Buttons in Funktion auswaehlen() deaktiviert / aktiviert werden, wenn auswählen betätigt wurde.
    clearwdw()
    pliste, rm_pliste = sql_befehle.personen_laden()
    if rm_pliste == 1:
        messagebox.showerror("Datenbank", "Es gab ein Problem bei der Datenübertragung")
        sys.exit()

    pic_logo4.pack()
    bnwidth = gui_werte.bnwidth

    # +++ Elemente +++
    # Labels
    lb_personen = tk.Label(root, text="Mensch*innen")

    # Buttons
    bn_auswaehlen = ttk.Button(root, text="Auswählen", width=bnwidth, command=lambda:auswaehlen(lib_personen))
    bn_personhnzfg = ttk.Button(root, text="Person hinzufügen", width=bnwidth, command=person_hinzufg)
    bn_verlauf = ttk.Button(root, text="Verlauf einsehen", width=bnwidth, command=lambda:verlauf(person), state="disabled")
    bn_beenden = ttk.Button(root, text="Beenden", width=bnwidth, command=sys.exit)

    # Platzieren
    xwert = 40 # Startwert
    ywert = 170 # Startwert

    global lib_personen
    lb_personen.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_lby
    lib_personen = listbox(pliste, xwert, ywert)
    ywert += 130
    bn_auswaehlen.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_verlauf.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_personhnzfg.place(x=xwert, y=ywert)
    ywert += gui_werte.abst_buty
    bn_beenden.place(x=xwert, y=ywert)

# Deklaration Pfade
lnk_azure = os.path.join(os.path.dirname(__file__), "themes", "azure", "azure.tcl")
lnk_logo4 = os.path.join(os.path.dirname(__file__), "images", "logo4.png")

# Objekte und Listen vorladen
global person
gui_werte = klassen.Guiwerte()
#pliste, rm_pliste = sql_befehle.personen_laden()
person = klassen.Person()

# if rm_pliste == 1:
#     messagebox.showerror("Datenbank", "Es gab ein Problem bei der Datenübertragung")
#     sys.exit()

# Erzeugung des Fensters
root = tk.Tk()
root.geometry("600x650")
root.title("auraBook v1.1.0 - Lass es raus!")

# Einstellung GUI
root.tk.call("source", lnk_azure)
root.tk.call("set_theme", "dark")

# Implementierung der Grafiken
logo4 = Image.open(lnk_logo4)
logo4 = logo4.resize((120, 140))
logo41 = ImageTk.PhotoImage(logo4)
pic_logo4 = tk.Label(root, image=logo41)


# Abfrage Key
tf_key = ttk.Entry(root)
tf_key.bind('<Return>', lambda event: startprogramm(tf_key.get()))

bn_key = ttk.Button(root, text="Bestätigen", command=lambda:startprogramm(tf_key.get()))

pic_logo4.pack()
tk.Label(root, text="Key eingeben:", fg="yellow").place(x=90, y=200)
tf_key.place(x=90, y=230)
bn_key.place(x=90, y=270)

root.mainloop()