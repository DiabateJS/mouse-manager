import pyautogui
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk

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
        if self.trajectoire == "Triangle":
            triangle = [Point(300,0),Point(0,300),Point(300,300)]
            t = Trajectoire(triangle,"Triangle")
        if self.trajectoire == "Carre":
            carre = [Point(300,300), Point(600,300), Point(600,600), Point(300,600)]
            t = Trajectoire(carre,"Carre")
        if self.trajectoire == "Z":
            z = [Point(300,300), Point(600,300), Point(450,450), Point(300,600),Point(600,600)]
            t = Trajectoire(z, "Z")
        return t  

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.createWidgets()

    def createWidgets(self): 
        self.title("Utilitaire de déplacement de souris")
        self.geometry("600x600") 

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True)

        self.deplacements = ttk.Frame(self.notebook, width=600, height=600)
        self.label = Label(self.deplacements,text='Choix de la stratégie de déplacement', font=("Arial", 18))
        self.label.pack()

        self.image = Image.open("deplacements.png")
        self.photoImage = ImageTk.PhotoImage(self.image)
        self.label2 = Label(self.deplacements, image=self.photoImage)
        self.label2.pack(pady=10)

        self.choix_combo = StringVar()
        self.combostrategies = ttk.Combobox(self.deplacements, textvariable=self.choix_combo)
        self.combostrategies['values'] = ('Triangle','Carre','Z','Autre')
        self.combostrategies['state'] = 'readonly'
        self.combostrategies.current(0)
        self.combostrategies.pack(pady=10)

        self.bouton = Button(self.deplacements, text="Lancer", width=15, height=3, font=("Arial",14), command=self.activer)
        self.bouton.pack(pady=10)

        self.parametrages = ttk.Frame(self.notebook, width=600, height=600)
        self.list_trajectoire = Listbox(self.parametrages)
        self.list_trajectoire.insert(1, 'Triangle')
        self.list_trajectoire.insert(2, 'Carre')
        self.list_trajectoire.insert(3, 'Z')

        self.list_trajectoire.bind('<<ListboxSelect>>',self.trajectoire_select)
        self.list_trajectoire.pack()

        self.list_points_trajectoire = Listbox(self.parametrages)
        self.list_points_trajectoire.bind('<<ListboxSelect>>', self.point_select)
        self.list_points_trajectoire.pack(pady=5)

        self.label_point_x = Label(self.parametrages, text="X = ")
        self.label_point_x.pack()
        self.point_x_var = StringVar()
        self.point_x = Entry(self.parametrages, textvariable=self.point_x_var)
        self.point_x.pack()

        self.label_point_y = Label(self.parametrages, text="Y = ")
        self.label_point_y.pack()
        self.point_y_var = StringVar()
        self.point_y = Entry(self.parametrages, textvariable=self.point_y_var)
        self.point_y.pack()

        self.apropos = ttk.Frame(self.notebook, width=600, height=600)
        self.label_textapropos = Label(self.apropos, text='Conception et Développement', font=("Arial",16))
        self.label_textapropos.pack(pady=30)
        self.label_entreprise = Label(self.apropos, text='DJS TECHNOLOGIES', font=("Arial",32,"italic"), fg="blue")
        self.label_entreprise.pack(pady=5)
        self.info_dev = Label(self.apropos, text='Auteur : Jean Sekou DIABATE', font=("Arial",18))
        self.info_dev.pack(pady=10)
        self.email_dev = Label(self.apropos, text='jeansekoudiabate@gmail.com')
        self.email_dev.pack()
        self.site_entreprise = Label(self.apropos, text='https://www.djstechnologies.fr')
        self.site_entreprise.pack(pady=20)

        self.deplacements.pack(fill='both', expand=True)
        self.parametrages.pack(fill='both', expand=True)

        self.apropos.pack(fill='both', expand=True)

        self.notebook.add(self.deplacements, text='Déplacements')
        self.notebook.add(self.parametrages, text='Paramétrages')
        self.notebook.add(self.apropos, text='A propos')

        self.label1 = Label(self, text="djstechnologies.fr - Mars 2024 - Version : 1.0.0", fg="green", font=("Courrier",12,"italic"))
        self.label1.pack(pady=10)

        self.mainloop()

    def activer(self):
        print(self.choix_combo.get())
        if self.choix_combo.get() != "Autre":
            trajectoireBuilder = TrajectoireBuilder(self.choix_combo.get())
            trajectoire = trajectoireBuilder.build()
            trajectoire.deplacerSurPoints()
        else:
            messagebox.showwarning(message="Veuillez choisir une stratégie de déplacement")
    
    def trajectoire_select(self, event):
        select_index = self.list_trajectoire.curselection()[0]
        tab_trajectoires = ('Triangle','Z','Carre')
        if select_index < len(tab_trajectoires):
            trajectoire = tab_trajectoires[select_index]
            trajectoirBuilder = TrajectoireBuilder(trajectoire)
            t = trajectoirBuilder.build()
            self.list_points_trajectoire.delete(0, END)
            for index in range(len(t.positions)):
                self.list_points_trajectoire.insert(index, t.positions[index])
    
    def point_select(self, event):
        index = self.list_points_trajectoire.curselection()[0]
        select_item = self.list_points_trajectoire.get(index)
        print(select_item)
        xy_str = select_item.split("(")[1].split(")")[0] 
        print(xy_str)
        xy_tab = xy_str.split(",")
        x = xy_tab[0]
        y = xy_tab[1]
        self.point_x_var.set(x)
        self.point_y_var.set(y)

            
if __name__ == "__main__":
    app = Application()
