import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class View_employee:

    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()


    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("select * from Employees where Name like ? or CPF like ? or Role like ? or Age like ?", ('%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%', '%' + self.search_value.get() + '%'))
            self.result = self.theCursor.fetchall()

            length = str(len(self.result))
            if(length == 0):
                messagebox.showinfo('Funcionários', 'Não foi possível encontrar um resultado!')
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
        self.Role_entry.delete(0, "end")
        self.Name_entry.delete(0, "end")
        self.cpf_no_entry.delete(0, "end")
        self.Age_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.theCursor.execute("delete FROM Employees WHERE ID_employee=?", (self.curItem['values'][0],))
            print("DADOS DELETADOS")
        
        except:
            print('Não foi possível deletar estes dados!')
        
        finally:
            self.curItem=0
            self.clear_entries()
            self.update_tree()
            self.sqlite_var.commit()

    def update_record(self):
        if(self.Role_value.get() != "" and self.Name_value.get() != "" and self.cpf_no_value.get() != "" and self.Age_value.get() != ""):
            try:
                self.theCursor.execute("""UPDATE Employees SET Role = ?, Name = ?, CPF = ?, Age = ? WHERE ID_employee = ? """, 
                (self.Role_value.get(), self.Name_value.get(),  self.cpf_no_value.get(), self.Age_value.get(), self.curItem['values'][0]))
                self.clear_entries()
                print('Dados atualizados!')
            except sqlite3.IntegrityError:
                messagebox.showerror('Funcionários', 'Este funcionário já se encontra no banco de dados!')
            except:
                print('Não foi possível atualizar os dados!')
            finally:
                self.update_tree()
                self.sqlite_var.commit()
        else:
            messagebox.showwarning('Funcionários', 'Favor preencher todos os campos')

    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)

        self.Role_value.set(self.curItem['values'][1])
        self.Name_value.set(self.curItem['values'][2])
        self.cpf_no_value.set(self.curItem['values'][3])
        self.Age_value.set(self.curItem['values'][4])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT ID_employee, Role, Name, CPF, Age FROM Employees")
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
        if(self.Role_value.get() != "" and self.Name_value.get() != "" and self.cpf_no_value.get() != "" and self.Age_value.get() != ""):
            try:
                self.theCursor.execute("""INSERT INTO Employees (Role, Name, CPF, Age, ID_team) VALUES(?,?,?,?,?) """, 
                (self.Role_value.get(), self.Name_value.get(),  self.cpf_no_value.get(), self.Age_value.get(), 1))
                self.sqlite_var.commit()
                self.theCursor.execute("SELECT*, max(ID_employee) FROM Employees")
                self.rows = self.theCursor.fetchall()
                self.clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror('Funcionários', 'Este funcionário já se encontra no banco de dados!')
            except:
                print('Não foi possível cadastrar funcionário!')
            finally:
                self.update_tree()
        else:
            messagebox.showwarning('Funcionários', 'Favor preencher todos os campos')
        
    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('Soccer Team.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print('Não foi possível conectar ao banco de dados!')
            
        try:
            self.theCursor.execute("CREATE TABLE if not exists Employees(ID_employee INTEGER PRIMARY KEY AUTOINCREMENT, Role TEXT NOT NULL, Name TEXT NOT NULL ,CPF TEXT UNIQUE NOT NULL, Age INTEGER NOT NULL, ID_team INTEGER NOT NULL, FOREIGN KEY (ID_team) REFERENCES Team (ID_team));")
        except:
            print('Não foi possível criar a tabela!')
        finally:
            self.sqlite_var.commit()
            self.update_tree()
    
    def back(self):
        self.root.destroy()

    def __init__(self):

        #janela de login
        self.root = tk.Tk()
        self.root.title('Funcionários')
        self.root.resizable(False, False)
        self.root.iconbitmap("futebol.ico")
        self.root.geometry('+350+30')
        self.root['bg'] = 'white'

        self.Role = tk.Label(self.root, text='Cargo:', font='Ariel', fg='black', bg='white')
        self.Role.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Role_value = tk.StringVar(self.root, value="")
        self.Role_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Role_value)
        self.Role_entry.grid(row=0, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Name = tk.Label(self.root, text='Nome:', font='Ariel', fg='black', bg='white')
        self.Name.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Name_value = tk.StringVar(self.root, value="")
        self.Name_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Name_value)
        self.Name_entry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.cpf = tk.Label(self.root, text='CPF:', font='Ariel', fg='black', bg='white')
        self.cpf.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.cpf_no_value = tk.StringVar(self.root, value="")
        self.cpf_no_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.cpf_no_value)
        self.cpf_no_entry.grid(row=2, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)

        self.Age = tk.Label(self.root, text='Idade:', font='Ariel', fg='black', bg='white')
        self.Age.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.Age_value = tk.StringVar(self.root, value="")
        self.Age_entry = ttk.Entry(self.root, font='Ariel, 10', textvariable=self.Age_value)
        self.Age_entry.grid(row=3, column=1, sticky=tk.W + tk.E, columnspan=2, padx=10, pady=10)     

        self.submit_button = ttk.Button(self.root, text='Cadastrar', cursor="hand2", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=tk.W+tk.E)

        self.update_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=tk.W+tk.E)

        self.delete_button = ttk.Button(self.root, text='Deletar', cursor="hand2", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=tk.W+tk.E)

        self.tree = ttk.Treeview(self.root, selectmode="browse", column=("column1", "column2", "column3", "column4", "column5"), show='headings')
        self.tree.column("column1", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#1", text="ID")
        self.tree.column("column2", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#2", text="Cargo")
        self.tree.column("column3", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#3", text="Nome")
        self.tree.column("column4", width=180, minwidth=100, stretch=tk.NO)
        self.tree.heading("#4", text="CPF")
        self.tree.column("column5", width=50, minwidth=100, stretch=tk.NO)
        self.tree.heading("#5", text="Idade")
        self.tree.bind("<ButtonRelease-1>", self.selectItem)
        self.tree.bind("<space>", self.selectItem)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='ivory2')
        self.tree.grid(row=4, column=0, padx=9, pady=9, sticky=tk.W+tk.E, columnspan=4)

        tk.Label(self.root, text='Pesquisar:', font='Ariel', fg='black', bg='white').grid(row=5, column=0, columnspan=2, sticky=tk.E, padx=9, pady=9)
        self.search_value = tk.StringVar(self.root, value="")
        tk.Entry(self.root, textvariable= self.search_value).grid(row=5, column=2, sticky=tk.W + tk.E, padx=9, pady=9)

        self.search_button = ttk.Button(self.root, text='Pesquisar', cursor="hand2", command=self.search_record)
        self.search_button.grid(row=5, column=3, padx=9, sticky=tk.W+tk.E)   

        self.refresh_button = ttk.Button(self.root, text='Atualizar', cursor="hand2", command=self.refresh)  
        self.refresh_button.grid(row=6, column=2, padx=9, pady=9, sticky=tk.W+tk.E)

        self.back_button = ttk.Button(self.root, text='Voltar', cursor="hand2", command=self.back)
        self.back_button.grid(row=6, column=3, padx=9, sticky=tk.W+tk.E)

        self.setup_db()
        self.root.mainloop()
