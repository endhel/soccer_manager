import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Player_Match:

    sqlite_var = 0
    theCursor = 0

    def clear_entries(self):
        self.Goal_entry.delete(0, "end")
        self.Assist_entry.delete(0, "end")
        self.Yellow_Card_entry.delete(0, "end")
        self.Red_Card_entry.delete(0, "end")

    def refresh(self):
        self.update_tree()
        self.clear_entries()
        self.search_value.set("")

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())

            query = """SELECT  m.Adversary, m.Place, m.Result, m.Date, p.Name, pm.Goal, pm.Assist, pm.Yellow_Card, pm.Red_Card 
                       FROM Player_Match pm, Players p, Team t, Matches m
                       WHERE pm.ID_matches = m.ID_matches and pm.ID_player = p.ID_player and (m.Adversary like ? or m.Place like ? or m.Date like ? or m.Tournament like ? or p.Name like ?)
                       ORDER BY pm.ID_matches ASC"""
            self.theCursor.execute(query, ('%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%'))
            self.result = self.theCursor.fetchall()

            length = str(len(self.result))
            if(length == 0):
                messagebox.showinfo('Jogos', 'Não foi possível encontrar um resultado!')
            if(length != '0'):
                i = 0

                for row in self.result:    
                    if(i % 2 == 0):
                        self.tree.insert("", tk.END, values=row, tag='1')
                    else:
                        self.tree.insert("", tk.END, values=row, tag='2')
                    i = i + 1
        except:
            print("Não foi possível encontrar dados!")

    def update_record(self):
        try:
            query1 = "SELECT ID_matches, ID_player FROM Matches, Players WHERE Date = ? and Name = ?"
            self.theCursor.execute(query1, (self.Date_value.get(), self.Name_value.get()))
            res = self.theCursor.fetchall()
            query2 = """UPDATE Player_Match 
                        SET Goal = ?, Assist = ?, Yellow_Card = ?, Red_Card = ? 
                        WHERE ID_matches = ? and ID_player = ?;"""
            self.theCursor.execute(query2, (self.Goal_value.get(), self.Assist_value.get(),  self.Yellow_Card_value.get(), self.Red_Card_value.get(), res[0][0], res[0][1]))
            print('Dados atualizados!')
        except sqlite3.IntegrityError:
            messagebox.showerror('Jogos', 'Este jogo já se encontra no banco de dados!')
        except:
            print('Não foi possível atualizar os dados!')
        finally:
            if self.search_value.get() == "":
                self.update_tree()
            else:
                self.search_record()
            self.sqlite_var.commit()
        

    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Goal_value.set(self.curItem['values'][5])
        self.Assist_value.set(self.curItem['values'][6])
        self.Yellow_Card_value.set(self.curItem['values'][7])
        self.Red_Card_value.set(self.curItem['values'][8])
        self.Date_value.set(self.curItem['values'][3])
        self.Name_value.set(self.curItem['values'][4])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())

            self.theCursor.execute("""SELECT  m.Adversary, m.Place, m.Result, m.Date, p.Name, pm.Goal, pm.Assist, pm.Yellow_Card, pm.Red_Card 
                                      FROM Player_Match pm, Players p, Team t, Matches m
                                      WHERE pm.ID_matches = m.ID_matches and pm.ID_player = p.ID_player
                                      ORDER BY pm.ID_matches ASC""")
            self.rows = self.theCursor.fetchall()
            i = 0

            for row in self.rows:
                if(i % 2 == 0):
                    self.tree.insert("", tk.END, values=row, tag='1')
                else:
                    self.tree.insert("", tk.END, values=row, tag='2')
                i = i + 1
        except:
            print('Não foi possível atualizar a árvore!')

    def populate_Database(self):
        
        self.theCursor.execute("SELECT ID_matches FROM Matches")
        result_1 = self.theCursor.fetchall()
        self.theCursor.execute("SELECT ID_player FROM Players")
        result_2 = self.theCursor.fetchall()

        for i in result_1:
            for j in result_2:
                self.theCursor.execute("SELECT * FROM Player_Match WHERE ID_matches = ? and ID_player = ?", (i[0], j[0]))
                res = self.theCursor.fetchall()
                if not res:
                    self.theCursor.execute("INSERT INTO Player_Match (ID_matches, ID_player, Goal, Assist, Yellow_Card, Red_Card) VALUES (?,?,?,?,?,?)", (i[0], j[0], 0, 0, 0, 0))
        self.sqlite_var.commit()

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('Soccer Team.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print('Não foi possível conectar ao banco de dados!')
            
        try:
            self.theCursor.execute("CREATE TABLE if not exists Player_Match(ID_player INTEGER NOT NULL, ID_matches INTEGER NOT NULL, Goal INTEGER DEFAULT 0, Assist INTEGER DEFAULT 0, Yellow_Card INTEGER DEFAULT 0, Red_Card INTEGER DEFAULT 0, PRIMARY KEY(ID_player, ID_matches), FOREIGN KEY (ID_player) REFERENCES Players (ID_player), FOREIGN KEY (ID_matches) REFERENCES Matches (ID_matches));")
            self.populate_Database()
        except:
            print('Não foi possível criar a tabela!')
        finally:
            self.sqlite_var.commit()
            self.update_tree()
    
    def back(self):
        self.pm.destroy()

    def __init__(self):

        self.pm = tk.Tk()
        self.pm.title('Jogos')
        self.pm.resizable(False, False)
        self.pm.iconbitmap("futebol.ico")
        self.pm.geometry('+350+30')
        self.pm['bg'] = '#4db8ff'

        self.Date_value = tk.StringVar()
        self.Name_value = tk.StringVar()

        self.Goal = tk.Label(self.pm, text='Gol:', font='Ariel', fg='white', bg='#4db8ff')
        self.Goal.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Goal_value = tk.StringVar(self.pm, value="")
        self.Goal_entry = ttk.Entry(self.pm, font='Ariel, 10', textvariable=self.Goal_value)
        self.Goal_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Assist = tk.Label(self.pm, text='Assistência:', font='Ariel', fg='white', bg='#4db8ff')
        self.Assist.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Assist_value = tk.StringVar(self.pm, value="")
        self.Assist_entry = ttk.Entry(self.pm, font='Ariel, 10', textvariable=self.Assist_value)
        self.Assist_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Yellow_Card = tk.Label(self.pm, text='Cartão Amarelo:', font='Ariel', fg='white', bg='#4db8ff')
        self.Yellow_Card.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Yellow_Card_value = tk.StringVar(self.pm, value="")
        self.Yellow_Card_entry = ttk.Entry(self.pm, font='Ariel, 10', textvariable=self.Yellow_Card_value)
        self.Yellow_Card_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Red_Card = tk.Label(self.pm, text='Cartão Vermelho:', font='Ariel', fg='white', bg='#4db8ff')
        self.Red_Card.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)    

        self.Red_Card_value = tk.StringVar(self.pm, value="")
        self.Red_Card_entry = ttk.Entry(self.pm, font='Ariel, 10', textvariable=self.Red_Card_value)
        self.Red_Card_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.update_button = ttk.Button(self.pm, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=0, column=3, padx=9, sticky=tk.W+tk.E)

        self.tree = ttk.Treeview(self.pm, selectmode="browse", column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9"), show='headings')
        self.tree.column("column1", width=150, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="Adversário")
        self.tree.column("column2", width=150, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Local")
        self.tree.column("column3", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Resultado")
        self.tree.column("column4", width=80, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Data")
        self.tree.column("column5", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Jogador")
        self.tree.column("column6", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#6", text="Gol")
        self.tree.column("column7", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#7", text="Ass")
        self.tree.column("column8", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#8", text="CA")
        self.tree.column("column9", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#9", text="CV")
        self.tree.bind("<ButtonRelease-1>", self.selectItem)
        self.tree.bind("<space>", self.selectItem)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=4, column=0, padx=9, pady=9, sticky=tk.W+tk.E, columnspan=4)

        tk.Label(self.pm, text='Pesquisar:', font='Ariel', fg='white', bg='#4db8ff').grid(row=5, column=0, columnspan=2, sticky=tk.E, padx=9, pady=9)
        self.search_value = tk.StringVar(self.pm, value="")
        tk.Entry(self.pm, textvariable= self.search_value).grid(row=5, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.pm, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=5, column=3, padx=9, sticky=tk.W+tk.E)   

        self.refresh_button = ttk.Button(self.pm, text='Atualizar', cursor="hand2", command=self.refresh)  
        self.refresh_button.grid(row=6, column=2, padx=9, pady=9, sticky=tk.W+tk.E)

        self.back_button = ttk.Button(self.pm, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=6, column=3, padx=9, sticky=tk.W+tk.E)

        self.setup_db()
        self.populate_Database()
        self.pm.mainloop()

        