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
    data_col = 0

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

    
    
    def __init__(self, num = 1):
        self.openData(num)
        self.dataOffset()
        self.initData()

        self.time = np.arange(0,1,1/self.f)
        self.half_f = np.arange(0, self.f, 2)

        self.selected(10)

    def openData(self,num):
        data = np.genfromtxt(r'Normal_test.csv', delimiter = ',',\
                             dtype = float, encoding = 'UTF-8')
        self.data_col = data.shape[1]
        self.data = data[1:,num]


    def dataOffset(self):
        self.dataMean = self.data.mean()
        self.data = self.data - self.dataMean

    def initData(self):
        self.f = len(self.data)
        self.fft = 2 * np.fft.fft( self.data ) / self.f
        self.amplitude = abs(self.fft[0:int(self.f / 2)])
        self.phase = np.angle(self.fft[0:int(self.f /2)] * 180 * pi)

        self.sortIndex = abs(self.fft[0:int(self.f / 2)]).argsort()
        self.sortAmp = 2 * self.fft[self.sortIndex]
        self.sortPha = self.phase[self.sortIndex]

    def selected(self, _N, _start = 30, _end = 1250):

        # 결과 값을 저장
        self.res = np.array( self.fft[0:int(self.f / 2)] )

        # 진폭 순으로 N개 데이터 선택
        N = _N
        self.res[ abs(self.res) < abs(self.res[ self.sortIndex[-N] ] )] = 0

        # 밴드 패스 필터
        start = _start
        end = _end
        self.res[start:end] = 0

        # 결과 값을 푸리에 역변환
        self.ifft = np.fft.ifft(self.res)*self.f/2

        # 출력 객체에 그래프 저장
        self.fig = Figure(figsize=(10, 7), dpi=100)

        # offset을 뺀 원본 데이터
        plt1 = self.fig.add_subplot(3,2,1)
        plt1.plot(self.time, self.data)

        # 진폭 스펙트럼
        plt3 = self.fig.add_subplot(3,2,3)
        plt3.plot(self.amplitude)

        # 위상 스펙트럼
        plt5 = self.fig.add_subplot(3,2,5)
        plt5.plot(self.phase)

        # 필터된 결과 값
        plt2 = self.fig.add_subplot(3,2,2)
        plt2.plot(self.half_f, self.ifft)

        # offset을 뺀 원본 데이터
        plt4 = self.fig.add_subplot(3,2,4)
        plt4.plot(self.data)

        # offset을 뺀 원본 데이터와 필터된 결과 데이터 비교
        plt6 = self.fig.add_subplot(3,2,6)
        plt6.plot(self.data)
        plt6.plot(self.half_f, self.ifft*self.f, 'red')



if __name__ == "__main__":
    work = Work(10)
    #work.selected(1250,1250,1250)






        
    
