/* Initialization */
#include "controldc_model.h"
#include "controldc_11mix.h"
#include "controldc_12jac.h"
#if defined(__cplusplus)
extern "C" {
#endif

void controldc_functionInitialEquations_0(DATA *data, threadData_t *threadData);

/*
equation index: 1
type: SIMPLE_ASSIGN
ground1.p.i = 0.0
*/
void controldc_eqFunction_1(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,1};
  data->localData[0]->realVars[14] /* ground1.p.i variable */ = 0.0;
  TRACE_POP
}

/*
equation index: 2
type: SIMPLE_ASSIGN
inertia1.flange_b.tau = 0.0
*/
void controldc_eqFunction_2(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,2};
  data->localData[0]->realVars[19] /* inertia1.flange_b.tau variable */ = 0.0;
  TRACE_POP
}

/*
equation index: 3
type: SIMPLE_ASSIGN
ground1.p.v = 0.0
*/
void controldc_eqFunction_3(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,3};
  data->localData[0]->realVars[15] /* ground1.p.v variable */ = 0.0;
  TRACE_POP
}

/*
equation index: 4
type: SIMPLE_ASSIGN
inertia1.w = $START.inertia1.w
*/
void controldc_eqFunction_4(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,4};
  data->localData[0]->realVars[2] /* inertia1.w STATE(1,inertia1.a) */ = data->modelData->realVarsData[2].attribute /* inertia1.w STATE(1,inertia1.a) */.start;
  TRACE_POP
}

/*
equation index: 5
type: SIMPLE_ASSIGN
inductor.Psi = $START.inductor.Psi
*/
void controldc_eqFunction_5(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,5};
  data->localData[0]->realVars[0] /* inductor.Psi STATE(1,inductor.v) */ = data->modelData->realVarsData[0].attribute /* inductor.Psi STATE(1,inductor.v) */.start;
  TRACE_POP
}
extern void controldc_eqFunction_24(DATA *data, threadData_t *threadData);


/*
equation index: 7
type: SIMPLE_ASSIGN
signalVoltage1.i = inductor.Psi / max(L, inductor.Lmin)
*/
void controldc_eqFunction_7(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,7};
  data->localData[0]->realVars[23] /* signalVoltage1.i variable */ = DIVISION_SIM(data->localData[0]->realVars[0] /* inductor.Psi STATE(1,inductor.v) */,fmax(data->localData[0]->realVars[8] /* L variable */,data->simulationInfo->realParameter[6] /* inductor.Lmin PARAM */),"max(L, inductor.Lmin)",equationIndexes);
  TRACE_POP
}
extern void controldc_eqFunction_33(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_34(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_37(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_23(DATA *data, threadData_t *threadData);


/*
equation index: 12
type: SIMPLE_ASSIGN
$DER.emf.phi = emf.w
*/
void controldc_eqFunction_12(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,12};
  data->localData[0]->realVars[6] /* der(emf.phi) DUMMY_DER */ = data->localData[0]->realVars[13] /* emf.w variable */;
  TRACE_POP
}

/*
equation index: 13
type: SIMPLE_ASSIGN
emf.v = emf.k * emf.w
*/
void controldc_eqFunction_13(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,13};
  data->localData[0]->realVars[12] /* emf.v variable */ = (data->simulationInfo->realParameter[4] /* emf.k PARAM */) * (data->localData[0]->realVars[13] /* emf.w variable */);
  TRACE_POP
}
extern void controldc_eqFunction_35(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_36(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_30(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_26(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_31(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_32(DATA *data, threadData_t *threadData);


/*
equation index: 20
type: SIMPLE_ASSIGN
inertia1.phi = $START.inertia1.phi
*/
void controldc_eqFunction_20(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,20};
  data->localData[0]->realVars[1] /* inertia1.phi STATE(1,inertia1.w) */ = data->modelData->realVarsData[1].attribute /* inertia1.phi STATE(1,inertia1.w) */.start;
  TRACE_POP
}
extern void controldc_eqFunction_27(DATA *data, threadData_t *threadData);

OMC_DISABLE_OPT
void controldc_functionInitialEquations_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  controldc_eqFunction_1(data, threadData);
  controldc_eqFunction_2(data, threadData);
  controldc_eqFunction_3(data, threadData);
  controldc_eqFunction_4(data, threadData);
  controldc_eqFunction_5(data, threadData);
  controldc_eqFunction_24(data, threadData);
  controldc_eqFunction_7(data, threadData);
  controldc_eqFunction_33(data, threadData);
  controldc_eqFunction_34(data, threadData);
  controldc_eqFunction_37(data, threadData);
  controldc_eqFunction_23(data, threadData);
  controldc_eqFunction_12(data, threadData);
  controldc_eqFunction_13(data, threadData);
  controldc_eqFunction_35(data, threadData);
  controldc_eqFunction_36(data, threadData);
  controldc_eqFunction_30(data, threadData);
  controldc_eqFunction_26(data, threadData);
  controldc_eqFunction_31(data, threadData);
  controldc_eqFunction_32(data, threadData);
  controldc_eqFunction_20(data, threadData);
  controldc_eqFunction_27(data, threadData);
  TRACE_POP
}


int controldc_functionInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->discreteCall = 1;
  controldc_functionInitialEquations_0(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
  TRACE_POP
  return 0;
}


int controldc_functionInitialEquations_lambda0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->discreteCall = 1;
  data->simulationInfo->discreteCall = 0;
  
  TRACE_POP
  return 0;
}
int controldc_functionRemovedInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int *equationIndexes = NULL;
  double res = 0.0;

  
  TRACE_POP
  return 0;
}


#if defined(__cplusplus)
}
#endif

