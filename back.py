# 2021 04 27 그래프의 축 값 계산, 그래프가 누적 오차가 생기는 듯한 현상 발견, 코드 길이 간결화
# 2021 05 03 교수님 요구 사항 수정 : GUI  개선, 잘라낸 구간 증폭, 신호 생성 구간 설정, 데이터 저장, 에러처리
# 2021 05 04 시발 왜 저장이 안됫지 시발 시발
# 2021 05 05 11:16 어린이날, 14:52 교수님 피드벡 -> 진폭에서 슬라이스, 피규어에 제목 18:45 

import numpy as np
from numpy import exp, pi, sin
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import math
import warnings
import pdb

warnings.filterwarnings(action='ignore')

class backend:

    file                  = 0   # 파일
    columnDataLength      = 0   # 파일의 열 길이
    
    orgnlData             = 0   # 데이터
    dcData                = 0   # 데이터 오프셋
    lngthData             = 0   # 데이터 길이

    Fs                    = 0   # 샘플링 주파수
    frqRez                = 0
    T                     = 0   # 주기            
    
    fftData               = 0   # 원 데이터를 푸리에 변환
    amplt                 = 0   # 원 데이터의 진폭 스펙트럼
    phase                 = 0   # 원 데이터의 위상 스펙트럼

    intrvlData            = []  #잘라낸 구간의 값들
    intrvl                = []  #잘려진 구간들의 위치

    ampLst                = []  # 잘라낸 구간들의 진폭
    phsLst                = []  # 잘라낸 구간들의 위상

    resAmpLst             = [] # 결과를 계속 바꺼 저장할 변수

    error                 = 0   # 에러율

    fig1                  = 0   # 그래프 저장할 객체
    fig2                  = 0   # 잘라낸 그래프 저장할 객체
    fig3                  = 0   # 잘라낸 그래프 합성하기
    fig4                  = 0   # 잘라낸 구간의 fft 

    Y                     = 0   #
    


    def __init__(self):
        pass
    
    def run(self):
        self.loadFile('Normal_test.csv')
        self.slctData()
        self.initData()

        self.getOrgn()
        
        self.getIntrvl()
        self.fftIntrvl()
        self.slctFft()
        self.genSgnl()


        
    # 파일 불러오기
    def loadFile(self, _path):
        self.file   = np.genfromtxt( _path, delimiter = ',', dtype = float, encoding = 'UTF-8')
        size        = len( self.file.shape )

        
        if( size == 1 ):
            self.columnDataLength = 1           
        else:
            self.columnDataLength = self.file.shape[1]
            
            
        self.row_name = np.genfromtxt( _path, delimiter = ',', dtype = str)[0]


        
    # 파일 안에서 데이터 선택하기
    def slctData(self, _num = 0):
        if ( self.columnDataLength == 1 ):
            self.orgnlData = self.file[1:]
        else:
            self.orgnlData = self.file[1:, _num] 



  
    # 변수 초기화
    def initData(self):
        self.lngthData      = len( self.orgnlData )
        self.dcData         = self.orgnlData.mean()
        self.orgnlData      = np.array( [self.orgnlData - self.dcData] ).T

        self.fftData        = np.fft.fft( self.orgnlData, axis = 0) / self.lngthData
        self.amplt          = 2 * abs( self.fftData[0:self.lngthData//2] )
        self.phase          = np.angle( self.fftData[0:self.lngthData//2], deg = False)

        self.Fs             = 0.2
        self.T              = 1 / self.f
        self.frqRez         = 1 / self.lngthData

    

    # 구간 잘라내기 
    def getIntrvl(self, _intrvl = [0, 2500], _mult = [1], _show = True ):
        self.fig2 = plt.figure("시계열 잘라낸 구간")
        
        intrvlData  = []                    # 잘라낸 구간들을 저장
        grphLst     = []                    # 그래프를 저장할 리스트
        cntIntrvl   = len(_intrvl) // 2     # 잘라낸 구간 갯수

        data        = self.orgnlData
        lngth       = self.lngthData
                      
        # 구간 자르고 변수에 저장 
        for i in range(0, cntIntrvl):
            start   = _intrvl[i*2]
            end     = _intrvl[i*2+1]


            # 잘라낸 구간이 문제가 있으면
            if ( start > end or start > lngth or end > lngth ):
                return -1
            
            num     = int( end - start )
            cutSmpl = np.linspace(start, end, num, endpoint = False  )


            #잘라내고 변수에 저장
            intrvlData.append(  _mult[i] * data[start:end]  )

            
            # 그래프를 리스트에 저장
            grphLst.append( self.fig2.add_subplot( cntIntrvl, 1, i +1))
            grphLst[i].plot(cutSmpl, intrvlData[i] )
            grphLst[i].grid()
            grphLst[i].set_ylabel("x(t) - dcData")
            grphLst[i].set_xlabel("Interval samples")
            grphLst[i].set_title(chr(65+i) + " section")
        
        
        self.intrvlData = intrvlData                                                                                   
        self.intrvl = _intrvl                                                                                          
        
        self.fig2.tight_layout()

        if( _show ):
            self.fig2.show()
        
        return self.fig2


    # 구간 합성하기 
    def genSgnl(self, _cntSmpl = 2500, _show = True):
        self.fig3   = plt.figure("합성 결과")
        cnt         = len( self.intrvlData )

        Y           = 0
        eY          = 0
        
        for i in range( cnt ):

            lngth   = len( self.intrvlData[i] )
            amplt   = self.resAmpLst
            phase   = self.phsLst


            f       = 1/self.lngthData
            t       = np.arange(0, _cntSmpl, 1);
            et      = np.arange(0, self.lngthData, 1)
            



            for j in range(lngth//2):
                A   = amplt[i][j]
                q   = phase[i][j] + (pi/2)
                Y   = Y + A*sin( 2*pi*j*f*t  + q )
                eY  = eY + A*sin( 2*pi*j*f*et  + q )

        self.Y = Y + self.dcData
        p       = self.fig3.add_subplot(1,1,1)
        
        p.plot(self.Y)
        p.set_xlabel("Number of samples")
        p.set_ylabel("x(t)")
        p.set_title(" Generate Signal ")
        plt.grid()

        eY = eY.reshape(( self.lngthData,1))

        e = ((self.orgnlData + self.dcData) - (eY +self.dcData) )**2
        e = np.sqrt( e.mean() )

        self.error = e

        

        if (_show):
            self.fig3.show()
        

        return self.fig3


    # 잘라낸 구간 fft 구하기
    def fftIntrvl(self):

        self.fig4 = plt.figure("잘라낸 구간들의 진폭 위상 ")

        fftLst          = []
        ampLst          = []
        phsLst          = []

        
        data      = self.intrvlData
        cnt             = len( data )
        

        for i in range( cnt ):
            lngth   = len( data[i] )
            fft     = np.fft.fft( data[i], axis = 0 ) / lngth
            amp     = 2 * abs( fft )
            phs     = np.angle( fft, deg = False )

            start   = self.intrvl[i*2]
            end     = self.intrvl[i*2+1]
            num     = int( end - start )
            
            cutSmpl = np.linspace(start, end, num, endpoint = False )

            fftLst.append( fft )
            ampLst.append( amp[0 : lngth//2] )
            phsLst.append( phs[0 : lngth//2] )


            p = self.fig4.add_subplot(2, cnt, 1 + 2*i - i )
            p.plot(cutSmpl, data[i] )
            p.set_title( chr(65 + i ) + " section")
            p.set_xlabel("Interval samples")
            p.set_ylabel("x(t) - dcData")
            plt.grid()

            p = self.fig4.add_subplot(2, cnt, 1 + 2*i + cnt - i )
            p.stem( ampLst[i] )
            p.set_xlabel("Point[Hz]")
            p.set_ylabel("∣X(f)∣")
            plt.grid()

        self.fig4.tight_layout()

        self.ampLst = ampLst
        self.phsLst = phsLst

        

        



    # 잘라낸 구간 선택하기
    def slctFft(self, _intrvl = [100,1250], _mult = [0]):

        amp = self.ampLst
        phs = self.phsLst

        cnt = len( amp )

        for i in range(cnt):
            srt = _intrvl[i*2] 
            end = _intrvl[i*2+1]

            amp[i][srt:end] = amp[i][srt:end] * _mult[i]

        self.resAmpLst = amp


    # 데이터 저장하기
    def saveSgnl(self):
        return np.array( [self.Y] ).T


    



                                   
    # 원 데이터, 진폭, 위상 출력 
    def getOrgn(self, _show = False):
        self.fig1    = plt.figure("원본 데이터의 FFT")
        plt1        = self.fig1.add_subplot(3,1,1)
        plt2        = self.fig1.add_subplot(3,1,2)
        plt3        = self.fig1.add_subplot(3,1,3)

        #Hz          = np.linspace(0, self.f/2, self.lngthData//2, endpoint = False)
        #time        = np.linspace(0, self.lngthData * self.T, self.lngthData, endpoint = False)

        cntSmpl     = np.linspace(0, self.lngthData, self.lngthData)
        cntHz       = np.linspace(0, self.lngthData//2, self.lngthData//2)


        # 원 데이터 출력
        plt1.plot(cntSmpl, self.orgnlData)
        plt1.grid()
        plt1.set_xlabel("Number of samples")
        plt1.set_ylabel("x(t) - DC value")
        plt1.set_title("Orignal")
        
        # 진폭 스펙트럼 출력
        plt2.stem(cntHz,self.amplt)
        plt2.grid()
        plt2.set_xlabel("Point[Hz]")
        plt2.set_ylabel("∣X(f)∣")
        plt2.set_title("Amplitude")
        
        # 위상 스펙트럼 출력
        plt3.stem(cntHz, self.phase)
        plt3.grid()
        plt3.set_xlabel("Point[Hz]")
        plt3.set_ylabel("∠X(f)")
        plt3.set_title("Phase")

        self.fig1.tight_layout()

        if (_show):
            self.fig1.show()
        
        return self.fig1


if __name__ == '__main__':
    test = backend()
    test.run()




### 선택된 구간의 fft들 ########################################################################
##    # getSlctFft같은걸로 이름 바꺼야 할듯
##    def synthetic(self):
##        cntData = len( self.intrvlData )                                                                                
##        
##        self.fig3 = plt.figure()
##        
##        for i in range(0, cntData): # 잘라낸 구간 만큼 fft 계산
##            
##            lngth = len( self.intrvlData[i] )                                                                           
##            hlfLngth = lngth // 2                                                                                       
##            fft = np.fft.fft( self.intrvlData[i] , axis = 0 ) / lngth                                                   
##            amplt = 2*abs( fft[0: hlfLngth] )                                                                           
##            phase = np.angle( fft[0: hlfLngth ], deg = False )
##            
##            self.slctFft.append(fft)                                                                                    
##            self.slctAmplt.append( amplt )                                                                              
##            self.slctPhase.append( phase )                                                                              
##            
##            
##            start = self.intrvl[i*2] // 5                                                                               
##            end = self.intrvl[i*2+1] // 5                                                                               
##            
##            cutTime = np.linspace(start*5, end*5, int(end - start), endpoint = False)                                   
##            step = 0.1/((end - start)/2)                                                                                
##            Hz = np.arange(0,0.1, step )                                                                                
##            
##
##            p = self.fig3.add_subplot(3,cntData,1+i)
##            p.plot(cutTime, self.intrvlData[i])
##            p.set_xlabel("time")
##            p.set_ylabel("x(t)")
##            p.set_title(chr(65+i))
##            p = self.fig3.add_subplot(3,cntData,2+(cntData-1)*math.ceil(2/cntData)+i)
##            p.stem(Hz,self.slctAmplt[i])
##            p.set_xlabel("Hz")
##            p.set_ylabel("∣X(f)∣")
##            p = self.fig3.add_subplot(3,cntData,3+(cntData-1)*math.ceil(3/cntData)+i)
##            p.stem(Hz,self.slctPhase[i])
##            p.set_xlabel("Hz")
##            p.set_ylabel("∠X(f)")
##
##
##        self.fig3.tight_layout()
##    # 구간의 fft들 end ##########################################################################
##
##    
##
##    # 진폭 크기순으로 뽑기 ######################################################################
##    def slctBySize(self, _N = 30):
##        self.fig4   = plt.figure()
##        
##        N           = _N   # 크기순으로 뽑을 개수
##        cntData     = len( self.intrvlData ) # N
##        Y           = 0
##        t           = np.linspace(0,12500*2,2500, endpoint = False) # N
##        t2          = np.linspace(0,12500*2,2500)
##        
##        #t = np.arange(0,12500,5)
##        #t2 = np.arange(0,12500*2,5)
##        
##        for cnt in range(cntData):  # 선택된 구간만큼 반복
##            
##            amplt = self.slctAmplt[cnt]     # [Nx1]
##            phase = self.slctPhase[cnt]     # [Nx1]
##            sortIdx = amplt.argsort(axis=0) # [Nx1]
##            size = sortIdx[-N]              # N
##            f =  (1 / ( self.intrvl[cnt*2+1] - self.intrvl[cnt*2] )) # N
##            
##            
##            amplt[ amplt < amplt[ size ] ] = 0 # [Nx1]
##            
##            for i in range(N):
##                k = sortIdx[ -(i+1) ]
##                A = amplt[k]
##                q = phase[k] + (pi/2)
##                
##                Y = Y + A*sin( 2*pi*k*f*t2  + q )
##
##        plt1 = self.fig4.add_subplot(1,1,1)
##        plt1.plot(t,self.orgnlData)
##        plt1.plot(t2,Y.T,'r')
##        plt1.grid()
##        plt1.set_xlabel("time")
##        plt1.set_ylabel("x(t)")
##        plt1.set_title("Result")
##        plt.legend(['Orignal', 'Synthesis'])
##        
####        self.fig4.show()
##        
##        self.e = (self.orgnlData  - Y.T )**2
##        self.e = np.sqrt( self.e.mean() )
##        
##        print(self.e)
##    # 진폭 크기순으로 뽑기 end ####################################################################

        

    

    
        

    
        

    

    
        
