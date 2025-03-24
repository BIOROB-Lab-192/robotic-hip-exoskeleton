#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:47:33 2021

@author: lzr
"""
import serial
import struct
import time

CMD_HEAD = 0xABCD  # Command header
CMD_LENGTH = 28  # Command length
DATA_HEAD = [0xBA, 0xDC]  # Data header
DATA_LENGTH = 68  # Data length

CMD_OBS_ONLY = 0  # Observe data only
CMD_INNER_DUAL_LEG_MODE = 11  # Internal algorithm mode, can adjust Force and Speed
CMD_SERVO_OVERRIDE = 200  # Directly control the servo motor
CMD_SHUTDOWN = 250  # Shutdown

TOR_LOOP = 1  # Torque control mode
TOR_MAX_VALUE = 15  # Maximum torque: 15Nm

SPEED_LOOP = 2  # Speed control mode
SPEED_MAX_VALUE = 12  # Maximum speed: 12rad/s

PLACE_LOOP = 3  # Position control mode, 0° is the lower limit
PLACE_MAX_VALUE = 2.62  # Maximum joint position: 150°

ANGLE_OFFSET = -0.61  # When standing, the hip joint is at 35°


def GetSec():
    return time.perf_counter()


def GetMs():
    return int(time.perf_counter_ns() / 1e6)


def GetUs():
    return int(time.perf_counter_ns() / 1e3)


class CmdStruct(object):
    def __init__(self):
        self.CmdCnt = 0
        self.CmdGapMs = 10
        self.CmdMode = CMD_OBS_ONLY  # CMD_OBS_ONLY, CMD_INNER_DUAL_LEG_MODE, CMD_SERVO_OVERRIDE, CMD_SHUTDOWN
        self.ForceValue = 0  # Effective in CMD_INNER_DUAL_LEG_MODE, the value must change and not exceed 20
        self.SpeedValue = 0  # Effective in CMD_INNER_DUAL_LEG_MODE, the value must change and not exceed 20

        self.Loop_L = 0  # Effective in CMD_SERVO_OVERRIDE mode, supports TOR_LOOP, SPEED_LOOP, PLACE_LOOP
        self.Loop_R = 0
        self.Value_L = 0
        self.Value_R = 0


class DataStruct(object):
    def __init__(self):
        self.PowerKeyState = 0  # Key state: 0 means released, 1 means pressed
        self.FuncKeyState = 0
        self.UpKeyState = 0
        self.DownKeyState = 0

        self.DeviceError = 0  # Device status: 1 means abnormal
        self.Battery = 0  # Battery percentage
        self.DeviceMs = 0  # Milliseconds after startup

        self.BackIncl = 0.0  # Back tilt angle
        self.HipAngle_L = 0.0
        self.HipAngle_R = 0.0
        self.HipSpeed_L = 0.0
        self.HipSpeed_R = 0.0
        self.HipTor_L = 0.0
        self.HipTor_R = 0.0

        self.Voltage = 0.0
        self.Current = 0.0
        self.AccX = 0.0
        self.AccY = 0.0
        self.AccZ = 0.0
        self.GyroX = 0.0
        self.GyroY = 0.0
        self.GyroZ = 0.0


class AntCH(object):
    # Create a Device Object
    def __init__(self, ComPort):

        self.__LastUs = GetUs()
        self.__LastDeviceMs = 0
        self.ComState = -1
        self.Ctrldt = 0.01
        self.Cmd = CmdStruct()
        self.Data = DataStruct()

        try:
            self.__s = serial.Serial(
                ComPort, 115200, timeout=0.007, parity=serial.PARITY_NONE
            )
            print("Serial Open Success")
            self.__s.flushInput()
            self.__s.flushOutput()
            time.sleep(0.1)
            for _ in range(20):
                if self.__SerialDataIO() == 1:
                    self.ComState = 1
                    print("Serial Connect Success")
                    break
            if self.ComState == 1:
                self.__s.read_all()
            else:
                print("Connect Fail, Device No Response")
                self.ComState = 1
                self.__CloseSerial()
        except Exception as e:
            print("Serial Init Fail:" + str(e))

    def Disconnect(self):
        if self.Cmd.CmdMode != CMD_SHUTDOWN:
            self.Cmd.CmdMode = CMD_OBS_ONLY
        if self.ComState == 1:
            for _ in range(10):
                if self.__SerialDataIO() == 1:
                    break
        self.__CloseSerial()

    def Update(self):
        if self.ComState == 1:
            return self.__SerialDataIO()
        else:
            time.sleep(0.008)
            if self.ComState == 0:
                print("Serial Closed")
                return 0
            else:
                print("Serial Error")
                return -1

    def __CloseSerial(self):
        if self.ComState == 1:
            try:
                self.__s.close()
                self.ComState = 0
                print("Serial Close Success")
            except Exception:
                self.ComState = -1
                print("Serial Close Fail", str(Exception))
        elif self.ComState == 0:
            print("Serial Already Closed")
        else:
            print("Serial Close Fail")

    def __U16XorCheck(self, Data):
        # XOR check for 16-bit data
        Check1 = 0
        Check2 = 0
        if len(Data) % 2 == 0:
            for i in range(len(Data)):
                if i % 2 == 0:
                    Check1 = Check1 ^ Data[i]
                else:
                    Check2 = Check2 ^ Data[i]

        return struct.pack("<2B", Check1, Check2)

    def __CmdCheck(self, Loop, Value):
        Fix_Loop = Loop
        Fix_Value = Value

        if Fix_Loop == TOR_LOOP:
            # Torque limit
            if Fix_Value > TOR_MAX_VALUE:
                Fix_Value = TOR_MAX_VALUE
            elif Fix_Value < -TOR_MAX_VALUE:
                Fix_Value = -TOR_MAX_VALUE

        elif Fix_Loop == SPEED_LOOP:
            # Speed limit
            if Fix_Value > SPEED_MAX_VALUE:
                Fix_Value = SPEED_MAX_VALUE
            elif Fix_Value < -SPEED_MAX_VALUE:
                Fix_Value = -SPEED_MAX_VALUE
        elif Fix_Loop == PLACE_LOOP:
            # Position limit
            if Fix_Value > PLACE_MAX_VALUE:
                Fix_Value = PLACE_MAX_VALUE
            elif Fix_Value < 0:
                Fix_Value = 0
        else:
            Fix_Loop = 0
            Fix_Value = 0

        if Fix_Loop != Loop:
            print("Warning: Loop Error")

        if Fix_Value != Value:
            print("Warning: Value has been Limited")

        return Fix_Loop, Fix_Value

    def __PackCmd(self):
        try:
            # Data error correction
            self.Cmd.Loop_L, self.Cmd.Value_L = self.__CmdCheck(
                self.Cmd.Loop_L, self.Cmd.Value_L
            )
            self.Cmd.Loop_R, self.Cmd.Value_R = self.__CmdCheck(
                self.Cmd.Loop_R, self.Cmd.Value_R
            )
            # Pack the data
            self.Cmd.CmdGapMs = int(min(250, self.Ctrldt * 1000))
            Data = struct.pack(
                "<H16B2f",
                CMD_HEAD,
                self.Cmd.CmdMode,
                self.Cmd.CmdCnt,
                self.Cmd.CmdGapMs,
                self.Cmd.ForceValue,
                self.Cmd.SpeedValue,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                self.Cmd.Loop_L,
                self.Cmd.Loop_R,
                self.Cmd.Value_L,
                self.Cmd.Value_R,
            )
        except Exception:
            print("Cmd Error")
            Data = struct.pack("<H3d", CMD_HEAD, 0, 0, 0)

        return Data + self.__U16XorCheck(Data)

    def __UnPackData(self, Data):
        UnpackState = 0
        if (
            (len(Data) == DATA_LENGTH)
            and (Data[0] == DATA_HEAD[0])
            and (Data[1] == DATA_HEAD[1])
        ):
            # Check header and length
            Check = self.__U16XorCheck(Data[:-2])
            if (Check[0] == Data[-2]) and (Check[1] == Data[-1]):
                # Unpack data
                [
                    self.Data.PowerKeyState,
                    self.Data.FuncKeyState,
                    self.Data.UpKeyState,
                    self.Data.DownKeyState,
                    self.Data.DeviceError,
                    self.Data.Battery,
                    Nouse0,
                    NoUse1,
                    Nouse2,
                    Nouse3,
                    Nouse4,
                    Nouse5,
                    Nouse6,
                    Nouse7,
                    Nouse8,
                    Nouse9,
                    self.Data.DeviceMs,
                    self.Data.BackIncl,
                    self.Data.HipAngle_L,
                    self.Data.HipAngle_R,
                    self.Data.HipSpeed_L,
                    self.Data.HipSpeed_R,
                    self.Data.HipTor_L,
                    self.Data.HipTor_R,
                    self.Data.Voltage,
                    self.Data.Current,
                    self.Data.AccX,
                    self.Data.AccY,
                    self.Data.AccZ,
                    self.Data.GyroX,
                    self.Data.GyroY,
                    self.Data.GyroZ,
                ] = struct.unpack("<16BI7f2H6h", Data[2:-2])

                # Correct data magnitudes
                self.Data.Voltage *= 0.01
                self.Data.Current *= 0.01
                self.Data.AccX *= 0.01
                self.Data.AccY *= 0.01
                self.Data.AccZ *= 0.01
                self.Data.GyroX *= 0.01
                self.Data.GyroY *= 0.01
                self.Data.GyroZ *= 0.01

                # Check if data has been refreshed
                if self.__LastDeviceMs != self.Data.DeviceMs:
                    self.__LastDeviceMs = self.Data.DeviceMs
                    # Notify the device of command refresh
                    if self.Cmd.CmdCnt > 250:
                        self.Cmd.CmdCnt = 0
                    else:
                        self.Cmd.CmdCnt += 1

                UnpackState = 1

        return UnpackState

    def __SerialDataIO(self):
        UpdateState = 0

        try:
            if self.__s.inWaiting() > 0:
                # 发送时不应该有未接收的数据
                time.sleep(0.005)
                self.__s.flushInput()

            SendFrame = self.__PackCmd()
            if self.__s.write(SendFrame) == CMD_LENGTH:
                # 发送数据成功后等待返回
                StartUs = GetUs()
                time.sleep(0.003)
                # print(str(StartUs), ' Send: ', str(SendFrame).encode('utf-8'))

                ExtraDelay = 0
                while True:
                    if self.__s.inWaiting() == 0:
                        # 等待返回数据
                        time.sleep(0.001)
                        ExtraDelay += 1
                        if ExtraDelay > 40:
                            # 超时
                            print("Device No Response")
                            break
                    elif self.__s.inWaiting() > DATA_LENGTH:
                        # 数据过长，清除缓冲区
                        print(
                            str(GetUs() - StartUs),
                            " Rec Too long!!!",
                            self.__s.inWaiting(),
                        )
                        time.sleep(0.005)
                        self.__s.flushInput()
                        break
                    else:
                        Rec = self.__s.read(DATA_LENGTH)
                        if self.__UnPackData(Rec) == 1:
                            # 数据正确通过校验
                            UpdateState = 1
                            # print(str(GetUs() - StartUs), 'Rec: ', str(Rec).encode('utf-8'))

                            NowUs = GetUs()
                            self.Ctrldt = (NowUs - self.__LastUs) / 1e6
                            self.__LastUs = NowUs
                        else:
                            # 显示错误数据
                            # print(str(GetUs() - StartUs), 'Check Fail: ', str(Rec))
                            print(
                                str(GetUs() - StartUs),
                                "Check Fail: ",
                                "".join(hex(Rec[i]) + " " for i in range(len(Rec))),
                            )
                        break
            else:
                print("Send Fail")

        except Exception:
            print("Serial Error")
            print("Trying To Disconnect...")
            self.__CloseSerial()

        finally:
            return UpdateState
