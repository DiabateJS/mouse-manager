import pyautogui
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return f'Point({self.x},{self.y})'
    def __repr__(self):
        return f'Point({self.x},{self.y})'

class Trajectoire:
    def __init__(self, positions, name):
        self.positions = positions
        self.name = name
    def affichage(self):
        print('Affichage des points de la trajectoire')
        for p in self.positions:
            print(p)
    def deplacerSurPoints(self):
        for p in self.positions:
            print(f'Déplacement de la souris à la position X = {p.x} , Y = {p.y}')
            pyautogui.moveTo(p.x,p.y, duration=10)

class TrajectoireBuilder:
    def __init__(self,trajectoire):
        self.trajectoire = trajectoire

    def build(self):
        t = Trajectoire([],"")
        if self.trajectoire == 0:
            triangle = [Point(300,0),Point(0,300),Point(300,300)]
            t = Trajectoire(triangle,"Triangle")
        if self.trajectoire == 1:
            carre = [Point(300,300), Point(600,300), Point(600,600), Point(300,600)]
            t = Trajectoire(carre,"Carre")
        if self.trajectoire == 2:
            z = [Point(300,300), Point(600,300), Point(450,450), Point(300,600),Point(600,600)]
            t = Trajectoire(z, "Z")
        return t  

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.createWidgets()

    def createWidgets(self): 
        self.title("Utilitaire de déplacement de souris")
        self.geometry("600x650")
        self.label = Label(self,text='Choix de la stratégie de déplacement', font=("Arial", 18))
        self.label.pack() 

        self.image = Image.open("deplacements.png")
        self.photoImage = ImageTk.PhotoImage(self.image)
        self.label2 = Label(image=self.photoImage)
        self.label2.pack()

        self.liste = Listbox(self, borderwidth=0, font=("Arial", 16))
        self.liste.insert(1, "Triangle")
        self.liste.insert(2, "Carre")
        self.liste.insert(3, "Z")
        self.liste.insert(3, "Autre")
        self.liste.pack()

        self.textBox = Text(self, height=8, width=65, relief='solid', font=("Arial",14,"bold"))
        self.textBox.pack(expand=True)
        self.textBox.insert('end','Console de log')
        self.textBox.pack(pady=1)

        self.bouton = Button(self, text="Lancer", width=15, height=3, font=("Arial",16), command=self.activer)
        self.bouton.pack(pady=5)

        self.label1 = Label(self, text="djstechnologies.fr - Mars 2024 - Version : 1.0.0", fg="green", font=("Courrier",12,"italic"))
        self.label1.pack(pady=20)

        self.mainloop()

    def activer(self):
        if len(self.liste.curselection()) > 0 :
            trajectoireBuilder = TrajectoireBuilder(self.liste.curselection()[0])
            trajectoire = trajectoireBuilder.build()
            self.textBox.delete('1.0', END)
            self.textBox.insert(END, 'Stratégie de déplacement '+trajectoire.name+'\n')
            for pt in trajectoire.positions:
                self.textBox.insert(END, str(pt) +'' + '\n')
            trajectoire.deplacerSurPoints()
        else:
            messagebox.showwarning("Attention !","Veuillez selectionner une stratégie de déplacement")


if __name__ == "__main__":
    app = Application()
