import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Team_data():

    sqlite_var = 0
    theCursor = 0

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('Soccer Team.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print('Não foi possível conectar ao banco de dados!')
            
        try:
            self.theCursor.execute("CREATE TABLE if not exists Team(ID_team INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Coach TEXT UNIQUE NOT NULL, President TEXT NOT NULL, Foundation TEXT NOT NULL, Stadium TEXT NOT NULL, Sponsor TEXT NOT NULL, Sports_Equipment TEXT NOT NULL);")
        except:
            print('Não foi possível criar a tabela!')
        finally:
            self.sqlite_var.commit()

    def back(self):
        self.root.destroy()
        
    def update_Datas(self):
        self.theCursor.execute("""UPDATE Team Set Name = ?, Coach = ?, President = ?, Foundation = ?, Stadium = ?, Sponsor = ?, Sports_Equipment = ? WHERE ID_team = 1""",
        (self.Name_value.get(), self.Coach_value.get(), self.President_value.get(), self.Foundation_value.get(), self.Stadium_value.get(), self.Sponsor_value.get(), self.Sports_Equipment_value.get()))
        self.sqlite_var.commit()
        messagebox.showinfo('Dados do Time', 'Dados Atualizados!')

    def statistics(self):

        self.theCursor.execute("SELECT Result, Place FROM Matches")
        res = self.theCursor.fetchall()

        goal_favor = 0
        goal_against = 0
        victory = 0
        defeat = 0
        draw = 0

        for row in res:
            aux = str(row[0]).split()
            
            goal_favor = goal_favor + int(aux[0])
            goal_against = goal_against + int(aux[2])

            if int(aux[0]) > int(aux[2]): victory = victory + 1
            elif int(aux[0]) < int(aux[2]): defeat = defeat + 1
            else: draw = draw + 1
            
            
        st = tk.Toplevel()
        st.title('Estatísticas do Clube')
        st['bg'] = '#4db8ff'
        st.geometry('300x300+500+200')

        tk.Label(st, text='Estatísticas Gerais', font='Ariel 14 bold', bg='#4db8ff', fg='white').grid(row=0, column=0, pady=20, columnspan=2, padx=70)

        tk.Label(st, text='Jogos: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=1, column=0)
        tk.Label(st, text=len(res), font='Ariel 12', bg='#4db8ff', fg='white').grid(row=1, column=1)

        tk.Label(st, text='Vitórias: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=2, column=0)
        tk.Label(st, text=victory, font='Ariel 12', bg='#4db8ff', fg='white').grid(row=2, column=1)

        tk.Label(st, text='Empates: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=3, column=0)
        tk.Label(st, text=draw, font='Ariel 12', bg='#4db8ff', fg='white').grid(row=3, column=1)

        tk.Label(st, text='Derrotas: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=4, column=0)
        tk.Label(st, text=defeat, font='Ariel 12', bg='#4db8ff', fg='white').grid(row=4, column=1)

        tk.Label(st, text='Gols marcados: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=5, column=0)
        tk.Label(st, text=goal_favor, font='Ariel 12', bg='#4db8ff', fg='white').grid(row=5, column=1)

        tk.Label(st, text='Gols sofridos: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=6, column=0)
        tk.Label(st, text=goal_against, font='Ariel 12', bg='#4db8ff', fg='white').grid(row=6, column=1)

        st.mainloop()



    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Time de Futebol')
        self.root['bg'] = '#4db8ff'
        self.root.geometry('600x600+350+30')
        self.root.iconbitmap("futebol.ico")

        tk.Label(self.root, text='Dados do Time', font='Avalon 20 bold', bg='#4db8ff', fg='white').place(x=200, y=60)

        tk.Label(self.root, text='Nome:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=160)
        tk.Label(self.root, text='Treinador:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=200)
        tk.Label(self.root, text='Presidente:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=240)
        tk.Label(self.root, text='Fundação:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=280)
        tk.Label(self.root, text='Estádio:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=320)
        tk.Label(self.root, text='Patrocinador Master:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=360)
        tk.Label(self.root, text='Material Esportivo:', font='Ariel 12 bold', bg='#4db8ff', fg='white').place(x=10, y=400)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Name_value)
        self.Name_entry.place(x=200, y=160)

        self.Coach_value = tk.StringVar(self.root, value="")
        self.Coach_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Coach_value)
        self.Coach_entry.place(x=200, y=200)

        self.President_value = tk.StringVar(self.root, value="")
        self.President_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.President_value)
        self.President_entry.place(x=200, y=240)

        self.Foundation_value = tk.StringVar(self.root, value="")
        self.Foundation_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Foundation_value)
        self.Foundation_entry.place(x=200, y=280)

        self.Stadium_value = tk.StringVar(self.root, value="")
        self.Stadium_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Stadium_value)
        self.Stadium_entry.place(x=200, y=320)

        self.Sponsor_value = tk.StringVar(self.root, value="")
        self.Sponsor_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Sponsor_value)
        self.Sponsor_entry.place(x=200, y=360)

        self.Sports_Equipment_value = tk.StringVar(self.root, value="")
        self.Sports_Equipment_entry = ttk.Entry(self.root, font='Ariel, 10', width=30, textvariable=self.Sports_Equipment_value)
        self.Sports_Equipment_entry.place(x=200, y=400)

        self.setup_db()

        self.theCursor.execute('SELECT * FROM Team WHERE ID_team = 1')
        self.result = self.theCursor.fetchall()
        self.Name_value.set(self.result[0][1])
        self.Coach_value.set(self.result[0][2])
        self.President_value.set(self.result[0][3])
        self.Foundation_value.set(self.result[0][4])
        self.Stadium_value.set(self.result[0][5])
        self.Sponsor_value.set(self.result[0][6])
        self.Sports_Equipment_value.set(self.result[0][7])

        tk.Button(self.root, width=20, text='Editar', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.update_Datas).place(x=210, y=450)
        tk.Button(self.root, width=20, text='Estatísticas Gerais', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.statistics).place(x=210, y=500)
        tk.Button(self.root, width=20, text='Voltar', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.back).place(x=210, y=550)

        
        self.root.mainloop()