import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from player_match import Player_Match

class View_player:

    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()


    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("select * from Players where Name like ? or Inscricao like ? or Position like ? or Age like ? or Height like ? or Weight like ?", ('%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%'))
            self.result = self.theCursor.fetchall()

            length = str(len(self.result))
            if(length == 0):
                messagebox.showinfo('Jogadores', 'Não foi possível encontrar um resultado!')
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
        self.Position_entry.delete(0, "end")
        self.Name_entry.delete(0, "end")
        self.subscription_no_entry.delete(0, "end")
        self.Age_entry.delete(0, "end")
        self.Height_entry.delete(0, "end")
        self.Weight_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.theCursor.execute("delete FROM Players WHERE ID_player=?", (self.curItem['values'][0],))
            print("DADOS DELETADOS")
        
        except:
            print('Não foi possível deletar estes dados!')
        
        finally:
            self.curItem=0
            self.clear_entries()
            self.update_tree()
            self.sqlite_var.commit()
    
    def playerMatch(self):
        self.root.destroy()
        Player_Match()
        View_player()

    def update_record(self):
        if(self.Position_value.get() != "" and self.Name_value.get() != "" and self.subscription_no_value.get() != "" and self.Age_value.get() != "" and self.Height_value.get() != "" and self.Weight_value.get() != ""):
            try:
                self.theCursor.execute("""UPDATE Players SET Position = ?, Name = ?, Inscricao = ?, Age = ?, Height = ?, Weight = ? WHERE ID_player = ? """, 
                (self.Position_value.get(), self.Name_value.get(),  self.subscription_no_value.get(), self.Age_value.get(), self.Height_value.get(), self.Weight_value.get(), self.curItem['values'][0]))
                self.clear_entries()
                print('Dados atualizados!')
            except sqlite3.IntegrityError:
                messagebox.showerror('Jogadores', 'Este jogador já se encontra no banco de dados!')
            except:
                print('Não foi possível atualizar os dados!')
            finally:
                self.update_tree()
                self.sqlite_var.commit()
        else:
            messagebox.showwarning('Jogadores', 'Favor preencher todos os campos')

    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Position_value.set(self.curItem['values'][1])
        self.Name_value.set(self.curItem['values'][2])
        self.subscription_no_value.set(self.curItem['values'][3])
        self.Age_value.set(self.curItem['values'][4])
        self.Height_value.set(self.curItem['values'][5])
        self.Weight_value.set(self.curItem['values'][6])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT ID_player, Position, Name, Inscricao, Age, Height, Weight FROM Players")
            self.rows = self.theCursor.fetchall()
            i = 0
            for row in self.rows:
                if(i % 2 == 0):
                    self.tree.insert("", tk.END, values=row, tag='1')
                else:
                    self.tree.insert("", tk.END, values=row, tag='2')
                i = i + 1
        except:
            print('Não foi possível inserir na árvore!')
 
    def write_record(self):
        if(self.Position_value.get() != "" and self.Name_value.get() != "" and self.subscription_no_value.get() != "" and self.Age_value.get() != "" and self.Height_value.get() != "" and self.Weight_value.get() != ""):
            try:
                self.theCursor.execute("""INSERT INTO Players (Position, Name, Inscricao, Age, Height, Weight, ID_team) VALUES(?,?,?,?,?,?,?) """, 
                (self.Position_value.get(), self.Name_value.get(),  self.subscription_no_value.get(), self.Age_value.get(), self.Height_value.get(), self.Weight_value.get(), 1))
                self.sqlite_var.commit()
                self.theCursor.execute("SELECT*, max(ID_player) FROM Players")
                self.rows = self.theCursor.fetchall()
                self.clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror('Jogadores', 'Este jogador já se encontra no banco de dados!')
            except:
                print('Não foi possível cadastrar os dados!')
            finally:
                self.update_tree()
        else:
            messagebox.showwarning('Jogadores', 'Favor preencher todos os campos')
        
    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('Soccer Team.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print('Não foi possível conectar ao banco de dados!')
            
        try:
            self.theCursor.execute("CREATE TABLE if not exists Players(ID_player INTEGER PRIMARY KEY AUTOINCREMENT, Position TEXT NOT NULL, Name TEXT NOT NULL ,Inscricao TEXT UNIQUE NOT NULL, Age INTEGER NOT NULL, Height TEXT NOT NULL, Weight TEXT NOT NULL, ID_team INTEGER NOT NULL, FOREIGN KEY (ID_team) REFERENCES Team (ID_team));")
        except:
            print('Não foi possível criar a tabela!')
        finally:
            self.sqlite_var.commit()
            self.update_tree()

    def back(self):
        self.root.destroy()
    
    def statistics(self):

        if(self.Position_value.get() != "" and self.Name_value.get() != "" and self.subscription_no_value.get() != "" and self.Age_value.get() != "" and self.Height_value.get() != "" and self.Weight_value.get() != ""):
            st = tk.Toplevel()
            st.title('Estatísticas do Jogador')
            st['bg'] = '#4db8ff'
            st.geometry('+500+200')

            query = """SELECT SUM(Goal), SUM(Assist), SUM(Yellow_Card), SUM(Red_Card), t.Name
                       FROM Player_Match pm, Players p, Team t
                       WHERE p.Inscricao = ? and p.ID_player = pm.ID_player"""

            self.theCursor.execute(query, (self.subscription_no_value.get(),))
            res = self.theCursor.fetchall()

            title = 'Números do Jogador pelo ' + res[0][4]

            tk.Label(st, text=title, font='Ariel 12 bold', bg='#4db8ff', fg='white').grid(row=0, column=0, pady=20, columnspan=2, padx=5)

            tk.Label(st, text='Nome: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=1, column=0, padx=5)
            tk.Label(st, text=self.Name_value.get(), font='Ariel 12', bg='#4db8ff', fg='white').grid(row=1, column=1, padx=5)
            
            tk.Label(st, text='Gols: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=2, column=0, padx=5)
            tk.Label(st, text=res[0][0], font='Ariel 12', bg='#4db8ff', fg='white').grid(row=2, column=1, padx=5)
            
            tk.Label(st, text='Assistências: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=3, column=0, padx=5)
            tk.Label(st, text=res[0][1], font='Ariel 12', bg='#4db8ff', fg='white').grid(row=3, column=1, padx=5)

            tk.Label(st, text='Cartões Amarelos: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=4, column=0, padx=5)
            tk.Label(st, text=res[0][2], font='Ariel 12', bg='#4db8ff', fg='white').grid(row=4, column=1, padx=5)

            tk.Label(st, text='Cartões Vermelhos: ', font='Ariel 12', bg='#4db8ff', fg='white').grid(row=5, column=0, padx=5)
            tk.Label(st, text=res[0][3], font='Ariel 12', bg='#4db8ff', fg='white').grid(row=5, column=1, padx=5)

            st.mainloop()
        else:
            messagebox.showwarning('Jogadores', 'Favor preencher todos os campos')

    def __init__(self):

        #janela de login
        self.root = tk.Tk()
        self.root.title('Jogadores')
        self.root.resizable(False, False)
        self.root.iconbitmap("futebol.ico")
        self.root.geometry('+350+30')
        self.root['bg'] = 'white'

        self.Position = tk.Label(self.root, text='Posição:', font='Ariel', fg='black', bg='white')
        self.Position.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Position_value = tk.StringVar(self.root, value="")
        self.Position_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Position_value)
        self.Position_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Name = tk.Label(self.root, text='Nome:', font='Ariel', fg='black', bg='white')
        self.Name.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Name_value)
        self.Name_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.subscription = tk.Label(self.root, text='Nº Inscrição:', font='Ariel', fg='black', bg='white')
        self.subscription.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.subscription_no_value = tk.StringVar(self.root, value="")
        self.subscription_no_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.subscription_no_value)
        self.subscription_no_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Age = tk.Label(self.root, text='Idade:', font='Ariel', fg='black', bg='white')
        self.Age.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Age_value = tk.StringVar(self.root, value="")
        self.Age_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Age_value)
        self.Age_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Height = tk.Label(self.root, text='Altura:', font='Ariel', fg='black', bg='white')
        self.Height.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Height_value = tk.StringVar(self.root, value="")
        self.Height_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Height_value)
        self.Height_entry.grid(row=4, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)     

        self.Weight = tk.Label(self.root, text='Peso:', font='Ariel', fg='black', bg='white')
        self.Weight.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Weight_value = tk.StringVar(self.root, value="")
        self.Weight_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Weight_value)
        self.Weight_entry.grid(row=5, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)            

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W+tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W+tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W+tk.E)

        self.statistics_club_button = ttk.Button(self.root, text='Estatísticas Gerais', cursor="hand2", command=self.playerMatch)
        self.statistics_club_button.grid(row=3, column=3, padx=9, sticky=tk.W+tk.E)

        self.statistics_player_button = ttk.Button(self.root, text='Estatísticas do Jogador', cursor="hand2", command=self.statistics)
        self.statistics_player_button.grid(row=4, column=3, padx=9, sticky=tk.W+tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse", column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
        self.tree.column("column1", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="ID")
        self.tree.column("column2", width=100, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Posição")
        self.tree.column("column3", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Nome")
        self.tree.column("column4", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="Nº de Inscrição")
        self.tree.column("column5", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Idade")
        self.tree.column("column6", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#6", text="Altura")
        self.tree.column("column7", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#7", text="Peso")
        self.tree.bind("<ButtonRelease-1>", self.selectItem)
        self.tree.bind("<space>", self.selectItem)
        self.tree.tag_configure('1', background='#d6d6c2')
        self.tree.tag_configure('2', background='#d6d6c2')
        self.tree.grid(row=7, column=0, padx=9, pady=9, sticky=tk.W+tk.E, columnspan=4)

        tk.Label(self.root, text='Pesquisar:', font='Ariel', fg='black', bg='white').grid(row=8, column=0, columnspan=2, sticky=tk.E, padx=9, pady=9)
        self.search_value = tk.StringVar(self.root, value="")
        tk.Entry(self.root, textvariable= self.search_value).grid(row=8, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.root, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=8, column=3, padx=9, sticky=tk.W+tk.E)   

        self.refresh_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.refresh)  
        self.refresh_button.grid(row=9, column=2, padx=9, pady=9, sticky=tk.W+tk.E)

        self.back_button = ttk.Button(self.root, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=9, column=3, padx=9, sticky=tk.W+tk.E)

        self.setup_db()
        self.root.mainloop()