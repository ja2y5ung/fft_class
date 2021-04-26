# 2021 04 22 Restart
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

    

    dataLngth             = 0 # 데이터 길이
    fftData               = 0 # 원 데이터를 푸리에 변환
    amplt                 = 0 # 원 데이터의 진폭 스펙트럼
    phase                 = 0 # 원 데이터의 위상 스펙트럼

    intrvList             = [] #잘라낸 구간을 저장할 리스트

    result                = 0 # 가공한 데이터 저장
    fig                   = 0 # 그래프 저장할 객체
    fig2                  = 0 # 잘라낸 그래프 저장할 객체
    
    


    def __init__(self):
##        self.run()
        pass
    
    def run(self):
        self.loadFile('Normal_test.csv')
        self.slctData(1)
        self.initData()

        self.slctBySize()
        self.ifft()
##        self.saveFig()
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
        
        self.fftData = np.fft.fft( self.orgnlData )
        self.amplt = 2 * abs( self.fftData[0:hlfLng] )
        self.phase = np.angle( self.fftData[0:hlfLng], deg = False)

    # 진폭순으로 선택
    def slctBySize(self , _N = 2):
        hlfLng = len( self.amplt )
        self.result = self.fftData
        idxSortAmp = self.amplt.argsort()
        self.a = idxSortAmp
        N = idxSortAmp[-_N]
        
        self.result[ abs(self.fftData) < abs(self.fftData[N]) ] = 0


    # 밴드 패스 필터
    def bandPassFltr(self, _intrvList):
        self.intrvList = []
        intrvLstln = len( _intrvList )

        # start, end값
        for i in range(0, intrvLstln, 2):
            start = _intrvList[i]
            end = _intrvList[i+1]
            self.intrvList.append( self.orgnlData[start:end] )

        # 출력할 수 있게 끔 열 데이터로 변환    
        for i in range(0, intrvLstln, 2):
            index = int(i/2)
            self.intrvList[index] = self.intrvList[index].reshape( len( self.intrvList[index]) ,1)

        # 원데이터 출력
        col = int(intrvLstln/2) + 1
        self.fig2 = plt.figure()
        plt1 = self.fig2.add_subplot(col,1,1)
        plt1.plot( self.orgnlData )

        # 잘래낸 값 출력
        temp = []
        for i in range(0, intrvLstln, 2):
            index = int(i/2)
            temp.append( self.fig2.add_subplot( col, 1, index +2))
            temp[index].plot( self.intrvList[index])
        self.fig2.tight_layout()
            
##        plt.show()
##        
    # 푸리에 역변환
    def ifft(self):
        self.result = np.fft.ifft( self.result ) * self.dataLngth
            
    # 출력
    def show(self):
        
        self.fig = plt.figure()
        plt1 = self.fig.add_subplot(3,2,1)
        plt3 = self.fig.add_subplot(3,2,3)
        plt5 = self.fig.add_subplot(3,2,5)

        plt2 = self.fig.add_subplot(3,2,2)
        plt4 = self.fig.add_subplot(3,2,4)
        plt6 = self.fig.add_subplot(3,2,6)

        # 원 데이터 출력
        time = np.arange(0,len(self.orgnlData)*5,5)
        plt1.plot(time, self.orgnlData)
        plt1.grid()
        plt1.set_xlabel("time")
        plt1.set_ylabel("y")
        
        # 진폭 스펙트럼 출력
        Hz = np.arange(0, 0.2/2, 0.1/(len( self.orgnlData )*0.5) )
        plt3.stem(Hz,self.amplt)
        plt3.grid()
        plt3.set_xlabel("Hz")
        plt3.set_ylabel("Amplitue")
        
        # 위상 스펙트럼 출력
        
        plt5.stem(Hz, self.phase)
        plt5.grid()
        plt5.set_xlabel("Hz")
        plt5.set_ylabel("Phase")
        
        # 진폭으로 크기 순으로 2개 뽑아서 ifft한 그래프
        plt2.plot(time, self.result)
        plt2.set_ylabel("y")
        plt2.set_xlabel("ifft")
        plt2.grid()

        # A*sin(wt-q)로 진폭 크기순 2개 뽑아서 만든 그래프 : 주기가 있는 연속 신호일 경우
        t = np.arange(0,2500*5,5)
        plt4.plot(t, self.amplt[1]*sin(2*pi*1*0.1/1250*t +1*0.1*self.phase[1] ) + \
                 self.amplt[4]*sin(2*pi*4*0.1/1250*t  + 4*0.1*self.phase[4] ))
        plt4.set_ylabel("y")
        plt4.set_xlabel("A*Sin( 2*pi*f(t - q))")
        plt4.grid()

        # A*sin(wt-q)로 진폭 크기순 2개 뽑아서 만든 그래프 : 길이가 N인 이산 신호일 경우
        plt6.plot(t, self.amplt[1]*sin(2*pi*1/2500*( t - self.phase[1] )) + \
                 self.amplt[4]*sin(2*pi*4/2500*( t - self.phase[4] )) )
        plt6.set_ylabel("y")
        plt6.set_xlabel("A*Sin( (2*pi*k)/N(t - q) )")
        plt6.grid()
        
        self.fig.tight_layout()
##        plt.show()

    

if __name__ == '__main__':
    test = backend()
    test.run()


        

    

    
        

    
        

    

    
        
