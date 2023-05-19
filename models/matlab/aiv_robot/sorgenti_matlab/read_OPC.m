close all;
clear all;
clc;
uaClient = opcua('localhost',4841); 
connect(uaClient); 

a=uaClient.Namespace
%a=uaClient.Namespace(2).Children;

%writeValue(uaClient, a(1), 22);
%writeValue(uaClient, a(2), 34);

%readValue(uaClient, a(3));
%writeValue(uaClient, a(4), '2,5')

%c = readValue(uaClient, a(3))
%d = strsplit(c,',')


%myNode = opcuanode(2,1)
%writeValue(uaClient,myNode,pi)


%a = uaClient.Namespace(2).Children

var1 = findNodeByName(a,'nextWaypoints');
%writeValue(uaClient, var1, 5);
prova = [2,3];
writeValue(uaClient, var1, prova)
a = readValue(uaClient, var1);




filename = 'arm.gif';
info = imfinfo(filename);
transparent_color = info(1).TransparentColor;
delays = [info.DelayTime] / 100;   %varies for each frame!
[gifImage cmap] = imread('arm.gif', 'Frames', 'all');
alphas = double(gifImage ~= transparent_color);
len = size(gifImage, 4);
for frame = 1 : len
   image(gifImage(:,:,:,frame));
   colormap(cmap);
   pause(delays(frame));
end

