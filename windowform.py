import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure
from back import backend
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class windowform1():
    num = 0
    combobox = 0
    window,window2,window3 = 0 ,0 ,0
    mainMenu,mainMenu2 = 0, 0
    fileMenu,fileMenu2 = 0, 0
    canvas = FigureCanvasTkAgg(plt.figure(), master = window)
    canvas2 = FigureCanvasTkAgg(plt.figure(), master = window2)
    label1,label2,label3,label4,label5,label6,label7 = 0,0,0,0,0,0,0
    sample_label = 0
    buttonframe,buttonframe2 = 0,0
    sampleframe = 0
    rng_exp_frame1, rng_exp_frame2, rng_exp_frame3 = 0,0,0
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
        self.fileMenu.add_command(label = "저장 하기", command = self.save_file, state = "disable")
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
        #dc 상태 프레임
        self.dcframe=tkinter.Frame(self.frame7, width=300, height = 100)
        self.dcframe.pack(side="left")
        #sampling rate 상태 프레임
        self.srframe=tkinter.Frame(self.frame7, width=300, height = 100)
        self.srframe.pack(side="left")
        #error 상태 프레임
        self.errframe=tkinter.Frame(self.frame7, width=300, height = 100)
        self.errframe.pack(side="left")
        #샘플 선택 프레임
        self.sampleframe=tkinter.Frame(self.topframe, width=300, height = 100)

        self.buttonframe2=tkinter.Frame(self.topframe, width=300, height = 100)
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
        
        self.label_input(self.dcframe,self.label5,"< DC value >","top")
        self.label_input(self.srframe,self.label5,"< sampling rate >","top")
        self.label_input(self.errframe,self.label5,"< error >","top")
        
        
        self.dc = tk.StringVar(self.frame1)
        self.dc.set("0")
        self.sr = tk.StringVar(self.frame1)
        self.sr.set("0")
        self.er = tk.StringVar(self.frame1)
        self.er.set("None")
        
        self.text_label_input(self.dcframe,self.label2,str(self.dc))
        self.text_label_input(self.srframe,self.label2,str(self.sr))
        self.text_label_input(self.errframe,self.label2,str(self.er))
        
        self.fileMenu.entryconfig(0,state = "disable")
        
    def save_file(self):
        self.Y = self.work.saveSgnl()

        self.YFrame = pd.DataFrame(self.Y, columns = ['genSgnl'])
        self.filename2 = filedialog.asksaveasfilename(initialdir = "E:/Images", title = "경로 선택",
                                               filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        self.YFrame.to_csv(str(self.filename2),index=False)

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
        self.label_input(self.frame1,self.label4,"< Data select > ","top")
        self.combobox.set("데이터를 선택 해주세요")
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.label_input(self.frame1,self.label4,"  ","top")

    def callbackFunc(self,event):
        self.num = int(self.combobox.get().split(' ')[0])
        self.work.slctData(self.num)
        self.work.initData()
        self.work.getOrgn()
        self.widget_clear(self.canvasframe)
        self.widget_clear(self.frame2)
        self.canvasframe=tkinter.Frame(self.frame3,  height = 50)
        self.canvasframe.pack(expand=True)
        self.draw_figure(self.canvas, self.work.fig1, self.canvasframe)
        self.dc.set(self.work.dcData)
        self.sr.set(self.work.f)
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
        
    def label_input(self,window,label,string,loc):
        label = tk.Label(window, text = string)
        label.pack(side = loc,expand=True)
        
    def text_input(self, window,label, string,wid,loc1,loc2):
        self.label_input(window, label, string,loc2)
        text_box = tk.Entry(window, width = wid)
        text_box.pack(side = loc1)
        return text_box
    
    def text_input2(self, window,window2,label, string,wid,loc1,loc2):
        self.label_input(window, label, string,loc2)
        text_box = tk.Entry(window2, width = wid)
        text_box.pack(side = loc1)
        return text_box
    
    def button_input(self,window,string,cmnd,wid,loc):
        button = tk.Button(window, width = wid,text = string,command = cmnd)
        button.pack(side=loc)

    def confirm1(self):
        start_end_list,exp_list = [], []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
        for textbox2 in self.list3:
            exp_list.append(float(textbox2.get()))
        self.work.getIntrvl(start_end_list,exp_list)
        self.fileMenu2.entryconfig(2,state = "normal")
        
    def number_range(self):
        self.widget_clear(self.sampleframe)
        self.widget_clear(self.buttonframe2)
        self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
        self.buttonframe2.pack(side="bottom")  
        self.button_input(self.buttonframe2,"입   력",self.confirm1,10,"left")        
        a = self.text_box.get()
        if self.text_box.get() != '' and self.count == 0 and int(self.text_box.get()) > 0:
            self.list1,self.list2,self.list3 = [], [], []
            self.frame6=tkinter.Frame(self.frame4, width=300, height = 350, relief="solid", bd=1)
            self.frame6.pack(side="top",fill = 'x')
            for i in range(int(self.text_box.get())):
                rng_exp_frame=tkinter.Frame(self.frame6, width=300, height = 350)
                self.list2.append(rng_exp_frame)
            for j in range(int(self.text_box.get())):
                self.label_input(self.frame6,self.label6,"< " + chr(j+65) + " range > ","top")
                rng_box = self.text_input2(self.list2[j], self.list2[j], self.label6," 범위 : ",10,"left","left")
                exp_box = self.text_input2(self.list2[j], self.list2[j], self.label6," 확대 비율 : ",3,"left","left")
                self.list3.append(exp_box)
                self.list2[j].pack(side="top",fill = 'x')
                self.list1.append(rng_box)
                
            self.label_input(self.frame6,self.label7,"● 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.","top")
            self.label_input(self.frame6,self.label7,"● 0~" + str(self.work.lngthData) +" 사이로 입력해주세요.","top")
            self.widget_clear(self.buttonframe)
            self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
            self.buttonframe2.pack(side="bottom")  
            self.button_input(self.buttonframe2,"입   력",self.confirm1,10,"left")             
            self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
            self.buttonframe.pack(side="bottom")              
            self.button_input(self.buttonframe,"갯수 리셋",self.range_select,10,"left")
            self.count += 1
        else:
            pass
        
    def range_select(self):
        self.count = 0
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.frame2.pack(side="left", anchor = "nw",fill='both')
        self.fileMenu2.entryconfig(2,state = "disable")
        self.frame4=tkinter.Frame(self.frame2, width=300, height = 350)
        self.frame4.pack(side="top",expand = True)
        self.frame5=tkinter.Frame(self.frame4, width=300, height = 150)
        self.frame5.pack(side="top",fill = 'x')
        self.text_box = self.text_input(self.frame5,self.label3,"< 범위 갯수 입력 (1이상 정수만 입력) > ",10,"top","top")
        self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
        self.buttonframe.pack(side="bottom")        
        self.button_input(self.buttonframe,"입   력",self.number_range,10,"left")

    def confirm1(self):     
        start_end_list,exp_list = [], []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
        for textbox2 in self.list3:
            exp_list.append(float(textbox2.get()))
        self.work.getIntrvl(start_end_list,exp_list)
        self.fileMenu2.entryconfig(2,state = "normal")
        self.sampleframe = tkinter.Frame(self.frame4, width=300, height = 150, relief="solid", bd=1)
        self.sampleframe.pack(side = "top",fill = 'x')
        self.sample_box = self.text_input(self.sampleframe, self.sample_label, "샘플 갯수 입력",10,"top","top")
        self.button_input(self.sampleframe,"입   력",self.sample_choice,10,"bottom")        
        self.widget_clear(self.buttonframe2)
        self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
        self.buttonframe2.pack(side="bottom")        
        self.button_input(self.buttonframe2,"범위 리셋",self.number_range,10,"left")
        
    def sample_choice(self):
        self.work.genSgnl(int(self.sample_box.get()))
        self.er.set(self.work.error)
        self.fileMenu.entryconfig(1,state = "normal")
        
    def test2(self):
        self.widget_clear(self.frame6)
        self.frame6=tkinter.Frame(self.frame2, width=300, height = 80,relief="solid", bd=1)
        self.frame6.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame6,"확인",self.confirm,250,50,5)
        self.text_input(self.frame6," < Test Button > ",80,50)


window1 = windowform1()
















