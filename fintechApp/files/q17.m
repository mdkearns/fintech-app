clear;
load('chemconc.mat');
load('chemconc2.mat');
histfit(ccr1)
hold
histfit(ccr2)
ylabel("Frequency")
xlabel("Chemical Concentration")
title("Chemical Concetration Comparison ccr1 & ccr2")
fitdist(ccr1, 'Normal')
fitdist(ccr2, 'Normal')