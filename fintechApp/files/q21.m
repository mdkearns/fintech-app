clear;
t = 0:0.005:0.2;
xy = (0.5 + (5.*t)) .* sin(((2*pi)/3).*t) .* cos((4*pi).*t);
z = (0.5 + (5.*t)) .* cos(((2*pi)/3).*t);
plot3(xy,xy,z)
grid on
xlabel("X (meters)")
ylabel("Y (meters)")
zlabel("Z (meters)")
title("Path of Robotic Arm")