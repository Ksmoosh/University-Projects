## Projekt na MMM

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from math import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = Tk()
root.title("Projekt")
root.geometry("1650x950")

group = LabelFrame(root)
group.grid(row=0, column=0)

wykresy = LabelFrame(root)
wykresy.grid(row=1, column=0)

sygnal = IntVar()

sygn_pros = BooleanVar()
sygn_troj = BooleanVar()
sygn_sin = BooleanVar()

sygn_pros.set(False)
sygn_troj.set(False)
sygn_sin.set(False)

PrzekrojS1 = Entry(group)
PrzekrojS2 = Entry(group)

ZwezkaA1 = Entry(group)
ZwezkaA2 = Entry(group)

Strumien = Entry(group)

PrzyciskModeluj = Button(group, text="Modeluj")
CheckPros = Radiobutton(group, text="Sygnał Prostokątny", variable=sygnal, value=1)
CheckTroj = Radiobutton(group, text="Sygnał Trójkątny", variable=sygnal, value=2)
CheckSin = Radiobutton(group, text="Sygnał Sinusoidalny", variable=sygnal, value=3)

# matplotlib
f1 = Figure(figsize=(15, 7), dpi=55)
a = f1.add_subplot(111)

f2 = Figure(figsize=(15, 7), dpi=55)
b = f2.add_subplot(111)

f3 = Figure(figsize=(15, 7), dpi=55)
c = f3.add_subplot(111)

g = 9.81
s1 = 0
s2 = 0
a1 = 0
a2 = 0
h1 = 0
h2 = 0

def blad_zmiennych(jakiblad):
    messagebox.showwarning("Uwaga", jakiblad)

def spr_dane(event=None):
    try:
        s1 = int(PrzekrojS1.get())
        s2 = int(PrzekrojS2.get())
        a1 = int(ZwezkaA1.get())
        a2 = int(ZwezkaA2.get())
    except ValueError:
        blad_zmiennych("Należy podać liczbę!")
        return 0
    if s2 >= s1:
        blad_zmiennych("Przekrój pierwszego zbiornika powinien być większy niż przekrój drugiego!")
        return 0
    elif a2 >= a1:
        blad_zmiennych("Przekrój pierwszej zwężki powinien być większy niż przekrój drugiej!")
        return 0
    elif (a1 > 1000) or (s1 > 1000):
        blad_zmiennych("Za duże wartości liczbowe! Wprowadź inne")
        return 0
    return 1

def upros(t):
    if (t % 12) < 6:
        return 500
    else:
        return 0

def utroj(t):
    if (t % 12) <= 6:
         return (t % 12) / 3 * 250
    else:
         return 1000 - (t % 12) / 3 * 250

def usine(t):
    return 250+250*sin(pi * 2 * t / 12)

def pobudzenie(u):
    if sygnal.get() == 1:
        return upros(u)
    elif sygnal.get() == 2:
        return utroj(u)
    elif sygnal.get() == 3:
        return usine(u)

def oblicz_dt(i):
    kon_sym = 60
    pocz_sym = 0
    liczba_iter = i
    return (kon_sym - pocz_sym)/liczba_iter

def rownania(t, dt, h1, h2):
    # opróżnianie zbiorników po zakończeniu symulacji
    if t == 30001:
        h2 = dt * ((1 / s2) * ((sqrt(2 * g * h1) * a1) - sqrt(2 * g * h2) * a2)) + h2
        h1 = dt * ((1 / s1) * (0 - sqrt(2 * g * h1) * a1)) + h1
        if h1 < 0:
            h1 = 0
        if h2 < 0:
            h2 = 0
        return h1, h2

    h2 = dt * ((1 / s2) * ((sqrt(2 * g * h1) * a1) - sqrt(2 * g * h2) * a2)) + h2
    h1 = dt * ((1 / s1) * (pobudzenie(t * dt) - sqrt(2 * g * h1) * a1)) + h1
    if h1 < 0:
        h1 = 0
    if h2 < 0:
        h2 = 0

    return h1, h2

def rysuj():
    canvas1 = FigureCanvasTkAgg(f1, master=wykresy)
    canvas1.get_tk_widget().grid(row=10, column=1)
    a.set_xlabel('Czas')
    a.set_ylabel('Poziom wody w pierwszym zbiorniku')
    canvas1.draw()

    canvas2 = FigureCanvasTkAgg(f2, master=wykresy)
    canvas2.get_tk_widget().grid(row=11, column=1)
    b.set_xlabel('Czas')
    b.set_ylabel('Poziom wody w drugim zbiorniku')
    canvas2.draw()

    canvas3 = FigureCanvasTkAgg(f3, master=wykresy)
    canvas3.get_tk_widget().grid(row=10, column=0)
    c.set_xlabel('Czas')
    c.set_ylabel('Wartość sygnału')
    canvas3.draw()

def modeluj(event=None):
    global s1
    global s2
    global a1
    global a2
    global a
    global h1
    global h2
    x1List = []
    y1List = []
    x2List = []
    y2List = []
    x3List = []
    y3List = []

    if not spr_dane():
        return
    else:
        s1 = int(PrzekrojS1.get())
        s2 = int(PrzekrojS2.get())
        a1 = int(ZwezkaA1.get())
        a2 = int(ZwezkaA2.get())
        print("Działa")
# 30000 iteracji, przy symulacji sygnału trwającej 60 sekund, natomiast dt=1/500s
    dt = oblicz_dt(30000)
    for i in range(30000):
        h1, h2 = rownania(i, dt, h1, h2)
        x1List.append(i * dt)
        y1List.append(h1)
        x2List.append(i * dt)
        y2List.append(h2)
        x3List.append(i * dt)
        y3List.append(pobudzenie(i * dt))
    while h2 != 0:
        i = i + 1
        h1, h2 = rownania(30001, dt, h1, h2)
        print(h1)
        print(h2)
        print(i)
        x1List.append(i * dt)
        y1List.append(h1)
        x2List.append(i * dt)
        y2List.append(h2)

    a.clear()
    b.clear()
    c.clear()
    a.plot(x1List, y1List)
    b.plot(x2List, y2List)
    c.plot(x3List, y3List)

    rysuj()

    h1 = 0
    h2 = 0


Label(group, text="Podaj przekrój pierwszego zbiornika: ").grid(row=2, column=0, sticky=W, padx=4, pady=10)
PrzekrojS1.grid(row=2, column=1, sticky=W, padx=4, pady=10)

Label(group, text="oraz przekrój jego zwężki: ").grid(row=2, column=2, sticky=W, padx=4)
ZwezkaA1.grid(row=2, column=3, sticky=W, padx=4, pady=10)

Label(group, text="Podaj przekrój drugiego zbiornika: ").grid(row=4, column=0, sticky=W, padx=4, pady=10)
PrzekrojS2.grid(row=4, column=1, sticky=W, padx=4, pady=10)

Label(group, text="oraz przekrój jego zwężki: ").grid(row=4, column=2, sticky=W, padx=4, pady=5)
ZwezkaA2.grid(row=4, column=3, sticky=W, padx=4, pady=10)

Label(group, text="Wybierz rodzaj strumienia na wejściu: ").grid(row=6, column=0, sticky=W, padx=4, pady=10)

CheckPros.grid(row=6, column=1, sticky=W, padx=4, pady=10)

CheckTroj.grid(row=6, column=2, sticky=W, padx=4, pady=10)

CheckSin.grid(row=6, column=3, sticky=W, padx=4, pady=10)

PrzyciskModeluj.bind("<Button-1>", modeluj)
PrzyciskModeluj.grid(row=8, column=2, sticky=W)

rysuj()

root.mainloop()