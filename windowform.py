import tkinter as tk
import tkinter.ttk
import tkinter.font
from tkinter import *
from tkinter import filedialog
from ttkwidgets.frames import ScrolledFrame
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.figure import Figure
from back2 import fuckMe
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pdb

class windowform1():
    num = 0
    combobox = 0
    window,window2,window3 = 0 ,0 ,0
    mainMenu,mainMenu2 = 0, 0
    fileMenu,fileMenu2 = 0, 0
##    canvas = FigureCanvasTkAgg(plt.figure(), master = window)
    label1,label2,label3,label4,label5,label6,label7,label8 = 0,0,0,0,0,0,0,0
    sample_label = 0
    buttonframe,buttonframe2 = 0,0
    sampleframe = 0
    rng_exp_frame1, rng_exp_frame2, rng_exp_frame3 = 0,0,0
    canvasframe = 0
    work = 0
    button = 0

    def __init__(self):
        self.work = fuckMe()
        
        self.window = tk.Tk()
        self.window.title('control')
        self.window.geometry("600x900+50+50")
        self.window.resizable(True, True)
        self.mainMenu = tk.Menu(self.window)

        self.choice = IntVar()
        
        self.window.config(menu = self.mainMenu)
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label = "파일", menu = self.fileMenu)
        self.fileMenu.add_command(label = "열기", command = self.open_file)
        self.fileMenu.add_command(label = "저장 하기", command = self.save_file, state = "disable")
        self.fileMenu.add_command(label = "끝내기", command = self.exit_file)
        
        self.fileMenu2 = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label = "기능", menu = self.fileMenu2)
        self.fileMenu2.add_command(label = "예측 신호 생성", command = self.range_select,state = "disable")
##        self.fileMenu2.add_command(label = "Test Button", command = self.test2, state = "disable")


        #에러 상태 프레임
        self.error_messageframe = tkinter.Frame(self.window, width=300, height = 50, relief="solid", bd=1)
        self.error_messageframe.pack(side="top",fill="x")
        #파일
        self.topframe = tkinter.Frame(self.window, width=300, height = 100, relief="solid", bd=1)
        self.topframe.pack(side="top",fill="x")
        self.frame1=tkinter.Frame(self.topframe, width=300, height = 100)
        self.frame1.pack(side="left",anchor = "nw",fill="x")
        #기능
        self.scrollframe1 = ScrolledFrame(self.window, compound=tk.RIGHT, canvasheight=700)
        self.scrollframe1.pack(side = "left",fill='y', expand=True)
        
        #그래프
        self.scrollframe2 = ScrolledFrame(self.window, compound=tk.RIGHT, canvasheight=700)
        self.scrollframe2.pack(side = "right",fill='y', expand=True)

        #범위 설정
        self.frame4=tkinter.Frame(self.window)
        #범위 갯수 입력
        self.frame5=tkinter.Frame(self.window)
        self.frame6=tkinter.Frame(self.window)
        #hz 범위 갯수 프레임
        self.hzrangeSlctframe = tkinter.Frame(self.topframe, width=300, height = 100)
        #hz 범위 입력 프레임
        self.hzSlctframe=tkinter.Frame(self.window)
        #상태 표시 프레임
        self.frame7=tkinter.Frame(self.topframe, width=300, height = 100)
        self.frame7.pack(side="left",fill="x")
        #dc 상태 프레임
        self.dcframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.dcframe.pack(side="top")
        #dc 상태 프레임
        self.inpdcframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.inpdcframe.pack(side="top")        
        #sampling rate 상태 프레임
        self.srframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.srframe.pack(side="top")
        #error 상태 프레임
        self.errframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.errframe.pack(side="top")
        #sample 갯수 프레임
        self.spframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.spframe.pack(side="top")
        #frequancy 프레임
        self.freframe=tkinter.Frame(self.scrollframe2.interior, width=300, height = 100)
        self.freframe.pack(side="top")        
        #샘플 선택 프레임
        self.sampleframe=tkinter.Frame(self.topframe, width=300, height = 100)
        #샘플 범위 프레임
        self.sample_rg_frame=tkinter.Frame(self.topframe, width=300, height = 100)
        #샘플 범위 갯수 프레임
        self.nb_sample_rg_frame=tkinter.Frame(self.topframe, width=300, height = 100)
        #버튼 프레임
        self.buttonframe2=tkinter.Frame(self.topframe, width=300, height = 100)
        self.buttonframe3=tkinter.Frame(self.topframe, width=300, height = 100)
        #에러 그래프 프레임
        self.errorgrframe = tkinter.Frame(self.topframe, width=300, height = 100)
        #frame4 스크롤 프레임
        self.scrollframe =  ScrolledFrame(self.frame4, compound=tk.RIGHT)
        #빈 프레임
        self.empty_frame=tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        self.empty_frame2=tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        self.empty_frame3=tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        self.empty_frame4=tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        self.empty_frame5=tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        
        self.hzrempty_frame = tkinter.Frame(self.scrollframe.interior, width=300, height = 100)
        #text바
        self.text = tk.StringVar(self.frame1)
        self.text.set("file = 파일을 열어주세요.")
        self.text_label_input(self.frame1,self.label1,self.text)

        self.error_message = tk.StringVar(self.error_messageframe)
        self.error_message.set(" ")
        self.text_label_input(self.error_messageframe,self.label1,self.error_message,12)

        self.window.mainloop()
        
    def open_file(self):
        
        self.filename = filedialog.askopenfilenames(initialdir = "E:/Images", title = "파일선택",
                                               filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        self.text.set("file = " + str(self.filename))
        self.work.loadFile(list(self.filename)[0])
        self.combobox(self.frame1)
        
        self.label_input(self.dcframe,self.label5,"< DC value >","top")
        self.label_input(self.inpdcframe,self.label5,"< Input DC value >","top")
        self.label_input(self.srframe,self.label5,"< sampling rate >","top")
        self.label_input(self.errframe,self.label5,"< error >","top")
        self.label_input(self.spframe,self.label5,"< number of sample >","top")
        self.label_input(self.freframe,self.label5,"< frequancy resolution >","top")
        
        self.dc = tk.StringVar(self.frame1)
        self.dc.set("0")
        self.ipdc = tk.StringVar(self.frame1)
        self.ipdc.set("0")
        self.sr = tk.StringVar(self.frame1)
        self.sr.set("0")
        self.er = tk.StringVar(self.frame1)
        self.er.set("None")
        self.sp = tk.StringVar(self.frame1)
        self.sp.set("0")
        self.fr = tk.StringVar(self.frame1)
        self.fr.set("0")

        
        self.text_label_input(self.dcframe,self.label2,str(self.dc))
        self.text_label_input(self.dcframe,self.label2," ")
        self.text_label_input(self.inpdcframe,self.label2,str(self.ipdc))
        self.text_label_input(self.inpdcframe,self.label2," ")
        self.text_label_input(self.srframe,self.label2,str(self.sr))
        self.text_label_input(self.srframe,self.label2," ")
        self.text_label_input(self.errframe,self.label2,str(self.er))
        self.text_label_input(self.errframe,self.label2," ")
        self.text_label_input(self.spframe,self.label2,str(self.sp))
        self.text_label_input(self.spframe,self.label2," ")
        self.text_label_input(self.freframe,self.label2, str(self.fr))
        self.text_label_input(self.freframe,self.label2," ")        

                

        self.fileMenu.entryconfig(0,state = "disable")
        
    def save_file(self):

        self.filename2 = filedialog.asksaveasfilename(initialdir = "E:/Images", title = "경로 선택",
                                               filetypes = (("txt files", "*.txt"), ("all files", "*.*")))
        self.work.saveFile(self.filename2)

    def exit_file(self):
        self.window.quit()
        self.window.destroy()
            
    def exit_file2(self):
        self.window2.quit()
        self.window2.destroy()

    def text_label_input(self,window,label,text,fsize = 10):
        fnt = tk.font.Font(size = fsize)
        label = tk.Label(window, textvariable = text,font = fnt)
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
        self.work.slctData([self.num])
        self.work.initData()
        self.work.showData()
<<<<<<< HEAD
        self.widget_clear(self.frame2)
=======
        self.widget_clear(self.scrollframe1)
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb

        self.dc.set(self.work.mean)
        self.ipdc.set(self.work.inptDC)
        self.sr.set(self.work.Fs)
        self.sp.set(self.work.lngth)
        self.fr.set(self.work.Fr)
        self.fileMenu2.entryconfig(0,state = "normal")
        self.widget_clear(self.frame4)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
##        self.fileMenu2.entryconfig(1,state = "disable")
    
<<<<<<< HEAD
        
    def canvas_clear(self, canvas):
        canvas.get_tk_widget().forget()
=======
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb

    def widget_clear(self, widget):
        widget.pack_forget()
        
    def label_input(self,window,label,string,loc):
        label = tk.Label(window, text = string)
        label.pack(side = loc)
        
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
<<<<<<< HEAD
=======
        self.error_message.set(self.work.errMsg)
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
##        self.fileMenu2.entryconfig(2,state = "normal")
            
    def range_select(self):
        self.count = 0
        self.widget_clear(self.scrollframe)
        self.widget_clear(self.frame5)
        self.widget_clear(self.frame6)
        self.scrollframe =  ScrolledFrame(self.window, compound=tk.RIGHT, canvasheight=700)
        self.scrollframe.pack(side = "left",fill='both', expand=True)

        self.fileMenu2.entryconfig(2,state = "disable")

        self.frame5=tkinter.Frame(self.scrollframe.interior, width=300, height = 150)
        self.frame5.pack(side="top",fill = 'x')
        self.text_box = self.text_input(self.frame5,self.label3,"  ● 시계열 범위 갯수 입력 (1이상 정수만 입력)   ",10,"top","top")
        self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
        self.buttonframe.pack(side="bottom")        
        self.button_input(self.buttonframe,"입   력",self.number_range,10,"left")
       
    def number_range(self):
        self.widget_clear(self.sampleframe)
        self.widget_clear(self.buttonframe2)
        self.widget_clear(self.hzSlctframe)
        self.widget_clear(self.empty_frame2)
        self.widget_clear(self.hzrangeSlctframe)
        self.widget_clear(self.hzrempty_frame)
        self.widget_clear(self.empty_frame3)
        self.widget_clear(self.sampleframe)
        self.widget_clear(self.empty_frame4)
        self.widget_clear(self.nb_sample_rg_frame)
        self.widget_clear(self.empty_frame5)
        self.widget_clear(self.sample_rg_frame)
        
        self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
        self.buttonframe2.pack(side="bottom")  
        self.button_input(self.buttonframe2,"입   력",self.hz_range_num,10,"left")        
        a = self.text_box.get()
        if self.text_box.get() != '' and self.count == 0 and int(self.text_box.get()) > 0:
            self.list1,self.list2,self.list3 = [], [], []
            self.empty_frame = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
            self.empty_frame.pack(side="top",fill = 'x')
            self.frame6=tkinter.Frame(self.scrollframe.interior, width=300, height = 350)
            self.frame6.pack(side="top",fill = 'x')
            self.label_input(self.frame6,self.label6," ● 시계열 범위 입력  ","top")
            for i in range(int(self.text_box.get())):
                rng_exp_frame=tkinter.Frame(self.frame6, width=300, height = 350)
                self.list2.append(rng_exp_frame)
            for j in range(int(self.text_box.get())):
                self.label_input(self.frame6,self.label6,"- " + chr(j+65) + " section - ","top")
                rng_box = self.text_input2(self.list2[j], self.list2[j], self.label6," 범위 : ",10,"left","left")
                exp_box = self.text_input2(self.list2[j], self.list2[j], self.label6,"   확대 비율 : ",10,"left","left")
                self.label_input(self.list2[j],self.label6," ","left")
                self.list2[j].pack(side="top",fill = 'x')
                self.list1.append(rng_box)
                self.list3.append(exp_box)
                
            self.label_input(self.frame6,self.label7,"○ 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.","top")
            self.label_input(self.frame6,self.label7,"○ 0~" + str(self.work.lngth) +" 사이로 입력해주세요.","top")
            self.widget_clear(self.buttonframe)
            self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
            self.buttonframe2.pack(side="bottom")  
            self.button_input(self.buttonframe2,"입   력",self.hz_range_num,10,"left")             
            self.buttonframe=tkinter.Frame(self.frame5, width=300, height = 350)
            self.buttonframe.pack(side="bottom")              
            self.button_input(self.buttonframe,"갯수 리셋",self.range_select,10,"left")
            self.count += 1
        else:
            pass


    def hz_range_num(self):
        start_end_list,exp_list = [], []
        for textbox in self.list1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list.append(i)
                
        for ex_textbox in self.list3:
            exp_list.append(float(ex_textbox.get()))

        self.work.slctIntrvl(start_end_list,exp_list)
        self.error_message.set(self.work.errMsg)
        
        self.fileMenu2.entryconfig(2,state = "normal")
        self.widget_clear(self.empty_frame2)
        self.widget_clear(self.hzSlctframe)
        self.widget_clear(self.hzrangeSlctframe)
        self.widget_clear(self.buttonframe2)
        self.widget_clear(self.empty_frame3)
        self.widget_clear(self.sampleframe)
        self.widget_clear(self.hzrempty_frame)
        self.widget_clear(self.empty_frame4)
        self.widget_clear(self.nb_sample_rg_frame)
        self.widget_clear(self.empty_frame5)
        self.widget_clear(self.sample_rg_frame)        
        
        self.hzrempty_frame = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
        self.hzrempty_frame.pack(side="top",fill = 'x')
        self.hzrangeSlctframe=tkinter.Frame(self.scrollframe.interior, width=300, height = 150)
        self.hzrangeSlctframe.pack(side="top",fill = 'x')
        self.text_box2 = self.text_input(self.hzrangeSlctframe,self.label3,"  ● 주파수 범위 갯수 입력 (1이상 정수만 입력) >  ",10,"top","top")
        self.hzrbuttonframe=tkinter.Frame(self.hzrangeSlctframe, width=300, height = 350)
        self.hzrbuttonframe.pack(side="bottom")        
        self.button_input(self.hzrbuttonframe,"입   력",self.hz_range,10,"left")        
        self.buttonframe2=tkinter.Frame(self.frame6, width=300, height = 350)
        self.buttonframe2.pack(side="bottom")              
        self.button_input(self.buttonframe2,"범위 리셋",self.number_range,10,"left")

    def hz_range(self):
        self.widget_clear(self.hzSlctframe)
        self.widget_clear(self.empty_frame2)
        self.widget_clear(self.hzrbuttonframe)
        self.widget_clear(self.empty_frame3)
        self.widget_clear(self.sampleframe)
        self.chrcount = 0;self.chlistcount = 0
        
        self.hzlist1,self.hzlist2,self.hzlist3 = [], [], []
        self.empty_frame2 = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
        self.empty_frame2.pack(side="top",fill = 'x')
        self.hzSlctframe=tkinter.Frame(self.scrollframe.interior, width=300, height = 350)
        self.hzSlctframe.pack(side="top",fill = 'x')
        self.label_input(self.hzSlctframe,self.label6," ● 주파수 범위 입력  ","top")        
        for i in range( int(self.text_box.get())*int(self.text_box2.get()) ):
            rng_exp_frame2=tkinter.Frame(self.hzSlctframe, width=300, height = 350)
            self.hzlist2.append(rng_exp_frame2)
        for j in range( int(self.text_box.get())):
            for k in range(int(self.text_box2.get())):
                self.label_input(self.hzSlctframe,self.label6,"- " + chr(self.chrcount+65) + " section - ","top")
                rng_box2 = self.text_input2(self.hzlist2[self.chlistcount], self.hzlist2[self.chlistcount], self.label6," 범위 : ",10,"left","left")
                exp_box2 = self.text_input2(self.hzlist2[self.chlistcount], self.hzlist2[self.chlistcount], self.label6,"   확대 비율 : ",10,"left","left")
                self.label_input(self.hzlist2[self.chlistcount],self.label6," ","left")
                self.hzlist3.append(exp_box2)
                self.hzlist2[self.chlistcount].pack(side="top",fill = 'x')
                self.hzlist1.append(rng_box2)
                self.chlistcount += 1
            self.chrcount+=1
            
        self.label_input(self.hzSlctframe,self.label7,"○ 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.","top")
        for i in range(len(self.work.maxIntrvl)):
<<<<<<< HEAD
            self.label_input(self.hzSlctframe,self.label7,"○ " + chr(i+65) + " : 0~" + str(self.work.maxIntrvl[i]//2) +" 사이로 입력해주세요.","top")
=======
            self.label_input(self.hzSlctframe,self.label7,"○ " + chr(i+65) + " : 0~" + str(self.work.maxIntrvl[i]) +" 사이로 입력해주세요.","top")
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
 
        self.buttonframe3=tkinter.Frame(self.hzSlctframe, width=300, height = 350)
        self.buttonframe3.pack(side="bottom")  
        self.button_input(self.buttonframe3,"입   력",self.confirm2,10,"left")
   
        self.hzrbuttonframe=tkinter.Frame(self.hzrangeSlctframe, width=300, height = 350)
        self.hzrbuttonframe.pack(side="bottom")              
        self.button_input(self.hzrbuttonframe,"갯수 리셋",self.hz_range_num,10,"left")
        
    def confirm2(self):
        self.widget_clear(self.empty_frame3)
        self.widget_clear(self.sampleframe)
        self.widget_clear(self.empty_frame4)
        self.widget_clear(self.nb_sample_rg_frame)
        self.widget_clear(self.empty_frame5)
        self.widget_clear(self.sample_rg_frame)
      
        
        start_end_list2, exp_list2 = [], []
        for textbox in self.hzlist1:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list2.append(i)
        for textbox2 in self.hzlist3:
            exp_list2.append(float(textbox2.get()))

        self.work.clcFft()
        self.work.slctFft(start_end_list2,exp_list2)
        self.error_message.set(self.work.errMsg)
        
        self.fileMenu2.entryconfig(2,state = "normal")
        self.empty_frame3 = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
        self.empty_frame3.pack(side="top",fill = 'x')        
        self.sampleframe = tkinter.Frame(self.scrollframe.interior, width=300, height = 150)
        self.sampleframe.pack(side = "top",fill = 'x')
        self.sample_box2 = self.text_input(self.sampleframe, self.sample_label, " ● 샘플 갯수 입력  ",10,"top","top")
<<<<<<< HEAD
        self.inputdc_box = self.text_input(self.sampleframe, self.sample_label, " ● Input DC Value  ",10,"top","top")
        self.button_input(self.sampleframe,"입   력",self.num_range_sample,10,"bottom")        

    def num_range_sample(self):
=======
        self.button_input(self.sampleframe,"입   력",self.num_range_sample,10,"bottom")        

    def num_range_sample(self):

>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
        self.widget_clear(self.empty_frame4)
        self.widget_clear(self.nb_sample_rg_frame)
        self.widget_clear(self.empty_frame5)
        self.widget_clear(self.sample_rg_frame)
        
<<<<<<< HEAD
        self.work.genSgnl(int(self.sample_box2.get()), int(self.inputdc_box.get()))
        self.ipdc.set(int(self.inputdc_box.get()))
=======
        self.work.genSgnl(int(self.sample_box2.get()))
        self.error_message.set(self.work.errMsg)
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
        self.empty_frame4 = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
        self.empty_frame4.pack(side="top",fill = 'x')       
        self.nb_sample_rg_frame = tkinter.Frame(self.scrollframe.interior, width=300, height = 150)
        self.nb_sample_rg_frame.pack(side = "top",fill = 'x')

<<<<<<< HEAD
        self.nb_sample_box = self.text_input(self.nb_sample_rg_frame,self.label8,"  ● 샘플 범위 갯수 입력 (1 or 2 입력)   ",10,"top","top")
=======
        self.label_input(self.nb_sample_rg_frame,self.label8," ● 샘플 범위(선택) ","top")
        self.radio1 = tk.Radiobutton(self.nb_sample_rg_frame, text = "모든 구간", variable = self.choice, value = 1).pack(side='top')
        self.radio2 = tk.Radiobutton(self.nb_sample_rg_frame, text = "3구간으로 분할", variable = self.choice, value = 2).pack(side='top')
        
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
        self.nb_smp_rg_buttonframe=tkinter.Frame(self.nb_sample_rg_frame, width=300, height = 350)
        self.nb_smp_rg_buttonframe.pack(side="bottom")        
        self.button_input(self.nb_smp_rg_buttonframe,"입   력",self.range_sample,10,"left")        

    def range_sample(self):
        self.widget_clear(self.empty_frame5)
        self.widget_clear(self.sample_rg_frame)
        
        self.rg_sample_list,self.rg_sample, self.dc_sample_list = [], [], []
        self.empty_frame5 = tkinter.Frame(self.scrollframe.interior, width=300, height = 20)
        self.empty_frame5.pack(side="top",fill = 'x')       
        self.sample_rg_frame = tkinter.Frame(self.scrollframe.interior, width=300, height = 150)
        self.sample_rg_frame.pack(side = "top",fill = 'x')
        self.label_input(self.sample_rg_frame, self.label8," ● 샘플 범위 입력  ","top")
<<<<<<< HEAD
        if int(self.nb_sample_box.get()) == 1:
            nb_smp_range = 1
        elif int(self.nb_sample_box.get()) == 2:
            nb_smp_range = 2

        if nb_smp_range == 2:
            for i in range(nb_smp_range):
                rng_sample_frame = tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
                self.rg_sample_list.append(rng_sample_frame)
            for j in range(nb_smp_range):
=======

        if self.choice.get() == 2:
            for i in range(int(self.choice.get())):
                rng_sample_frame = tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
                self.rg_sample_list.append(rng_sample_frame)
            for j in range(int(self.choice.get())):
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
                self.label_input(self.sample_rg_frame,self.label8,"- " + chr(j+65) + " section - ","top")
                rng_box3 = self.text_input2(self.rg_sample_list[j], self.rg_sample_list[j], self.label8," 범위 : ",10,"left","left")
                dc_box = self.text_input2(self.rg_sample_list[j], self.rg_sample_list[j], self.label8,"  D C : ",10,"left","left")
                self.label_input(self.rg_sample_list[j],self.label8," ","left")
                self.rg_sample_list[j].pack(side="top",fill = 'x')
                self.rg_sample.append(rng_box3)
                self.dc_sample_list.append(dc_box)
            self.label_input(self.sample_rg_frame,self.label8,"○ 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.","top")
            self.label_input(self.sample_rg_frame,self.label8,"○ 0~" + str(self.work.cntGenSmpl) +" 사이로 입력해주세요.","top")

            self.sample_rg_buttonframe=tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
            self.sample_rg_buttonframe.pack(side="bottom")  
            self.button_input(self.sample_rg_buttonframe,"입   력",self.sample_choice,10,"left")
<<<<<<< HEAD
        elif nb_smp_range == 1:
            for i in range(nb_smp_range):
                rng_sample_frame = tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
                self.rg_sample_list.append(rng_sample_frame)
            for j in range(nb_smp_range):
                self.label_input(self.sample_rg_frame,self.label8,"- " + chr(j+65) + " section - ","top")
                dc_box = self.text_input2(self.rg_sample_list[j], self.rg_sample_list[j], self.label8,"  D C : ",10,"left","left")
                self.label_input(self.rg_sample_list[j],self.label8," ","left")
                self.rg_sample_list[j].pack(side="top",fill = 'x')
                self.dc_sample_list.append(dc_box)
            self.label_input(self.sample_rg_frame,self.label8,"○ 100,200처럼 범위 사이를\n 쉼표로 구분 해주세요.","top")
            self.label_input(self.sample_rg_frame,self.label8,"○ 0~" + str(self.work.cntGenSmpl) +" 사이로 입력해주세요.","top")
=======
        elif self.choice.get() == 1:
            for i in range(int(self.choice.get())):
                rng_sample_frame = tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
                self.rg_sample_list.append(rng_sample_frame)
            for j in range(int(self.choice.get())):
                dc_box = self.text_input2(self.rg_sample_list[j], self.rg_sample_list[j], self.label8," - D C - ",10,"top","top")
                self.label_input(self.rg_sample_list[j],self.label8," ","left")
                self.rg_sample_list[j].pack(side="top",fill = 'x')
                self.dc_sample_list.append(dc_box)
            self.label_input(self.sample_rg_frame,self.label8,"○ DC값을 입력 해주세요.","top")
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb

            self.sample_rg_buttonframe=tkinter.Frame(self.sample_rg_frame, width=300, height = 350)
            self.sample_rg_buttonframe.pack(side="bottom")  
            self.button_input(self.sample_rg_buttonframe,"입   력",self.sample_choice,10,"left")
            
        
    def sample_choice(self):
        self.widget_clear(self.errorgrframe)

        start_end_list3, dc_list = [], []
        for textbox in self.rg_sample:
            a = list(map(int, textbox.get().split(',')))
            for i in a:
                start_end_list3.append(i)
        for textbox2 in self.dc_sample_list:
            dc_list.append(float(textbox2.get()))

        if len(start_end_list3) < 1:
            start_end_list3.append(0)
<<<<<<< HEAD
        print(start_end_list3)
        print(dc_list)
=======

        self.ipdc.set(dc_list)
>>>>>>> c14b7c7b706acabf01f23761b29627357bb8f2eb
        
        if self.choice.get() == 1:
            print(dc_list)
            self.work.slctGenIntrvl(_inptDC = dc_list)

        elif self.choice.get() == 2:
            self.work.slctGenIntrvl(start_end_list3, dc_list)

        self.error_message.set(self.work.errMsg)
        self.errorgrframe = tkinter.Frame(self.sample_rg_frame, width=300, height = 20)
        self.errorgrframe.pack(side = "top",fill = 'x')
  
        self.fileMenu.entryconfig(1,state = "normal")
        self.button_input(self.errorgrframe,"에러 그래프",self.error_graph,10,"bottom")
        self.fileMenu2.entryconfig(2,state = "normal")        
    def error_graph(self):
        self.work.getError()
        self.er.set(self.work.e)
        
    def test2(self):
        self.widget_clear(self.frame6)
        self.frame6=tkinter.Frame(self.frame2, width=300, height = 80)
        self.frame6.pack(side="top",fill = 'both', expand=True)
        self.button_input(self.frame6,"확인",self.confirm,250,50,5)
        self.text_input(self.frame6," < Test Button > ",80,50)


window1 = windowform1()









