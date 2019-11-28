import tkinter as tk
from menu import Main_Window

class First_Window():

    def mainwindow(self):
        self.root.destroy()
        Main_Window()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Soccer Manager')
        self.root['bg'] = '#4db8ff'
        self.root.geometry('600x600+350+30')
        self.root.iconbitmap("futebol.ico")

        tk.Label(self.root, text='Soccer Manager', font='Avalon 30', bg='#4db8ff', fg='white').place(x=165, y=200)
        tk.Label(self.root, text='Gerencie sua equipe', font='Arial 15', fg='white', bg='#4db8ff').place(x=215, y=280)

        tk.Button(self.root, width=10, text='Entrar', fg='white', bg='#4db8ff', font='Avalon 13', bd=2, relief='ridge', cursor="hand2", command=self.mainwindow).place(x=258, y=350)


        self.root.mainloop()

try:
    First_Window()
except:
    print('Não foi possível abrir a janela!')