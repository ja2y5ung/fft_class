# 2021 04 22 Restart
import numpy as np
from numpy import exp, pi, sin
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import math
import warnings

warnings.filterwarnings(action='ignore')

class backend:

    file                  = 0 # 파일
    columnDataLength      = 0 # 파일의 열 길이
    orgnlData             = 0 # 데이터
    dcData                = 0 # 데이터 오프셋

    dataLngth             = 0 # 데이터 길이
    fftData               = 0 # 원 데이터를 푸리에 변환
    amplt                 = 0 # 원 데이터의 진폭 스펙트럼
    phase                 = 0 # 원 데이터의 위상 스펙트럼

    result                = 0 # 가공한 데이터 저장
    fig                   = 0 # 그래프 저장할 객체
    
    


    def __init__(self):
##        self.run()
        pass

    def run(self):
        self.loadFile('Normal_test.csv')
        self.slctData(1)
        self.initData()

        self.slctBySize()
        self.ifft()
        self.saveFig()
        self.show()
        

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
        self.dataLngth = len( self.orgnlData )
        self.dcData = self.orgnlData.mean()
        self.orgnlData = self.orgnlData - self.dcData

        
        hlfLng = int( self.dataLngth / 2 )
        
        self.fftData = np.fft.fft( self.orgnlData ) / self.dataLngth
        self.amplt = 2 * abs( self.fftData[0:hlfLng] )
        self.phase = np.angle( self.fftData[0:hlfLng], deg = False )

    # 진폭순으로 선택
    def slctBySize(self , _N = 2):
        hlfLng = len( self.amplt )
        self.result = self.fftData
        idxSortAmp = self.amplt.argsort()
        self.a = idxSortAmp
        N = idxSortAmp[-_N]
        
        self.result[ abs(self.fftData) < abs(self.fftData[N]) ] = 0


    # 밴드 패스 필터
    def bandPassFltr(self):
        pass

    # 푸리에 역변환
    def ifft(self):
        self.result = np.fft.ifft( self.result ) * self.dataLngth

    # 그래프 저장
    def saveFig(self):
        self.fig = Figure( figsize=(10,7), dpi = 100 )

        plt1 = self.fig.add_subplot(1, 1, 1)
        plt1.plot(self.orgnlData)
        
        
        
        
    # 작업
    def processing(self):
        pass
        
    # 출력
    def show(self):
        time = np.linspace(0,5,2500)
        
        self.fig = plt.figure()
        plt1 = self.fig.add_subplot(3,2,1)
        plt3 = self.fig.add_subplot(3,2,3)
        plt5 = self.fig.add_subplot(3,2,5)

        plt2 = self.fig.add_subplot(3,2,2)
        plt4 = self.fig.add_subplot(3,2,4)
        plt6 = self.fig.add_subplot(3,2,6)

        
        plt1.plot(time, self.orgnlData)
        plt1.set_xlabel("time")
        plt1.set_ylabel("y")
        plt3.stem(self.amplt)
        plt3.set_xlabel("Hz")
        plt3.set_ylabel("Amplitue")
        plt5.stem(self.phase)
        plt5.set_xlabel("Hz")
        plt5.set_ylabel("Phase")

        plt2.plot(time, self.orgnlData)
        plt4.plot(self.result)
        t = np.arange(0,2500,0.4/1250)
        plt6.plot(t, self.amplt[1]*sin(2*pi*1*0.4/1250*( t - self.phase[1] )) + \
                 self.amplt[4]*sin(2*pi*4*0.4/1250*( t - self.phase[4] )), 'r' )
        self.fig.tight_layout()

        
##        plt.subplot(3, 2, 1)
##        plt.plot( time,self.orgnlData )
##        plt.xlabel('time')
##        plt.ylabel('y')
##
##        plt.subplot(3, 2, 3)
##        plt.stem( self.amplt )
##        plt.xlabel('Hz')
##        plt.ylabel('Amplitue')
##
##        plt.subplot(3, 2, 5)
##        plt.stem( self.phase )
##        plt.xlabel('Hz')
##        plt.ylabel('Phase')
##
##        plt.subplot(3, 2, 2)
##        plt.plot( self.orgnlData )
##
##        plt.subplot(3, 2, 4)
##        plt.plot( self.result , 'r' )
##
##        plt.subplot(3, 2, 6)

        # Asin(wt+q)로 그래프 만들기
        t = np.arange(0,2500,1)
        plt.plot(self.amplt[1]*sin(2*pi*1*0.4/1250*( t - self.phase[1] )) + \
                 self.amplt[4]*sin(2*pi*4*0.4/1250*( t - self.phase[4] )), 'r' )
        #end
        
##        plt.show()



if __name__ == '__main__':
    test = backend()


        

    

    
        

    
        

    

    
        
