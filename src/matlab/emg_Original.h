/*
 * emg_Original.h
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

#ifndef RTW_HEADER_emg_Original_h_
#define RTW_HEADER_emg_Original_h_
#ifndef emg_Original_COMMON_INCLUDES_
#define emg_Original_COMMON_INCLUDES_
#include "rtwtypes.h"
#include "rtw_extmode.h"
#include "sysran_types.h"
#include "rtw_continuous.h"
#include "rtw_solver.h"
#include "MW_I2C.h"
#include "io_wrappers.h"
#include "MW_AnalogIn.h"
#endif                                 /* emg_Original_COMMON_INCLUDES_ */

#include "emg_Original_types.h"
#include <string.h>
#include "MW_target_hardware_resources.h"

/* Macros for accessing real-time model data structure */
#ifndef rtmGetFinalTime
#define rtmGetFinalTime(rtm)           ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetRTWExtModeInfo
#define rtmGetRTWExtModeInfo(rtm)      ((rtm)->extModeInfo)
#endif

#ifndef rtmGetErrorStatus
#define rtmGetErrorStatus(rtm)         ((rtm)->errorStatus)
#endif

#ifndef rtmSetErrorStatus
#define rtmSetErrorStatus(rtm, val)    ((rtm)->errorStatus = (val))
#endif

#ifndef rtmGetStopRequested
#define rtmGetStopRequested(rtm)       ((rtm)->Timing.stopRequestedFlag)
#endif

#ifndef rtmSetStopRequested
#define rtmSetStopRequested(rtm, val)  ((rtm)->Timing.stopRequestedFlag = (val))
#endif

#ifndef rtmGetStopRequestedPtr
#define rtmGetStopRequestedPtr(rtm)    (&((rtm)->Timing.stopRequestedFlag))
#endif

#ifndef rtmGetT
#define rtmGetT(rtm)                   ((rtm)->Timing.taskTime0)
#endif

#ifndef rtmGetTFinal
#define rtmGetTFinal(rtm)              ((rtm)->Timing.tFinal)
#endif

#ifndef rtmGetTPtr
#define rtmGetTPtr(rtm)                (&(rtm)->Timing.taskTime0)
#endif

/* Block signals (default storage) */
typedef struct {
  real_T CastToDouble2;                /* '<Root>/Cast To Double2' */
  real_T CastToDouble1;                /* '<Root>/Cast To Double1' */
  real_T CastToDouble3;                /* '<Root>/Cast To Double3' */
  real_T DigitalClock;                 /* '<Root>/Digital Clock' */
  real_T TmpSignalConversionAt_asyncqueue_inserted_for_ToWorkspace1Inport1[4];
  /* '<Root>/TmpSignal ConversionAt_asyncqueue_inserted_for_To Workspace1Inport1' */
  real_T
    TmpSignalConversionAtTAQSigLogging_InsertedFor_Mux1_at_outport_0Inport1[3];
  /* '<Root>/TmpSignal ConversionAtTAQSigLogging_InsertedFor_Mux1_at_outport_0Inport1' */
  real_T MathFunction[3];              /* '<S2>/Math Function' */
  real_T MathFunction_gbcgyykyf5[3];   /* '<S4>/Math Function' */
  real_T MathFunction_h0mruf3kx5[3];   /* '<S3>/Math Function' */
  real_T MathFunction_ij4ila1vln;      /* '<S5>/Math Function' */
} B_emg_Original_T;

/* Block states (default storage) for system '<Root>' */
typedef struct {
  codertarget_arduinobase_internal_arduinoBNO055_emg_Original_T obj;/* '<S1>/Base sensor block' */
  codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T
    obj_iidzvev33p;                    /* '<Root>/pronator' */
  codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T
    obj_nvudd4eoi5;                    /* '<Root>/flexor' */
  codertarget_arduinobase_internal_arduino_AnalogInput_emg_Original_T
    obj_l0mr0qnxdf;                    /* '<Root>/Bicep' */
  struct {
    void *LoggedData;
  } Scope_PWORK;                       /* '<Root>/Scope' */

  struct {
    void *LoggedData;
  } Scope2_PWORK;                      /* '<Root>/Scope2' */

  struct {
    void *LoggedData;
  } Scope1_PWORK;                      /* '<Root>/Scope1' */

  struct {
    void *LoggedData;
  } Scope3_PWORK;                      /* '<Root>/Scope3' */

  struct {
    void *LoggedData;
  } Scope4_PWORK;                      /* '<Root>/Scope4' */

  struct {
    void *LoggedData;
  } Scope5_PWORK;                      /* '<Root>/Scope5' */

  struct {
    void *LoggedData;
  } Scope6_PWORK;                      /* '<Root>/Scope6' */

  struct {
    void *LoggedData;
  } Scope7_PWORK;                      /* '<Root>/Scope7' */

  boolean_T objisempty;                /* '<Root>/pronator' */
  boolean_T objisempty_bdj5qwb522;     /* '<Root>/flexor' */
  boolean_T objisempty_dkoet2rytn;     /* '<Root>/Bicep' */
  boolean_T objisempty_dpujp2emtg;     /* '<S1>/Base sensor block' */
} DW_emg_Original_T;

/* Parameters (default storage) */
struct P_emg_Original_T_ {
  real_T BNO055IMUSensor_SampleTime;
                                   /* Mask Parameter: BNO055IMUSensor_SampleTime
                                    * Referenced by: '<S1>/Base sensor block'
                                    */
  real_T Bicep_SampleTime;             /* Expression: -1
                                        * Referenced by: '<Root>/Bicep'
                                        */
  real_T flexor_SampleTime;            /* Expression: -1
                                        * Referenced by: '<Root>/flexor'
                                        */
  real_T pronator_SampleTime;          /* Expression: -1
                                        * Referenced by: '<Root>/pronator'
                                        */
};

/* Real-time Model Data Structure */
struct tag_RTM_emg_Original_T {
  const char_T *errorStatus;
  RTWExtModeInfo *extModeInfo;

  /*
   * Sizes:
   * The following substructure contains sizes information
   * for many of the model attributes such as inputs, outputs,
   * dwork, sample times, etc.
   */
  struct {
    uint32_T checksums[4];
  } Sizes;

  /*
   * SpecialInfo:
   * The following substructure contains special information
   * related to other components that are dependent on RTW.
   */
  struct {
    const void *mappingInfo;
  } SpecialInfo;

  /*
   * Timing:
   * The following substructure contains information regarding
   * the timing information for the model.
   */
  struct {
    time_T taskTime0;
    uint32_T clockTick0;
    uint32_T clockTickH0;
    time_T stepSize0;
    time_T tFinal;
    boolean_T stopRequestedFlag;
  } Timing;
};

/* Block parameters (default storage) */
extern P_emg_Original_T emg_Original_P;

/* Block signals (default storage) */
extern B_emg_Original_T emg_Original_B;

/* Block states (default storage) */
extern DW_emg_Original_T emg_Original_DW;

/* Model entry point functions */
extern void emg_Original_initialize(void);
extern void emg_Original_step(void);
extern void emg_Original_terminate(void);

/* Real-time Model object */
extern RT_MODEL_emg_Original_T *const emg_Original_M;
extern volatile boolean_T stopRequested;
extern volatile boolean_T runModel;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'emg_Original'
 * '<S1>'   : 'emg_Original/BNO055 IMU Sensor'
 * '<S2>'   : 'emg_Original/Transpose'
 * '<S3>'   : 'emg_Original/Transpose1'
 * '<S4>'   : 'emg_Original/Transpose2'
 * '<S5>'   : 'emg_Original/Transpose3'
 */
#endif                                 /* RTW_HEADER_emg_Original_h_ */
