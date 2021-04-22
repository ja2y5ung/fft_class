# 2021 04 19 그래프 출력부분 fig 객체에 저장하는 걸로 수정함
import numpy as np
from numpy import exp, pi
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import math
import warnings

warnings.filterwarnings(action='ignore')

class Work:

    
    data = 0          # numpy array로 csv 데이터 전체 저장하는 변수 (np.array)
    dataMean = 0      # 데이터의 offset (int)
    data_col = 0      # 데이터의 갯수
    f = 0             # 열 데이터 개수 (int)
    fft = 0           # 열 데이터를 퓨리에 변환한 값들 (np.array)
    ifft = 0          # 퓨리에 역변환 값들 (np.array)
    amplitude = 0     # 진폭 스펙트럼, (np.array)
    phase = 0         # 위상 스펙트럼, (np.array)

    sortIndex = 0     # 진폭을 크기순으로 정렬했을 때 인댁스 값들 (np.array)
    sortAmp = 0       # 진폭을 크기순으로 정렬한 값들 (np.array)
    sortPha = 0       # 위상을 진폭 크기순으로 정렬한 값들 (np.array)

    res = 0           # fft를 필터를 적용해 저장한 배열 (np.array)

    half_f = 0        # 진폭, 위상을 출력하기 0 ~ 2500을 1250개로 쪼갬 (np.array)
    time = 0          # 원본 데이터를 0 ~ 1초로 표현하기위해 1/f 간격으로 2500개 쪼갬 (np.array)

    fig = 0           # 그래프를 저장할 객체
    fig2 = 0          # A, B 구간 출력할 그래프 객체

    
    section_A = 0     # 구간A
    section_B = 0     # 구간B
    fft_A     = 0     # 구간A 푸리에 변환
    fft_B     = 0     # 구간B 푸리에 변환
    sort_A    = 0     # 구간A 정렬
    sort_B    = 0     # 구간B 정렬
    ifft_A     = 0     # 구간A 푸리에 역변환
    ifft_B    = 0     # 구간B 푸리에 역변환
    add_A_B   = 0    #구간A와 구간B를 합성

    

    
    # 생성자
    def __init__(self):
        self.run()

    # 데이터 읽어옴
    def openData(self,num):
        data = np.genfromtxt(r'Normal_test.csv', delimiter = ',',\
                             dtype = float, encoding = 'UTF-8')
        self.data_col = data.shape[1]

        self.data = data[1:,num]


    # 데이터의 평균을 뺌
    def dataOffset(self):
        self.dataMean = self.data.mean()
        self.data = self.data - self.dataMean

    # 데이터로 fft 필요한 변수들을 계산함
    def initData(self):
        self.f = len(self.data)
        self.fft = 2 * np.fft.fft( self.data ) / self.f
        self.amplitude = abs(self.fft[0:int(self.f / 2)])
        self.phase = np.angle(self.fft[0:int(self.f /2)] * 180 * pi)

        self.sortIndex = abs(self.fft[0:int(self.f / 2)]).argsort()
        self.sortAmp = 2 * self.fft[self.sortIndex]
        self.sortPha = self.phase[self.sortIndex]

        self.time = np.arange(0,1,1/self.f)
        self.half_f = np.arange(0, self.f, 2)

    # 필터 처리
    def processing(self, _N = 1250, _start = 30, _end = 1250):
        # 결과 값을 저장
        self.res = np.array( self.fft[0:int(self.f / 2)] )

        # 진폭 순으로 N개 데이터 선택
        N = _N
        self.res[ abs(self.res) < abs(self.res[ self.sortIndex[-N] ] )] = 0

        # 밴드 패스 필터
        start = _start
        end = _end
        self.res[start:end] = 0


    def cut(self, _start1, _end1, _start2, _end2):
        # A,B 구간을 잘라냄
        self.section_A = self.data[_start1:_end1]
        self.section_B = self.data[_start2:_end2]

        # A, B 푸리에 변환
        self.fft_A = np.fft.fft(self.section_A)
        self.fft_B = np.fft.fft(self.section_B)

        #A, B 푸리에 변환 후 정렬
        index_a = abs(self.fft_A[0:int(len(self.section_A)/2)]).argsort()
        index_b = abs(self.fft_B[0:int(len(self.section_B)/2)]).argsort()

        self.sort_A = self.fft_A[index_a]
        self.sort_B = self.fft_B[index_b]

        # A에서 크기순 1/3개 B에서 크기순 2/3개 선택
        self.fft_A[ abs(self.fft_A) < abs( self.fft_A[ index_a[-int(len( index_a ) * (1/3) ) ] ] ) ] = 0
        self.fft_B[ abs(self.fft_B) < abs( self.fft_B[ index_b[-int(len( index_b ) * (2/3) ) ] ] ) ] = 0
        # A, B 푸리에 역변환
        self.ifft_A = np.fft.ifft(self.fft_A)
        self.ifft_B = np.fft.ifft(self.fft_B)

        # A, B 합성
        self.add_A_B = self.ifft_A + self.ifft_B


        #plt.plot( self.ifft_B)
        #plt.show()

        

        

        

        

        
        
    # 필터된 데이터들을 fig 객체에 저장
    def saveFig(self):
        # 결과 값을 푸리에 역변환
        self.ifft = np.fft.ifft(self.res)*self.f/2

        # 출력 객체에 그래프 저장
        self.fig = Figure(figsize=(10, 7), dpi=100)
        self.fig2 = Figure(figsize=(10, 7), dpi = 100)

        # offset을 뺀 원본 데이터
        plt1 = self.fig.add_subplot(3,2,1)
        plt1.plot(self.time, self.data)


        # 진폭 스펙트럼
        plt4 = self.fig.add_subplot(3,2,3)
        plt4.stem(self.amplitude)

        # 위상 스펙트럼
        plt7 = self.fig.add_subplot(3,2,5)
        plt7.stem(self.phase)

        # 필터된 결과 값
        plt2 = self.fig.add_subplot(3,2,2)
        plt2.plot(self.half_f, self.ifft)

        # offset을 뺀 원본 데이터
        plt5 = self.fig.add_subplot(3,2,4)
        plt5.plot(self.data)

        # offset을 뺀 원본 데이터와 필터된 결과 데이터 비교
        plt8 = self.fig.add_subplot(3,2,6)
        a = np.arange(0,2500,1)
        plt8.plot(a, self.data)
        plt8.plot(self.half_f, self.ifft, 'red')

        # A구간
        plt1 = self.fig2.add_subplot(3, 1, 1)
        plt1.plot(self.section_A)

        # B구간
        plt2 = self.fig2.add_subplot(3, 1, 2)
        plt2.plot(self.section_B)

        # A, B합성
        plt3 = self.fig2.add_subplot(3, 1, 3)
        plt3.plot(self.add_A_B)


        



##        # 구간 짤라내는 코딩하는중 0421 03:32 start#
##
##        # 원 데이터 출력
##        plt.subplot(3, 3, 1)
##        origin_data = self.data
##        plt.plot(origin_data)
##        
##        # 구간A의 데이터 출력
##        plt.subplot(3, 3, 4)
##        start1 = 0
##        end1 = 1000
##        data_A = origin_data[start1:end1]
##        plt.plot(data_A)
##        
##        # 구간A의 푸리에 변환 후 정렬 출력
##        plt.subplot(3, 3, 7)
##        ffta = np.fft.fft(data_A)
##        a_index = abs(ffta[0:501]).argsort()
##        sort_ffta = ffta[a_index]
##        plt.stem(abs(sort_ffta))
##
##
##        # 구간B의 데이터 출력
##        plt.subplot(3, 3, 5)
##        start2 = 1500
##        end2 = 2500
##        data_b = origin_data[start2:end2]
##        plt.plot(data_b)
##
##        # 구간B의 푸리에 변환 후 정렬 출력
##        plt.subplot(3, 3, 8)
##        fftb = np.fft.fft(data_b)
##        b_index = abs(fftb[0:int((2500-1500)/2)]).argsort()
##        sort_fftb = fftb[b_index]
##        plt.stem(abs(sort_fftb))
##
##
##        # 구간A 데이터를 크기순 N개를 뽑음
##        
##        ffta[ abs(ffta) < abs(ffta[ a_index[-int( len(ffta)*(1/3))] ])  ] = 0
##        plt.subplot(3, 3, 3)
##        plt.plot(np.fft.ifft(ffta))
##
##        # 구간B 데이터를 크기순 N개를 뽑음
##        
##        fftb[ abs(fftb) < 50  ] = 0
##        plt.subplot(3, 3, 6)
##        plt.plot(np.fft.ifft(fftb))
##
##        # 구간A + 구간B
##        plt.subplot(3, 3, 9)
##        aADDb = np.fft.ifft(ffta)   + np.fft.ifft(fftb)
##        plt.plot(aADDb)
##        plt.show()
#end

    def run(self, num = 1, _s1 = 0, _e1 = 1000, _s2 = 1500, _e2 = 2500):
        self.openData(num)
        self.dataOffset()
        self.initData()
        self.processing()
        self.cut(_s1, _e1, _s2, _e2);
        self.saveFig()




if __name__ == "__main__":
    work = Work()
    work.processing()
