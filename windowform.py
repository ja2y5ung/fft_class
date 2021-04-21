import tkinter as tk
import tkinter.ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from fft_class0419 import Work
import numpy as np
import matplotlib.pyplot as plt


class windowform1():
    num = 0
    combobox = 0
    window = 0
    window2 = 0
    canvas = 0
    work = 0
    
    def __init__(self):
        self.work = Work()
        
        self.window = tk.Tk()
        self.window.title('control')
        self.window.geometry("1200x800+200+100")
        self.window.resizable(False, False)
        self.combobox()
        
    def combobox(self):
        values=[str(i)+"" for i in range(0, self.work.data_col)] 
        self.combobox=tk.ttk.Combobox(self.window, height=15, values=values)
        self.combobox.set(0)
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.callbackFunc)
        
    def callbackFunc(self,event):
        self.num = int(self.combobox.get())
        self.work1 = Work(self.num)
        self.window2 = tk.Tk()
        self.window2.geometry("1500x700")
        self.window2.title('control')
        self.draw_figure(self.work1.fig)

    def draw_figure(self,fig):
        self.canvas = FigureCanvasTkAgg(fig, master = self.window2)
        self.canvas.get_tk_widget().pack()

    def main_loop(self):
        self.window.mainloop()


window1 = windowform1()
window1.main_loop()
##














