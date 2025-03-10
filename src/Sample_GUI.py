#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:28:47 2021

@author: lzr
"""

# from pyqtgraph.Qt import QtGui, QtCore<- Deprecated library
from pyqtgraph.Qt  import QtWidgets 

import pyqtgraph as pg
import numpy as np
import threading
import kqExoskeletonIO as kqio

#PlotLength = 500
#PlotLength = 1000
#Added this

# Total Runtime in seconds
Hertz = 25
total_runtime = 1
PlotLength = 25*total_runtime


class ExoGUI(object):
    def __init__(self):
        self.GetSec = kqio.GetSec
        self.Ant = kqio.AntCH('com6')  # "/dev/ttyAMA0"
        self.StartSec = self.GetSec()
        self.GUI_Break = 0

        self.PlotTime = np.linspace(-1, 0, PlotLength)
        self.Loop_L = [0] * PlotLength
        self.Loop_R = [0] * PlotLength
        self.Value_L = [0] * PlotLength
        self.Value_R = [0] * PlotLength
        # self.Battery = [self.Ant.Data.Battery] * PlotLength
        # self.BackIncl = [self.Ant.Data.BackIncl] * PlotLength
        self.HipAngle_L = [self.Ant.Data.HipAngle_L] * PlotLength
        self.HipAngle_R = [self.Ant.Data.HipAngle_R] * PlotLength
        self.HipSpeed_L = [self.Ant.Data.HipSpeed_L] * PlotLength
        self.HipSpeed_R = [self.Ant.Data.HipSpeed_R] * PlotLength
        self.HipTor_L = [self.Ant.Data.HipTor_L] * PlotLength
        self.HipTor_R = [self.Ant.Data.HipTor_R] * PlotLength
        self.Voltage = [self.Ant.Data.Voltage] * PlotLength
        self.Current = [self.Ant.Data.Current] * PlotLength
        # self.AccX = [self.Ant.Data.AccX] * PlotLength
        # self.AccY = [self.Ant.Data.AccY] * PlotLength
        # self.AccZ = [self.Ant.Data.AccZ] * PlotLength
        # self.GyroX = [self.Ant.Data.GyroX] * PlotLength
        # self.GyroY = [self.Ant.Data.GyroY] * PlotLength
        # self.GyroZ = [self.Ant.Data.GyroZ] * PlotLength

        # 设置窗口参数
        pg.setConfigOptions(antialias=False, background='w', foreground='k')
        #self.app = QtGui.QApplication([]) <- Deprecated library 
        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Kenqing Exoskeleton Observer')
        self.win.resize(1000, 600)

        # 绘图
        self.p_Att = self.win.addPlot(title="Device Attitude")
        self.d_Leg_L = self.p_Att.plot(pen='b', symbolBrush='b', symbolSize=10, symbolPen='g')
        self.d_Leg_R = self.p_Att.plot(pen='r', symbolBrush='r', symbolSize=10, symbolPen='g')
        self.d_Back = self.p_Att.plot(pen='g', symbolBrush='g', symbolSize=10, symbolPen='g')
        self.p_Att.setXRange(-0.4, 0.4)
        self.p_Att.setYRange(-0.4, 0.4)
        self.p_Att.setAspectLocked()
        self.p_Att.showGrid(x=True, y=True)
        # self.p_Att.hideAxis('bottom')
        # self.p_Att.hideAxis('left')

        self.p_Angle = self.win.addPlot(title="Joint Angle")
        self.d_Angle_L = self.p_Angle.plot(pen='b')
        self.d_Angle_R = self.p_Angle.plot(pen='r')

        self.win.nextRow()

        self.p_Voltage = self.win.addPlot(title="Battery Voltage")
        self.d_Voltage = self.p_Voltage.plot(pen='b')
        self.p_Voltage.setXLink(self.p_Angle)

        self.p_Speed = self.win.addPlot(title="Joint Speed")
        self.d_Speed_L = self.p_Speed.plot(pen='b')
        self.d_Speed_R = self.p_Speed.plot(pen='r')
        self.p_Speed.setXLink(self.p_Angle)

        self.win.nextRow()

        self.p_Current = self.win.addPlot(title="Battery Current")
        self.d_Current = self.p_Current.plot(pen='r')
        self.p_Current.setXLink(self.p_Angle)

        self.p_Torque = self.win.addPlot(title="Joint Torque")
        self.d_Torque_L = self.p_Torque.plot(pen='b')
        self.d_Torque_R = self.p_Torque.plot(pen='r')
        self.p_Torque.setXLink(self.p_Angle)

        self.win.nextRow()
        self.p_Loop = self.win.addPlot(title="Target Loop")
        self.d_Loop_L = self.p_Loop.plot(pen='b')
        self.d_Loop_R = self.p_Loop.plot(pen='r')
        self.p_Loop.setXLink(self.p_Angle)

        self.p_Value = self.win.addPlot(title="Target Value")
        self.d_Value_L = self.p_Value.plot(pen='b')
        self.d_Value_R = self.p_Value.plot(pen='r')
        self.p_Value.setXLink(self.p_Angle)
        

    def StopNow(self):
        self.GUI_Break = 1

    def CtrlLoop(self):
        # 激活控制指令
        self.Ant.Cmd.CmdMode = kqio.CMD_SERVO_OVERRIDE  # CMD_OBS_ONLY
        # self.Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY
        # 位置环目标初始化
        StartHipAngle_L = self.Ant.Data.HipAngle_L
        StartHipAngle_R = self.Ant.Data.HipAngle_R
        SmoothRate = 0
        SmoothTime = 2

        PlaceFreq = 0.5
        PlaceMiddle = 0.5 * kqio.PLACE_MAX_VALUE
        PlaceRange = 0.25 * kqio.PLACE_MAX_VALUE
        PlacePhase = 0
        PlaceRef = 0
        # 观测数据
        ComTotalCnt = 1
        ComErrorCnt = 0

        self.StartSec = self.GetSec()
        UpdateSuccessSec = self.StartSec
        UpdateState = self.Ant.ComState
        AntConnected = (self.Ant.ComState == 1)

        while AntConnected:
            if UpdateState == 1:
                UpdateSuccessSec = self.GetSec()
                self.__ObsUpdate()

                # 正弦位置环，并对起始位置缓切
                SmoothRate = min(self.Ant.Ctrldt / SmoothTime + SmoothRate, 1)
                PlacePhase += PlaceFreq * self.Ant.Ctrldt
                if PlacePhase > 1:
                    PlacePhase -= 1
                PlaceRef = PlaceRange * np.sin(PlacePhase * np.pi * 2)

                self.Ant.Cmd.Loop_L = kqio.PLACE_LOOP
                self.Ant.Cmd.Loop_R = kqio.PLACE_LOOP
                self.Ant.Cmd.Value_L = (PlaceMiddle + PlaceRef) * SmoothRate + StartHipAngle_L * (1 - SmoothRate)
                self.Ant.Cmd.Value_R = (PlaceMiddle - PlaceRef) * SmoothRate + StartHipAngle_R * (1 - SmoothRate)

                # 结束条件
                #if UpdateSuccessSec - self.StartSec > 20 or self.GUI_Break: <- OG Line
                if UpdateSuccessSec - self.StartSec > total_runtime or self.GUI_Break:
                    # self.Ant.Cmd.CmdMode = kqio.CMD_SHUTDOWN  # 运行结束后关机
                    self.Ant.Disconnect()
                    print('Run Finish')
                    break
            elif UpdateState == -1:
                # 通讯错误
                print('Com Error')
                break
            else:
                ComErrorCnt += 1
                # 通讯失败
                if self.GetSec() - UpdateSuccessSec > 0.3:
                    print('Error: Com Lost')
                    self.Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY
                    self.Ant.Disconnect()
                    break

            UpdateState = self.Ant.Update()  # 下发指令，并获取设备数据
            ComTotalCnt += 1
            # print('Run Time:%.3fs' % self.GetSec(), '  Update Time:%.6fs' % self.Ant.Ctrldt)

        # 控制循环结束后显示运行时间及通讯错误率
        print('total:%.3fs' % (self.GetSec() - self.StartSec), '   Com Error Rate:%.1f%%' % (ComErrorCnt * 100 / ComTotalCnt))

    def __ObsUpdate(self):
        # 添加观测数据
        self.PlotTime[:-1] = self.PlotTime[1:]
        self.PlotTime[-1] = self.GetSec() - self.StartSec

        self.Loop_L[:-1] = self.Loop_L[1:]
        self.Loop_L[-1] = self.Ant.Cmd.Loop_L

        self.Loop_R[:-1] = self.Loop_R[1:]
        self.Loop_R[-1] = self.Ant.Cmd.Loop_R

        self.Value_L[:-1] = self.Value_L[1:]
        self.Value_L[-1] = self.Ant.Cmd.Value_L

        self.Value_R[:-1] = self.Value_R[1:]
        self.Value_R[-1] = self.Ant.Cmd.Value_R

        self.HipAngle_L[:-1] = self.HipAngle_L[1:]
        self.HipAngle_L[-1] = self.Ant.Data.HipAngle_L

        self.HipAngle_R[:-1] = self.HipAngle_R[1:]
        self.HipAngle_R[-1] = self.Ant.Data.HipAngle_R

        self.HipSpeed_L[:-1] = self.HipSpeed_L[1:]
        self.HipSpeed_L[-1] = self.Ant.Data.HipSpeed_L

        self.HipSpeed_R[:-1] = self.HipSpeed_R[1:]
        self.HipSpeed_R[-1] = self.Ant.Data.HipSpeed_R

        self.HipTor_L[:-1] = self.HipTor_L[1:]
        self.HipTor_L[-1] = self.Ant.Data.HipTor_L

        self.HipTor_R[:-1] = self.HipTor_R[1:]
        self.HipTor_R[-1] = self.Ant.Data.HipTor_R

        self.Voltage[:-1] = self.Voltage[1:]
        self.Voltage[-1] = self.Ant.Data.Voltage

        self.Current[:-1] = self.Current[1:]
        self.Current[-1] = self.Ant.Data.Current

        self.d_Value_L.setData(self.PlotTime, self.Value_L)
        self.d_Value_R.setData(self.PlotTime, self.Value_R)

        self.d_Loop_L.setData(self.PlotTime, self.Loop_L)
        self.d_Loop_R.setData(self.PlotTime, self.Loop_R)

        self.d_Angle_L.setData(self.PlotTime, self.HipAngle_L)
        self.d_Angle_R.setData(self.PlotTime, self.HipAngle_R)

        self.d_Speed_L.setData(self.PlotTime, self.HipSpeed_L)
        self.d_Speed_R.setData(self.PlotTime, self.HipSpeed_R)

        self.d_Torque_L.setData(self.PlotTime, self.HipTor_L)
        self.d_Torque_R.setData(self.PlotTime, self.HipTor_R)

        self.d_Leg_L.setData([0, np.sin(self.Ant.Data.HipAngle_L + kqio.ANGLE_OFFSET + self.Ant.Data.BackIncl - np.pi) * 0.4], [0, np.cos(self.Ant.Data.HipAngle_L + kqio.ANGLE_OFFSET + self.Ant.Data.BackIncl - np.pi) * -0.4])
        self.d_Leg_R.setData([0, np.sin(self.Ant.Data.HipAngle_R + kqio.ANGLE_OFFSET + self.Ant.Data.BackIncl - np.pi) * 0.4], [0, np.cos(self.Ant.Data.HipAngle_R + kqio.ANGLE_OFFSET + self.Ant.Data.BackIncl - np.pi) * -0.4])
        self.d_Back.setData([0, np.sin(self.Ant.Data.BackIncl) * 0.3], [0, np.cos(self.Ant.Data.BackIncl) * -0.3])

        self.d_Voltage.setData(self.PlotTime, self.Voltage)
        self.d_Current.setData(self.PlotTime, self.Current)
        print(self.PlotTime[-1])
        


if __name__ == '__main__':
    import sys

    # 开启多线程运行与设备通讯
    AntGUI = ExoGUI()
    th1 = threading.Thread(target=AntGUI.CtrlLoop)
    th1.start()

    #
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    # 如果关闭GUI窗口，停止运行
    AntGUI.StopNow()
