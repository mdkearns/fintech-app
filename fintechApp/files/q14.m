clear
mag = xlsread('Earthquake data Idaho.xlsx', 'sheet1', 'E2:E51');
magErr = xlsread('Earthquake data Idaho.xlsx', 'sheet1', 'R2:R51');
errorbar(mag, magErr)
title('Magnitude of 1st 50 Earthquakes with Error')
xlabel('Earthquake #')
ylabel('Magnitude')