clc, close all, clear all;

T = readtable('data.xlsx');

sampleTime = 0.1;               % Sample time [s]
tVec = 0:sampleTime:600;         % Time array
r = rateControl(0.1/sampleTime);

%value from opc server
uaClient = opcua('localhost',4841); 
connect(uaClient);
ua=uaClient.Namespace;
s1x = findNodeByName(ua,'75xi821bx');
s1y = findNodeByName(ua,'75xi821by');
s2x = findNodeByName(ua,'75xi822bx');
s2y = findNodeByName(ua,'75xi822by');
s3x = findNodeByName(ua,'75xi823bx');
s3y = findNodeByName(ua,'75xi823by');
s4x = findNodeByName(ua,'75xi824bx');
s4y = findNodeByName(ua,'75xi824by');
s5a = findNodeByName(ua,'75zi800ba');
s5b = findNodeByName(ua,'75zi800bb');
s6a = findNodeByName(ua,'75zi801ba');
s6b = findNodeByName(ua,'75zi801bb');

var1 = findNodeByName(ua,'on_off');
var2 = findNodeByName(ua,'noise_A');
var3 = findNodeByName(ua,'noise_B');
var4 = findNodeByName(ua,'noise_C');

var5 = findNodeByName(ua,'ST-7501_A');
var6 = findNodeByName(ua,'ST-7501_B');
var7 = findNodeByName(ua,'ST-7501_C');

var8 = findNodeByName(ua,'K-7502_A');
var9 = findNodeByName(ua,'K-7502_B');
var10 = findNodeByName(ua,'K-7502_C');


%means and variance sensors
data = T(:,2);
s75xi821bx_mean=mean(data.Var2);
s75xi821bx_var=std(data.Var2);

data = T(:,3);
s75xi821by_mean=mean(data.Var3);
s75xi821by_var=std(data.Var3);

data = T(:,4);
s75xi822bx_mean=mean(data.Var4);
s75xi822bx_var=std(data.Var4);

data = T(:,5);
s75xi822by_mean=mean(data.Var5);
s75xi822by_var=std(data.Var5);

data = T(:,6);
s75xi823bx_mean=mean(data.Var6);
s75xi823bx_var=std(data.Var6);

data = T(:,7);
s75xi823by_mean=mean(data.Var7);
s75xi823by_var=std(data.Var7);

data = T(:,8);
s75xi824bx_mean=mean(data.Var8);
s75xi824bx_var=std(data.Var8);

data = T(:,9);
s75xi824by_mean=mean(data.Var9);
s75xi824by_var=std(data.Var9);

data = T(:,10);
s75zi800ba_mean=mean(data.Var10);
s75zi800ba_var=std(data.Var10);

data = T(:,11);
s75zi800bb_mean=mean(data.Var11);
s75zi800bb_var=std(data.Var11);

data = T(:,12);
s75zi801ba_mean=mean(data.Var12);
s75zi801ba_var=std(data.Var12);

data = T(:,13);
s75zi801bb_mean=mean(data.Var13);
s75zi801bb_var=std(data.Var13);


%mean and variance for sim values
sim1_mean = 1;
sim1_std = 0.05;

sim2_mean = 1;
sim2_std = 0.05;

sim3_mean = 1;
sim3_std = 0.05;


sim4_mean = 1.2;
sim4_std = 0.1;

sim5_mean = 1.2;
sim5_std = 0.01;

sim6_mean = 1.2;
sim6_std = 0.1;


diff_A = 0;
diff_B = 0;
diff_C = 0;
tol=.05;
on_off = 1;
for idx = 2:numel(tVec) 

    %sensor = a.*randn(1,1) + (b* (exp(sim)/exp(1)) );
    %sensor = a.*randn(1,1) + (b*exp(double(noise)));
    %figure(2), plot(idx, sensor, '-bx')
    %hold on
    %grid on
    %drawnow
    %ylim([0 300])
    %figure(2), plot(sim_var * randn(1,1) + b, '*-')
    
    noise_A = readValue(uaClient, var2);
    noise_A=double(noise_A);
    if abs(diff_A-noise_A) > tol
        if diff_A < noise_A
            diff_A = diff_A + 1/10;
        elseif diff_A > noise_A
            diff_A = diff_A - 1/10;
        end
    end
    
    noise_B = readValue(uaClient, var3);
    noise_B=double(noise_B);
    if abs(diff_B-noise_B) > tol
        if diff_B < noise_B
            diff_B = diff_B + 1/10;
        elseif diff_B > noise_B
            diff_B = diff_B - 1/10;
        end
    end
    
    noise_C = readValue(uaClient, var4);
    noise_C=double(noise_C);
    if abs(diff_C-noise_C) > tol
        if diff_C < noise_C
            diff_C = diff_C + 1/10;
        elseif diff_C > noise_C
            diff_C = diff_C - 1/10;
        end
    end
    
    on_off_received = readValue(uaClient, var1);
    if on_off_received == 0 && on_off ~= 0
        on_off = on_off - 1/5;
        on_off = round(on_off,4);
    elseif on_off_received == 1 && on_off ~= 1
        on_off = on_off + 1/5;
        on_off = round(on_off,4);
    end
    
    %simulation for ST-7501
    sim1 = on_off * (sim1_std.*randn(1,1) + (sim1_mean+(diff_A)));
    sim2 = on_off * (sim2_std.*randn(1,1) + (sim2_mean+(diff_B)));
    sim3 = on_off * (sim3_std.*randn(1,1) + (sim3_mean+(diff_C)));
    
    %simulation for K-7502
    sim4 = on_off * (sim4_std.*randn(1,1) + (sim4_mean+(diff_A)));
    sim5 = on_off * (sim5_std.*randn(1,1) + (sim5_mean+(diff_B)));
    sim6 = on_off * (sim6_std.*randn(1,1) + (sim6_mean+(diff_C)));
    
    
    s75xi821bx = on_off * (s75xi821bx_var.*randn(1,1) + (s75xi821bx_mean*exp(double(diff_A))) );
    s75xi821by = on_off * (s75xi821by_var.*randn(1,1) + (s75xi821by_mean*exp(1.5*(double(diff_A)))) );
    s75xi822bx = on_off * (s75xi822bx_var.*randn(1,1) + (s75xi822bx_mean*exp(double(diff_B))) );
    s75xi822by = on_off * (s75xi822by_var.*randn(1,1) + (s75xi822by_mean*exp(double(diff_B))) );
    s75xi823bx = on_off * (s75xi823bx_var.*randn(1,1) + s75xi823bx_mean );
    s75xi823by = on_off * (s75xi823by_var.*randn(1,1) + s75xi823by_mean );
    s75xi824bx = on_off * (s75xi824bx_var.*randn(1,1) + s75xi824bx_mean );
    s75xi824by = on_off * (s75xi824by_var.*randn(1,1) + s75xi824by_mean );
    s75zi800ba = on_off * (s75zi800ba_var.*randn(1,1) + (s75zi800ba_mean*exp(double(diff_C/2))) );
    s75zi800bb = on_off * (s75zi800bb_var.*randn(1,1) + (s75zi800bb_mean*exp(double(diff_C/2))) );
    s75zi801ba = on_off * (s75zi801ba_var.*randn(1,1) + s75zi801ba_mean );
    s75zi801bb = on_off * (s75zi801bb_var.*randn(1,1) + s75zi801bb_mean );
    
%     figure(1), subplot(3,2,1), plot(idx, s75xi821bx, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 150])
%     xlabel('s75xi821bx')
%     subplot(3,2,2), plot(idx, s75xi821by, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 20])
%     xlabel('s75xi821by')
%     subplot(3,2,3), plot(idx, s75xi822bx, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 20])
%     xlabel('s75xi822bx')
%     subplot(3,2,4), plot(idx, s75xi822by, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 20])
%     xlabel('s75xi822by')
%     subplot(3,2,5), plot(idx, s75zi800ba, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([-1 1])
%     xlabel('s75zi800ba')
%     subplot(3,2,6), plot(idx, s75zi800bb, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([-1 1])
%     xlabel('s75zi800bb')
%     
%     figure(2), subplot(3,1,1), plot(idx, sim1, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 10])
%     xlabel('ST-7501_A')
%     subplot(3,1,2), plot(idx, sim2, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 10])
%     xlabel('ST-7501_B')
%     subplot(3,1,3), plot(idx, sim3, '-bx');
%     hold on
%     grid on
%     drawnow
%     ylim([0 10])
%     xlabel('ST-7501_C')
   
    %figure(1), plot(idx, s75xi822bx, '-bx')
    %hold on
    %grid on
    %drawnow
    %ylim([0 200])
    
    %figure(3), plot(idx, s75xi822by, '-bx')
    %hold on
    %grid on
    %drawnow
    %ylim([0 200])
    
    %figure(2), plot(idx, sim2, '-bx')
    %hold on
    %grid on
    %drawnow
    %ylim([0 10])
    
    
    writeValue(uaClient, s1x, s75xi821bx);
    writeValue(uaClient, s1y, s75xi821by);
    writeValue(uaClient, s2x, s75xi822bx);
    writeValue(uaClient, s2y, s75xi822by);
    writeValue(uaClient, s3x, s75xi823bx);
    writeValue(uaClient, s3y, s75xi823by);
    writeValue(uaClient, s4x, s75xi824bx);
    writeValue(uaClient, s4y, s75xi824by);
    writeValue(uaClient, s5a, s75zi800ba);
    writeValue(uaClient, s5b, s75zi800bb);
    writeValue(uaClient, s6a, s75zi801ba);
    writeValue(uaClient, s6b, s75zi801bb);
    
    writeValue(uaClient, var5, sim1);
    writeValue(uaClient, var6, sim2);
    writeValue(uaClient, var7, sim3);
    
    writeValue(uaClient, var8, sim4);
    writeValue(uaClient, var9, sim5);
    writeValue(uaClient, var10, sim6);
    
waitfor(r);
end


