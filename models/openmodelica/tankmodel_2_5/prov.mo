model prov
  Modelica.Blocks.Sources.BooleanTable booleanTable(startValue = false, table = {0, 10, 20, 50}) annotation(
    Placement(visible = true, transformation(origin = {-36, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.BooleanOutput y annotation(
    Placement(visible = true, transformation(origin = {12, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {12, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.BooleanExpression booleanExpression annotation(
    Placement(visible = true, transformation(origin = {-28, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.BooleanOutput y1 annotation(
    Placement(visible = true, transformation(origin = {10, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {10, -44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.BooleanPulse booleanPulse annotation(
    Placement(visible = true, transformation(origin = {-36, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
//  if time > 30 then
//   y2 = 4;
//   ciao = 0;
// else
//  y2 = time;
//end if;
  connect(booleanTable.y, y) annotation(
    Line(points = {{-24, 2}, {4, 2}, {4, 0}, {12, 0}}, color = {255, 0, 255}));
  connect(booleanExpression.y, y1) annotation(
    Line(points = {{-16, -44}, {4, -44}, {4, -44}, {10, -44}}, color = {255, 0, 255}));
  annotation(
    uses(Modelica(version = "3.2.2")));
end prov;