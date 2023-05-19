model tankmodel_plc
  package Medium = Modelica.Media.Water.ConstantPropertyLiquidWater;
  
  inner Modelica.Fluid.System system(energyDynamics = Modelica.Fluid.Types.Dynamics.FixedInitial) annotation(
    Placement(visible = true, transformation(extent = {{240, 80}, {260, 100}}, rotation = 0)));
  
  Modelica.Fluid.Vessels.OpenTank mainTank(
  redeclare package Medium = Medium, 
  crossArea = 3, 
  height = 20, 
  level_start = 0.05, 
  nPorts = 3, 
  portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1),     Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2, height = 2, zeta_out = 0, zeta_in = 1)}) annotation(
    Placement(visible = true, transformation(extent = {{46, 52}, {86, 92}}, rotation = 0)));
  
  Modelica.Fluid.Vessels.OpenTank secondaryTank(
  redeclare package Medium = Medium, 
  crossArea = 3, 
  height = 30, 
  level_start = 0.05, 
  nPorts = 2, 
  portsData = {Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.2), Modelica.Fluid.Vessels.BaseClasses.VesselPortsData(diameter = 0.1, height = 18)}) annotation(
    Placement(visible = true, transformation(extent = {{-44, -20}, {-4, 20}}, rotation = 0)));
  
  Modelica.Fluid.Sensors.Pressure pressure(redeclare package Medium = Medium) annotation(
    Placement(visible = true, transformation(extent = {{98, 56}, {118, 76}}, rotation = 0)));
  
  Modelica.Blocks.MathBoolean.Not not2 annotation(
    Placement(visible = true, transformation(origin = {-75, 81}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  
  Modelica.Fluid.Sources.Boundary_pT source(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 2.5e6) annotation(
    Placement(visible = true, transformation(origin = {-230, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  
  Modelica.Blocks.Sources.RealExpression inputOne(y = product1.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -2}, {-209, 18}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve1 annotation(
    Placement(visible = true, transformation(origin = {-188, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Division division annotation(
    Placement(visible = true, transformation(origin = {141, 69}, extent = {{-7, -7}, {7, 7}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const(k = 100000)  annotation(
    Placement(visible = true, transformation(origin = {128, 66}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  
  Modelica.Fluid.Sources.FixedBoundary sink(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{260, 30}, {240, 50}}, rotation = 0)));
  
  Modelica.Blocks.Sources.Step valveOpening(height = 1,offset = 1e-6, startTime = 30) annotation(
    Placement(visible = true, transformation(origin = {-224, 92}, extent = {{4, -4}, {-4, 4}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveDiscrete emergencyValve(redeclare package Medium = Medium, dp(start = 10000), dp_nominal = 100000, m_flow_nominal = 50) annotation(
    Placement(visible = true, transformation(origin = {-192, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.RealToBoolean realToBoolean annotation(
    Placement(visible = true, transformation(origin = {-193, 85}, extent = {{-5, -5}, {5, 5}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput on(start=1) annotation(
    Placement(visible = true, transformation(origin = {-235, 79}, extent = {{-13, -13}, {13, 13}}, rotation = 0), iconTransformation(origin = {-235, 79}, extent = {{-13, -13}, {13, 13}}, rotation = 0)));
  
  Modelica.Fluid.Valves.ValveLinear valve1(redeclare package Medium = Medium, dp_nominal = 250000, m_flow_nominal = 46) annotation(
    Placement(visible = true, transformation(origin = {-26, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valve2(redeclare package Medium = Medium, dp_nominal = 500000, m_flow_nominal = 37) annotation(
    Placement(visible = true, transformation(origin = {-106, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Fluid.Valves.ValveLinear valveOutput(redeclare package Medium = Medium, dp_nominal = 100000, m_flow_nominal = 303) annotation(
    Placement(visible = true, transformation(origin = {192, 42}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal annotation(
    Placement(visible = true, transformation(origin = {-58, 82}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput input1(start = 0.6) annotation(
    Placement(visible = true, transformation(origin = {-16, 98}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-16, 98}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input2(start = 0.3) annotation(
    Placement(visible = true, transformation(origin = {-96, 48}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {-96, 48}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput input3(start = 0.5) annotation(
    Placement(visible = true, transformation(origin = {198, 82}, extent = {{-8, -8}, {8, 8}}, rotation = -90), iconTransformation(origin = {198, 82}, extent = {{-8, -8}, {8, 8}}, rotation = -90)));
  Modelica.Blocks.Math.Product product1 annotation(
    Placement(visible = true, transformation(origin = {-26, 74}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product2 annotation(
    Placement(visible = true, transformation(origin = {-106, 30}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product3 annotation(
    Placement(visible = true, transformation(origin = {192, 62}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal1 annotation(
    Placement(visible = true, transformation(origin = {-114, 44}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.BooleanToReal booleanToReal2 annotation(
    Placement(visible = true, transformation(origin = {184, 78}, extent = {{-4, -4}, {4, 4}}, rotation = -90)));
  Modelica.Blocks.Math.Product product annotation(
    Placement(visible = true, transformation(origin = {-212, 84}, extent = {{-4, -4}, {4, 4}}, rotation = 0)));
  Modelica.Fluid.Sources.FixedBoundary environment(redeclare package Medium = Medium, T = system.T_ambient, nPorts = 1, p = 1) annotation(
    Placement(visible = true, transformation(extent = {{78, -40}, {58, -20}}, rotation = 0)));
  Modelica.Fluid.Pipes.StaticPipe pipe(redeclare package Medium = Medium, diameter = 0.1, height_ab = -18, length = 30) annotation(
    Placement(visible = true, transformation(origin = {24, -8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputTwo(y = product2.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -18}, {-209, 2}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve2 annotation(
    Placement(visible = true, transformation(origin = {-188, -8}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression inputThree(y = product3.y) annotation(
    Placement(visible = true, transformation(extent = {{-244, -34}, {-209, -14}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput ApertureValve3 annotation(
    Placement(visible = true, transformation(origin = {-188, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {-188, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.RealExpression tank2_flow(y = secondaryTank.ports[1].m_flow) annotation(
    Placement(visible = true, transformation(extent = {{114, -12}, {149, 8}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput velocityTank2 annotation(
    Placement(visible = true, transformation(origin = {170, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput massOverflow annotation(
    Placement(visible = true, transformation(origin = {170, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {170, -24}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant const1(k = 75.5)  annotation(
    Placement(visible = true, transformation(origin = {146, -24}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput pressure1 annotation(
    Placement(visible = true, transformation(origin = {172, 96}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {172, 96}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput PLC(start=0) annotation(
    Placement(visible = true, transformation(origin = {-128, 122}, extent = {{-14, -14}, {14, 14}}, rotation = 0), iconTransformation(origin = {-128, 122}, extent = {{-14, -14}, {14, 14}}, rotation = 0)));
  Modelica.Blocks.Math.RealToBoolean realToBoolean1 annotation(
    Placement(visible = true, transformation(origin = {-104, 80}, extent = {{-6, -6}, {6, 6}}, rotation = 0)));
equation
  connect(inputOne.y, ApertureValve1) annotation(
    Line(points = {{-207, 8}, {-188, 8}}, color = {0, 0, 127}));
  connect(division.u1, pressure.p) annotation(
    Line(points = {{133, 73}, {118, 73}, {118, 66}, {120, 66}}, color = {0, 0, 127}));
  connect(const.y, division.u2) annotation(
    Line(points = {{132, 66}, {132, 65.5}, {133, 65.5}, {133, 65}}, color = {0, 0, 127}));
  connect(emergencyValve.port_a, source.ports[1]) annotation(
    Line(points = {{-202, 52}, {-220, 52}}, color = {0, 127, 255}));
  connect(realToBoolean.y, emergencyValve.open) annotation(
    Line(points = {{-187.5, 85}, {-192, 85}, {-192, 60}}, color = {255, 0, 255}));
  connect(mainTank.ports[1], pressure.port) annotation(
    Line(points = {{66, 52}, {68, 52}, {68, 48}, {108, 48}, {108, 56}, {108, 56}}, color = {0, 127, 255}));
  connect(mainTank.ports[2], valveOutput.port_a) annotation(
    Line(points = {{66, 52}, {74, 52}, {74, 42}, {182, 42}}, color = {0, 127, 255}));
  connect(valveOutput.port_b, sink.ports[1]) annotation(
    Line(points = {{202, 42}, {240, 42}, {240, 40}}, color = {0, 127, 255}));
  connect(not2.y, booleanToReal.u) annotation(
    Line(points = {{-68, 82}, {-63, 82}}, color = {255, 0, 255}));
  connect(product1.y, valve1.opening) annotation(
    Line(points = {{-26, 70}, {-26, 70}, {-26, 60}, {-26, 60}}, color = {0, 0, 127}));
  connect(product1.u1, input1) annotation(
    Line(points = {{-24, 78}, {-16, 78}, {-16, 98}, {-16, 98}}, color = {0, 0, 127}));
  connect(booleanToReal.y, product1.u2) annotation(
    Line(points = {{-54, 82}, {-28, 82}, {-28, 78}, {-28, 78}}, color = {0, 0, 127}));
  connect(input2, product2.u1) annotation(
    Line(points = {{-96, 48}, {-96, 41}, {-104, 41}, {-104, 34}}, color = {0, 0, 127}));
  connect(booleanToReal1.y, product2.u2) annotation(
    Line(points = {{-114, 40}, {-108, 40}, {-108, 34}}, color = {0, 0, 127}));
  connect(product2.y, valve2.opening) annotation(
    Line(points = {{-106, 26}, {-106, 26}, {-106, 16}, {-106, 16}}, color = {0, 0, 127}));
  connect(product3.u1, input3) annotation(
    Line(points = {{194, 66}, {198, 66}, {198, 82}, {198, 82}}, color = {0, 0, 127}));
  connect(booleanToReal2.y, product3.u2) annotation(
    Line(points = {{184, 74}, {190, 74}, {190, 66}}, color = {0, 0, 127}));
  connect(product3.y, valveOutput.opening) annotation(
    Line(points = {{192, 58}, {192, 58}, {192, 50}, {192, 50}}, color = {0, 0, 127}));
  connect(valve1.port_b, mainTank.ports[3]) annotation(
    Line(points = {{-16, 52}, {60, 52}, {60, 52}, {66, 52}}, color = {0, 127, 255}));
  connect(valve2.port_b, secondaryTank.ports[1]) annotation(
    Line(points = {{-96, 8}, {-66, 8}, {-66, -26}, {-30, -26}, {-30, -20}, {-24, -20}}, color = {0, 127, 255}));
  connect(emergencyValve.port_b, valve1.port_a) annotation(
    Line(points = {{-182, 52}, {-36, 52}}, color = {0, 127, 255}));
  connect(valve2.port_a, emergencyValve.port_b) annotation(
    Line(points = {{-116, 8}, {-160, 8}, {-160, 52}, {-182, 52}}, color = {0, 127, 255}));
  connect(on, product.u2) annotation(
    Line(points = {{-235, 79}, {-206, 79}, {-206, 82}, {-217, 82}}, color = {0, 0, 127}));
  connect(valveOpening.y, product.u1) annotation(
    Line(points = {{-228, 92}, {-218, 92}, {-218, 86}, {-217, 86}}, color = {0, 0, 127}));
  connect(product.y, realToBoolean.u) annotation(
    Line(points = {{-208, 84}, {-199, 84}, {-199, 85}}, color = {0, 0, 127}));
  connect(pipe.port_a, secondaryTank.ports[2]) annotation(
    Line(points = {{14, -8}, {-24, -8}, {-24, -20}, {-24, -20}}, color = {0, 127, 255}));
  connect(pipe.port_b, environment.ports[1]) annotation(
    Line(points = {{34, -8}, {58, -8}, {58, -30}, {58, -30}}, color = {0, 127, 255}));
  connect(inputTwo.y, ApertureValve2) annotation(
    Line(points = {{-207, -8}, {-188, -8}}, color = {0, 0, 127}));
  connect(inputThree.y, ApertureValve3) annotation(
    Line(points = {{-207, -24}, {-188, -24}}, color = {0, 0, 127}));
  connect(tank2_flow.y, velocityTank2) annotation(
    Line(points = {{151, -2}, {170, -2}}, color = {0, 0, 127}));
  connect(const1.y, massOverflow) annotation(
    Line(points = {{152, -24}, {164, -24}, {164, -24}, {170, -24}}, color = {0, 0, 127}));
  connect(division.y, pressure1) annotation(
    Line(points = {{148, 70}, {156, 70}, {156, 94}, {172, 94}, {172, 96}}, color = {0, 0, 127}));
  connect(realToBoolean1.y, not2.u) annotation(
    Line(points = {{-98, 80}, {-82, 80}, {-82, 82}, {-82, 82}}, color = {255, 0, 255}));
  connect(realToBoolean1.y, booleanToReal1.u) annotation(
    Line(points = {{-98, 80}, {-114, 80}, {-114, 48}, {-114, 48}}, color = {255, 0, 255}));
  connect(PLC, realToBoolean1.u) annotation(
    Line(points = {{-128, 122}, {-128, 80}, {-112, 80}}, color = {0, 0, 127}));
  connect(booleanToReal2.u, realToBoolean1.y) annotation(
    Line(points = {{184, 82}, {184, 82}, {184, 120}, {-98, 120}, {-98, 80}, {-98, 80}}, color = {255, 0, 255}));
  annotation(
    uses(Modelica(version = "3.2.2"), Buildings(version = "7.0.0")));

end tankmodel_plc;