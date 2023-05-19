/* Linearization */
#include "controldc_model.h"
#if defined(__cplusplus)
extern "C" {
#endif
const char *controldc_linear_model_frame()
{
  return "model linear_controldc\n  parameter Integer n = 3 \"number of states\";\n  parameter Integer p = 3 \"number of inputs\";\n  parameter Integer q = 0 \"number of outputs\";\n"
  "\n"
  "  parameter Real x0[n] = %s;\n"
  "  parameter Real u0[p] = %s;\n"
  "\n"
  "  parameter Real A[n, n] = [%s];\n"
  "  parameter Real B[n, p] = [%s];\n"
  "  parameter Real C[q, n] = zeros(q, n);%s\n"
  "  parameter Real D[q, p] = zeros(q, p);%s\n"
  "\n"
  "  Real x[n](start=x0);\n"
  "  input Real u[p](start=u0);\n"
  "  output Real y[q];\n"
  "\n"
  "  Real 'x_inductor.Psi' = x[1];\n""  Real 'x_inertia1.phi' = x[2];\n""  Real 'x_inertia1.w' = x[3];\n"
  "  Real 'u_L' = u[1];\n""  Real 'u_R' = u[2];\n""  Real 'u_u' = u[3];\n"
  "equation\n  der(x) = A * x + B * u;\n  y = C * x + D * u;\nend linear_controldc;\n";
}
const char *controldc_linear_model_datarecovery_frame()
{
  return "model linear_controldc\n  parameter Integer n = 3 \"number of states\";\n  parameter Integer p = 3 \"number of inputs\";\n  parameter Integer q = 0 \"number of outputs\";\n  parameter Integer nz = 19 \"data recovery variables\";\n"
  "\n"
  "  parameter Real x0[3] = %s;\n"
  "  parameter Real u0[3] = %s;\n"
  "  parameter Real z0[19] = %s;\n"
  "\n"
  "  parameter Real A[n, n] = [%s];\n"
  "  parameter Real B[n, p] = [%s];\n"
  "  parameter Real C[q, n] = zeros(q, n);%s\n"
  "  parameter Real D[q, p] = zeros(q, p);%s\n"
  "  parameter Real Cz[nz, n] = [%s];\n"
  "  parameter Real Dz[nz, p] = [%s];\n"
  "\n"
  "  Real x[n](start=x0);\n"
  "  input Real u[p](start=u0);\n"
  "  output Real y[q];\n"
  "  output Real z[nz];\n"
  "\n"
  "  Real 'x_inductor.Psi' = x[1];\n""  Real 'x_inertia1.phi' = x[2];\n""  Real 'x_inertia1.w' = x[3];\n"
  "  Real 'u_L' = u[1];\n""  Real 'u_R' = u[2];\n""  Real 'u_u' = u[3];\n"
  "  Real 'z_der(emf.phi)' = z[1];\n""  Real 'z_$cse1' = z[2];\n""  Real 'z_L' = z[3];\n""  Real 'z_R' = z[4];\n""  Real 'z_emf.phi' = z[5];\n""  Real 'z_emf.tau' = z[6];\n""  Real 'z_emf.v' = z[7];\n""  Real 'z_emf.w' = z[8];\n""  Real 'z_ground1.p.i' = z[9];\n""  Real 'z_ground1.p.v' = z[10];\n""  Real 'z_inductor.p.v' = z[11];\n""  Real 'z_inductor.v' = z[12];\n""  Real 'z_inertia1.a' = z[13];\n""  Real 'z_inertia1.flange_b.tau' = z[14];\n""  Real 'z_resistor.LossPower' = z[15];\n""  Real 'z_resistor.R_actual' = z[16];\n""  Real 'z_resistor.v' = z[17];\n""  Real 'z_signalVoltage1.i' = z[18];\n""  Real 'z_u' = z[19];\n"
  "equation\n  der(x) = A * x + B * u;\n  y = C * x + D * u;\n  z = Cz * x + Dz * u;\nend linear_controldc;\n";
}
#if defined(__cplusplus)
}
#endif

