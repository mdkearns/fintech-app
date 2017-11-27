clear;
load('chemconc.mat');
bins = 16:0.1:18.2;
x = hist(ccr1,bins);
area = sum(x);
y_scaled = x/area;
bar(bins,y_scaled);