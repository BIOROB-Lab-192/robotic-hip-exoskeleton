#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:28:47 2021

@author: lzr
"""

import numpy as np
import kqExoskeletonIO as kqio
import matplotlib.pyplot as plt

GetSec = kqio.GetSec
Ant = kqio.AntCH('com3')  # "/dev/ttyAMA0"

# 位置环目标初始化
StartHipAngle_L = Ant.Data.HipAngle_L
StartHipAngle_R = Ant.Data.HipAngle_R
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
PlotLength = 1000
PlotX = []
PlotY = []

# Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY  # 在这里更改指令
Ant.Cmd.CmdMode = kqio.CMD_SERVO_OVERRIDE

StartSec = GetSec()
UpdateSec = StartSec
UpdateSuccessSec = StartSec
UpdateState = Ant.ComState
AntConnected = (Ant.ComState == 1)

while AntConnected:

    if UpdateState == 1:
        UpdateSuccessSec = GetSec()

        # 正弦位置环，并对起始位置缓切
        SmoothRate = min(Ant.Ctrldt / SmoothTime + SmoothRate, 1)
        PlacePhase += PlaceFreq * Ant.Ctrldt
        if PlacePhase > 1:
            PlacePhase -= 1
        PlaceRef = PlaceRange * np.sin(PlacePhase * np.pi * 2)

        Ant.Cmd.Loop_L = kqio.PLACE_LOOP
        Ant.Cmd.Loop_R = kqio.PLACE_LOOP
        Ant.Cmd.Value_L = (PlaceMiddle + PlaceRef) * SmoothRate + StartHipAngle_L * (1 - SmoothRate)
        Ant.Cmd.Value_R = (PlaceMiddle - PlaceRef) * SmoothRate + StartHipAngle_R * (1 - SmoothRate)

        # 结束条件
        if UpdateSec - StartSec > 20:
            # Ant.Cmd.CmdMode = kqio.CMD_SHUTDOWN
            Ant.Disconnect()
            print('Run Finish')
            break
    elif UpdateState == -1:
        # 通讯错误
        print('Com Error')
        break
    else:
        ComErrorCnt += 1
        # 通讯失败
        if GetSec() - UpdateSuccessSec > 0.3:
            print('Error: Com Lost')
            Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY
            Ant.Disconnect()
            break

    UpdateState = Ant.Update()  # 下发指令，并获取设备状态
    ComTotalCnt += 1

    # 添加观测数据
    UpdateSec = GetSec()
    print('Run Time:%.3fs' % UpdateSec, '  Update Time:%.6fs' % Ant.Ctrldt)
    XValue = UpdateSec - StartSec
    YValue = Ant.Cmd.Value_L

    if len(PlotX) < PlotLength:
        PlotX.append(XValue)
        PlotY.append(YValue)
    else:
        PlotX[:-1] = PlotX[1:]
        PlotY[:-1] = PlotY[1:]
        PlotX[-1] = XValue
        PlotY[-1] = YValue

print('total:%.3fs' % (GetSec() - StartSec), '   Com Error Rate:%.1f%%' % (ComErrorCnt * 100 / ComTotalCnt))
plt.plot(PlotX, PlotY)
