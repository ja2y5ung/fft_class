# 2021 04 27 그래프의 축 값 계산, 그래프가 누적 오차가 생기는 듯한 현상 발견, 코드 길이 간결화
# 2021 05 03 교수님 요구 사항 수정 : GUI  개선, 잘라낸 구간 증폭, 신호 생성 구간 설정, 데이터 저장, 에러처리
# 2021 05 04 시발 왜 저장이 안됫지 시발 시발
# 2021 05 05 11:16 어린이날, 14:52 교수님 피드벡 -> 진폭에서 슬라이스, 피규어에 제목, 20:43 -> 집에와서 수정하려고 함
# 2021 05 06 01:30 새벽 그래프 겹치게 그려서 좀 변화한게 잘 보이도록 수정함, 해야할 것 : 오류 계산과 원그래프와 비교 그래프
# 2021 05 06 14:14 slctItrvl 메서드에서 리스트 범위를 넘는 문제 해
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
    frqRez                = 0   # 주파수 해상도
    T                     = 0   # 주기            
    
    fftData               = 0   # 원 데이터를 푸리에 변환
    amplt                 = 0   # 원 데이터의 진폭 스펙트럼
    phase                 = 0   # 원 데이터의 위상 스펙트럼

    intrvlData            = []  #잘라낸 구간의 값들
    intrvl                = []  #잘려진 구간들의 위치

    ampLst                = []  # 잘라낸 구간들의 진폭
    phsLst                = []  # 잘라낸 구간들의 위상

    resAmpLst             = [] # 결과를 계속 바꺼 저장할 변수
    maxIntrvl             = []

    error                 = 0   # 에러율

    fig1                  = 0   # 그래프 저장할 객체
    fig2                  = 0   # 잘라낸 그래프 저장할 객체
    fig3                  = 0   # 잘라낸 그래프 합성하기
    fig4                  = 0   # 잘라낸 구간의 fft
    fig5                  = 0   # 에러 그래프

    Y                     = 0   # 최종결과
    eY                    = 0   #에러 비교 
    


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

        plt.cla()



  
    # 변수 초기화
    def initData(self):
        self.lngthData      = len( self.orgnlData )
        self.dcData         = self.orgnlData.mean()
        self.orgnlData      = np.array( [self.orgnlData - self.dcData] ).T

        self.fftData        = np.fft.fft( self.orgnlData, axis = 0) / self.lngthData
        self.amplt          = 2 * abs( self.fftData[0:self.lngthData//2] )
        self.phase          = np.angle( self.fftData[0:self.lngthData//2], deg = False)

        self.Fs             = 0.2
        self.T              = 1 / self.Fs
        self.frqRez         = self.Fs / self.lngthData

    

    # 구간 잘라내기 
    def getIntrvl(self, _intrvl = [100,200], _show = True ):

        
        
        self.fig2 = plt.figure("시계열 잘라낸 구간")
        plt.cla()
        p = self.fig2.add_subplot(1,1,1)
        p.plot(np.arange(0, 2500,1), self.orgnlData)
        
        
        intrvLst    = []                    # 잘라낸 구간들을 저장
        pltLgn      = ['Original']          # 그래프 레전드
        cntIntrvl   = len(_intrvl) // 2     # 잘라낸 구간 갯수
        maxIntrvl   = []

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
            maxIntrvl.append(num)
            cutSmpl = np.linspace(start, end, num, endpoint = False  )


            #잘라내고 변수에 저장
            intrvLst.append(  data[start:end]  )

            
            # 그래프를 리스트에 저장         
            p.plot(cutSmpl, intrvLst[i])
            p.set_xlabel(" Number of samples ")
            p.set_ylabel(" x(t) - dcData " )
            pltLgn.append("Section " + chr(65+i) )

            
        plt.grid()
        plt.legend(pltLgn)
        
        
        self.intrvlData = intrvLst                                                                                   
        self.intrvl = _intrvl
        self.maxIntrvl = maxIntrvl
        
        self.fig2.tight_layout()

        if( _show ):
            self.fig2.show()
            
        self.fftIntrvl()
        
        return self.fig2


    # 구간 합성하기 
    def genSgnl(self, _cntSmpl = 2500, _dc = 0, _show = True):
        self.fig3   = plt.figure("합성 결과")
        plt.cla()
        cnt         = len( self.intrvlData )

        self.

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

        self.Y = Y + _dc
        self.eY = eY + _dc
        p       = self.fig3.add_subplot(1,1,1)
        p.plot(self.Y,)
        p.set_xlabel("Number of samples")
        p.set_ylabel("x(t)")
        p.set_title(" Generate Signal ")
        plt.grid()

        eY = eY.reshape(( self.lngthData,1))

        e = ((self.orgnlData + _dc) - (eY + _dc) )**2
        e = np.sqrt( e.mean() )

        self.error = e

        

        if (_show):
            self.fig3.show()
        
        
        return self.fig3


    # 에러 그래프 출력
    def showErorr(self, _dc = 0):
        self.fig5 = plt.figure(" 신호 오차 " )
        plt.cla()

        p = self.fig5.add_subplot(1,1,1)
        t = np.linspace(0, self.lngthData, self.lngthData, endpoint = False )
        p.plot(t, self.orgnlData + _dc)
        p.plot(t, self.eY, 'r')
        p.set_title("Error")
        p.set_xlabel("Number of samples")
        p.set_ylabel("x(t)")
        plt.grid()

        plt.legend(['Original', 'Result'])

        self.fig5.show()
        
        
        

    # 잘라낸 구간 fft 구하기
    def fftIntrvl(self):

        self.fig4 = plt.figure("잘라낸 구간들의 진폭")
        plt.clf()
        fftLst          = []
        ampLst          = []
        phsLst          = []

        
        data            = self.intrvlData
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
            p.set_title( 'Section ' + chr(65 + i ) )
            p.set_xlabel("Interval samples")
            p.set_ylabel("x(t) - dcData")
            plt.grid()

            p = self.fig4.add_subplot(2, cnt, 1 + 2*i + cnt - i )
            p.stem( ampLst[i], markerfmt  = 'none' )
            p.set_xlabel("Point[Hz]")
            p.set_ylabel("∣X(f)∣")
            plt.grid()

        self.fig4.tight_layout()

        self.fig4.show()

        self.ampLst = ampLst
        self.phsLst = phsLst


    # 잘라낸 구간 선택하기
    def slctFft(self, _intrvl = [20,30], _mult = [1]):
        
        self.fig4 = plt.figure("잘라낸 구간들의 진폭")
        amp = self.ampLst
        phs = self.phsLst


        cnt = len( amp ) 

        for i in range(cnt):
            p               = self.fig4.add_subplot(2, cnt, 1+2*i+cnt-i)
            Hz              = np.linspace(0, len(self.intrvlData[i])//2, len(self.intrvlData[i])//2, endpoint = False )
            
            for j in range( len( _intrvl ) //(2 * cnt ) ):
                
                srt = _intrvl[2*i+j*cnt] 
                end = _intrvl[2*i+j*cnt+1]


                amp[i][srt:end] = amp[i][srt:end] * _mult[i*(len(_mult)//2)+j]

                
                plt.cla()
                p.stem(Hz, amp[i], markerfmt = 'none')


                if ( len( _mult ) // 2 ) == 0:
                    srt = _intrvl[2*i] 
                    end = _intrvl[2*i+1]
                    cutHz = np.linspace(srt, end, end - srt, endpoint = False )
                    p.stem(cutHz, amp[i][srt:end], linefmt = 'orange', markerfmt = 'none' )
                    p.set_ylabel("∣X(f)∣")
                    p.set_xlabel('Point[Hz]')
                    plt.grid()


                for k in range( len( _mult ) // 2 ):
                    srt = _intrvl[2*i+k*cnt] 
                    end = _intrvl[2*i+k*cnt+1]
                    cutHz = np.linspace(srt, end, end - srt, endpoint = False )
                    p.stem(cutHz, amp[i][srt:end], linefmt = 'orange', markerfmt = 'none' )
                    p.set_ylabel("∣X(f)∣")
                    p.set_xlabel('Point[Hz]')
                    plt.grid()

                    
        self.fig4.show()

        
        self.resAmpLst = amp


    # 데이터 저장하기
    def saveSgnl(self):
        return np.array( [self.Y] ).T

                               
    # 원 데이터, 진폭, 위상 출력 
    def getOrgn(self, _show = False):
        self.fig1    = plt.figure("원본 데이터의 FFT")
        plt.cla()

        #Hz          = np.linspace(0, self.f/2, self.lngthData//2, endpoint = False)
        #time        = np.linspace(0, self.lngthData * self.T, self.lngthData, endpoint = False)

        cntSmpl     = np.linspace(0, self.lngthData, self.lngthData)
        cntHz       = np.linspace(0, self.lngthData//2, self.lngthData//2)


        # 원 데이터 출력
        p = self.fig1.add_subplot(3,1,1)
        plt.cla()
        p.plot(cntSmpl, self.orgnlData)
        p.grid()
        p.set_xlabel("Number of samples")
        p.set_ylabel("x(t) - DC value")
        p.set_title("Orignal")
        
        # 진폭 스펙트럼 출력
        p = self.fig1.add_subplot(3,1,2)
        p.stem(cntHz,self.amplt)
        p.grid()
        p.set_xlabel("Point[Hz]")
        p.set_ylabel("∣X(f)∣")
        p.set_title("Amplitude")
        
        # 위상 스펙트럼 출력
        p = self.fig1.add_subplot(3,1,3)
        p.stem(cntHz, self.phase)
        p.grid()
        p.set_xlabel("Point[Hz]")
        p.set_ylabel("∠X(f)")
        p.set_title("Phase")

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

        

    

    
        

    
        

    

    
        
