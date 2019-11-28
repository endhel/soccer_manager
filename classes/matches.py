import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re

class Matches_dates():

    sqlite_var = 0
    theCursor = 0
    curItem = 0
    list_id = []
    list_names = []

    def refresh(self):
        self.update_tree()
        self.clear_entries()

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM Matches WHERE Adversary like ? or Date like ? or Place like ? or Tournament like ? or Result like ?", ('%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%'))
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

    def clear_entries(self):
        self.Adversary_entry.delete(0, "end")
        self.Date_entry.delete(0, "end")
        self.Place_entry.delete(0, "end")
        self.Tournament_entry.delete(0, "end")
        self.Result_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.theCursor.execute("delete FROM Matches WHERE ID_matches=?", (self.curItem['values'][0],))
            print("DADOS DELETADOS")
        
        except:
            print('Não foi possível deletar estes dados!')
        
        finally:
            self.curItem=0
            self.clear_entries()
            self.update_tree()
            self.sqlite_var.commit()

    def update_record(self):
        if(self.Adversary_value.get() != "" and self.Date_value.get() != "" and self.Place_value.get() != "" and self.Tournament_value.get() != ""):
            aux = str(self.Result_value.get()).split()
            if  len(aux) == 3 and aux[0].isdecimal() and aux[2].isdecimal():
                try:
                    self.theCursor.execute("""UPDATE Matches SET Adversary = ?, Date = ?, Place = ?, Tournament = ?, Result = ? WHERE ID_matches = ? """, 
                    (self.Adversary_value.get(), self.Date_value.get(),  self.Place_value.get(), self.Tournament_value.get(), self.Result_value.get(), self.curItem['values'][0]))
                    self.clear_entries()
                    print('Dados atualizados!')
                except sqlite3.IntegrityError:
                    messagebox.showerror('Jogos', 'Este jogo já se encontra no banco de dados!')
                except:
                    print('Não foi possível atualizar os dados!')
                finally:
                    self.update_tree()
                    self.sqlite_var.commit()
            else:
                messagebox.showwarning('Jogos', 'O Formato padrão do campo "Resultado" é: \n[número x número]')
        else:
            messagebox.showwarning('Jogos', 'Atenção! Apenas o campo Resultado não é obrigatório preencher. Favor preencher os restantes!')

    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Adversary_value.set(self.curItem['values'][1])
        self.Date_value.set(self.curItem['values'][2])
        self.Place_value.set(self.curItem['values'][3])
        self.Tournament_value.set(self.curItem['values'][4])
        self.Result_value.set(self.curItem['values'][5])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT ID_matches, Adversary, Date, Place, Tournament, Result FROM Matches")
            self.rows = self.theCursor.fetchall()
            i = 0
            for row in self.rows:
                if(i % 2 == 0):
                    self.tree.insert("", tk.END, values=row, tag='1')
                else:
                    self.tree.insert("", tk.END, values=row, tag='2')
                i = i + 1
        except:
            print('Não foi possível atualizar os dados!')
    
    def write_record(self):
        if(self.Adversary_value.get() != "" and self.Date_value.get() != "" and self.Place_value.get() != "" and self.Tournament_value.get() != ""):
            aux = str(self.Result_value.get()).split()
            if  len(aux) == 3 and aux[0].isnumeric and aux[2].isnumeric:
                try:
                    self.theCursor.execute("""INSERT INTO Matches (Adversary, Date, Place, Tournament, Result, ID_team) VALUES(?,?,?,?,?,?) """, 
                    (self.Adversary_value.get(), self.Date_value.get(),  self.Place_value.get(), self.Tournament_value.get(), self.Result_value.get(), 1))
                    self.sqlite_var.commit()
                    self.theCursor.execute("SELECT*, max(ID_matches) FROM Matches")
                    self.rows = self.theCursor.fetchall()
                    self.clear_entries()
                except sqlite3.IntegrityError:
                    messagebox.showerror('Jogos', 'Este jogo já se encontra no banco de dados!')
                except:
                    print('Não foi possível cadastrar o jogo!')
                finally:
                    self.update_tree()
            else:
                messagebox.showwarning('Jogos', 'O Formato padrão do campo "Resultado" é: \n[número x número]')
        else:
            messagebox.showwarning('Jogos', 'Favor preencher todos os campos')
        
    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('Soccer Team.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print('Não foi possível conectar ao banco de dados!')
            
        try:
            self.theCursor.execute("CREATE TABLE if not exists Matches(ID_matches INTEGER PRIMARY KEY AUTOINCREMENT, Adversary TEXT NOT NULL, Date TEXT UNIQUE NOT NULL ,Place TEXT NOT NULL, Tournament TEXT NOT NULL, Result TEXT, ID_team INTEGER NOT NULL, FOREIGN KEY (ID_team) REFERENCES Team (ID_team));")
        except:
            print('Não foi possível criar a tabela!')
        finally:
            self.sqlite_var.commit()
            self.update_tree()

    def back(self):
        self.root.destroy()
    

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Jogos')
        self.root.resizable(False, False)
        self.root.iconbitmap("futebol.ico")
        self.root.geometry('+350+30')
        self.root['bg'] = 'white'

        self.Adversary = tk.Label(self.root, text='Adversário:', font='Ariel', fg='black', bg='white')
        self.Adversary.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Adversary_value = tk.StringVar(self.root, value="")
        self.Adversary_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Adversary_value)
        self.Adversary_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Date = tk.Label(self.root, text='Data:', font='Ariel', fg='black', bg='white')
        self.Date.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Date_value = tk.StringVar(self.root, value="")
        self.Date_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Date_value)
        self.Date_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Place = tk.Label(self.root, text='Local:', font='Ariel', fg='black', bg='white')
        self.Place.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Place_value = tk.StringVar(self.root, value="")
        self.Place_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Place_value)
        self.Place_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Tournament = tk.Label(self.root, text='Torneio:', font='Ariel', fg='black', bg='white')
        self.Tournament.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Tournament_value = tk.StringVar(self.root, value="")
        self.Tournament_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Tournament_value)
        self.Tournament_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10) 

        self.Result = tk.Label(self.root, text='Resultado:', font='Ariel', fg='black', bg='white')
        self.Result.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Result_value = tk.StringVar(self.root, value="")
        self.Result_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Result_value)
        self.Result_entry.grid(row=4, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)     

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W+tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W+tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W+tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse", column=("column1", "column2", "column3", "column4", "column5", "column6"), show='headings')
        self.tree.column("column1", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="ID")
        self.tree.column("column2", width=200, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Adversário")
        self.tree.column("column3", width=100, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Data")
        self.tree.column("column4", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Local")
        self.tree.column("column5", width=150, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Torneio")
        self.tree.column("column6", width=80, minwidth=100, stretch=tk.NO)
        self.tree.heading("#6", text="Resultado")
        self.tree.bind("<ButtonRelease-1>", self.selectItem)
        self.tree.bind("<space>", self.selectItem)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=5, column=0, padx=9, pady=9, sticky=tk.W+tk.E, columnspan=4)

        tk.Label(self.root, text='Pesquisar:', font='Ariel', fg='black', bg='white').grid(row=6, column=0, columnspan=2, sticky=tk.E, padx=9, pady=9)
        self.search_value = tk.StringVar(self.root, value="")
        tk.Entry(self.root, textvariable= self.search_value).grid(row=6, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.root, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=6, column=3, padx=9, sticky=tk.W+tk.E)   

        self.refresh_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.refresh)  
        self.refresh_button.grid(row=7, column=2, padx=9, pady=9, sticky=tk.W+tk.E)

        self.back_button = ttk.Button(self.root, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=7, column=3, padx=9, sticky=tk.W+tk.E)

        self.setup_db()
        self.root.mainloop()