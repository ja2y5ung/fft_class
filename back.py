# 2021 04 26 그래프 복원 문제 해결, 구간 선택하는 부분 코딩
import numpy as np
from numpy import exp, pi, sin
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import math
import warnings
import pdb

warnings.filterwarnings(action='ignore')

class backend:

    file                  = 0 # 파일
    columnDataLength      = 0 # 파일의 열 길이
    
    orgnlData             = 0 # 데이터
    dcData                = 0 # 데이터 오프셋
    lngthData             = 0 # 데이터 길이

    f = 0.2
    T = 1/f
    
    fftData               = 0 # 원 데이터를 푸리에 변환
    amplt                 = 0 # 원 데이터의 진폭 스펙트럼
    phase                 = 0 # 원 데이터의 위상 스펙트럼

    intrvlData             = [] #잘라낸 구간을 저장할 리스트

    result                = 0 # 가공한 데이터 저장
    fig                   = 0 # 그래프 저장할 객체
    fig2                  = 0 # 잘라낸 그래프 저장할 객체
    fig3                  = 0 # 잘라낸 그래프 합성하기
    
    


    def __init__(self):
        pass
    
    def run(self):
        self.loadFile('Normal_test.csv')
        self.slctData(1)
        self.initData()

        self.getOrgn()
        self.getIntrvl([0,800,1000,1500])
        self.synthetic()






        
    # 파일 불러오기
    def loadFile(self, _path):
        self.file = np.genfromtxt( _path, delimiter = ',', dtype = float, encoding = 'UTF-8')
        self.columnDataLength = self.file.shape[1]
        self.row_name = np.genfromtxt( _path, delimiter = ',', dtype = str)[0]




        
    # 파일 안에서 데이터 선택하기
    def slctData(self, _num):
        self.orgnlData = self.file[1:, _num]




        
    # 변수 초기화
    def initData(self):
        self.lngthData = len( self.orgnlData )
        self.dcData = self.orgnlData.mean()
        self.orgnlData = np.array([self.orgnlData - self.dcData]).T

        hlfLngth = self.lngthData // 2
        
        self.fftData = np.fft.fft( self.orgnlData, axis = 0) / self.lngthData
        self.amplt = 2 * abs( self.fftData[0:hlfLngth] )
        self.phase = np.angle( self.fftData[0:hlfLngth], deg = False)




        
    # 진폭순으로 선택
    def slctBySize(self , _N = 2):
        lngth = len( self.orgnlData ) // 2
##        0425 백업용.. 쓸지 모름
##        hlfLng = len( self.amplt )
##        self.result = self.fftData
##        idxSortAmp = self.amplt.argsort()
##        self.a = idxSortAmp
##        N = idxSortAmp[-_N]
##        
##        self.result[ abs(self.fftData) < abs(self.fftData[N]) ] = 0





    # 구간 잘라내기
    def getIntrvl(self, _value):
        intrvl = []
        lngth = len(_value)

        # start, end값
        for i in range(0, lngth, 2):
            start = _value[i]
            end = _value[i+1]
            intrvl.append( self.orgnlData[start:end] )
            index = i // 2

            

        Hz = np.linspace(0, self.f/2, self.lngthData//2)
        time = np.linspace(0, self.lngthData * self.T, self.lngthData)      
        # 원데이터 출력
        col = (lngth//2) + 1
        self.fig2 = plt.figure()
        plt1 = self.fig2.add_subplot(col,1,1)
        plt1.plot(time, self.orgnlData )
        plt1.grid()
        plt1.set_xlabel("time")
        plt1.set_ylabel("x(t))")
        plt1.set_title("Orignal")

        # 잘래낸 값 출력
        grphLst = []
        for i in range(0, lngth, 2):
            index = i//2
            start = _value[i]
            end = _value[i+1]
            xAxis = np.linspace(start, end, end-start)
            grphLst.append( self.fig2.add_subplot( col, 1, index +2))
            grphLst[index].plot(xAxis, intrvl[index] )
            grphLst[index].set_ylabel("x(t)")
            grphLst[index].set_xlabel("time")
            grphLst[index].set_title(chr(65+index))
            
<<<<<<< HEAD
        self.intrvlData = intrvl
        self.intrvl = _value
        self.fig2.tight_layout()  
        self.fig2.show()




        
    # 선택된 구간 합성
    def synthetic(self):
        lngth = len( self.intrvlData )
        fft = []
        amplt = []
        phase = []
        self.fig3 = plt.figure()
        


        for i in range(0,lngth):
            index = i
            fft.append(np.fft.fft( self.intrvlData[index], axis = 0 ))
            amplt.append( abs( fft[index][0: len(fft[index])//2] ))
            phase.append( np.angle( fft[index][0: len(fft[index])//2 ], deg = False ))
            start = self.intrvl[i*2]
            end = self.intrvl[i*2+1]
            xAxis = np.linspace(start,end,end-start)
=======
>>>>>>> ec5d11e966b2cbad12c94e13a65222f4440a2a51
            
            p = self.fig3.add_subplot(lngth,3,1+index*3)
            p.plot(xAxis, self.intrvlData[index])
            p.set_xlabel("time")
            p.set_ylabel("x(t)")
            p = self.fig3.add_subplot(lngth,3,2+index*3)
            p.stem(amplt[index])
            p.set_xlabel("Hz")
            p.set_ylabel("∣X(f)∣")
            p = self.fig3.add_subplot(lngth,3,3+index*3)
            p.stem(phase[index])
            p.set_xlabel("Hz")
            p.set_ylabel("∠X(f)")


        ## 함수 합성하는 부분 def로 만들어야 함 04 25
            self.fig4 = plt.figure()
            

        

        self.fig3.tight_layout()
##        self.fig3.show()
            






                                      
    # 원 데이터, 진폭, 위상 
    def getOrgn(self):
        self.fig = plt.figure()
        plt1 = self.fig.add_subplot(3,1,1)
        plt2 = self.fig.add_subplot(3,1,2)
        plt3 = self.fig.add_subplot(3,1,3)

        Hz = np.linspace(0, self.f/2, self.lngthData//2)
        time = np.linspace(0, self.lngthData * self.T, self.lngthData)


        # 원 데이터 출력
        plt1.plot(time, self.orgnlData)
        plt1.grid()
        plt1.set_xlabel("time")
        plt1.set_ylabel("x(t)")
        plt1.set_title("Orignal")
        
        
        
        # 진폭 스펙트럼 출력
        plt2.stem(Hz,self.amplt)
        plt2.grid()
        plt2.set_xlabel("Hz")
        plt2.set_ylabel("∣X(f)∣")
        plt2.set_title("Amplitude")
        
        # 위상 스펙트럼 출력
        plt3.stem(Hz, self.phase)
        plt3.grid()
        plt3.set_xlabel("Hz")
        plt3.set_ylabel("∠X(f)")
        plt3.set_title("Phase")
        

        self.fig.tight_layout()
##        self.fig.show()

    

if __name__ == '__main__':
    test = backend()
##    test.run()


        

    

    
        

    
        

    

    
        
