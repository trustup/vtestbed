/* Simulation code for controldc generated by the OpenModelica Compiler OpenModelica 1.14.1. */
#if !defined(controldc__MODEL_H)
#define controldc__MODEL_H

#include "openmodelica.h"
#include "openmodelica_func.h"
#include "simulation_data.h"
#include "simulation/simulation_info_json.h"
#include "simulation/simulation_runtime.h"
#include "util/omc_error.h"
#include "util/parallel_helper.h"
#include "simulation/solver/model_help.h"
#include "simulation/solver/delay.h"
#include "simulation/solver/linearSystem.h"
#include "simulation/solver/nonlinearSystem.h"
#include "simulation/solver/mixedSystem.h"

#if defined(__cplusplus)
extern "C" {
#endif

#include <string.h>

#include "controldc_functions.h"


extern void controldc_callExternalObjectDestructors(DATA *_data, threadData_t *threadData);
#if !defined(OMC_NUM_NONLINEAR_SYSTEMS) || OMC_NUM_NONLINEAR_SYSTEMS>0
#endif
#if !defined(OMC_NUM_LINEAR_SYSTEMS) || OMC_NUM_LINEAR_SYSTEMS>0
#endif
#if !defined(OMC_NUM_MIXED_SYSTEMS) || OMC_NUM_MIXED_SYSTEMS>0
#endif
#if !defined(OMC_NO_STATESELECTION)
extern void controldc_initializeStateSets(int nStateSets, STATE_SET_DATA* statesetData, DATA *data);
#endif
extern int controldc_functionAlgebraics(DATA *data, threadData_t *threadData);
extern int controldc_function_storeDelayed(DATA *data, threadData_t *threadData);
extern int controldc_updateBoundVariableAttributes(DATA *data, threadData_t *threadData);
extern int controldc_functionInitialEquations(DATA *data, threadData_t *threadData);
extern int controldc_functionInitialEquations_lambda0(DATA *data, threadData_t *threadData);
extern int controldc_functionRemovedInitialEquations(DATA *data, threadData_t *threadData);
extern int controldc_updateBoundParameters(DATA *data, threadData_t *threadData);
extern int controldc_checkForAsserts(DATA *data, threadData_t *threadData);
extern int controldc_function_ZeroCrossingsEquations(DATA *data, threadData_t *threadData);
extern int controldc_function_ZeroCrossings(DATA *data, threadData_t *threadData, double* gout);
extern int controldc_function_updateRelations(DATA *data, threadData_t *threadData, int evalZeroCross);
extern const char* controldc_zeroCrossingDescription(int i, int **out_EquationIndexes);
extern const char* controldc_relationDescription(int i);
extern void controldc_function_initSample(DATA *data, threadData_t *threadData);
extern int controldc_initialAnalyticJacobianG(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_initialAnalyticJacobianA(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_initialAnalyticJacobianB(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_initialAnalyticJacobianC(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_initialAnalyticJacobianD(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_initialAnalyticJacobianF(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *jacobian);
extern int controldc_functionJacG_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern int controldc_functionJacA_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern int controldc_functionJacB_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern int controldc_functionJacC_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern int controldc_functionJacD_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern int controldc_functionJacF_column(void* data, threadData_t *threadData, ANALYTIC_JACOBIAN *thisJacobian, ANALYTIC_JACOBIAN *parentJacobian);
extern const char* controldc_linear_model_frame(void);
extern const char* controldc_linear_model_datarecovery_frame(void);
extern int controldc_mayer(DATA* data, modelica_real** res, short *);
extern int controldc_lagrange(DATA* data, modelica_real** res, short *, short *);
extern int controldc_pickUpBoundsForInputsInOptimization(DATA* data, modelica_real* min, modelica_real* max, modelica_real*nominal, modelica_boolean *useNominal, char ** name, modelica_real * start, modelica_real * startTimeOpt);
extern int controldc_setInputData(DATA *data, const modelica_boolean file);
extern int controldc_getTimeGrid(DATA *data, modelica_integer * nsi, modelica_real**t);
extern void controldc_function_initSynchronous(DATA * data, threadData_t *threadData);
extern void controldc_function_updateSynchronous(DATA * data, threadData_t *threadData, long i);
extern int controldc_function_equationsSynchronous(DATA * data, threadData_t *threadData, long i);
extern void controldc_read_input_fmu(MODEL_DATA* modelData, SIMULATION_INFO* simulationData);
extern void controldc_function_savePreSynchronous(DATA *data, threadData_t *threadData);
extern int controldc_inputNames(DATA* data, char ** names);
extern int controldc_initializeDAEmodeData(DATA *data, DAEMODE_DATA*);
extern int controldc_functionLocalKnownVars(DATA*, threadData_t*);
extern int controldc_symbolicInlineSystem(DATA*, threadData_t*);

#include "controldc_literals.h"




#if defined(HPCOM) && !defined(_OPENMP)
  #error "HPCOM requires OpenMP or the results are wrong"
#endif
#if defined(_OPENMP)
  #include <omp.h>
#else
  /* dummy omp defines */
  #define omp_get_max_threads() 1
#endif

#if defined(__cplusplus)
}
#endif

#endif /* !defined(controldc__MODEL_H) */


