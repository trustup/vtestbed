/* update bound parameters and variable attributes (start, nominal, min, max) */
#include "controldc_model.h"
#if defined(__cplusplus)
extern "C" {
#endif

OMC_DISABLE_OPT
int controldc_updateBoundVariableAttributes(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  /* min ******************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating min-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* max ******************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating max-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* nominal **************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating nominal-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* start ****************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating primary start-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  TRACE_POP
  return 0;
}

void controldc_updateBoundParameters_0(DATA *data, threadData_t *threadData);

/*
equation index: 40
type: SIMPLE_ASSIGN
resistor.T = resistor.T_ref
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_40(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,40};
  data->simulationInfo->realParameter[8] /* resistor.T PARAM */ = data->simulationInfo->realParameter[10] /* resistor.T_ref PARAM */;
  TRACE_POP
}

/*
equation index: 41
type: SIMPLE_ASSIGN
resistor.T_heatPort = resistor.T
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_41(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,41};
  data->simulationInfo->realParameter[9] /* resistor.T_heatPort PARAM */ = data->simulationInfo->realParameter[8] /* resistor.T PARAM */;
  TRACE_POP
}

/*
equation index: 43
type: SIMPLE_ASSIGN
emf.internalSupport.phi = emf.fixed.phi0
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_43(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,43};
  data->simulationInfo->realParameter[3] /* emf.internalSupport.phi PARAM */ = data->simulationInfo->realParameter[1] /* emf.fixed.phi0 PARAM */;
  TRACE_POP
}

/*
equation index: 44
type: SIMPLE_ASSIGN
emf.internalSupport.flange.phi = emf.fixed.phi0
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_44(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,44};
  data->simulationInfo->realParameter[2] /* emf.internalSupport.flange.phi PARAM */ = data->simulationInfo->realParameter[1] /* emf.fixed.phi0 PARAM */;
  TRACE_POP
}

/*
equation index: 45
type: SIMPLE_ASSIGN
emf.fixed.flange.phi = emf.fixed.phi0
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_45(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,45};
  data->simulationInfo->realParameter[0] /* emf.fixed.flange.phi PARAM */ = data->simulationInfo->realParameter[1] /* emf.fixed.phi0 PARAM */;
  TRACE_POP
}
extern void controldc_eqFunction_3(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_2(DATA *data, threadData_t *threadData);

extern void controldc_eqFunction_1(DATA *data, threadData_t *threadData);


/*
equation index: 53
type: ALGORITHM

  assert(resistor.T_ref >= 0.0, "Variable violating min constraint: 0.0 <= resistor.T_ref, has value: " + String(resistor.T_ref, "g"));
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_53(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,53};
  modelica_boolean tmp0;
  static const MMC_DEFSTRINGLIT(tmp1,69,"Variable violating min constraint: 0.0 <= resistor.T_ref, has value: ");
  modelica_string tmp2;
  static int tmp3 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp3)
  {
    tmp0 = GreaterEq(data->simulationInfo->realParameter[10] /* resistor.T_ref PARAM */,0.0);
    if(!tmp0)
    {
      tmp2 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[10] /* resistor.T_ref PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp1),tmp2);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Electrical/Analog/Basic.mo",1578,5,1578,66,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nresistor.T_ref >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp3 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 54
type: ALGORITHM

  assert(resistor.T >= 0.0, "Variable violating min constraint: 0.0 <= resistor.T, has value: " + String(resistor.T, "g"));
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_54(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,54};
  modelica_boolean tmp4;
  static const MMC_DEFSTRINGLIT(tmp5,65,"Variable violating min constraint: 0.0 <= resistor.T, has value: ");
  modelica_string tmp6;
  static int tmp7 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp7)
  {
    tmp4 = GreaterEq(data->simulationInfo->realParameter[8] /* resistor.T PARAM */,0.0);
    if(!tmp4)
    {
      tmp6 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[8] /* resistor.T PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp5),tmp6);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Electrical/Analog/Interfaces.mo",306,5,307,99,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nresistor.T >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp7 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 55
type: ALGORITHM

  assert(resistor.T_heatPort >= 0.0, "Variable violating min constraint: 0.0 <= resistor.T_heatPort, has value: " + String(resistor.T_heatPort, "g"));
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_55(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,55};
  modelica_boolean tmp8;
  static const MMC_DEFSTRINGLIT(tmp9,74,"Variable violating min constraint: 0.0 <= resistor.T_heatPort, has value: ");
  modelica_string tmp10;
  static int tmp11 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp11)
  {
    tmp8 = GreaterEq(data->simulationInfo->realParameter[9] /* resistor.T_heatPort PARAM */,0.0);
    if(!tmp8)
    {
      tmp10 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[9] /* resistor.T_heatPort PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp9),tmp10);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Electrical/Analog/Interfaces.mo",313,5,313,56,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nresistor.T_heatPort >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp11 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 56
type: ALGORITHM

  assert(inertia1.stateSelect >= StateSelect.never and inertia1.stateSelect <= StateSelect.always, "Variable violating min/max constraint: StateSelect.never <= inertia1.stateSelect <= StateSelect.always, has value: " + String(inertia1.stateSelect, "d"));
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_56(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,56};
  modelica_boolean tmp12;
  modelica_boolean tmp13;
  static const MMC_DEFSTRINGLIT(tmp14,115,"Variable violating min/max constraint: StateSelect.never <= inertia1.stateSelect <= StateSelect.always, has value: ");
  modelica_string tmp15;
  static int tmp16 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp16)
  {
    tmp12 = GreaterEq(data->simulationInfo->integerParameter[0] /* inertia1.stateSelect PARAM */,1);
    tmp13 = LessEq(data->simulationInfo->integerParameter[0] /* inertia1.stateSelect PARAM */,5);
    if(!(tmp12 && tmp13))
    {
      tmp15 = modelica_integer_to_modelica_string_format(data->simulationInfo->integerParameter[0] /* inertia1.stateSelect PARAM */, (modelica_string) mmc_strings_len1[100]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp14),tmp15);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Mechanics/Rotational.mo",2411,7,2413,61,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\ninertia1.stateSelect >= StateSelect.never and inertia1.stateSelect <= StateSelect.always", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp16 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 57
type: ALGORITHM

  assert(inertia1.J >= 0.0, "Variable violating min constraint: 0.0 <= inertia1.J, has value: " + String(inertia1.J, "g"));
*/
OMC_DISABLE_OPT
static void controldc_eqFunction_57(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,57};
  modelica_boolean tmp17;
  static const MMC_DEFSTRINGLIT(tmp18,65,"Variable violating min constraint: 0.0 <= inertia1.J, has value: ");
  modelica_string tmp19;
  static int tmp20 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp20)
  {
    tmp17 = GreaterEq(data->simulationInfo->realParameter[7] /* inertia1.J PARAM */,0.0);
    if(!tmp17)
    {
      tmp19 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[7] /* inertia1.J PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp18),tmp19);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.2/Mechanics/Rotational.mo",2410,7,2410,65,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\ninertia1.J >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp20 = 1;
    }
  }
  TRACE_POP
}
OMC_DISABLE_OPT
void controldc_updateBoundParameters_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  controldc_eqFunction_40(data, threadData);
  controldc_eqFunction_41(data, threadData);
  controldc_eqFunction_43(data, threadData);
  controldc_eqFunction_44(data, threadData);
  controldc_eqFunction_45(data, threadData);
  controldc_eqFunction_3(data, threadData);
  controldc_eqFunction_2(data, threadData);
  controldc_eqFunction_1(data, threadData);
  controldc_eqFunction_53(data, threadData);
  controldc_eqFunction_54(data, threadData);
  controldc_eqFunction_55(data, threadData);
  controldc_eqFunction_56(data, threadData);
  controldc_eqFunction_57(data, threadData);
  TRACE_POP
}
OMC_DISABLE_OPT
int controldc_updateBoundParameters(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  data->simulationInfo->realParameter[1] /* emf.fixed.phi0 PARAM */ = 0.0;
  data->modelData->realParameterData[1].time_unvarying = 1;
  data->simulationInfo->booleanParameter[0] /* emf.useSupport PARAM */ = 0;
  data->modelData->booleanParameterData[0].time_unvarying = 1;
  data->simulationInfo->booleanParameter[1] /* inductor.UIC PARAM */ = 0;
  data->modelData->booleanParameterData[1].time_unvarying = 1;
  data->simulationInfo->booleanParameter[2] /* resistor.useHeatPort PARAM */ = 0;
  data->modelData->booleanParameterData[2].time_unvarying = 1;
  data->simulationInfo->integerParameter[0] /* inertia1.stateSelect PARAM */ = 3;
  data->modelData->integerParameterData[0].time_unvarying = 1;
  controldc_updateBoundParameters_0(data, threadData);
  TRACE_POP
  return 0;
}

#if defined(__cplusplus)
}
#endif

