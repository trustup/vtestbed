/* Main Simulation File */

#if defined(__cplusplus)
extern "C" {
#endif

#include "controldc_model.h"
#include "simulation/solver/events.h"

#define prefixedName_performSimulation controldc_performSimulation
#define prefixedName_updateContinuousSystem controldc_updateContinuousSystem
#include <simulation/solver/perform_simulation.c.inc>

#define prefixedName_performQSSSimulation controldc_performQSSSimulation
#include <simulation/solver/perform_qss_simulation.c.inc>

/* dummy VARINFO and FILEINFO */
const FILE_INFO dummyFILE_INFO = omc_dummyFileInfo;
const VAR_INFO dummyVAR_INFO = omc_dummyVarInfo;

int controldc_input_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->localData[0]->realVars[8] /* L variable */ = data->simulationInfo->inputVars[0];
  data->localData[0]->realVars[9] /* R variable */ = data->simulationInfo->inputVars[1];
  data->localData[0]->realVars[24] /* u variable */ = data->simulationInfo->inputVars[2];
  
  TRACE_POP
  return 0;
}

int controldc_input_function_init(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->inputVars[0] = data->modelData->realVarsData[8].attribute.start;
  data->simulationInfo->inputVars[1] = data->modelData->realVarsData[9].attribute.start;
  data->simulationInfo->inputVars[2] = data->modelData->realVarsData[24].attribute.start;
  
  TRACE_POP
  return 0;
}

int controldc_input_function_updateStartValues(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->modelData->realVarsData[8].attribute.start = data->simulationInfo->inputVars[0];
  data->modelData->realVarsData[9].attribute.start = data->simulationInfo->inputVars[1];
  data->modelData->realVarsData[24].attribute.start = data->simulationInfo->inputVars[2];
  
  TRACE_POP
  return 0;
}

int controldc_inputNames(DATA *data, char ** names){
  TRACE_PUSH

  names[0] = (char *) data->modelData->realVarsData[8].info.name;
  names[1] = (char *) data->modelData->realVarsData[9].info.name;
  names[2] = (char *) data->modelData->realVarsData[24].info.name;
  
  TRACE_POP
  return 0;
}

int controldc_data_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  TRACE_POP
  return 0;
}

int controldc_output_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int controldc_setc_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/*
equation index: 22
type: SIMPLE_ASSIGN
$DER.emf.phi = inertia1.w
*/
void controldc_eqFunction_22(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,22};
  data->localData[0]->realVars[6] /* der(emf.phi) DUMMY_DER */ = data->localData[0]->realVars[2] /* inertia1.w STATE(1,inertia1.a) */;
  TRACE_POP
}
/*
equation index: 23
type: SIMPLE_ASSIGN
emf.w = inertia1.w
*/
void controldc_eqFunction_23(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,23};
  data->localData[0]->realVars[13] /* emf.w variable */ = data->localData[0]->realVars[2] /* inertia1.w STATE(1,inertia1.a) */;
  TRACE_POP
}
/*
equation index: 24
type: SIMPLE_ASSIGN
resistor.R_actual = R * (1.0 + resistor.alpha * (resistor.T - resistor.T_ref))
*/
void controldc_eqFunction_24(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,24};
  data->localData[0]->realVars[21] /* resistor.R_actual variable */ = (data->localData[0]->realVars[9] /* R variable */) * (1.0 + (data->simulationInfo->realParameter[11] /* resistor.alpha PARAM */) * (data->simulationInfo->realParameter[8] /* resistor.T PARAM */ - data->simulationInfo->realParameter[10] /* resistor.T_ref PARAM */));
  TRACE_POP
}
/*
equation index: 25
type: SIMPLE_ASSIGN
emf.v = emf.k * inertia1.w
*/
void controldc_eqFunction_25(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,25};
  data->localData[0]->realVars[12] /* emf.v variable */ = (data->simulationInfo->realParameter[4] /* emf.k PARAM */) * (data->localData[0]->realVars[2] /* inertia1.w STATE(1,inertia1.a) */);
  TRACE_POP
}
/*
equation index: 26
type: SIMPLE_ASSIGN
$DER.inertia1.phi = inertia1.w
*/
void controldc_eqFunction_26(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,26};
  data->localData[0]->realVars[4] /* der(inertia1.phi) STATE_DER */ = data->localData[0]->realVars[2] /* inertia1.w STATE(1,inertia1.a) */;
  TRACE_POP
}
/*
equation index: 27
type: SIMPLE_ASSIGN
emf.phi = inertia1.phi - emf.fixed.phi0
*/
void controldc_eqFunction_27(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,27};
  data->localData[0]->realVars[10] /* emf.phi DUMMY_STATE */ = data->localData[0]->realVars[1] /* inertia1.phi STATE(1,inertia1.w) */ - data->simulationInfo->realParameter[1] /* emf.fixed.phi0 PARAM */;
  TRACE_POP
}
/*
equation index: 28
type: SIMPLE_ASSIGN
$cse1 = max(L, inductor.Lmin)
*/
void controldc_eqFunction_28(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,28};
  data->localData[0]->realVars[7] /* $cse1 variable */ = fmax(data->localData[0]->realVars[8] /* L variable */,data->simulationInfo->realParameter[6] /* inductor.Lmin PARAM */);
  TRACE_POP
}
/*
equation index: 29
type: SIMPLE_ASSIGN
signalVoltage1.i = inductor.Psi / $cse1
*/
void controldc_eqFunction_29(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,29};
  data->localData[0]->realVars[23] /* signalVoltage1.i variable */ = DIVISION_SIM(data->localData[0]->realVars[0] /* inductor.Psi STATE(1,inductor.v) */,data->localData[0]->realVars[7] /* $cse1 variable */,"$cse1",equationIndexes);
  TRACE_POP
}
/*
equation index: 30
type: SIMPLE_ASSIGN
emf.tau = (-emf.k) * signalVoltage1.i
*/
void controldc_eqFunction_30(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,30};
  data->localData[0]->realVars[11] /* emf.tau variable */ = ((-data->simulationInfo->realParameter[4] /* emf.k PARAM */)) * (data->localData[0]->realVars[23] /* signalVoltage1.i variable */);
  TRACE_POP
}
/*
equation index: 31
type: SIMPLE_ASSIGN
inertia1.a = (-emf.tau) / inertia1.J
*/
void controldc_eqFunction_31(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,31};
  data->localData[0]->realVars[18] /* inertia1.a variable */ = DIVISION_SIM((-data->localData[0]->realVars[11] /* emf.tau variable */),data->simulationInfo->realParameter[7] /* inertia1.J PARAM */,"inertia1.J",equationIndexes);
  TRACE_POP
}
/*
equation index: 32
type: SIMPLE_ASSIGN
$DER.inertia1.w = inertia1.a
*/
void controldc_eqFunction_32(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,32};
  data->localData[0]->realVars[5] /* der(inertia1.w) STATE_DER */ = data->localData[0]->realVars[18] /* inertia1.a variable */;
  TRACE_POP
}
/*
equation index: 33
type: SIMPLE_ASSIGN
resistor.v = resistor.R_actual * signalVoltage1.i
*/
void controldc_eqFunction_33(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,33};
  data->localData[0]->realVars[22] /* resistor.v variable */ = (data->localData[0]->realVars[21] /* resistor.R_actual variable */) * (data->localData[0]->realVars[23] /* signalVoltage1.i variable */);
  TRACE_POP
}
/*
equation index: 34
type: SIMPLE_ASSIGN
inductor.p.v = (-u) - resistor.v
*/
void controldc_eqFunction_34(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,34};
  data->localData[0]->realVars[16] /* inductor.p.v variable */ = (-data->localData[0]->realVars[24] /* u variable */) - data->localData[0]->realVars[22] /* resistor.v variable */;
  TRACE_POP
}
/*
equation index: 35
type: SIMPLE_ASSIGN
inductor.v = inductor.p.v - emf.v
*/
void controldc_eqFunction_35(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,35};
  data->localData[0]->realVars[17] /* inductor.v variable */ = data->localData[0]->realVars[16] /* inductor.p.v variable */ - data->localData[0]->realVars[12] /* emf.v variable */;
  TRACE_POP
}
/*
equation index: 36
type: SIMPLE_ASSIGN
$DER.inductor.Psi = inductor.v
*/
void controldc_eqFunction_36(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,36};
  data->localData[0]->realVars[3] /* der(inductor.Psi) STATE_DER */ = data->localData[0]->realVars[17] /* inductor.v variable */;
  TRACE_POP
}
/*
equation index: 37
type: SIMPLE_ASSIGN
resistor.LossPower = resistor.v * signalVoltage1.i
*/
void controldc_eqFunction_37(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,37};
  data->localData[0]->realVars[20] /* resistor.LossPower variable */ = (data->localData[0]->realVars[22] /* resistor.v variable */) * (data->localData[0]->realVars[23] /* signalVoltage1.i variable */);
  TRACE_POP
}
/*
equation index: 39
type: ALGORITHM

  assert(L >= 0.0, "Inductance L_ (= " + String(L, 6, 0, true) + ") has to be >= 0!");
*/
void controldc_eqFunction_39(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,39};
  modelica_boolean tmp0;
  static const MMC_DEFSTRINGLIT(tmp1,17,"Inductance L_ (= ");
  modelica_string tmp2;
  static const MMC_DEFSTRINGLIT(tmp3,17,") has to be >= 0!");
  static int tmp4 = 0;
  modelica_metatype tmpMeta[2] __attribute__((unused)) = {0};
  {
    tmp0 = GreaterEq(data->localData[0]->realVars[8] /* L variable */,0.0);
    if(!tmp0)
    {
      tmp2 = modelica_real_to_modelica_string(data->localData[0]->realVars[8] /* L variable */, ((modelica_integer) 6), ((modelica_integer) 0), 1);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp1),tmp2);
      tmpMeta[1] = stringAppend(tmpMeta[0],MMC_REFSTRINGLIT(tmp3));
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Electrical/Analog/Basic.mo",1789,5,1789,74,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nL >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(tmpMeta[1]));
      }
    }
  }
  TRACE_POP
}
/*
equation index: 38
type: ALGORITHM

  assert(1.0 + resistor.alpha * (resistor.T - resistor.T_ref) >= 1e-15, "Temperature outside scope of model!");
*/
void controldc_eqFunction_38(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,38};
  modelica_boolean tmp5;
  static const MMC_DEFSTRINGLIT(tmp6,35,"Temperature outside scope of model!");
  static int tmp7 = 0;
  {
    tmp5 = GreaterEq(1.0 + (data->simulationInfo->realParameter[11] /* resistor.alpha PARAM */) * (data->simulationInfo->realParameter[8] /* resistor.T PARAM */ - data->simulationInfo->realParameter[10] /* resistor.T_ref PARAM */),1e-15);
    if(!tmp5)
    {
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Electrical/Analog/Basic.mo",1591,5,1592,45,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\n1.0 + resistor.alpha * (resistor.T - resistor.T_ref) >= 1e-15", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(MMC_REFSTRINGLIT(tmp6)));
      }
    }
  }
  TRACE_POP
}

OMC_DISABLE_OPT
int controldc_functionDAE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  int equationIndexes[1] = {0};
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_DAE);
#endif

  data->simulationInfo->needToIterate = 0;
  data->simulationInfo->discreteCall = 1;
  controldc_functionLocalKnownVars(data, threadData);
  controldc_eqFunction_22(data, threadData);

  controldc_eqFunction_23(data, threadData);

  controldc_eqFunction_24(data, threadData);

  controldc_eqFunction_25(data, threadData);

  controldc_eqFunction_26(data, threadData);

  controldc_eqFunction_27(data, threadData);

  controldc_eqFunction_28(data, threadData);

  controldc_eqFunction_29(data, threadData);

  controldc_eqFunction_30(data, threadData);

  controldc_eqFunction_31(data, threadData);

  controldc_eqFunction_32(data, threadData);

  controldc_eqFunction_33(data, threadData);

  controldc_eqFunction_34(data, threadData);

  controldc_eqFunction_35(data, threadData);

  controldc_eqFunction_36(data, threadData);

  controldc_eqFunction_37(data, threadData);

  controldc_eqFunction_39(data, threadData);

  controldc_eqFunction_38(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_DAE);
#endif
  TRACE_POP
  return 0;
}


int controldc_functionLocalKnownVars(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/* forwarded equations */
extern void controldc_eqFunction_24(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_25(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_26(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_28(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_29(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_30(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_31(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_32(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_33(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_34(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_35(DATA* data, threadData_t *threadData);
extern void controldc_eqFunction_36(DATA* data, threadData_t *threadData);

static void functionODE_system0(DATA *data, threadData_t *threadData)
{
    controldc_eqFunction_24(data, threadData);

    controldc_eqFunction_25(data, threadData);

    controldc_eqFunction_26(data, threadData);

    controldc_eqFunction_28(data, threadData);

    controldc_eqFunction_29(data, threadData);

    controldc_eqFunction_30(data, threadData);

    controldc_eqFunction_31(data, threadData);

    controldc_eqFunction_32(data, threadData);

    controldc_eqFunction_33(data, threadData);

    controldc_eqFunction_34(data, threadData);

    controldc_eqFunction_35(data, threadData);

    controldc_eqFunction_36(data, threadData);
}

int controldc_functionODE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_FUNCTION_ODE);
#endif

  
  data->simulationInfo->callStatistics.functionODE++;
  
  controldc_functionLocalKnownVars(data, threadData);
  functionODE_system0(data, threadData);

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_FUNCTION_ODE);
#endif

  TRACE_POP
  return 0;
}

/* forward the main in the simulation runtime */
extern int _main_SimulationRuntime(int argc, char**argv, DATA *data, threadData_t *threadData);

#include "controldc_12jac.h"
#include "controldc_13opt.h"

struct OpenModelicaGeneratedFunctionCallbacks controldc_callback = {
   (int (*)(DATA *, threadData_t *, void *)) controldc_performSimulation,
   (int (*)(DATA *, threadData_t *, void *)) controldc_performQSSSimulation,
   controldc_updateContinuousSystem,
   controldc_callExternalObjectDestructors,
   NULL,
   NULL,
   NULL,
   #if !defined(OMC_NO_STATESELECTION)
   controldc_initializeStateSets,
   #else
   NULL,
   #endif
   controldc_initializeDAEmodeData,
   controldc_functionODE,
   controldc_functionAlgebraics,
   controldc_functionDAE,
   controldc_functionLocalKnownVars,
   controldc_input_function,
   controldc_input_function_init,
   controldc_input_function_updateStartValues,
   controldc_data_function,
   controldc_output_function,
   controldc_setc_function,
   controldc_function_storeDelayed,
   controldc_updateBoundVariableAttributes,
   controldc_functionInitialEquations,
   1, /* useHomotopy - 0: local homotopy (equidistant lambda), 1: global homotopy (equidistant lambda), 2: new global homotopy approach (adaptive lambda), 3: new local homotopy approach (adaptive lambda)*/
   controldc_functionInitialEquations_lambda0,
   controldc_functionRemovedInitialEquations,
   controldc_updateBoundParameters,
   controldc_checkForAsserts,
   controldc_function_ZeroCrossingsEquations,
   controldc_function_ZeroCrossings,
   controldc_function_updateRelations,
   controldc_zeroCrossingDescription,
   controldc_relationDescription,
   controldc_function_initSample,
   controldc_INDEX_JAC_A,
   controldc_INDEX_JAC_B,
   controldc_INDEX_JAC_C,
   controldc_INDEX_JAC_D,
   controldc_INDEX_JAC_F,
   controldc_initialAnalyticJacobianA,
   controldc_initialAnalyticJacobianB,
   controldc_initialAnalyticJacobianC,
   controldc_initialAnalyticJacobianD,
   controldc_initialAnalyticJacobianF,
   controldc_functionJacA_column,
   controldc_functionJacB_column,
   controldc_functionJacC_column,
   controldc_functionJacD_column,
   controldc_functionJacF_column,
   controldc_linear_model_frame,
   controldc_linear_model_datarecovery_frame,
   controldc_mayer,
   controldc_lagrange,
   controldc_pickUpBoundsForInputsInOptimization,
   controldc_setInputData,
   controldc_getTimeGrid,
   controldc_symbolicInlineSystem,
   controldc_function_initSynchronous,
   controldc_function_updateSynchronous,
   controldc_function_equationsSynchronous,
   controldc_inputNames,
   NULL,
   NULL,
   NULL,
   -1

};

#define _OMC_LIT_RESOURCE_0_name_data "Complex"
#define _OMC_LIT_RESOURCE_0_dir_data "/usr/lib/omlibrary"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_name,7,_OMC_LIT_RESOURCE_0_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir,18,_OMC_LIT_RESOURCE_0_dir_data);

#define _OMC_LIT_RESOURCE_1_name_data "Modelica"
#define _OMC_LIT_RESOURCE_1_dir_data "/usr/lib/omlibrary/Modelica 3.2.2"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_name,8,_OMC_LIT_RESOURCE_1_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir,33,_OMC_LIT_RESOURCE_1_dir_data);

#define _OMC_LIT_RESOURCE_2_name_data "ModelicaServices"
#define _OMC_LIT_RESOURCE_2_dir_data "/usr/lib/omlibrary/ModelicaServices 3.2.2"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_name,16,_OMC_LIT_RESOURCE_2_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir,41,_OMC_LIT_RESOURCE_2_dir_data);

#define _OMC_LIT_RESOURCE_3_name_data "controldc"
#define _OMC_LIT_RESOURCE_3_dir_data "/home/ubuntu"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_name,9,_OMC_LIT_RESOURCE_3_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir,12,_OMC_LIT_RESOURCE_3_dir_data);

static const MMC_DEFSTRUCTLIT(_OMC_LIT_RESOURCES,8,MMC_ARRAY_TAG) {MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir)}};
void controldc_setupDataStruc(DATA *data, threadData_t *threadData)
{
  assertStreamPrint(threadData,0!=data, "Error while initialize Data");
  threadData->localRoots[LOCAL_ROOT_SIMULATION_DATA] = data;
  data->callback = &controldc_callback;
  OpenModelica_updateUriMapping(threadData, MMC_REFSTRUCTLIT(_OMC_LIT_RESOURCES));
  data->modelData->modelName = "controldc";
  data->modelData->modelFilePrefix = "controldc";
  data->modelData->resultFileName = NULL;
  data->modelData->modelDir = "/home/ubuntu";
  data->modelData->modelGUID = "{cb569c03-2223-41e3-bb73-3ae23754b664}";
  #if defined(OPENMODELICA_XML_FROM_FILE_AT_RUNTIME)
  data->modelData->initXMLData = NULL;
  data->modelData->modelDataXml.infoXMLData = NULL;
  #else
  #if defined(_MSC_VER) /* handle joke compilers */
  {
  /* for MSVC we encode a string like char x[] = {'a', 'b', 'c', '\0'} */
  /* because the string constant limit is 65535 bytes */
  static const char contents_init[] =
    #include "controldc_init.c"
    ;
  static const char contents_info[] =
    #include "controldc_info.c"
    ;
    data->modelData->initXMLData = contents_init;
    data->modelData->modelDataXml.infoXMLData = contents_info;
  }
  #else /* handle real compilers */
  data->modelData->initXMLData =
  #include "controldc_init.c"
    ;
  data->modelData->modelDataXml.infoXMLData =
  #include "controldc_info.c"
    ;
  #endif /* defined(_MSC_VER) */
  #endif /* defined(OPENMODELICA_XML_FROM_FILE_AT_RUNTIME) */
  
  data->modelData->nStates = 3;
  data->modelData->nVariablesReal = 25;
  data->modelData->nDiscreteReal = 0;
  data->modelData->nVariablesInteger = 0;
  data->modelData->nVariablesBoolean = 0;
  data->modelData->nVariablesString = 0;
  data->modelData->nParametersReal = 12;
  data->modelData->nParametersInteger = 1;
  data->modelData->nParametersBoolean = 3;
  data->modelData->nParametersString = 0;
  data->modelData->nInputVars = 3;
  data->modelData->nOutputVars = 0;
  
  data->modelData->nAliasReal = 30;
  data->modelData->nAliasInteger = 0;
  data->modelData->nAliasBoolean = 0;
  data->modelData->nAliasString = 0;
  
  data->modelData->nZeroCrossings = 0;
  data->modelData->nSamples = 0;
  data->modelData->nRelations = 0;
  data->modelData->nMathEvents = 0;
  data->modelData->nExtObjs = 0;
  
  data->modelData->modelDataXml.fileName = "controldc_info.json";
  data->modelData->modelDataXml.modelInfoXmlLength = 0;
  data->modelData->modelDataXml.nFunctions = 0;
  data->modelData->modelDataXml.nProfileBlocks = 0;
  data->modelData->modelDataXml.nEquations = 58;
  data->modelData->nMixedSystems = 0;
  data->modelData->nLinearSystems = 0;
  data->modelData->nNonLinearSystems = 0;
  data->modelData->nStateSets = 0;
  data->modelData->nJacobians = 5;
  data->modelData->nOptimizeConstraints = 0;
  data->modelData->nOptimizeFinalConstraints = 0;
  
  data->modelData->nDelayExpressions = 0;
  
  data->modelData->nClocks = 0;
  data->modelData->nSubClocks = 0;
  
  data->modelData->nSensitivityVars = 0;
  data->modelData->nSensitivityParamVars = 0;
  data->modelData->nSetcVars = 0;
  data->modelData->ndataReconVars = 0;
}

static int rml_execution_failed()
{
  fflush(NULL);
  fprintf(stderr, "Execution failed!\n");
  fflush(NULL);
  return 1;
}

#if defined(threadData)
#undef threadData
#endif
/* call the simulation runtime main from our main! */
int main(int argc, char**argv)
{
  int res;
  DATA data;
  MODEL_DATA modelData;
  SIMULATION_INFO simInfo;
  data.modelData = &modelData;
  data.simulationInfo = &simInfo;
  measure_time_flag = 0;
  compiledInDAEMode = 0;
  compiledWithSymSolver = 0;
  MMC_INIT(0);
  omc_alloc_interface.init();
  {
    MMC_TRY_TOP()
  
    MMC_TRY_STACK()
  
    controldc_setupDataStruc(&data, threadData);
    res = _main_SimulationRuntime(argc, argv, &data, threadData);
    
    MMC_ELSE()
    rml_execution_failed();
    fprintf(stderr, "Stack overflow detected and was not caught.\nSend us a bug report at https://trac.openmodelica.org/OpenModelica/newticket\n    Include the following trace:\n");
    printStacktraceMessages();
    fflush(NULL);
    return 1;
    MMC_CATCH_STACK()
    
    MMC_CATCH_TOP(return rml_execution_failed());
  }

  fflush(NULL);
  EXIT(res);
  return res;
}

#ifdef __cplusplus
}
#endif


