/*
 * emg_Original_data.c
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

/* Block parameters (default storage) */
P_emg_Original_T emg_Original_P = {
  /* Mask Parameter: BNO055IMUSensor_SampleTime
   * Referenced by: '<S1>/Base sensor block'
   */
  0.05,

  /* Expression: -1
   * Referenced by: '<Root>/Bicep'
   */
  -1.0,

  /* Expression: -1
   * Referenced by: '<Root>/flexor'
   */
  -1.0,

  /* Expression: -1
   * Referenced by: '<Root>/pronator'
   */
  -1.0
};
