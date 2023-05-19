clc, clear all, close all;
T = readtable('data.xlsx');

uaClient = opcua('localhost',4841); 
connect(uaClient);
ua=uaClient.Namespace;
var1 = findNodeByName(ua,'noise');
var2 = findNodeByName(ua,'on_off');

sim_mean = 1;
sim_std = 0.05;
%noise=0;
noise = readValue(uaClient, var1);


data = T(:,2);
b=mean(data.Var2);
a=std(data.Var2);

sampleTime = 0.1;               % Sample time [s]
tVec = 0:sampleTime:300;         % Time array
r = rateControl(0.1/sampleTime);


sensor_data = a.*randn(1,3001) + b;
%figure(1), plot(tVec, sensor_data, '*-')

%yy = randi(10, 1000, 1);     % Simulated Data
%xx = 1:length(yy);            % ‘x’ (Independent) Variable
%figure(1)                   % Plot
%plot(tVec, sensor_data)
%grid

%figure(2), plot(tVec(1:100), a.*randn(1,100) + b, '-b') 
%hold on
%grid on
%ylim([0 50])
%hold off

diff = 0;
c=0;
tol=.05;
on_off = 1;
for idx = 2:numel(tVec) 
    
    noise = readValue(uaClient, var1);
    noise=double(noise);
    if abs(diff-noise) > tol
        if diff < noise
            diff = diff + 1/10;
        elseif diff > noise
            diff = diff - 1/10;
        end
        %c = c+1;
    end
    
    on_off_received = readValue(uaClient, var2);
    if on_off_received == 0 && on_off ~= 0
        on_off = on_off - 1/5;
    elseif on_off_received == 1 && on_off ~= 1
        on_off = on_off + 1/5;
    end
    
    disp(diff)
    disp(noise)
    sim = on_off * (sim_std.*randn(1,1) + (sim_mean+(diff)));
    figure(1), plot(idx, sim, '-bx')
    hold on
    grid on
    drawnow
    ylim([0 5])
    
    
    %sensor = a.*randn(1,1) + (b* (exp(sim)/exp(1)) );
    sensor = on_off* (a.*randn(1,1) + (b* (exp(double(diff))) ));
    figure(2), plot(idx, sensor, '-bx')
    hold on
    grid on
    drawnow
    ylim([0 300])
    %figure(2), plot(sim_var * randn(1,1) + b, '*-')
    
waitfor(r);
end
