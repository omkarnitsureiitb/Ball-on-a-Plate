import numpy as np
from scipy.integrate import odeint

g = 9.8
Kc = -3.6      #Constants used in the PID controller
Kd = -6.4
Ki = -0.2
dt = 0.3

# The following function gives the ordinary differential
# equation that our plant follows. Do not meddle with this.
def f(XV, t, theta):
    return (XV[1], (-5 * g / 7) * np.radians(theta))


# Write your function here.

#OP = output (theta)
#PV = plant variable (x)
#SP = set point (X-coordinate of the mouse click)

def solve( xf_, XV0, i0, e0, theta0, t0):
    e = xf_ - XV0[0]        #calculating the current error

    P = Kc*e                # Calculating each of P,I,D terms
    I = i0 + Ki*e*dt
    D = Kd/dt*(e - e0)

    theta_ = P + I + D
    if theta_ - theta0 > 1.0:       #Setting the limits for the theta
        theta_ = theta0 + 1
    if theta_ - theta0 < -1.0:
        theta_ = theta0 - 1

    if theta_ < -15.0:
        theta_ = -15
    if theta_ > 15.0:
        theta_ = 15

    t_ = t0 + dt                    #Updating time

    XV_ = odeint( f, XV0, [ t0, t_], args=( theta_, )).T        #Solving the differential equation using 'odeint' function

    dx = XV_[1][0] - XV0[0]

    XVf = XV_[1]
    if XVf[0] > 300:                                    #setting limits for the newly calculated position,velocity vector
        XVf[0] = 300
    if XVf[0] < -300:
        XVf[0] = -300

    info = [ dx, I, theta_, XVf, e, t_]                       #returning the final values of all the parameters
    return info