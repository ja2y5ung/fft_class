import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure
from back import backend
import numpy as np
import matplotlib.pyplot as plt

class windowform1():
    num = 0
    combobox = 0
    window,window2,window3 = 0 ,0 ,0
    mainMenu,mainMenu2 = 0, 0
    fileMenu,fileMenu2 = 0, 0
    canvas = FigureCanvasTkAgg(plt.figure(), master = window)
    canvas2 = FigureCanvasTkAgg(plt.figure(), master = window2)
    label1 = 0
    work = 0
    button = 0

    def __init__(self):
        self.work = backend()
        
        self.window = tk.Tk()
        self.window.title('control')
        self.window.geometry("1800x900+50+50")
        self.window.resizable(False, False)
        self.mainMenu = tk.Menu(self.window)
        self.window.config(menu = self.mainMenu)
        self.fileMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "열기", command = self.open_file)
        self.fileMenu.add_command(label = "저장 하기", command = self.exit_file)
        self.fileMenu.add_command(label = "끝내기", command = self.exit_file)
        self.window.config(menu = self.mainMenu)
        self.fileMenu2 = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label = "기능", menu = self.fileMenu2)
        self.fileMenu2.add_command(label = "범위 선택", command = self.range_select)
        self.fileMenu2.add_command(label = "ㅇ", command = self.test)
        
        self.frame1=tkinter.Frame(self.window, width=300, height = 100, relief="solid", bd=1)
        self.frame1.pack(fill="both")
        self.frame2=tkinter.Frame(self.window)
        self.frame3=tkinter.Frame(self.window, width=1400, height = 50,relief="solid", bd=1)
        self.frame3.pack(side="right", fill="both", expand=True)
        self.text = tk.StringVar(self.frame1)
        self.text.set("file = None")
        self.text_label_input(self.frame1,self.text,10,0)
        self.window.mainloop()
        
    def open_file(self):
        self.filename = filedialog.askopenfilenames(initialdir = "E:/Images", title = "파일선택",
                                               filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        self.text.set("file = " + str(self.filename))
        self.work.loadFile(list(self.filename)[0])
        self.combobox(self.frame1)
        self.label_input(self.frame1,"< DC value >",250,30)
        self.dc = tk.StringVar(self.frame1)
        self.dc.set("0")

    def save_file(self,data):
        csvfile = open(r"graph_data.csv","w", newline= "")
        csvwrtier = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
        csvfile.close()

    def exit_file(self):
        self.window.quit()
        self.window.destroy()
            
    def exit_file2(self):
        self.window2.quit()
        self.window2.destroy()

    def text_label_input(self,window,text,Xloc,Yloc):
        label = tk.Label(window, textvariable = text)
        label.place(x=Xloc,y=Yloc)
        
    def combobox(self,window):
        values=[str(i)+ ' <' + str(self.work.row_name[i]) + '>'\
                for i in range(0, self.work.columnDataLength)] 
        self.combobox=tk.ttk.Combobox(window, height=15, values=values)
        self.combobox.set(0)
        self.combobox.place(x=10,y=60)
        self.label_input(self.frame1,"< Data select > ",50,30)
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)

    def callbackFunc(self,event):
        self.num = int(self.combobox.get().split(' ')[0])
        self.work.slctData(self.num)
        self.work.initData()

        self.work.getOrgn()
        self.draw_figure(self.canvas, self.work.fig, self.frame3,500,200)
        self.dc.set(self.work.dcData)
        self.text_label_input(self.frame1,str(self.dc),230,60)
    
    def draw_figure(self,canvas,fig,window,Xloc,Yloc):
        self.canvas_clear(canvas)
        self.canvas = FigureCanvasTkAgg(fig, master = window)
        self.canvas.get_tk_widget().place(x = Xloc,y = Yloc)
        
    def canvas_clear(self, canvas):
        canvas.get_tk_widget().forget()

    def widget_clear(self, widget):
        widget.pack_forget()
        
    def label_input(self,window,string,Xloc,Yloc):
        label = tk.Label(window, text = string)
        label.place(x = Xloc,y = Yloc)
                         
    def text_input(self,window,string,Xloc, Yloc):
        self.label_input(window,string,Xloc+35,Yloc-30)
        self.text_box = tk.Entry(window, width = 22)
        self.text_box.place(x=Xloc,y=Yloc)
        return self.text_box

    def button_input(self,window,string,cmnd,Xloc,Yloc):
        button = tk.Button(window, text = string,command = cmnd)
        button.place(x=Xloc,y=Yloc)

    def confirm(self):
        start_end_list = []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
        print(start_end_list)
        self.work.getIntrvl(start_end_list)
        self.window2 = tk.Tk()
        self.window2.geometry("800x800")
        self.window2.title(str(self.num)+" graph")
        self.draw_figure(self.canvas2,self.work.fig2,self.window2,100,100)

    def range_select(self):
        self.widget_clear(self.frame2)
        self.frame2=tkinter.Frame(self.window, width=300, height = 700,relief="solid", bd=1)
        self.frame2.pack(side="left", fill="both", expand=True)
        self.button_input(self.frame2,"확인",self.number_range,250,50)
        self.button_input(self.frame2,"리셋",self.range_select,300,50)
        self.text_input(self.frame2,"< number of range > ",80,50)

    def number_range(self):
        self.list1 = []
        for i in range(int(self.text_box.get())):
            self.a = self.text_input(self.frame2,"< " + str(i+1) + " range > ",80,150+(50*i))
            self.list1.append(self.a)
        self.button_input(self.frame2,"확인",self.confirm,250,150+(50*i))
    
    def test(self):
        self.widget_clear(self.frame2)
        self.frame2=tkinter.Frame(self.window, width=300, height = 700,relief="solid", bd=1)
        self.frame2.pack(side="left", fill="both", expand=True)
        self.button_input(self.frame2,"확인",self.confirm,250,50)
        self.text_input(self.frame2," < Test Button > ",80,50)

    
    
        
window1 = windowform1()
















