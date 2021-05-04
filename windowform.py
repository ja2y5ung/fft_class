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
    label1,label2,label3,label4,label5,label6,label7 = 0,0,0,0,0,0,0
    buttonframe,buttonframe2 = 0,0
    canvasframe = 0
    work = 0
    button = 0

    def __init__(self):
        self.work = backend()
        
        self.window = tk.Tk()
        self.window.title('control')
        self.window.geometry("900x900+50+50")
        self.window.resizable(True, True)
        self.mainMenu = tk.Menu(self.window)
        
        self.window.config(menu = self.mainMenu)
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "열기", command = self.open_file)
        self.fileMenu.add_command(label = "저장 하기", command = self.exit_file)
        self.fileMenu.add_command(label = "끝내기", command = self.exit_file)
        
        self.fileMenu2 = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label = "기능", menu = self.fileMenu2)
        self.fileMenu2.add_command(label = "범위 선택", command = self.range_select,state = "disable")
        self.fileMenu2.add_command(label = "Test Button", command = self.test2, state = "disable")

        #파일
        self.topframe = tkinter.Frame(self.window, width=300, height = 100, relief="solid", bd=1)
        self.topframe.pack(side="top",fill="x")
        self.frame1=tkinter.Frame(self.topframe, width=300, height = 100)
        self.frame1.pack(side="left",anchor = "nw",fill="x")
        #기능
        self.frame2=tkinter.Frame(self.window, width=300, height = 350,relief="solid", bd=1)
        #그래프
        self.frame3=tkinter.Frame(self.window, width=1400, height = 50,relief="solid", bd=1)
        self.frame3.pack(side="right", fill="both", expand=True)
        self.canvasframe = tkinter.Frame(self.window)
        #범위 설정
        self.frame4=tkinter.Frame(self.window)
        #범위 갯수 입력
        self.frame5=tkinter.Frame(self.window)
        self.frame6=tkinter.Frame(self.window)
        #상태 표시 프레임
        self.frame7=tkinter.Frame(self.topframe, width=300, height = 100)
        self.frame7.pack(side="left",fill="x")
        
        self.text = tk.StringVar(self.frame1)
        self.text.set("file = 파일을 열어주세요.")
        self.text_label_input(self.frame1,self.label1,self.text)
        self.window.mainloop()
        
    def open_file(self):
        
        self.filename = filedialog.askopenfilenames(initialdir = "E:/Images", title = "파일선택",
                                               filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        self.text.set("file = " + str(self.filename))
        self.work.loadFile(list(self.filename)[0])
        self.combobox(self.frame1)
        self.label_input(self.frame7,self.label5,"< DC value >")
        self.dc = tk.StringVar(self.frame1)
        self.dc.set("0")
        self.text_label_input(self.frame7,self.label2,str(self.dc))
        self.fileMenu.entryconfig(0,state = "disable")
        
    def save_file(self):
        csvfile = open(r"graph_data.csv","w", newline= "")
        csvwrtier = csv.writer(csvfile)
        for row in self.work.orgnlData:
            csvwriter.writerow(row)
        csvfile.close()

    def exit_file(self):
        self.window.quit()
        self.window.destroy()
            
    def exit_file2(self):
        self.window2.quit()
        self.window2.destroy()

    def text_label_input(self,window,label,text):
        label = tk.Label(window, textvariable = text)
        label.pack()
        
    def combobox(self,window):
        values=[str(i)+ ' <' + str(self.work.row_name[i]) + '>'\
                for i in range(0, self.work.columnDataLength)] 
        self.combobox=tk.ttk.Combobox(window, height=15, values=values)
        self.label_input(self.frame1,self.label4,"< Data select > ")
        self.combobox.set("데이터를 선택 해주세요")
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.label_input(self.frame1,self.label4,"  ")

    def callbackFunc(self,event):
        self.num = int(self.combobox.get().split(' ')[0])
        self.work.slctData(self.num)
        self.work.initData()
        self.work.getOrgn()
        self.widget_clear(self.canvasframe)
        self.widget_clear(self.frame2)
        self.canvasframe=tkinter.Frame(self.frame3,  height = 50)
        self.canvasframe.pack(expand=True)
        self.draw_figure(self.canvas, self.work.fig, self.canvasframe)
        self.dc.set(self.work.dcData)
        self.fileMenu2.entryconfig(0,state = "normal")
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.fileMenu2.entryconfig(1,state = "disable")
    
    def draw_figure(self,canvas,fig,window):
        self.canvas = FigureCanvasTkAgg(fig, master = window)
        self.canvas.get_tk_widget().pack( expand=True)
        
    def canvas_clear(self, canvas):
        canvas.get_tk_widget().forget()

    def widget_clear(self, widget):
        widget.pack_forget()
        
    def label_input(self,window,label,string):
        label = tk.Label(window, text = string)
        label.pack()
        
    def text_input(self, window,label, string):
        self.label_input(window, label, string)
        self.text_box = tk.Entry(window, width = 22)
        self.text_box.pack()
        return self.text_box

    def button_input(self,window,string,cmnd,wid,loc):
        button = tk.Button(window, width = wid,text = string,command = cmnd)
        button.pack(side=loc)

    def confirm1(self):
        start_end_list = []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
        self.work.getIntrvl(start_end_list)
        self.work.synthetic()
        self.draw_figure(self.frame3, self.work.fig2, self.frame3, 50,150)
        self.draw_figure(self.frame3, self.work.fig3, self.frame3, 750,150)
        self.fileMenu2.entryconfig(2,state = "normal")
        
    def range_select(self):
        self.count = 0
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.frame2.pack(side="left", anchor = "nw",fill='both')
        self.fileMenu2.entryconfig(2,state = "disable")
        self.frame4=tkinter.Frame(self.frame2, width=300, height = 350, relief="solid", bd=1)
        self.frame4.pack(side="top",expand = True)
        self.frame5=tkinter.Frame(self.frame4, width=300, height = 150, relief="solid", bd=1)
        self.frame5.pack(side="top",fill = 'x')
        self.text_input(self.frame5,self.label3,"< 범위 갯수 입력 (1이상 정수만 입력) > ")
        self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
        self.buttonframe.pack(side="bottom")        
        self.button_input(self.buttonframe,"입   력",self.number_range,10,"left")
        
    def number_range(self):
        a = self.text_box.get()
        if self.text_box.get() != '' and self.count == 0 and int(self.text_box.get()) > 0:
            self.list1 = []
            print(type(a))
            self.frame6=tkinter.Frame(self.frame4, width=300, height = 350, relief="solid", bd=1)
            self.frame6.pack(side="top",fill = 'x')
            for i in range(int(self.text_box.get())):
                self.a = self.text_input(self.frame6,self.label6,"< " + chr(i+65) + " range > ")
                self.list1.append(self.a)
            self.label_input(self.frame6,self.label7,"● 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.")           
            self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
            self.buttonframe2.pack(side="bottom")  
            self.button_input(self.buttonframe2,"입   력",self.confirm1,10,"left")
            self.widget_clear(self.buttonframe)
            self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
            self.buttonframe.pack(side="bottom")              
            self.button_input(self.buttonframe,"갯수 리셋",self.range_select,10,"left")
            self.count += 1
        else:
            pass
        
    def test2(self):
        self.widget_clear(self.frame6)
        self.frame6=tkinter.Frame(self.frame2, width=300, height = 80,relief="solid", bd=1)
        self.frame6.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame6,"확인",self.confirm,250,50,5)
        self.text_input(self.frame6," < Test Button > ",80,50)


window1 = windowform1()
















