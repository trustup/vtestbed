model tankmodel_2
  output Real vff;
  package Medium = Modelica.Media.Water.ConstantPropertyLiquidWater;
  inner Modelica.Fluid.System system(energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial) annotation(
    Placement(visible = true, transformation(extent = {{240, 50}, {260, 70}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank mainTank(redeclare package Medium = Medium, crossArea = 3, height = 20, level_start = 0.05, nPorts = 3, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1)}) annotation(
    Placement(visible = true, transformation(extent = {{46, 22}, {86, 62}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank secondaryTank(redeclare package Medium = Medium, crossArea = 3, height = 30, level_start = 0.05, nPorts = 2, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1, height = 18)}) annotation(
    Placement(visible = true, transformation(extent = {{-44, -50}, {-4, -10}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis hysteresis(pre_y_start = false, uHigh = 2.4, uLow = 1.014) annotation(
    Placement(visible = true, transformation(extent = {{-118, 42}, {-98, 62}}, rotation = 0)));
  Modelica.Fluid.Sensors.Pressure pressure(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(extent = {{98, 26}, {118, 46}}, rotation = 0)));
  Modelica.Blocks.MathBoolean.Not not2 annotation(
    Placement(visible = true, transformation(origin = {-75, 51}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Fluid.Sources.Boundary_pT source(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 2.5e6) annotation(
    Placement(visible = true, transformation(origin = {-230, 22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputOne(y = product1.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -32}, {-209, -12}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve1 annotation(
    Placement(visible = true, transformation(origin = {-188, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Division division annotation(
    Placement(visible = true, transformation(origin = {141, 39}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 100000) annotation(
    Placement(visible = true, transformation(origin = {128, 36}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Sources.FixedBoundary sink(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{260, 0}, {240, 20}}, rotation = 0)));
  Modelica.Blocks.Sources.Step valveOpening(height = 1, offset = 1e-6, startTime = 30) annotation(
    Placement(visible = true, transformation(origin = {-224, 62}, extent = {{4, -4}, {-4, 4}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveDiscrete emergencyValve(redeclare package Medium = Medium, dp(start = 10000), dp_nominal = 100000, m_flow_nominal = 50) annotation(
    Placement(visible = true, transformation(origin = {-192, 22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.RealToBoolean realToBoolean annotation(
    Placement(visible = true, transformation(origin = {-193, 55}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput on(start = 1) annotation(
    Placement(visible = true, transformation(origin = {-235, 49}, extent = {{-13, -13}, {13, 13}}, rotation = 0), iconTransformation(origin = {-235, 49}, extent = {{-13, -13}, {13, 13}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valve1(redeclare package Medium = Medium, dp_nominal = 250000, m_flow_nominal = 46) annotation(
    Placement(visible = true, transformation(origin = {-26, 22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valve2(redeclare package Medium = Medium, dp_nominal = 500000, m_flow_nominal = 37) annotation(
    Placement(visible = true, transformation(origin = {-106, -22}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valveOutput(redeclare package Medium = Medium, dp_nominal = 100000, m_flow_nominal = 303) annotation(
    Placement(visible = true, transformation(origin = {192, 12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal annotation(
    Placement(visible = true, transformation(origin = {-58, 52}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput input1(start = 0.6) annotation(
    Placement(visible = true, transformation(origin = {-16, 68}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-16, 68}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input2(start = 0.3) annotation(
    Placement(visible = true, transformation(origin = {-96, 18}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-96, 18}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input3(start = 0.5) annotation(
    Placement(visible = true, transformation(origin = {198, 52}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {198, 52}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Math.Product product1 annotation(
    Placement(visible = true, transformation(origin = {-26, 44}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product2 annotation(
    Placement(visible = true, transformation(origin = {-106, 0}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product3 annotation(
    Placement(visible = true, transformation(origin = {192, 32}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal1 annotation(
    Placement(visible = true, transformation(origin = {-114, 14}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product annotation(
    Placement(visible = true, transformation(origin = {-212, 54}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Sources.FixedBoundary environment(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{78, -70}, {58, -50}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe(redeclare package Medium = Medium, diameter = 0.1, height_ab = -18, length = 30) annotation(
    Placement(visible = true, transformation(origin = {24, -38}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputTwo(y = product2.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -48}, {-209, -28}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve2 annotation(
    Placement(visible = true, transformation(origin = {-188, -38}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -38}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputThree(y = product3.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -64}, {-209, -44}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve3 annotation(
    Placement(visible = true, transformation(origin = {-188, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression tank2_flow(y = secondaryTank.ports[1].m_flow) annotation(
    Placement(visible = true, transformation(extent = {{114, -42}, {149, -22}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput velocityTank2 annotation(
    Placement(visible = true, transformation(origin = {170, -32}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -32}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Logical.Timer timer annotation(
    Placement(visible = true, transformation(origin = {-71, 91}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput massOverflow annotation(
    Placement(visible = true, transformation(origin = {170, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -54}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const1(k = 75.5) annotation(
    Placement(visible = true, transformation(origin = {146, -54}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis hysteresis1(pre_y_start = true, uHigh = 0.1, uLow = -0.1) annotation(
    Placement(visible = true, transformation(extent = {{-4, 88}, {16, 108}}, rotation = 0)));
  Modelica.Blocks.Logical.Timer timer1 annotation(
    Placement(visible = true, transformation(origin = {59, 121}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis newHyster(pre_y_start = false, uHigh = 40, uLow = 1) annotation(
    Placement(visible = true, transformation(extent = {{100, 106}, {120, 126}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal3 annotation(
    Placement(visible = true, transformation(origin = {182, 86}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal4 annotation(
    Placement(visible = true, transformation(origin = {198, 86}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.MathBoolean.Not not1 annotation(
    Placement(visible = true, transformation(origin = {153, 117}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression realExpression(y = vff) annotation(
    Placement(visible = true, transformation(extent = {{-82, 108}, {-47, 128}}, rotation = 0)));
  Modelica.Blocks.Math.Product product4 annotation(
    Placement(visible = true, transformation(origin = {184, 66}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
equation
  vff = 3 * sin(0.05 * timer.y);
  connect(hysteresis.y, not2.u) annotation(
    Line(points = {{-97, 52}, {-83.5, 52}, {-83.5, 51}, {-82, 51}}, color = {255, 0, 255}));
  connect(inputOne.y, ApertureValve1) annotation(
    Line(points = {{-207, -22}, {-188, -22}}, color = {0, 0, 127}));
  connect(division.u1, pressure.p) annotation(
    Line(points = {{133, 43}, {118, 43}, {118, 36}, {119, 36}}, color = {0, 0, 127}));
  connect(const.y, division.u2) annotation(
    Line(points = {{132, 36}, {132, 35.5}, {133, 35.5}, {133, 35}}, color = {0, 0, 127}));
  connect(division.y, hysteresis.u) annotation(
    Line(points = {{149, 39}, {154.5, 39}, {154.5, 41}, {160, 41}, {160, 76}, {-132, 76}, {-132, 52}, {-120, 52}}, color = {0, 0, 127}));
  connect(emergencyValve.port_a, source.ports[1]) annotation(
    Line(points = {{-202, 22}, {-220, 22}}, color = {0, 127, 255}));
  connect(realToBoolean.y, emergencyValve.open) annotation(
    Line(points = {{-187.5, 55}, {-192, 55}, {-192, 30}}, color = {255, 0, 255}));
  connect(mainTank.ports[1], pressure.port) annotation(
    Line(points = {{66, 22}, {68, 22}, {68, 18}, {108, 18}, {108, 26}}, color = {0, 127, 255}));
  connect(mainTank.ports[2], valveOutput.port_a) annotation(
    Line(points = {{66, 22}, {74, 22}, {74, 12}, {182, 12}}, color = {0, 127, 255}));
  connect(valveOutput.port_b, sink.ports[1]) annotation(
    Line(points = {{202, 12}, {221, 12}, {221, 10}, {240, 10}}, color = {0, 127, 255}));
  connect(not2.y, booleanToReal.u) annotation(
    Line(points = {{-69, 51}, {-65.5, 51}, {-65.5, 52}, {-63, 52}}, color = {255, 0, 255}));
  connect(product1.y, valve1.opening) annotation(
    Line(points = {{-26, 40}, {-26, 30}}, color = {0, 0, 127}));
  connect(product1.u1, input1) annotation(
    Line(points = {{-24, 49}, {-16, 49}, {-16, 68}}, color = {0, 0, 127}));
  connect(booleanToReal.y, product1.u2) annotation(
    Line(points = {{-54, 52}, {-28, 52}, {-28, 49}}, color = {0, 0, 127}));
  connect(input2, product2.u1) annotation(
    Line(points = {{-96, 18}, {-96, 11}, {-104, 11}, {-104, 5}}, color = {0, 0, 127}));
  connect(booleanToReal1.y, product2.u2) annotation(
    Line(points = {{-114, 10}, {-108, 10}, {-108, 5}}, color = {0, 0, 127}));
  connect(booleanToReal1.u, hysteresis.y) annotation(
    Line(points = {{-114, 19}, {-114, 34}, {-92, 34}, {-92, 52}, {-97, 52}}, color = {255, 0, 255}));
  connect(product2.y, valve2.opening) annotation(
    Line(points = {{-106, -4}, {-106, -14}}, color = {0, 0, 127}));
  connect(product3.u1, input3) annotation(
    Line(points = {{194, 37}, {198, 37}, {198, 52}}, color = {0, 0, 127}));
  connect(product3.y, valveOutput.opening) annotation(
    Line(points = {{192, 28}, {192, 20}}, color = {0, 0, 127}));
  connect(valve1.port_b, mainTank.ports[3]) annotation(
    Line(points = {{-16, 22}, {66, 22}}, color = {0, 127, 255}));
  connect(valve2.port_b, secondaryTank.ports[1]) annotation(
    Line(points = {{-96, -22}, {-66, -22}, {-66, -56}, {-30, -56}, {-30, -50}, {-24, -50}}, color = {0, 127, 255}));
  connect(emergencyValve.port_b, valve1.port_a) annotation(
    Line(points = {{-182, 22}, {-36, 22}}, color = {0, 127, 255}));
  connect(valve2.port_a, emergencyValve.port_b) annotation(
    Line(points = {{-116, -22}, {-160, -22}, {-160, 22}, {-182, 22}}, color = {0, 127, 255}));
  connect(on, product.u2) annotation(
    Line(points = {{-235, 49}, {-206, 49}, {-206, 52}, {-217, 52}}, color = {0, 0, 127}));
  connect(valveOpening.y, product.u1) annotation(
    Line(points = {{-228, 62}, {-218, 62}, {-218, 56}, {-217, 56}}, color = {0, 0, 127}));
  connect(product.y, realToBoolean.u) annotation(
    Line(points = {{-208, 54}, {-199, 54}, {-199, 55}}, color = {0, 0, 127}));
  connect(pipe.port_a, secondaryTank.ports[2]) annotation(
    Line(points = {{14, -38}, {-24, -38}, {-24, -50}}, color = {0, 127, 255}));
  connect(pipe.port_b, environment.ports[1]) annotation(
    Line(points = {{34, -38}, {58, -38}, {58, -60}}, color = {0, 127, 255}));
  connect(inputTwo.y, ApertureValve2) annotation(
    Line(points = {{-207, -38}, {-188, -38}}, color = {0, 0, 127}));
  connect(inputThree.y, ApertureValve3) annotation(
    Line(points = {{-207, -54}, {-188, -54}}, color = {0, 0, 127}));
  connect(tank2_flow.y, velocityTank2) annotation(
    Line(points = {{151, -32}, {170, -32}}, color = {0, 0, 127}));
  connect(const1.y, massOverflow) annotation(
    Line(points = {{153, -54}, {170, -54}}, color = {0, 0, 127}));
  connect(timer.u, hysteresis.y) annotation(
    Line(points = {{-77, 91}, {-86, 91}, {-86, 52}, {-97, 52}}, color = {255, 0, 255}));
  connect(timer1.y, newHyster.u) annotation(
    Line(points = {{64.5, 121}, {98, 121}, {98, 116}}, color = {0, 0, 127}));
  connect(timer1.u, hysteresis1.y) annotation(
    Line(points = {{53, 121}, {40, 121}, {40, 98}, {18, 98}}, color = {255, 0, 255}));
  connect(newHyster.y, not1.u) annotation(
    Line(points = {{122, 116}, {144, 116}, {144, 118}, {146, 118}}, color = {255, 0, 255}));
  connect(not1.y, booleanToReal4.u) annotation(
    Line(points = {{160, 118}, {198, 118}, {198, 90}, {198, 90}}, color = {255, 0, 255}));
  connect(booleanToReal3.u, hysteresis1.y) annotation(
    Line(points = {{182, 90}, {182, 90}, {182, 98}, {18, 98}, {18, 98}}, color = {255, 0, 255}));
  connect(realExpression.y, hysteresis1.u) annotation(
    Line(points = {{-46, 118}, {-6, 118}, {-6, 98}, {-6, 98}}, color = {0, 0, 127}));
  connect(product4.y, product3.u2) annotation(
    Line(points = {{184, 62}, {190, 62}, {190, 36}, {190, 36}}, color = {0, 0, 127}));
  connect(booleanToReal4.y, product4.u1) annotation(
    Line(points = {{198, 82}, {198, 78.5}, {186, 78.5}, {186, 71}}, color = {0, 0, 127}));
  connect(booleanToReal3.y, product4.u2) annotation(
    Line(points = {{182, 82}, {182, 71}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.2"), Buildings(version = "7.0.0")));
end tankmodel_2;