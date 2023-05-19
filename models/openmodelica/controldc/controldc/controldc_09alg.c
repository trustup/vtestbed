/* Algebraic */
#include "controldc_model.h"

#ifdef __cplusplus
extern "C" {
#endif


/* forwarded equations */
extern void controldc_eqFunction_27(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_37(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_23(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_22(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_39(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_38(DATA* data, threadData_t *threadData);

static void functionAlg_system0(DATA *data, threadData_t *threadData)
{
    controldc_eqFunction_27(data, threadData);

    controldc_eqFunction_37(data, threadData);

    controldc_eqFunction_23(data, threadData);

    controldc_eqFunction_22(data, threadData);

    controldc_eqFunction_39(data, threadData);

    controldc_eqFunction_38(data, threadData);
}
/* for continuous time variables */
int controldc_functionAlgebraics(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_ALGEBRAICS);
#endif
  data->simulationInfo->callStatistics.functionAlgebraics++;

  functionAlg_system0(data, threadData);

  controldc_function_savePreSynchronous(data, threadData);
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_ALGEBRAICS);
#endif

  TRACE_POP
  return 0;
}

#ifdef __cplusplus
}
#endif
