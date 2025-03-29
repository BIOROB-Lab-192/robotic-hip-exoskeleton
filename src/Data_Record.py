#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sept 19 2024

@author: Gerardo R Padilla Jr.

"""

import kqExoskeletonIO as kqio
import datetime
import csv
import logging

logging.basicConfig(filename="log/Data_Record.log", level=logging.INFO)
logger = logging.getLogger(__name__)


def record_to_csv(testname="", total_time=5, port="com3"):

    GetSec = kqio.GetSec
    Ant = kqio.AntCH(port)  # "/dev/ttyAMA0"

    # 观测数据
    ComTotalCnt = 1
    ComErrorCnt = 0
    # PlotLength = 1000
    if testname == "":
        testname = input("Enter Test Name: ")
        testname = "data/" + testname

    FileName = (
        testname
        + "_AntData_"
        + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        + ".csv"
    )

    Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY
    StartSec = GetSec()
    UpdateSec = StartSec
    UpdateSuccessSec = StartSec
    UpdateState = Ant.ComState
    AntConnected = Ant.ComState == 1

    with open(FileName, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Time",
                "PowerKeyState",
                "FuncKeyState",
                "UpKeyState",
                "DownKeyState",
                "DeviceError",
                "Battery",
                "DeviceMs",
                "BackIncl",
                "HipAngle_L",
                "HipAngle_R",
                "HipSpeed_L",
                "HipSpeed_R",
                "HipTor_L",
                "HipTor_R",
                "Voltage",
                "Current",
                "AccX",
                "AccY",
                "AccZ",
                "GyroX",
                "GyroY",
                "GyroZ",
            ]
        )
        while AntConnected:

            if UpdateState == 1:
                UpdateSec = GetSec()  # -StartSec

                # Set timing end condition (seconds),  stop data collection after a few seconds.
                if UpdateSec - StartSec > total_time:
                    # Ant.Cmd.CmdMode = kqio.CMD_SHUTDOWN
                    Ant.Disconnect()
                    print("Run Finish")
                    break
            elif UpdateState == -1:
                # Communication error
                print("Com Error")
                break
            else:
                ComErrorCnt += 1
                # Communication failed; more than .3 seconds since last update.
                if GetSec() - (StartSec + UpdateSuccessSec) > 0.3:
                    print("Error: Com Lost")
                    Ant.Cmd.CmdMode = kqio.CMD_OBS_ONLY
                    Ant.Disconnect()
                    break

            UpdateState = Ant.Update()  # Issue command and retrieve device status
            ComTotalCnt += 1

            # Add observation data
            # UpdateSec = GetSec()
            writer.writerow(
                [
                    (UpdateSec - StartSec),
                    Ant.Data.PowerKeyState,
                    Ant.Data.FuncKeyState,
                    Ant.Data.UpKeyState,
                    Ant.Data.DownKeyState,
                    Ant.Data.DeviceError,
                    Ant.Data.Battery,
                    Ant.Data.DeviceMs,
                    Ant.Data.BackIncl,
                    Ant.Data.HipAngle_L,
                    Ant.Data.HipAngle_R,
                    Ant.Data.HipSpeed_L,
                    Ant.Data.HipSpeed_R,
                    Ant.Data.HipTor_L,
                    Ant.Data.HipTor_R,
                    Ant.Data.Voltage,
                    Ant.Data.Current,
                    Ant.Data.AccX,
                    Ant.Data.AccY,
                    Ant.Data.AccZ,
                    Ant.Data.GyroX,
                    Ant.Data.GyroY,
                    Ant.Data.GyroZ,
                ]
            )

            logger.debug(
                "Run Time:%.3fs" % (UpdateSec - StartSec),
                "  Update Time:%.3fs" % Ant.Ctrldt,
            )


if __name__ == "__main__":
    record_to_csv()
