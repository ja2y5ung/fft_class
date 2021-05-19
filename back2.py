# 최선을 다해서 수정함.. 메모리 사용률에 따른 다이나믹한 연산을 하고 싶었지만.. 못했다
# 파일 저장 기능을 추가 해야
import numpy as np
from numpy.fft import fft
from numpy import zeros, array, pi, sin
from matplotlib import pyplot as plt
import warnings
#import psutil
#from sys import getsizeof

warnings.filterwarnings(action='ignore')
#PSU = psutil.Process()


Frequency   = 0.2
VRT         = 1000
HRZ         = 1000

class fuckMe:

    oFile       = 0
    oData       = 0
    oLngth      = 0
    oMean       = 0

    data        = 0
    lngth       = 0
    mean        = 0

    Fs          = 0
    Fr          = 0


    intrvl      = 0
    intrvlData  = 0

    ampLst      = []
    phsLst      = []

    Y           = 0
    tmpY        = 0
    e           = 0
    inptDC      = 0
    cntGenSmpl  = 0
    DCvalue     = 0

    


    
    def __init__(self):
        pass


    
    def loadFile(self, _path = 'Normal_test.csv'):
        print('데이터 불러오는 중..')
        #self.oFile = np.loadtxt(_path)#
        self.oFile   = np.genfromtxt( _path, delimiter = ',', dtype = float, encoding = 'UTF-8')
        self.row_name = np.genfromtxt( _path, delimiter = ',', dtype = str)[0]
        size        = len( self.oFile.shape )

        
        if( size == 1 ):
            self.columnDataLength = 1           
        else:
            self.columnDataLength = self.oFile.shape[1]
        print('데이터 불러오기 완료')


        
    def slctData(self, _num = [1]):
        lngthData   = len(self.oFile)
        cntData     = len(_num)
        
        res1    = zeros((cntData, lngthData-1))
        res2    = zeros(cntData)
        
        for i in range(cntData):
            idx     = _num[i]
            res1[i] = self.oFile[1:,idx] - res2[i]
            res2[i] = self.oFile[:,idx].mean()

        
        self.oMean = res2#
        self.oData = res1#
        self.oLngth= len(self.oData[0])


        
    def draw(self, _fig = 0, _x = [], _y = []):
        if _fig == 1:
            self.fig1 = plt.figure('원본 데이터')
            plt.cla()
            cnt = len(_y)
            for i in range(cnt):
                p   = self.fig1.add_subplot(1, 1, 1)
                plt .cla()
                p   .set_xlabel('Number of samples')
                p   .set_ylabel('x(N)')
                p   .set_title('Original')
                p   .plot(_x[i], _y[i])
                plt .legend(['Original'])
                plt .grid(True)
                self.fig1.show()


                
        elif _fig == 2:
            self.fig2   = plt.figure('원본 데이터에서 선택한 구간')
            plt  .cla()
            cnt = len(_y)
            pltLgn      = ['Original - dc']
            # 시계열 선택된 구간 갯수
            for i in range(cnt):
               p    = self.fig2.add_subplot(1, 1, 1)
               p    .set_xlabel('Number of samples')
               p    .set_ylabel('x(N)')
               p    .plot(_x[i], _y[i])
               pltLgn.append('Section ' + chr(65 + i))
               
            plt.grid(True)
            plt.legend(pltLgn)
            self.fig2.show()


            
        elif _fig == 3:         
            cnt = len(self.intrvl) // 2
            self.fig3   = plt.figure('선택된 구간의 FFT',figsize = (5*cnt,3*2))
            self.fig3.set_size_inches(5*cnt,3*2)
            plt.clf()
            # 시계열 선택된 구간 갯수
            for i in range(cnt):
                p   = self.fig3.add_subplot(2, cnt, 1 + 2*i - i)
                plt .cla()
                p   .set_title('Section ' + chr(65 + i))
                p   .set_xlabel('Interval number of samples')
                p   .set_ylabel('x(N)')
                p   .plot(_x[i], _y[2*i])
                plt .grid(True)

                p   = self.fig3.add_subplot(2, cnt, 1 + 2*i - i + cnt)
                plt .cla()
                p   .set_xlabel('Point[Hz]')
                p   .set_ylabel('X(P)')
                p   .stem(_y[2*i+1], markerfmt = 'none')
                plt.grid(True)

            self.fig3.tight_layout()
            self.fig3.show()


            
        elif _fig == 4:
            cntIntrvl   = len(self.intrvl) // 2
            cnt         = len(_y)
            self.fig3   = plt.figure('선택된 구간의 FFT', figsize = (5*cntIntrvl, 3*2))
            self.fig3   .set_size_inches(5*cntIntrvl, 3*2)
            # 시계열에서 선택된 갯수
            for i in range(cntIntrvl):
                p   = self.fig3.add_subplot(2, cntIntrvl, 1 + i//cntIntrvl + cntIntrvl + i)
                plt .cla()
                p   .stem(self.ampLst[i], markerfmt = 'none')
                
            # 주파수계열에서 선택된 갯수
            for i in range(cnt):
                k   = cnt // cntIntrvl
                p   = self.fig3.add_subplot(2, cntIntrvl, 1 + cntIntrvl + i//k )
                p   .set_xlabel('Point[Hz]')
                p   .set_ylabel('|∠X(P)|')
                p   .stem(_x[i], _y[i], linefmt = 'orange', markerfmt = 'none')

            plt.grid(True)
            self.fig3.tight_layout()
            self.fig3.show()



        elif _fig == 5:
            cnt = len(_y)
            self.fig4   = plt.figure('생성한 신호', figsize =(10,4))
            self.fig4   .set_size_inches(10,4)
            plt.cla()
            for i in range(cnt):
                p = self.fig4.add_subplot(1,1,1)
                p.set_title('Generated signal')
                p.set_xlabel('Number of samples')
                p.set_ylabel('x(N)')                
                p.plot(_x[i], _y[i].reshape(len(_x[i])))
                plt.legend(['Generated + input dc'])
                plt.grid(True)
                
            self.fig4.tight_layout()
            self.fig4.show()

        elif _fig == 6:
            cnt = len(_y)
            self.fig5 = plt.figure('에러률',figsize = (10,4))

            for i in range(cnt):
                p = self.fig5.add_subplot(1,1,1)
                pltLgn = ['Orignal', 'Generated + input dc']
                p.set_title('Error')
                p.set_xlabel('Number of samples')
                p.set_ylabel('x(N)')
                p.plot(_x[i], self.data[0] + self.mean[0])
                p.plot(_x[i],_y[i], 'r')
                plt.legend(pltLgn)
                plt.grid(True)
            self.fig5.tight_layout()
            self.fig5.show()



            
    def initData(self, maxLngth = 144000):
        lngthData   = len(self.oData[0])
        lngthRst    = lngthData % maxLngth
        cnt         = lngthData // maxLngth
        cntData     = len(self.oData)

        if lngthData >= maxLngth:
            res                 = zeros((len(self.oData), maxLngth))
            tmp                 = self.oData[:,0:cnt*maxLngth].reshape(cntData, cnt, maxLngth).sum(axis = 1, keepdims = True).reshape(cntData,maxLngth)
            tmpRst              = self.oData[:,cnt*maxLngth:].reshape(cntData, 1, lngthRst).sum(axis = 1, keepdims = True).reshape(cntData,lngthRst)

            res[:,:]            = res[:,:] + tmp
            res[:,:lngthRst]    = res[:,:lngthRst] + tmpRst
            res[:,:]            = res[:,:] / (cnt + 1)
            
            self.mean           = res.mean(axis = 1, keepdims = True)#
            self.data           = res - self.mean#
            self.lngth          = maxLngth#
        else:
            self.mean           = self.oData.mean(axis = 1, keepdims = True)#
            self.data           = self.oData - self.mean#
            self.lngth          = len(self.oData[0])#


        self.Fs                 = Frequency
        self.Fr                 = 1 / self.lngth


        
    def showData(self, original = False):
        if not original:
            end = self.lngth
            t   = np.linspace(0, end, end, endpoint = False)
            self.draw(1, [t], [self.data[0] + self.mean[0]])
            
        else:
            end = self.oLngth
            t   = np.linspace(0, end, end, endpoint = False)
            self.draw(1, [t], [self.oData[0] + self.oMean[0]])


            
    def slctIntrvl(self, _intrvl = [41234, 75643], _scale = [1]):   
        tmpT    = []
        tmpData = []
        tmpT    .append(np.linspace(0, self.lngth, self.lngth, endpoint = False))
        tmpData .append(self.data[0])
        maxIntrvl = []
        
        cntIntrvl = len(_intrvl) // 2

        # 입력이 완전하지 않은 경우
        if len(_intrvl)//2 != len(_scale):
            return -1
        
        # 시계열에서 선택된 구간 갯수
        for i in range(cntIntrvl):
            srt     = _intrvl[2*i]
            end     = _intrvl[2*i + 1]
            
            # 범위가 잘못 입력된 경우
            if(srt > end or srt > self.lngth or end > self.lngth):
                return -1

            num     = end - srt
            tmpT    .append(np.linspace(srt, end, num, endpoint = False))
            tmpData .append(self.data[0][srt:end]*_scale[i])
            maxIntrvl.append( (end - srt )//2)


        # result
        self.intrvl = _intrvl#시계열 선택된 범위
        self.intrvlData = array(tmpData[1:])#선택된 범위 안에 있는 데이터
        self.maxIntrvl = maxIntrvl
        self.draw(2, tmpT, tmpData)
        
        # 다음 실행될 메서드
        self.clcFft()


        
    def clcFft(self):
        cntIntrvl   = len(self.intrvl) // 2
        resAmp      = []
        resPhs      = []
        tmpCut      = []
        tmpData     = []
        
        # 시계열에서 선택된 구간 갯수 
        for i in range(cntIntrvl):
            half    = len(self.intrvlData[i]) // 2
            tmpFft  = fft(self.intrvlData[i]) / len(self.intrvlData[i])           
            tmpAmp  = abs(tmpFft[:half])*2
            tmpPhs  = np.angle(tmpFft[:half], deg = False)

            resAmp  .append(tmpAmp)
            resPhs  .append(tmpPhs)
            
            # 데이터 하나에 대해서만 계산함.. 일단은
            srt     = self.intrvl[2*i]
            end     = self.intrvl[2*i + 1]
            num     = end - srt
            cut     = np.linspace(srt, end, num, endpoint = False)

            tmpCut  .append(cut)
            tmpData .append(self.intrvlData[i])
            tmpData .append(tmpAmp)

            
        # result
        self.ampLst = resAmp#시계열 선택된 각 구간의 amp들
        self.phsLst = resPhs#시계열 선택된 각 구간의 phs들

        self.draw(3, tmpCut, tmpData)


        
    def slctFft(self, _intrvl = [0,100,300,500, 100,200,500,600], _scale = [1,1,1,1]):
        self.clcFft()#원본 유지를 위해 실행함

        
        cntIntrvl       = len(self.ampLst)
        cntIntrvlFft    = len(_scale) // cntIntrvl

        tmpAmp          = []
        tmpPhs          = []
        tmpCut          = []

        # 시계열에서 선택된 구간 갯수
        for i in range(cntIntrvl):
            
            # fft에서 선택된 갯수
            for j in range(cntIntrvlFft):
                srt = _intrvl[i*cntIntrvlFft*2 + 2*j]
                end = _intrvl[i*cntIntrvlFft*2 + 2*j + 1]

                tmpCut.append(np.linspace(srt, end, end-srt, endpoint = False))
                tmpAmp.append(self.ampLst[i][srt:end]*_scale[i*cntIntrvlFft+j])
                tmpPhs.append(self.phsLst[i][srt:end]*_scale[i*cntIntrvlFft+j])

            
                # result
                self.ampLst[i][srt:end] = self.ampLst[i][srt:end]*_scale[i*cntIntrvlFft+j]#주파수 범위에서 선택된 amp들만 증폭

        self.draw(4, tmpCut, tmpAmp)


        
    def genSgnl(self, _cntGenSmpl = 10000, _inptDC = 0):
        print('신호 생성중..')

        if type(_cntGenSmpl) != int:
            return -1


        cntIntrvl = len(self.intrvlData)
        Y = 0
        resY = 0
        
        #시계열에서 선택된 갯수
        for k in range(cntIntrvl):
            lngth   = len(self.intrvlData[k]) // 2
            amp     = self.ampLst[k]
            phs     = self.phsLst[k]


            f       = 1 / len(self.intrvlData[k])
            t       = np.arange(0, _cntGenSmpl, 1)
            n       = np.arange(0, lngth, 1).reshape(lngth, 1)


            # processing >>
            vrt = VRT
            hrz = HRZ
            vCnt = lngth // vrt
            hCnt = _cntGenSmpl // hrz

            tmp = zeros((vrt, _cntGenSmpl))
            print('신호 생성중..')
            # 세로 크기 vCnt+1
            for i in range(vCnt+1):

                # 세로 계산
                if i != vCnt:

                    # 가로 크기 hCnt+1
                    for j in range(hCnt+1):
                        # 가로 계산
                        if j != hCnt:
                            A   = amp.reshape(lngth, 1)[i*vrt:i*vrt+vrt]
                            W   = 2*pi*f*n[i*vrt:i*vrt+vrt]
                            P   = phs.reshape(lngth, 1)[i*vrt:i*vrt+vrt] + (pi/2)
                            tmp[:, j*hrz:j*hrz+hrz] = tmp[:, j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)

                        # 가로 나머지 계산
                        else:
                            A   = amp.reshape(lngth, 1)[i*vrt:i*vrt+vrt]
                            W   = 2*pi*f*n[i*vrt:i*vrt+vrt]
                            P   = phs.reshape(lngth, 1)[i*vrt:i*vrt+vrt] + (pi/2)
                            tmp[:, j*hrz:] = tmp[:, j*hrz:] + A*sin(W*t[j*hrz:] + P)

                            
                # 세로 나머지 계산
                else:

                    # 가로 크기 hCnt+1
                    for j in range(hCnt+1):
                        # 가로 계산
                        if j != hCnt:
                            A       = amp.reshape(lngth, 1)[i*vrt:]
                            W       = 2*pi*f*n[i*vrt:]
                            P       = phs.reshape(lngth, 1)[i*vrt:] + (pi/2)
                            tmp[:len(A),j*hrz:j*hrz+hrz] = tmp[:len(A),j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)

                        # 가로 나머지 계산
                        else:
                            A       = amp.reshape(lngth, 1)[i*vrt:]
                            W       = 2*pi*f*n[i*vrt:]
                            P       = phs.reshape(lngth, 1)[i*vrt:] + (pi/2)
                            tmp[:len(A),j*hrz:j*hrz+hrz] = tmp[:len(A),j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)



        #Result
        self.Y = tmp.sum(axis=0) + _inptDC#
        self.cntGenSmpl = _cntGenSmpl
        self.tmpY = np.copy(self.Y)
        self.draw(5, [t], [self.Y])
        
        print('신호 생성 완료')


    def slctGenIntrvl(self, _intrvl = [0,200,1000,2500], _inptDC = [0,2] ):
        fig = plt.figure('test')
        p   = fig.add_subplot(1,1,1)
        
        # 입력이 완전하지 안은 경우
        if len(_intrvl)//2 != len(_inptDC):
            return -1

        # 범위 입력이 잘못된 경우
        cnt = len(_intrvl) // 2
        for i in range(cnt):
            srt = _intrvl[2*i]
            end = _intrvl[2*i+1]
            if end-srt == 0 or srt > end:
                return -1

        res = np.zeros(self.cntGenSmpl)
        t   = np.linspace(0,self.cntGenSmpl, self.cntGenSmpl)

        cntInptDC = len(_inptDC)

        if cntInptDC == 1:
            #Result
            tmp     = np.linspace(0, len(t), len(t), endpoint = False )
            res[:]  = tmp
            self.Y  = self.tmpY.reshape(len(t)) + res
            self.draw(5,[t], [self.Y])
        elif cntInptDC != 1:
            srt = _intrvl[1]
            end = _intrvl[2]
        
            tmp             = np.linspace(_inptDC[0], _inptDC[1], end-srt, endpoint = False)
            res[:srt]       = tmp[0]
            res[srt:end]    = tmp
            res[end:]       = tmp[-1]

            #Result
            self.DCvalue = res
            self.Y = self.tmpY.reshape(len(t)) + res
            self.inptDC = _inptDC
            self.draw(5,[t], [self.Y])

        
        




    def getError(self):
        print('에러 계산중..')
        cntIntrvl = len(self.intrvlData)
        Y = 0
        resY = 0
        
        #시계열에서 선택된 갯수
        for k in range(cntIntrvl):
            lngth   = len(self.intrvlData[k]) // 2
            amp     = self.ampLst[k]
            phs     = self.phsLst[k]


            f       = 1 / len(self.intrvlData[k])
            t       = np.arange(0, self.lngth, 1)
            n       = np.arange(0, lngth, 1).reshape(lngth, 1)


            # processing >>
            vrt = VRT
            hrz = HRZ
            vCnt = lngth // vrt
            hCnt = self.lngth // hrz

            tmp = zeros((vrt, self.lngth))
            print('에러 계산중..')
            # 세로 크기 vCnt+1
            for i in range(vCnt+1):

                # 세로 계산
                if i != vCnt:
                    # 가로 크기 hCnt+1
                    for j in range(hCnt+1):
                        # 가로 계산
                        if j != hCnt:
                            A   = amp.reshape(lngth, 1)[i*vrt:i*vrt+vrt]
                            W   = 2*pi*f*n[i*vrt:i*vrt+vrt]
                            P   = phs.reshape(lngth, 1)[i*vrt:i*vrt+vrt] + (pi/2)
                            tmp[:, j*hrz:j*hrz+hrz] = tmp[:, j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)

                        # 가로 나머지 계산
                        else:
                            A   = amp.reshape(lngth, 1)[i*vrt:i*vrt+vrt]
                            W   = 2*pi*f*n[i*vrt:i*vrt+vrt]
                            P   = phs.reshape(lngth, 1)[i*vrt:i*vrt+vrt] + (pi/2)
                            tmp[:, j*hrz:] = tmp[:, j*hrz:] + A*sin(W*t[j*hrz:] + P)

                            
                # 세로 나머지 계산
                else:

                    # 가로 크기 hCnt+1
                    for j in range(hCnt+1):
                        # 가로 계산
                        if j != hCnt:
                            A       = amp.reshape(lngth, 1)[i*vrt:]
                            W       = 2*pi*f*n[i*vrt:]
                            P       = phs.reshape(lngth, 1)[i*vrt:] + (pi/2)
                            tmp[:len(A),j*hrz:j*hrz+hrz] = tmp[:len(A),j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)

                        # 가로 나머지 계산
                        else:
                            A       = amp.reshape(lngth, 1)[i*vrt:]
                            W       = 2*pi*f*n[i*vrt:]
                            P       = phs.reshape(lngth, 1)[i*vrt:] + (pi/2)
                            tmp[:len(A),j*hrz:j*hrz+hrz] = tmp[:len(A),j*hrz:j*hrz+hrz] + A*sin(W*t[j*hrz:j*hrz+hrz] + P)
        


                    
        

        #Result
        

        if len(self.DCvalue) // self.lngth == 0:
            tmpDC = []
            i = 0;
            while len(tmpDC) != self.lngth:
                
                tmpDC = np.hstack((tmpDC,self.DCvalue[i]))
                i = i +1
                if( i >= len(self.Y)):
                    i = 0
            
            eY      = tmp.sum(axis = 0) + tmpDC
            e       = (self.data[0] - eY)**2
            self.e  = np.sqrt(e.sum())
            self.draw(6,[t], [eY])
            breakpoint()
            print('에러 계산 완료')
        else:
            tmpDC = []
            i = 0
            while len(tmpDC) != self.lngth:
                tmpDC = np.hstack((tmpDC, self.DCvalue[i]))
                i = i+1
                if i >= self.lngth:
                    i = 0

            
            eY      = tmp.sum(axis = 0) + tmpDC
            e       = (self.data[0] - eY)**2
            self.e  = np.sqrt(e.sum())

            self.draw(6,[t], [eY])
            print('에러 계산 완료')

        
         



if __name__ == '__main__':

    fuck = fuckMe()
    fuck.loadFile()
    fuck.slctData()
    fuck.initData()
    fuck.showData()

    #fuck.slctIntrvl([0,1000,4000,5000],[1,1])
    #fuck.slctFft([0,100,1000,2000,0,200,1000,4000], [1,1,1,1])
    
    #fuck.slctIntrvl([0,5000,  10000,20000,  6000,7000],[1,1,1])
    #fuck.slctFft([0,100,1000,2000,  0,200,1000,4000,  0,100,300,500], [1,1,  1,1,  1,1])

    #fuck.slctIntrvl([0,12800], [1])
    #fuck.slctFft([0,12800//2], [1])
    #fuck.genSgnl(12800)

    #fuck.slctIntrvl([0,14400],[1])
    #fuck.slctFft([0,14400//2], [1])
    #fuck.genSgnl(14400)

    fuck.slctIntrvl([0,2500])
    fuck.slctFft([0,2500//2], [1])
    fuck.genSgnl(3000)
    fuck.slctGenIntrvl([0,300,900,1000],[244,280])
    
    fuck.getError()
