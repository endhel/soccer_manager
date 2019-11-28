import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from employees import View_employee
from players import View_player
from matches import Matches_dates
from team_data import Team_data

class Main_Window():

    def quit_window(self):
        if messagebox.askokcancel('Soccer Manager', 'Deseja realmente sair?'):
            self.root.destroy()

    def teamData(self):
        self.root.destroy()
        Team_data()
        Main_Window()

    def matchDates(self):
        self.root.destroy()
        Matches_dates()
        Main_Window()

    def viewPlayer(self):
        self.root.destroy()
        View_player()
        Main_Window()

    def viewEmployee(self):
        self.root.destroy()
        View_employee()
        Main_Window()
        
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Soccer Manager')
        self.root['bg'] = '#4db8ff'
        self.root.geometry('600x600+350+30')
        self.root.iconbitmap("futebol.ico")

        tk.Label(self.root, text='Soccer Manager', font='Avalon 30', bg='#4db8ff', fg='white').place(x=165, y=100)
        
        tk.Button(self.root, width=20, text='Sobre o Time', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.teamData).place(x=210, y=200)
        tk.Button(self.root, width=20, text='Jogos', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.matchDates).place(x=210, y=250)
        tk.Button(self.root, width=20, text='Jogadores', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.viewPlayer).place(x=210, y=300)
        tk.Button(self.root, width=20, text='Funcionários', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.viewEmployee).place(x=210, y=350)
        tk.Button(self.root, width=20, text='Sair', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.quit_window).place(x=210, y=400)

        self.root.mainloop()