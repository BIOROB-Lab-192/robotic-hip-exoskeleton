/*
 * emg_Original_types.h
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

#ifndef RTW_HEADER_emg_Original_types_h_
#define RTW_HEADER_emg_Original_types_h_
#include "MW_SVD.h"
#include "rtwtypes.h"

/* Custom Type definition for MATLABSystem: '<Root>/pronator' */
#include "MW_SVD.h"
#ifndef struct_tag_jbIFaTBEZATkkvPSmnoPa
#define struct_tag_jbIFaTBEZATkkvPSmnoPa

struct tag_jbIFaTBEZATkkvPSmnoPa
{
  MW_Handle_Type MW_I2C_HANDLE;
};

#endif                                 /* struct_tag_jbIFaTBEZATkkvPSmnoPa */

#ifndef typedef_c_arduinodriver_ArduinoI2C_emg_Original_T
#define typedef_c_arduinodriver_ArduinoI2C_emg_Original_T

typedef struct tag_jbIFaTBEZATkkvPSmnoPa
  c_arduinodriver_ArduinoI2C_emg_Original_T;

#endif                   /* typedef_c_arduinodriver_ArduinoI2C_emg_Original_T */

#ifndef struct_tag_9AnIRoZpmWNSR76ytV7oUG
#define struct_tag_9AnIRoZpmWNSR76ytV7oUG

struct tag_9AnIRoZpmWNSR76ytV7oUG
{
  boolean_T matlabCodegenIsDeleted;
  int32_T isInitialized;
  c_arduinodriver_ArduinoI2C_emg_Original_T I2CDriverObj;
  uint32_T BusSpeed;
  real_T DefaultMaximumBusSpeedInHz;
};

#endif                                 /* struct_tag_9AnIRoZpmWNSR76ytV7oUG */

#ifndef typedef_b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T
#define typedef_b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T

typedef struct tag_9AnIRoZpmWNSR76ytV7oUG
  b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T;

#endif
/* typedef_b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T */

#ifndef struct_tag_TyJSH6R1I3sZx6CTdR9Tw
#define struct_tag_TyJSH6R1I3sZx6CTdR9Tw

struct tag_TyJSH6R1I3sZx6CTdR9Tw
{
  boolean_T matlabCodegenIsDeleted;
  int32_T isInitialized;
  boolean_T isSetupComplete;
  real_T SampleTime;
  boolean_T IsFirstStep;
  boolean_T isBNOcorrect;
  b_codertarget_arduinobase_internal_arduinoI2CWrite_emg_Original_T i2cObj;
};

#endif                                 /* struct_tag_TyJSH6R1I3sZx6CTdR9Tw */

#ifndef typedef_codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T
#define typedef_codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T

typedef struct tag_TyJSH6R1I3sZx6CTdR9Tw
  codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T;

#endif
     /* typedef_codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T */

#ifndef struct_tag_UTG5XI0vJCsmjbgura8BP
#define struct_tag_UTG5XI0vJCsmjbgura8BP

struct tag_UTG5XI0vJCsmjbgura8BP
{
  MW_Handle_Type MW_ANALOGIN_HANDLE;
};

#endif                                 /* struct_tag_UTG5XI0vJCsmjbgura8BP */

#ifndef typedef_c_arduinodriver_ArduinoAnalogInput_emg_Original_T
#define typedef_c_arduinodriver_ArduinoAnalogInput_emg_Original_T

typedef struct tag_UTG5XI0vJCsmjbgura8BP
  c_arduinodriver_ArduinoAnalogInput_emg_Original_T;

#endif           /* typedef_c_arduinodriver_ArduinoAnalogInput_emg_Original_T */

#ifndef struct_tag_8ohiN1FAOgR98njPNu14NC
#define struct_tag_8ohiN1FAOgR98njPNu14NC

struct tag_8ohiN1FAOgR98njPNu14NC
{
  boolean_T matlabCodegenIsDeleted;
  int32_T isInitialized;
  boolean_T isSetupComplete;
  c_arduinodriver_ArduinoAnalogInput_emg_Original_T AnalogInDriverObj;
  real_T SampleTime;
};

#endif                                 /* struct_tag_8ohiN1FAOgR98njPNu14NC */

#ifndef typedef_codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T
#define typedef_codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T

typedef struct tag_8ohiN1FAOgR98njPNu14NC
  codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T;

#endif
/* typedef_codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T */

/* Parameters (default storage) */
typedef struct P_emg_Original_T_ P_emg_Original_T;

/* Forward declaration for rtModel */
typedef struct tag_RTM_emg_Original_T RT_MODEL_emg_Original_T;

#endif                                 /* RTW_HEADER_emg_Original_types_h_ */
