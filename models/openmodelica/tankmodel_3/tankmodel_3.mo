model tankmodel_3
  output Real vff;
  package Medium = Modelica.Media.Water.ConstantPropertyLiquidWater;
  inner Modelica.Fluid.System system(energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial) annotation(
    Placement(visible = true, transformation(extent = {{240, 24}, {260, 44}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank mainTank(redeclare package Medium = Medium, crossArea = 3, height = 30, level_start = 0.05, nPorts = 3, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1)}) annotation(
    Placement(visible = true, transformation(extent = {{46, -4}, {86, 36}}, rotation = 0)));
  Modelica.Fluid.Vessels.OpenTank secondaryTank(redeclare package Medium = Medium, crossArea = 3, height = 30, level_start = 0.05, nPorts = 2, portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1, height = 18)}) annotation(
    Placement(visible = true, transformation(extent = {{-44, -76}, {-4, -36}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis hysteresis(pre_y_start = false, uHigh = 2.7, uLow = 1.014) annotation(
    Placement(visible = true, transformation(extent = {{-118, 16}, {-98, 36}}, rotation = 0)));
  Modelica.Fluid.Sensors.Pressure pressure(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(extent = {{98, 0}, {118, 20}}, rotation = 0)));
  Modelica.Blocks.MathBoolean.Not not2 annotation(
    Placement(visible = true, transformation(origin = {-73, 25}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Fluid.Sources.Boundary_pT source(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 2.5e6) annotation(
    Placement(visible = true, transformation(origin = {-230, -4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputOne(y = product1.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -58}, {-209, -38}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve1 annotation(
    Placement(visible = true, transformation(origin = {-188, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Division division annotation(
    Placement(visible = true, transformation(origin = {141, 13}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 100000) annotation(
    Placement(visible = true, transformation(origin = {128, 10}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Sources.FixedBoundary sink(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{260, -26}, {240, -6}}, rotation = 0)));
  Modelica.Blocks.Sources.Step valveOpening(height = 1, offset = 1e-6, startTime = 30) annotation(
    Placement(visible = true, transformation(origin = {-226, 40}, extent = {{4, -4}, {-4, 4}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveDiscrete emergencyValve(redeclare package Medium = Medium, dp(start = 10000), dp_nominal = 100000, m_flow_nominal = 50) annotation(
    Placement(visible = true, transformation(origin = {-192, -4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.RealToBoolean realToBoolean annotation(
    Placement(visible = true, transformation(origin = {-193, 29}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput on(start = 1) annotation(
    Placement(visible = true, transformation(origin = {-235, 23}, extent = {{-13, -13}, {13, 13}}, rotation = 0), iconTransformation(origin = {-235, 23}, extent = {{-13, -13}, {13, 13}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valve1(redeclare package Medium = Medium, dp_nominal = 250000, m_flow_nominal = 46) annotation(
    Placement(visible = true, transformation(origin = {-26, -4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valve2(redeclare package Medium = Medium, dp_nominal = 500000, m_flow_nominal = 37) annotation(
    Placement(visible = true, transformation(origin = {-106, -48}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valveOutput(redeclare package Medium = Medium, dp_nominal = 100000, m_flow_nominal = 303) annotation(
    Placement(visible = true, transformation(origin = {192, -14}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal annotation(
    Placement(visible = true, transformation(origin = {-58, 26}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput input1(start = 0.6) annotation(
    Placement(visible = true, transformation(origin = {-16, 42}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-16, 42}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input2(start = 0.3) annotation(
    Placement(visible = true, transformation(origin = {-96, -8}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-96, -8}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input3(start = 0.5) annotation(
    Placement(visible = true, transformation(origin = {198, 26}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {198, 26}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Math.Product product1 annotation(
    Placement(visible = true, transformation(origin = {-26, 18}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product2 annotation(
    Placement(visible = true, transformation(origin = {-106, -26}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product3 annotation(
    Placement(visible = true, transformation(origin = {192, 6}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal1 annotation(
    Placement(visible = true, transformation(origin = {-114, -12}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product annotation(
    Placement(visible = true, transformation(origin = {-212, 28}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Sources.FixedBoundary environment(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{78, -96}, {58, -76}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe(redeclare package Medium = Medium, diameter = 0.1, height_ab = -18, length = 30) annotation(
    Placement(visible = true, transformation(origin = {24, -64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputTwo(y = product2.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -74}, {-209, -54}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve2 annotation(
    Placement(visible = true, transformation(origin = {-188, -64}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputThree(y = product3.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -90}, {-209, -70}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve3 annotation(
    Placement(visible = true, transformation(origin = {-188, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression tank2_flow(y = secondaryTank.ports[1].m_flow) annotation(
    Placement(visible = true, transformation(extent = {{114, -68}, {149, -48}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput velocityTank2 annotation(
    Placement(visible = true, transformation(origin = {170, -58}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -58}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Logical.Timer timer annotation(
    Placement(visible = true, transformation(origin = {-75, 43}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput massOverflow annotation(
    Placement(visible = true, transformation(origin = {170, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const1(k = 75.5) annotation(
    Placement(visible = true, transformation(origin = {146, -80}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis hysteresis1(pre_y_start = true, uHigh = 0.1, uLow = -0.1) annotation(
    Placement(visible = true, transformation(extent = {{-4, 62}, {16, 82}}, rotation = 0)));
  Modelica.Blocks.Logical.Timer timer1 annotation(
    Placement(visible = true, transformation(origin = {59, 95}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Logical.Hysteresis newHyster(pre_y_start = false, uHigh = 40, uLow = 1) annotation(
    Placement(visible = true, transformation(extent = {{100, 80}, {120, 100}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal3 annotation(
    Placement(visible = true, transformation(origin = {182, 60}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal4 annotation(
    Placement(visible = true, transformation(origin = {198, 60}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.MathBoolean.Not not1 annotation(
    Placement(visible = true, transformation(origin = {153, 91}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression realExpression(y = vff) annotation(
    Placement(visible = true, transformation(extent = {{-82, 82}, {-47, 102}}, rotation = 0)));
  Modelica.Blocks.Math.Product product4 annotation(
    Placement(visible = true, transformation(origin = {184, 40}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput PLC(start = 0) annotation(
    Placement(visible = true, transformation(origin = {-157, 65}, extent = {{-11, -11}, {11, 11}}, rotation = 0), iconTransformation(origin = {-157, 65}, extent = {{-11, -11}, {11, 11}}, rotation = 0)));
  Modelica.Blocks.Math.RealToBoolean realToBoolean1 annotation(
    Placement(visible = true, transformation(origin = {-126, 66}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.MathBoolean.Not not3 annotation(
    Placement(visible = true, transformation(origin = {-99, 67}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Logical.Timer timer_plc annotation(
    Placement(visible = true, transformation(origin = {-105, 85}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal5 annotation(
    Placement(visible = true, transformation(origin = {-78, 68}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Math.Product product5 annotation(
    Placement(visible = true, transformation(origin = {-34, 38}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealOutput pressure1 annotation(
    Placement(visible = true, transformation(origin = {166, 0}, extent = {{-6, -6}, {6, 6}}, rotation = 0), iconTransformation(origin = {166, 0}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
equation
  vff = 3 * sin(0.05 * timer_plc.y);
  connect(hysteresis.y, not2.u) annotation(
    Line(points = {{-97, 26}, {-83.5, 26}, {-83.5, 25}, {-80, 25}}, color = {255, 0, 255}));
  connect(inputOne.y, ApertureValve1) annotation(
    Line(points = {{-207, -48}, {-188, -48}}, color = {0, 0, 127}));
  connect(division.u1, pressure.p) annotation(
    Line(points = {{133, 17}, {118, 17}, {118, 10}, {119, 10}}, color = {0, 0, 127}));
  connect(const.y, division.u2) annotation(
    Line(points = {{132, 10}, {132, 9.5}, {133, 9.5}, {133, 9}}, color = {0, 0, 127}));
  connect(division.y, hysteresis.u) annotation(
    Line(points = {{149, 13}, {153.75, 13}, {153.75, 15}, {158.5, 15}, {158.5, 50}, {-132, 50}, {-132, 26}, {-120, 26}}, color = {0, 0, 127}));
  connect(emergencyValve.port_a, source.ports[1]) annotation(
    Line(points = {{-202, -4}, {-220, -4}}, color = {0, 127, 255}));
  connect(realToBoolean.y, emergencyValve.open) annotation(
    Line(points = {{-187.5, 29}, {-192, 29}, {-192, 4}}, color = {255, 0, 255}));
  connect(mainTank.ports[1], pressure.port) annotation(
    Line(points = {{66, -4}, {68, -4}, {68, -8}, {108, -8}, {108, 0}}, color = {0, 127, 255}));
  connect(mainTank.ports[2], valveOutput.port_a) annotation(
    Line(points = {{66, -4}, {74, -4}, {74, -14}, {182, -14}}, color = {0, 127, 255}));
  connect(valveOutput.port_b, sink.ports[1]) annotation(
    Line(points = {{202, -14}, {221, -14}, {221, -16}, {240, -16}}, color = {0, 127, 255}));
  connect(not2.y, booleanToReal.u) annotation(
    Line(points = {{-67, 25}, {-65.5, 25}, {-65.5, 26}, {-63, 26}}, color = {255, 0, 255}));
  connect(product1.y, valve1.opening) annotation(
    Line(points = {{-26, 14}, {-26, 4}}, color = {0, 0, 127}));
  connect(product1.u1, input1) annotation(
    Line(points = {{-24, 23}, {-16, 23}, {-16, 42}}, color = {0, 0, 127}));
  connect(input2, product2.u1) annotation(
    Line(points = {{-96, -8}, {-96, -15}, {-100, -15}, {-100, -21}, {-104, -21}}, color = {0, 0, 127}));
  connect(booleanToReal1.y, product2.u2) annotation(
    Line(points = {{-114, -16}, {-108, -16}, {-108, -21}}, color = {0, 0, 127}));
  connect(booleanToReal1.u, hysteresis.y) annotation(
    Line(points = {{-114, -7}, {-114, 8}, {-92, 8}, {-92, 26}, {-97, 26}}, color = {255, 0, 255}));
  connect(product2.y, valve2.opening) annotation(
    Line(points = {{-106, -30}, {-106, -40}}, color = {0, 0, 127}));
  connect(product3.u1, input3) annotation(
    Line(points = {{194, 11}, {198, 11}, {198, 26}}, color = {0, 0, 127}));
  connect(product3.y, valveOutput.opening) annotation(
    Line(points = {{192, 2}, {192, -6}}, color = {0, 0, 127}));
  connect(valve1.port_b, mainTank.ports[3]) annotation(
    Line(points = {{-16, -4}, {66, -4}}, color = {0, 127, 255}));
  connect(valve2.port_b, secondaryTank.ports[1]) annotation(
    Line(points = {{-96, -48}, {-66, -48}, {-66, -82}, {-45, -82}, {-45, -76}, {-24, -76}}, color = {0, 127, 255}));
  connect(emergencyValve.port_b, valve1.port_a) annotation(
    Line(points = {{-182, -4}, {-36, -4}}, color = {0, 127, 255}));
  connect(valve2.port_a, emergencyValve.port_b) annotation(
    Line(points = {{-116, -48}, {-160, -48}, {-160, -4}, {-182, -4}}, color = {0, 127, 255}));
  connect(on, product.u2) annotation(
    Line(points = {{-235, 23}, {-206, 23}, {-206, 26}, {-217, 26}}, color = {0, 0, 127}));
  connect(valveOpening.y, product.u1) annotation(
    Line(points = {{-230, 40}, {-218, 40}, {-218, 30}, {-217, 30}}, color = {0, 0, 127}));
  connect(product.y, realToBoolean.u) annotation(
    Line(points = {{-208, 28}, {-199, 28}, {-199, 29}}, color = {0, 0, 127}));
  connect(pipe.port_a, secondaryTank.ports[2]) annotation(
    Line(points = {{14, -64}, {-24, -64}, {-24, -76}}, color = {0, 127, 255}));
  connect(pipe.port_b, environment.ports[1]) annotation(
    Line(points = {{34, -64}, {58, -64}, {58, -86}}, color = {0, 127, 255}));
  connect(inputTwo.y, ApertureValve2) annotation(
    Line(points = {{-207, -64}, {-188, -64}}, color = {0, 0, 127}));
  connect(inputThree.y, ApertureValve3) annotation(
    Line(points = {{-207, -80}, {-188, -80}}, color = {0, 0, 127}));
  connect(tank2_flow.y, velocityTank2) annotation(
    Line(points = {{151, -58}, {170, -58}}, color = {0, 0, 127}));
  connect(const1.y, massOverflow) annotation(
    Line(points = {{153, -80}, {170, -80}}, color = {0, 0, 127}));
  connect(timer.u, hysteresis.y) annotation(
    Line(points = {{-81, 43}, {-86, 43}, {-86, 26}, {-97, 26}}, color = {255, 0, 255}));
  connect(timer1.y, newHyster.u) annotation(
    Line(points = {{64.5, 95}, {98, 95}, {98, 90}}, color = {0, 0, 127}));
  connect(timer1.u, hysteresis1.y) annotation(
    Line(points = {{53, 95}, {40, 95}, {40, 72}, {17, 72}}, color = {255, 0, 255}));
  connect(newHyster.y, not1.u) annotation(
    Line(points = {{121, 90}, {144, 90}, {144, 92}, {145, 92}, {145, 91}, {146, 91}}, color = {255, 0, 255}));
  connect(not1.y, booleanToReal4.u) annotation(
    Line(points = {{159, 91}, {179, 91}, {179, 92}, {198, 92}, {198, 65}}, color = {255, 0, 255}));
  connect(booleanToReal3.u, hysteresis1.y) annotation(
    Line(points = {{182, 65}, {182, 72}, {17, 72}}, color = {255, 0, 255}));
  connect(realExpression.y, hysteresis1.u) annotation(
    Line(points = {{-45, 92}, {-6, 92}, {-6, 72}}, color = {0, 0, 127}));
  connect(product4.y, product3.u2) annotation(
    Line(points = {{184, 36}, {190, 36}, {190, 11}}, color = {0, 0, 127}));
  connect(booleanToReal4.y, product4.u1) annotation(
    Line(points = {{198, 56}, {198, 52.5}, {186, 52.5}, {186, 45}}, color = {0, 0, 127}));
  connect(booleanToReal3.y, product4.u2) annotation(
    Line(points = {{182, 56}, {182, 45}}, color = {0, 0, 127}));
  connect(PLC, realToBoolean1.u) annotation(
    Line(points = {{-157, 65}, {-123.5, 65}, {-123.5, 66}, {-131, 66}}, color = {0, 0, 127}));
  connect(realToBoolean1.y, not3.u) annotation(
    Line(points = {{-122, 66}, {-115, 66}, {-115, 67}, {-106, 67}}, color = {255, 0, 255}));
  connect(realToBoolean1.y, timer_plc.u) annotation(
    Line(points = {{-122, 66}, {-116, 66}, {-116, 85}, {-111, 85}}, color = {255, 0, 255}));
  connect(not3.y, booleanToReal5.u) annotation(
    Line(points = {{-93, 67}, {-93, 68}, {-83, 68}}, color = {255, 0, 255}));
  connect(booleanToReal5.y, product5.u1) annotation(
    Line(points = {{-74, 68}, {-32, 68}, {-32, 43}}, color = {0, 0, 127}));
  connect(product5.y, product1.u2) annotation(
    Line(points = {{-34, 34}, {-34, 22}, {-31, 22}, {-31, 23}, {-28, 23}}, color = {0, 0, 127}));
  connect(booleanToReal.y, product5.u2) annotation(
    Line(points = {{-54, 26}, {-46, 26}, {-46, 46}, {-36, 46}, {-36, 43}}, color = {0, 0, 127}));
  connect(division.y, pressure1) annotation(
    Line(points = {{149, 13}, {151, 13}, {151, 14}, {154, 14}, {154, 0}, {166, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.2"), Buildings(version = "7.0.0")));
end tankmodel_3;