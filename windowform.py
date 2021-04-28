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
##        self.window.resizable(False, False)
        self.mainMenu = tk.Menu(self.window)
        
        self.window.config(menu = self.mainMenu)
        self.fileMenu = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "열기", command = self.open_file)
        self.fileMenu.add_command(label = "저장 하기", command = self.exit_file)
        self.fileMenu.add_command(label = "끝내기", command = self.exit_file)
        
        self.fileMenu2 = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label = "기능", menu = self.fileMenu2)
        self.fileMenu2.add_command(label = "범위 선택", command = self.range_select,state = "disable")
        self.fileMenu2.add_command(label = "선별", command = self.range_choice, state = "disable")
        self.fileMenu2.add_command(label = "Test Button", command = self.test2, state = "disable")
        
        self.frame1=tkinter.Frame(self.window, width=300, height = 100, relief="solid", bd=1)
        self.frame1.pack(side="top",fill="both")
        self.frame2=tkinter.Frame(self.window, width=300, height = 350,relief="solid", bd=1)
        self.frame2.pack(side="left", anchor = "nw",fill='both', expand=True)
        self.frame3=tkinter.Frame(self.window, width=1400, height = 50,relief="solid", bd=1)
        self.frame3.pack(side="right", fill="both", expand=True)
        self.frame4=tkinter.Frame(self.window)
        self.frame5=tkinter.Frame(self.window)
        self.frame6=tkinter.Frame(self.window)
        
        
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
        self.widget_clear(self.frame3)
        self.frame3=tkinter.Frame(self.window, width=1400, height = 50,relief="solid", bd=1)
        self.frame3.pack(side="right", fill="both", expand=True)
        self.draw_figure(self.canvas, self.work.fig, self.frame3,50,150)
        self.dc.set(self.work.dcData)
        self.text_label_input(self.frame1,str(self.dc),230,60)
        self.fileMenu2.entryconfig(1,state = "normal")
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.fileMenu2.entryconfig(2,state = "disable")
    
    def draw_figure(self,canvas,fig,window,Xloc,Yloc):
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

    def confirm1(self):
        start_end_list = []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
        print(start_end_list)
        self.work.getIntrvl(start_end_list)
        self.work.synthetic()
        self.draw_figure(self.frame3, self.work.fig2, self.frame3, 50,150)
        self.draw_figure(self.frame3, self.work.fig3, self.frame3, 750,150)
        self.fileMenu2.entryconfig(2,state = "normal")
        
    def confirm2(self):
        a = int(self.text_box.get())
        self.work.slctBySize(a)
        self.draw_figure(self.canvas, self.work.fig3, self.frame3,50,150)
        
        self.window2 = tk.Tk()
        self.window2.title('control')
        self.window2.geometry("800x800+50+50")
        self.draw_figure(self.canvas, self.work.fig4, self.window2,50,150)
        
    def range_select(self):
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.fileMenu2.entryconfig(2,state = "disable")
        self.frame4=tkinter.Frame(self.frame2, width=300, height = 350,relief="solid", bd=1)
        self.frame4.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame4,"확인",self.number_range,250,50)
        self.button_input(self.frame4,"리셋",self.range_select,40,50)
        self.text_input(self.frame4,"< number of range > ",80,50)

    def number_range(self):
        self.list1 = []
        for i in range(int(self.text_box.get())):
            self.a = self.text_input(self.frame4,"< " + str(i+1) + " range > ",80,150+(50*i))
            self.list1.append(self.a)
        self.button_input(self.frame4,"확인",self.confirm1,250,150+(50*i))
    
    def range_choice(self):
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.frame5=tkinter.Frame(self.frame2, width=300, height = 80,relief="solid", bd=1)
        self.frame5.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame5,"확인",self.confirm2,250,50)
        self.text_input(self.frame5," < Number of selection > ",80,50)
        

    def test2(self):
        self.widget_clear(self.frame6)
        self.frame6=tkinter.Frame(self.frame2, width=300, height = 80,relief="solid", bd=1)
        self.frame6.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame6,"확인",self.confirm,250,50)
        self.text_input(self.frame6," < Test Button > ",80,50)


window1 = windowform1()
















