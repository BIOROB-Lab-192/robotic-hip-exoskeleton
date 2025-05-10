/*
 * emg_Original.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "emg_Original".
 *
 * Model version              : 4.0
 * Simulink Coder version : 23.2 (R2023b) 01-Aug-2023
 * C source code generated on : Fri Apr 18 11:57:44 2025
 *
 * Target selection: ert.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Atmel->AVR
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "emg_Original.h"
#include "emg_Original_types.h"
#include <string.h>
#include "rtwtypes.h"
#include <stddef.h>
#include "emg_Original_private.h"

/* Block signals (default storage) */
B_emg_Original_T emg_Original_B;

/* Block states (default storage) */
DW_emg_Original_T emg_Original_DW;

/* Real-time model */
static RT_MODEL_emg_Original_T emg_Original_M_;
RT_MODEL_emg_Original_T *const emg_Original_M = &emg_Original_M_;

/* Forward declaration for local functions */
static void emg_Original_SystemCore_setup
  (codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T *obj);
static void emg_Original_SystemCore_setup
  (codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T *obj)
{
  MW_I2C_Mode_Type modename;
  uint32_T i2cname;
  uint8_T SwappedDataBytes[2];
  uint8_T b_SwappedDataBytes[2];
  uint8_T CastedData;
  uint8_T SwappedDataBytes_0;
  uint8_T status;
  obj->isInitialized = 1L;
  modename = MW_I2C_MASTER;
  i2cname = 0;
  obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE = MW_I2C_Open(i2cname, modename);
  obj->i2cObj.BusSpeed = 100000UL;
  MW_I2C_SetBusSpeed(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE,
                     obj->i2cObj.BusSpeed);
  MW_delay_in_milliseconds(600UL);
  status = 0U;
  memcpy((void *)&SwappedDataBytes_0, (void *)&status, (size_t)1 * sizeof
         (uint8_T));
  status = MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
    &SwappedDataBytes_0, 1UL, true, false);
  if (status == 0) {
    MW_I2C_MasterRead(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL, &status, 1UL,
                      false, true);
    memcpy((void *)&CastedData, (void *)&status, (size_t)1 * sizeof(uint8_T));
  } else {
    CastedData = 0U;
  }

  obj->isBNOcorrect = (CastedData == 160);
  if (obj->isBNOcorrect) {
    CastedData = 0U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 61U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    MW_delay_in_milliseconds(25UL);
    CastedData = 32U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 63U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    status = 0U;
    memcpy((void *)&SwappedDataBytes_0, (void *)&status, (size_t)1 * sizeof
           (uint8_T));
    status = MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
      &SwappedDataBytes_0, 1UL, true, false);
    if (status == 0) {
      MW_I2C_MasterRead(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL, &status,
                        1UL, false, true);
      memcpy((void *)&CastedData, (void *)&status, (size_t)1 * sizeof(uint8_T));
    } else {
      CastedData = 0U;
    }

    obj->isBNOcorrect = (CastedData == 160);
    while (!obj->isBNOcorrect) {
      MW_delay_in_milliseconds(10UL);
      status = 0U;
      memcpy((void *)&SwappedDataBytes_0, (void *)&status, (size_t)1 * sizeof
             (uint8_T));
      status = MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
        &SwappedDataBytes_0, 1UL, true, false);
      if (status == 0) {
        MW_I2C_MasterRead(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL, &status,
                          1UL, false, true);
        memcpy((void *)&CastedData, (void *)&status, (size_t)1 * sizeof(uint8_T));
      } else {
        CastedData = 0U;
      }

      obj->isBNOcorrect = (CastedData == 160);
    }

    MW_delay_in_milliseconds(50UL);
    CastedData = 0U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 62U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    CastedData = 0U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 63U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    CastedData = 0U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 7U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    MW_delay_in_milliseconds(10UL);
    CastedData = 128U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 59U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    CastedData = 12U;
    memcpy((void *)&b_SwappedDataBytes[1], (void *)&CastedData, (size_t)1 *
           sizeof(uint8_T));
    b_SwappedDataBytes[0] = 61U;
    memcpy((void *)&SwappedDataBytes[0], (void *)&b_SwappedDataBytes[0], (size_t)
           2 * sizeof(uint8_T));
    MW_I2C_MasterWrite(obj->i2cObj.I2CDriverObj.MW_I2C_HANDLE, 40UL,
                       &SwappedDataBytes[0], 2UL, false, false);
    MW_delay_in_milliseconds(25UL);
  }

  obj->isSetupComplete = true;
}

/* Model step function */
void emg_Original_step(void)
{
  MW_AnalogIn_ResultDataType_Type datatype_id;
  b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T *obj_tmp;
  int16_T b_RegisterValue[3];
  int16_T b_RegisterValue_0[3];
  int16_T b_RegisterValue_1[3];
  int16_T b_output[3];
  uint16_T b_varargout_1;
  uint8_T output_raw[6];
  uint8_T SwappedDataBytes;
  uint8_T status;

  /* MATLABSystem: '<Root>/pronator' */
  if (emg_Original_DW.obj_iidzvev33p.SampleTime !=
      emg_Original_P.pronator_SampleTime) {
    emg_Original_DW.obj_iidzvev33p.SampleTime =
      emg_Original_P.pronator_SampleTime;
  }

  emg_Original_DW.obj_iidzvev33p.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
    MW_AnalogIn_GetHandle(54UL);
  datatype_id = MW_ANALOGIN_UINT16;
  MW_AnalogInSingle_ReadResult
    (emg_Original_DW.obj_iidzvev33p.AnalogInDriverObj.MW_ANALOGIN_HANDLE,
     &b_varargout_1, datatype_id);

  /* DataTypeConversion: '<Root>/Cast To Double2' incorporates:
   *  MATLABSystem: '<Root>/pronator'
   */
  emg_Original_B.CastToDouble2 = b_varargout_1;

  /* MATLABSystem: '<Root>/flexor' */
  if (emg_Original_DW.obj_nvudd4eoi5.SampleTime !=
      emg_Original_P.flexor_SampleTime) {
    emg_Original_DW.obj_nvudd4eoi5.SampleTime = emg_Original_P.flexor_SampleTime;
  }

  emg_Original_DW.obj_nvudd4eoi5.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
    MW_AnalogIn_GetHandle(55UL);
  datatype_id = MW_ANALOGIN_UINT16;
  MW_AnalogInSingle_ReadResult
    (emg_Original_DW.obj_nvudd4eoi5.AnalogInDriverObj.MW_ANALOGIN_HANDLE,
     &b_varargout_1, datatype_id);

  /* DataTypeConversion: '<Root>/Cast To Double1' incorporates:
   *  MATLABSystem: '<Root>/flexor'
   */
  emg_Original_B.CastToDouble1 = b_varargout_1;

  /* MATLABSystem: '<Root>/Bicep' */
  if (emg_Original_DW.obj_l0mr0qnxdf.SampleTime !=
      emg_Original_P.Bicep_SampleTime) {
    emg_Original_DW.obj_l0mr0qnxdf.SampleTime = emg_Original_P.Bicep_SampleTime;
  }

  emg_Original_DW.obj_l0mr0qnxdf.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
    MW_AnalogIn_GetHandle(56UL);
  datatype_id = MW_ANALOGIN_UINT16;
  MW_AnalogInSingle_ReadResult
    (emg_Original_DW.obj_l0mr0qnxdf.AnalogInDriverObj.MW_ANALOGIN_HANDLE,
     &b_varargout_1, datatype_id);

  /* DataTypeConversion: '<Root>/Cast To Double3' incorporates:
   *  MATLABSystem: '<Root>/Bicep'
   */
  emg_Original_B.CastToDouble3 = b_varargout_1;

  /* DigitalClock: '<Root>/Digital Clock' */
  emg_Original_B.DigitalClock = emg_Original_M->Timing.taskTime0;

  /* SignalConversion generated from: '<Root>/To Workspace1' */
  emg_Original_B.TmpSignalConversionAt_asyncqueue_inserted_for_ToWorkspace1Inport1
    [0] = emg_Original_B.DigitalClock;
  emg_Original_B.TmpSignalConversionAt_asyncqueue_inserted_for_ToWorkspace1Inport1
    [1] = emg_Original_B.CastToDouble2;
  emg_Original_B.TmpSignalConversionAt_asyncqueue_inserted_for_ToWorkspace1Inport1
    [2] = emg_Original_B.CastToDouble1;
  emg_Original_B.TmpSignalConversionAt_asyncqueue_inserted_for_ToWorkspace1Inport1
    [3] = emg_Original_B.CastToDouble3;

  /* SignalConversion generated from: '<Root>/Mux1' */
  emg_Original_B.TmpSignalConversionAtTAQSigLogging_InsertedFor_Mux1_at_outport_0Inport1
    [0] = emg_Original_B.CastToDouble2;
  emg_Original_B.TmpSignalConversionAtTAQSigLogging_InsertedFor_Mux1_at_outport_0Inport1
    [1] = emg_Original_B.CastToDouble1;
  emg_Original_B.TmpSignalConversionAtTAQSigLogging_InsertedFor_Mux1_at_outport_0Inport1
    [2] = emg_Original_B.CastToDouble3;

  /* Outputs for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Outputs for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* MATLABSystem: '<S1>/Base sensor block' */
  if (emg_Original_DW.obj.SampleTime !=
      emg_Original_P.BNO055IMUSensor_SampleTime) {
    emg_Original_DW.obj.SampleTime = emg_Original_P.BNO055IMUSensor_SampleTime;
  }

  /* End of Outputs for SubSystem: '<Root>/BNO055 IMU Sensor' */
  if (!emg_Original_DW.obj.IsFirstStep) {
    MW_getCurrentTime_in_milliseconds();
    emg_Original_DW.obj.IsFirstStep = true;
  }

  obj_tmp = &emg_Original_DW.obj.i2cObj;
  status = 20U;
  memcpy((void *)&SwappedDataBytes, (void *)&status, (size_t)1 * sizeof(uint8_T));
  status = MW_I2C_MasterWrite(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL,
    &SwappedDataBytes, 1UL, true, false);
  if (status == 0) {
    MW_I2C_MasterRead(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL, &output_raw[0],
                      6UL, false, true);
    memcpy((void *)&b_RegisterValue[0], (void *)&output_raw[0], (size_t)3 *
           sizeof(int16_T));
  } else {
    b_RegisterValue[0] = 0;
    b_RegisterValue[1] = 0;
    b_RegisterValue[2] = 0;
  }

  status = 26U;
  memcpy((void *)&SwappedDataBytes, (void *)&status, (size_t)1 * sizeof(uint8_T));
  status = MW_I2C_MasterWrite(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL,
    &SwappedDataBytes, 1UL, true, false);
  if (status == 0) {
    MW_I2C_MasterRead(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL, &output_raw[0],
                      6UL, false, true);
    memcpy((void *)&b_RegisterValue_0[0], (void *)&output_raw[0], (size_t)3 *
           sizeof(int16_T));
  } else {
    b_RegisterValue_0[0] = 0;
    b_RegisterValue_0[1] = 0;
    b_RegisterValue_0[2] = 0;
  }

  status = 40U;
  memcpy((void *)&SwappedDataBytes, (void *)&status, (size_t)1 * sizeof(uint8_T));
  status = MW_I2C_MasterWrite(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL,
    &SwappedDataBytes, 1UL, true, false);
  if (status == 0) {
    MW_I2C_MasterRead(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL, &output_raw[0],
                      6UL, false, true);
    memcpy((void *)&b_RegisterValue_1[0], (void *)&output_raw[0], (size_t)3 *
           sizeof(int16_T));
  } else {
    b_RegisterValue_1[0] = 0;
    b_RegisterValue_1[1] = 0;
    b_RegisterValue_1[2] = 0;
  }

  status = 46U;
  memcpy((void *)&SwappedDataBytes, (void *)&status, (size_t)1 * sizeof(uint8_T));
  status = MW_I2C_MasterWrite(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL,
    &SwappedDataBytes, 1UL, true, false);
  if (status == 0) {
    MW_I2C_MasterRead(obj_tmp->I2CDriverObj.MW_I2C_HANDLE, 40UL, &output_raw[0],
                      6UL, false, true);
    memcpy((void *)&b_output[0], (void *)&output_raw[0], (size_t)3 * sizeof
           (int16_T));
  }

  /* Math: '<S2>/Math Function' incorporates:
   *  MATLABSystem: '<S1>/Base sensor block'
   */
  emg_Original_B.MathFunction[0] = (real_T)b_RegisterValue[0] / 16.0;
  emg_Original_B.MathFunction[1] = (real_T)b_RegisterValue[1] / 16.0;
  emg_Original_B.MathFunction[2] = (real_T)b_RegisterValue[2] / 16.0;

  /* End of Outputs for SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Outputs for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Math: '<S4>/Math Function' incorporates:
   *  MATLABSystem: '<S1>/Base sensor block'
   */
  emg_Original_B.MathFunction_gbcgyykyf5[0] = (real_T)b_RegisterValue_0[0] /
    16.0;
  emg_Original_B.MathFunction_gbcgyykyf5[1] = (real_T)b_RegisterValue_0[1] /
    16.0;
  emg_Original_B.MathFunction_gbcgyykyf5[2] = (real_T)b_RegisterValue_0[2] /
    16.0;

  /* End of Outputs for SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Outputs for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Math: '<S3>/Math Function' incorporates:
   *  MATLABSystem: '<S1>/Base sensor block'
   */
  emg_Original_B.MathFunction_h0mruf3kx5[0] = (real_T)b_RegisterValue_1[0] /
    100.0;
  emg_Original_B.MathFunction_h0mruf3kx5[1] = (real_T)b_RegisterValue_1[1] /
    100.0;
  emg_Original_B.MathFunction_h0mruf3kx5[2] = (real_T)b_RegisterValue_1[2] /
    100.0;

  /* End of Outputs for SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Math: '<S5>/Math Function' */
  emg_Original_B.MathFunction_ij4ila1vln = 0.0;

  {                                    /* Sample time: [0.05s, 0.0s] */
  }

  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++emg_Original_M->Timing.clockTick0)) {
    ++emg_Original_M->Timing.clockTickH0;
  }

  emg_Original_M->Timing.taskTime0 = emg_Original_M->Timing.clockTick0 *
    emg_Original_M->Timing.stepSize0 + emg_Original_M->Timing.clockTickH0 *
    emg_Original_M->Timing.stepSize0 * 4294967296.0;
}

/* Model initialize function */
void emg_Original_initialize(void)
{
  /* Registration code */

  /* initialize real-time model */
  (void) memset((void *)emg_Original_M, 0,
                sizeof(RT_MODEL_emg_Original_T));
  rtmSetTFinal(emg_Original_M, -1);
  emg_Original_M->Timing.stepSize0 = 0.05;

  /* External mode info */
  emg_Original_M->Sizes.checksums[0] = (3953162961U);
  emg_Original_M->Sizes.checksums[1] = (1942301575U);
  emg_Original_M->Sizes.checksums[2] = (3014324300U);
  emg_Original_M->Sizes.checksums[3] = (3066611299U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[6];
    emg_Original_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = &rtAlwaysEnabled;
    systemRan[2] = &rtAlwaysEnabled;
    systemRan[3] = &rtAlwaysEnabled;
    systemRan[4] = &rtAlwaysEnabled;
    systemRan[5] = &rtAlwaysEnabled;
    rteiSetModelMappingInfoPtr(emg_Original_M->extModeInfo,
      &emg_Original_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(emg_Original_M->extModeInfo,
                        emg_Original_M->Sizes.checksums);
    rteiSetTPtr(emg_Original_M->extModeInfo, rtmGetTPtr(emg_Original_M));
  }

  /* block I/O */
  (void) memset(((void *) &emg_Original_B), 0,
                sizeof(B_emg_Original_T));

  /* states (dwork) */
  (void) memset((void *)&emg_Original_DW, 0,
                sizeof(DW_emg_Original_T));

  {
    b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T *obj;

    /* Start for MATLABSystem: '<Root>/pronator' */
    emg_Original_DW.obj_iidzvev33p.matlabCodegenIsDeleted = false;
    emg_Original_DW.objisempty = true;
    emg_Original_DW.obj_iidzvev33p.SampleTime =
      emg_Original_P.pronator_SampleTime;
    emg_Original_DW.obj_iidzvev33p.isInitialized = 1L;
    emg_Original_DW.obj_iidzvev33p.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
      MW_AnalogInSingle_Open(54UL);
    emg_Original_DW.obj_iidzvev33p.isSetupComplete = true;

    /* Start for MATLABSystem: '<Root>/flexor' */
    emg_Original_DW.obj_nvudd4eoi5.matlabCodegenIsDeleted = false;
    emg_Original_DW.objisempty_bdj5qwb522 = true;
    emg_Original_DW.obj_nvudd4eoi5.SampleTime = emg_Original_P.flexor_SampleTime;
    emg_Original_DW.obj_nvudd4eoi5.isInitialized = 1L;
    emg_Original_DW.obj_nvudd4eoi5.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
      MW_AnalogInSingle_Open(55UL);
    emg_Original_DW.obj_nvudd4eoi5.isSetupComplete = true;

    /* Start for MATLABSystem: '<Root>/Bicep' */
    emg_Original_DW.obj_l0mr0qnxdf.matlabCodegenIsDeleted = false;
    emg_Original_DW.objisempty_dkoet2rytn = true;
    emg_Original_DW.obj_l0mr0qnxdf.SampleTime = emg_Original_P.Bicep_SampleTime;
    emg_Original_DW.obj_l0mr0qnxdf.isInitialized = 1L;
    emg_Original_DW.obj_l0mr0qnxdf.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
      MW_AnalogInSingle_Open(56UL);
    emg_Original_DW.obj_l0mr0qnxdf.isSetupComplete = true;

    /* Start for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
    /* Start for MATLABSystem: '<S1>/Base sensor block' */
    emg_Original_DW.obj.isInitialized = 0L;
    emg_Original_DW.obj.IsFirstStep = false;
    obj = &emg_Original_DW.obj.i2cObj;
    emg_Original_DW.obj.i2cObj.DefaultMaximumBusSpeedInHz = 400000.0;
    emg_Original_DW.obj.i2cObj.isInitialized = 0L;
    obj->I2CDriverObj.MW_I2C_HANDLE = NULL;
    emg_Original_DW.obj.i2cObj.matlabCodegenIsDeleted = false;
    emg_Original_DW.obj.matlabCodegenIsDeleted = false;
    emg_Original_DW.objisempty_dpujp2emtg = true;

    /* Start for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
    emg_Original_DW.obj.SampleTime = emg_Original_P.BNO055IMUSensor_SampleTime;

    /* End of Start for SubSystem: '<Root>/BNO055 IMU Sensor' */
    emg_Original_SystemCore_setup(&emg_Original_DW.obj);

    /* End of Start for SubSystem: '<Root>/BNO055 IMU Sensor' */
  }
}

/* Model terminate function */
void emg_Original_terminate(void)
{
  b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T *obj;

  /* Terminate for MATLABSystem: '<Root>/pronator' */
  if (!emg_Original_DW.obj_iidzvev33p.matlabCodegenIsDeleted) {
    emg_Original_DW.obj_iidzvev33p.matlabCodegenIsDeleted = true;
    if ((emg_Original_DW.obj_iidzvev33p.isInitialized == 1L) &&
        emg_Original_DW.obj_iidzvev33p.isSetupComplete) {
      emg_Original_DW.obj_iidzvev33p.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
        MW_AnalogIn_GetHandle(54UL);
      MW_AnalogIn_Close
        (emg_Original_DW.obj_iidzvev33p.AnalogInDriverObj.MW_ANALOGIN_HANDLE);
    }
  }

  /* End of Terminate for MATLABSystem: '<Root>/pronator' */

  /* Terminate for MATLABSystem: '<Root>/flexor' */
  if (!emg_Original_DW.obj_nvudd4eoi5.matlabCodegenIsDeleted) {
    emg_Original_DW.obj_nvudd4eoi5.matlabCodegenIsDeleted = true;
    if ((emg_Original_DW.obj_nvudd4eoi5.isInitialized == 1L) &&
        emg_Original_DW.obj_nvudd4eoi5.isSetupComplete) {
      emg_Original_DW.obj_nvudd4eoi5.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
        MW_AnalogIn_GetHandle(55UL);
      MW_AnalogIn_Close
        (emg_Original_DW.obj_nvudd4eoi5.AnalogInDriverObj.MW_ANALOGIN_HANDLE);
    }
  }

  /* End of Terminate for MATLABSystem: '<Root>/flexor' */

  /* Terminate for MATLABSystem: '<Root>/Bicep' */
  if (!emg_Original_DW.obj_l0mr0qnxdf.matlabCodegenIsDeleted) {
    emg_Original_DW.obj_l0mr0qnxdf.matlabCodegenIsDeleted = true;
    if ((emg_Original_DW.obj_l0mr0qnxdf.isInitialized == 1L) &&
        emg_Original_DW.obj_l0mr0qnxdf.isSetupComplete) {
      emg_Original_DW.obj_l0mr0qnxdf.AnalogInDriverObj.MW_ANALOGIN_HANDLE =
        MW_AnalogIn_GetHandle(56UL);
      MW_AnalogIn_Close
        (emg_Original_DW.obj_l0mr0qnxdf.AnalogInDriverObj.MW_ANALOGIN_HANDLE);
    }
  }

  /* End of Terminate for MATLABSystem: '<Root>/Bicep' */
  /* Terminate for Atomic SubSystem: '<Root>/BNO055 IMU Sensor' */
  /* Terminate for MATLABSystem: '<S1>/Base sensor block' */
  if (!emg_Original_DW.obj.matlabCodegenIsDeleted) {
    emg_Original_DW.obj.matlabCodegenIsDeleted = true;
    if ((emg_Original_DW.obj.isInitialized == 1L) &&
        emg_Original_DW.obj.isSetupComplete) {
      obj = &emg_Original_DW.obj.i2cObj;
      MW_I2C_Close(obj->I2CDriverObj.MW_I2C_HANDLE);
    }
  }

  obj = &emg_Original_DW.obj.i2cObj;
  if (!obj->matlabCodegenIsDeleted) {
    obj->matlabCodegenIsDeleted = true;
    if (obj->isInitialized == 1L) {
      obj->isInitialized = 2L;
    }
  }

  /* End of Terminate for MATLABSystem: '<S1>/Base sensor block' */
  /* End of Terminate for SubSystem: '<Root>/BNO055 IMU Sensor' */
}
