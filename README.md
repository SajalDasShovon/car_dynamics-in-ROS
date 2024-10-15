# car_dynamics

The kinematic car model is a simplified model used in vehicle dynamics.



et the state vector x consist of:
x : Position in the x-direction (global frame).
y : Position in the y-direction .
θ : Heading angle (relative to the x-axis).
δ : Steering angle (front wheel's orientation relative to the car's heading).
input vector is:
u=[v, ϕ]   velocity & steering rate




Car parameters:
Wheelbase (L): distance between the front and rear axles is 3 meters
Initial Steering Angle (delta): The starting angle for steering = 0.1 radians.
Steering Rate (phi): The rate of change of the steering angle, set to 0.01 rps.
Speed (v): The constant forward speed of the car, set to 2 meters per second.


Lastly the  simulation is done with RViz  marker
