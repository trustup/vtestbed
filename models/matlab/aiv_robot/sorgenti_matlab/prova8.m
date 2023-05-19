clc, close all, clear all;


uaClient = opcua('localhost',4841); 
connect(uaClient);
%ua=uaClient.Namespace(2).Children
ua=uaClient.Namespace;
var1 = findNodeByName(ua,'position_X');
var2 = findNodeByName(ua,'position_Y');
var3 = findNodeByName(ua,'start');
var4 = findNodeByName(ua,'nextWaypoints');
var5 = findNodeByName(ua,'speed');
var6 = findNodeByName(ua,'station');

var7 = findNodeByName(ua,'plc_control');
var8 = findNodeByName(ua, 'state_station');



R = 0.1;                % Wheel radius [m]
L = 0.5;                % Wheelbase [m]
dd = DifferentialDrive(R,L);

sampleTime = 0.1;               % Sample time [s]
tVec = 0:sampleTime:300;         % Time array

initPose = [8;3.1;60];             % Initial pose (x y theta)
pose = zeros(3,numel(tVec));    % Pose matrix
pose(:,1) = initPose;

stations = [4,2.4; 4,3.45];
%stations_reached = zeros(1, length(stations));
stations_reached = [0 0 0];
%waypoints = [8,3.2; 4.35,3.2; 4.35,2.7; 4.35,4; 3.7,8.7; 8,8.7; 10,10; 9,8; 8,2];
waypoints = [8,3.1; 4.7,3.1; 4.7,2.4; 4,2.4; 4.7,2.4; 4.7,3.1; 4.7,3.45; 4,3.45];
waypoints_start = [8,3.1; 4.7,3.1; 4.7,2.4; 4,2.4; 4.7,2.4; 4.7,3.1; 4.7,3.45; 4,3.45];
%stri = num2str(waypoints(end,1))+","+num2str(waypoints(end,2));

%vct = [waypoints(end,1), waypoints(end,2)];
%writeValue(uaClient, var4, vct);

% Load map and inflate it by a safety distance
close all
%load exampleMap
%inflate(map,R);

controller = controllerPurePursuit;
controller.Waypoints = waypoints;
controller.LookaheadDistance = 0.10;
controller.DesiredLinearVelocity = 0.35;
writeValue(uaClient, var5, controller.DesiredLinearVelocity);
controller.MaxAngularVelocity = 5;

load depuy_map % Reload original (uninflated) map for visualization
viz = Visualizer2D;
viz.hasWaypoints = true;
viz.mapName = 'mapForSim.simMap';

start = 1;
writeValue(uaClient, var3, start); %start
station_actual = 0;
station_idx = 1;
writeValue(uaClient, var6, station_actual); %station 
writeValue(uaClient, var8, 0);
%tol = controller.DesiredLinearVelocity * 2
tol=.03;
numberStations = length(stations);


img = imread('dep.png');
imshow(img);
%hold on;
r = rateControl(1/sampleTime);

rep = 5;
position = 0;
for idx = 2:numel(tVec) 
    
    %%tmp = str2double(strsplit(readValue(uaClient, var4),","));
    %tmp = readValue(uaClient, var4);
    %if tmp(1,1) ~= waypoints(end,1) || tmp(1,2) ~= waypoints(end,2)
    %    waypoints(end+1,:) = [tmp(1,1),tmp(1,2)]; 
        %%waypoints(end+1,2) = tmp_y;
    %    controller.Waypoints = waypoints;
    %end
    if readValue(uaClient, var5) ~= controller.DesiredLinearVelocity
        controller.DesiredLinearVelocity = readValue(uaClient, var5);
    end
    
    if readValue(uaClient, var3) == 1 && readValue(uaClient, var7) == 1
        [vRef,wRef] = controller(pose(:,idx-1));
        [wL,wR] = inverseKinematics(dd,vRef,wRef);
    
        % Compute the velocities
        [v,w] = forwardKinematics(dd,wL,wR);
        velB = [v;0;w]; % Body velocities [vx;vy;w]
        vel = bodyToWorld(velB,pose(:,idx-1));  % Convert from body to world
        
        pose(:,idx) = round(pose(:,idx-1),2) + vel*sampleTime; 
        writeValue(uaClient, var1, pose(1,idx));
        writeValue(uaClient, var2, pose(2,idx));
        A = stations(station_idx,1);
        B = stations(station_idx,2);
        if pose(:,idx) ~= pose(:, idx-1)
            position = position + 1;
        end
        if position > 10 && abs(stations(station_idx,1)-round(pose(1,idx),2)) < tol && abs(stations(station_idx,2) - round(pose(2,idx),2)) < tol %&& stations_reached(1, station_idx-1) == 0
            %station_ok = 0;
            writeValue(uaClient, var8, 0);
            station_actual = station_actual + 1;
            writeValue(uaClient, var6, station_actual);
            position = 0;
            station_graph(uaClient, var8);
            if station_idx < numberStations
                station_idx = station_idx + 1;
            else
                waypoints = [waypoints; waypoints_start];
                controller.Waypoints = waypoints;
                station_idx = 1;
                station_actual = 0;
                writeValue(uaClient, var6, station_actual);
                writeValue(uaClient, var8, 0);
            end
            %waitfor(2);
        end
    else
        pose(:,idx) = pose(:,idx-1);
        writeValue(uaClient, var1, pose(1,idx));
        writeValue(uaClient, var2, pose(2,idx));
    end
    % Update visualization
    viz(pose(:,idx),stations)
    waitfor(r);
end


function station_graph(ua, var8)
    %writeValue(ua, var, 0)
    filename = 'arm.gif';
    info = imfinfo(filename);
    transparent_color = info(1).TransparentColor;
    delays = [info.DelayTime] / 100;   %varies for each frame!
    [gifImage cmap] = imread('arm.gif', 'Frames', 'all');
    alphas = double(gifImage ~= transparent_color);
    len = size(gifImage, 4);
    for frame = 1 : len
        figure(3), image(gifImage(:,:,:,frame));
        colormap(cmap);
        pause(delays(frame));
    end
    writeValue(ua, var8, 1);
end


