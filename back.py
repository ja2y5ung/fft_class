# 2021 04 27 그래프의 축 값 계산, 그래프가 누적 오차가 생기는 듯한 현상 발견, 코드 길이 간결화
import numpy as np
from numpy import exp, pi, sin
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import math
import warnings
import pdb

warnings.filterwarnings(action='ignore')

class backend:

    file                  = 0 # 파일                              # [NxM]
    columnDataLength      = 0 # 파일의 열 길이                    # N
    
    orgnlData             = 0 # 데이터                            # [Nx1]
    dcData                = 0 # 데이터 오프셋                     # N
    lngthData             = 0 # 데이터 길이                       # N

    f = 0.2
    T = 1/f
    
    fftData               = 0 # 원 데이터를 푸리에 변환           # [Nx1]
    amplt                 = 0 # 원 데이터의 진폭 스펙트럼         # [Nx1]
    phase                 = 0 # 원 데이터의 위상 스펙트럼         # [Nx1]

    intrvlData            = [] #잘라낸 구간의 값들                # list[ np[Nx1], np[Nx1], np[Nx1] ... ]
    intrvl                = [] #잘려진 구간들의 위치              # list[ N, N, N, N ... ]

    slctFft               = [] #잘라낸 구간들의 fft               # list[ np[Nx1], np[Nx1], np[Nx1] ... ]
    slctAmplt             = [] #잘라낸 구간들의 amplt             # list[ np[Nx1], np[Nx1], np[Nx1] ... ]
    slctPhase             = [] #잘라낸 구간들의 phase             # list[ np[Nx1], np[Nx1], np[Nx1] ... ]


    error                 = 0  # 에러 

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
        self.getIntrvl([0,12500])
        self.synthetic()
        self.slctBySize()






        
    # 파일 불러오기
    def loadFile(self, _path):
        self.file = np.genfromtxt( _path, delimiter = ',', dtype = float, encoding = 'UTF-8')
        self.columnDataLength = self.file.shape[1]
        self.row_name = np.genfromtxt( _path, delimiter = ',', dtype = str)[0]




        
    # 파일 안에서 데이터 선택하기
    def slctData(self, _num):
        self.orgnlData = self.file[1:, _num]                                                                            # N




        
    # 변수 초기화
    def initData(self):
        self.lngthData = len( self.orgnlData )
        self.dcData = self.orgnlData.mean()
        self.orgnlData = np.array([self.orgnlData - self.dcData]).T                                                     # [1xN]

        hlfLngth = self.lngthData // 2
        
        self.fftData = np.fft.fft( self.orgnlData, axis = 0) / self.lngthData                                           # [Nx1]
        self.amplt = 2 * abs( self.fftData[0:hlfLngth] )
        self.phase = np.angle( self.fftData[0:hlfLngth], deg = False)







        


    # 구간 잘라내기
    def getIntrvl(self, _intrvl):
        intrvlData = []
        cntSlct = len(_intrvl) // 2 # 잘라낸 구간 개수

        self.fig2 = plt.figure()
        
        grphLst = []
        # start, end값 잘라 내고 출력하기
        for i in range(0, cntSlct):
            start = _intrvl[i*2]// int( self.T ) 
            end = _intrvl[i*2+1]// int( self.T ) 
            step = int( end - start )
            cutTime = np.linspace(start*5, end*5, step, endpoint = False  )                                             # N
            
            intrvlData.append( self.orgnlData[start:end] )                                                              # list[ np[end-startx1], np[end-startx1], np[end-startx1], ... ]
    
            grphLst.append( self.fig2.add_subplot( cntSlct, 1, i +1))
            grphLst[i].plot(cutTime, intrvlData[i] )
            grphLst[i].grid()
            grphLst[i].set_ylabel("x(t)")
            grphLst[i].set_xlabel("time")
            grphLst[i].set_title(chr(65+i))
            

          
        self.intrvlData = intrvlData                                                                                    # list[ np[end-startx1], np[end-startx1], np[end-startx1], ... ]  
        self.intrvl = _intrvl                                                                                           # list[ N, N, N ... ]
        
        self.fig2.tight_layout()  
        self.fig2.show()

        

##    # 진폭순으로 선택
##    def slctBySize(self , _N = 1250):
##        lngth = len( self.orgnlData ) // 2
####        0425 백업용.. 쓸지 모름
####        hlfLng = len( self.amplt )
####        self.result = self.fftData
####        idxSortAmp = self.amplt.argsort()
####        self.a = idxSortAmp
####        N = idxSortAmp[-_N]
####        
####        self.result[ abs(self.fftData) < abs(self.fftData[N]) ] = 0

        
    # 선택된 구간의 fft들
    # getSlctFft같은걸로 이름 바꺼야 할듯
    def synthetic(self):
        cntData = len( self.intrvlData )                                                                                # N
        
        self.fig3 = plt.figure()
        
        for i in range(0, cntData): # 잘라낸 구간 만큼 fft 계산
            
            lngth = len( self.intrvlData[i] )                                                                           # N
            hlfLngth = lngth // 2                                                                                       # N
            fft = np.fft.fft( self.intrvlData[i] , axis = 0 ) / lngth                                                   # [Nx1]
            amplt = 2*abs( fft[0: hlfLngth] )                                                                           # [Nx1]
            phase = np.angle( fft[0: hlfLngth ], deg = False )
            
            self.slctFft.append(fft)                                                                                    # list[ np[Nx1], np[Nx1], np[Nx1] ... ]
            self.slctAmplt.append( amplt )                                                                              # list[ np[Nx1], np[Nx1] ... ]
            self.slctPhase.append( phase )                                                                              # list[ np[Nx1], np[Nx1] ... ]
            
            
            start = self.intrvl[i*2] // 5                                                                               # N
            end = self.intrvl[i*2+1] // 5                                                                               # N
            
            cutTime = np.linspace(start*5, end*5, int(end - start), endpoint = False)                                   # N
            step = 0.1/((end - start)/2)                                                                                # N
            Hz = np.arange(0,0.1, step )                                                                                # N
            

            p = self.fig3.add_subplot(3,cntData,1+i)
            p.plot(cutTime, self.intrvlData[i])
            p.set_xlabel("time")
            p.set_ylabel("x(t)")
            p.set_title(chr(65+i))
            p = self.fig3.add_subplot(3,cntData,2+(cntData-1)*math.ceil(2/cntData)+i)
            p.stem(Hz,self.slctAmplt[i])
            p.set_xlabel("Hz")
            p.set_ylabel("∣X(f)∣")
            p = self.fig3.add_subplot(3,cntData,3+(cntData-1)*math.ceil(3/cntData)+i)
            p.stem(Hz,self.slctPhase[i])
            p.set_xlabel("Hz")
            p.set_ylabel("∠X(f)")


        self.fig3.tight_layout()

        

    def slctBySize(self, _N = 30):
        N = _N   # 크기순으로 뽑을 개수
        cntData = len( self.intrvlData ) # N
        
        self.fig4 = plt.figure()

        Y = 0
        t = np.linspace(0,12500,2500, endpoint = False) # N
        t = np.arange(0,12500,5)
        for cnt in range(cntData):  # 선택된 구간만큼 반복
            
            amplt = self.slctAmplt[cnt]     # [Nx1]
            phase = self.slctPhase[cnt]     # [Nx1]
            sortIdx = amplt.argsort(axis=0) # [Nx1]
            size = sortIdx[-N]              # N
            f =  (1 / ( self.intrvl[cnt*2+1] - self.intrvl[cnt*2] )) # N
            
            
            amplt[ amplt < amplt[ size ] ] = 0 # [Nx1]
            
            for i in range(N):
                k = sortIdx[ -(i+1) ]
                A = amplt[k]
                q = phase[k] + (pi/2)
                
                Y = Y + A*sin( 2*pi*k*f*t  + q )

        plt1 = self.fig4.add_subplot(1,1,1)
        plt1.plot(t,self.orgnlData)
        plt1.plot(t,Y.T,'r')
        plt1.grid()
        plt1.set_xlabel("time")
        plt1.set_ylabel("x(t)")
        plt1.set_title("Result")
        plt.legend(['Orignal', 'Synthesis'])
        
        self.fig4.show()
        
        self.e = (self.orgnlData  - Y.T )**2
        self.e = np.sqrt( self.e.mean() )
        
        print(self.e)


                                      
    # 원 데이터, 진폭, 위상 
    def getOrgn(self):
        self.fig = plt.figure()
        plt1 = self.fig.add_subplot(3,1,1)
        plt2 = self.fig.add_subplot(3,1,2)
        plt3 = self.fig.add_subplot(3,1,3)

        Hz = np.linspace(0, self.f/2, self.lngthData//2, endpoint = False)
        time = np.linspace(0, self.lngthData * self.T, self.lngthData, endpoint = False)


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
        self.fig.show()

    

if __name__ == '__main__':
    test = backend()
    test.run()


        

    

    
        

    
        

    

    
        
