import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from back import backend
import numpy as np
import matplotlib.pyplot as plt


class windowform1():
    num = 0
    combobox = 0
    window,window2,window3 = 0 ,0 ,0
    mainMenu = 0
    fileMenu = 0
    canvas,canvas2 = 0, 0
    label1 = 0
    work = 0
    button = 0
    
    def __init__(self):
        self.work = backend()
        
        self.window = tk.Tk()
        self.window.title('control')
        self.window.geometry("600x600+200+100")
        self.window.resizable(False, False)
        self.mainMenu = tk.Menu(self.window)
        self.window.config(menu = self.mainMenu)
        self.fileMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "열기", command = self.open_file)
        self.text = tk.StringVar()
        self.text.set("None")
        self.file_name_label()       

    def open_file(self):
        self.filename = filedialog.askopenfilenames(initialdir = "E:/Images", title = "파일선택",
                                               filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        self.text.set(self.filename)
        self.combobox()

    def file_name_label(self):
        self.label1 = tk.Label(self.window, textvariable = self.text)
        self.label1.pack()
        
    def combobox(self):
        
        values=[str(i)+ "" for i in range(0, self.work.columnDataLength)] 
        self.combobox=tk.ttk.Combobox(self.window, height=15, values=values)
        self.combobox.set(0)
        self.combobox.pack(padx = 1, pady = 20)
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)

    def callbackFunc(self,event):
        self.num = int(self.combobox.get())
        self.work.run(self.num)
        self.window2 = tk.Tk()
        self.window2.geometry("1500x800")
        self.window2.title(str(self.num)+" graph")
        self.text_input(self.window2)
        self.button_input(self.window2)
        self.draw_figure(self.canvas, self.work.fig, self.window2)
        

    def draw_figure(self,canvas,fig,window):
        self.canvas = FigureCanvasTkAgg(fig, master = window)
        self.canvas.get_tk_widget().pack(expand = 1)

    def text_input(self,window):
        self.text_box = tk.Entry(window, width = 30)
        self.text_box.pack(expand = 1)

    def button_input(self,window):
        self.button = tk.Button(window, text = "확인",command = self.confirm)
        self.button.pack(expand = 1)

    def confirm(self):
        start_end_list = list(map(int, self.text_box.get().split(',')))
        print(start_end_list)
        self.work.run(self.num,start_end_list[0],start_end_list[1],\
                      start_end_list[2],start_end_list[3])

        self.window3 = tk.Tk()
        self.window3.geometry("1500x800")
        self.window3.title(str(self.num)+" graph")
        self.draw_figure(self.canvas2, self.work.fig2, self.window3)
       
    def main_loop(self):
        self.window.mainloop()


window1 = windowform1()
window1.main_loop()















