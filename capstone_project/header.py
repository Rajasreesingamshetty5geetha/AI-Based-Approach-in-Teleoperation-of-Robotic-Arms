""" 
    source code
"""
from numpy import sin,cos,radians,arctan2,arcsin,arccos,rad2deg,sqrt,square


#link lenght
l1 = 1.5
l2 = 12 
l3 = 12



def fk(thetaf):
    theta_1 = radians(thetaf[0])
    theta_2 = radians(thetaf[1])
    theta_3 = radians(thetaf[2])
    
    z = (l2*sin(theta_2)) + (l3*sin(theta_2+theta_3))    

    n = l1 + l2*cos(theta_2) + l3*cos(theta_2+theta_3)

    y = n*cos(theta_1)
    x = n*sin(theta_1)
    return [x,y,z]

def ik(d):

    x = d[0]
    y = d[1]
    z = d[2]

    theta1 = arctan2(x,y)

    n = (sqrt(square(x) + square(y)))-l1
    ap = square(z) + square(n)

    inv = (ap - square(l2) - square(l3))/(2*l2*l3)

    theta3 = - arccos(inv)

    beta = arctan2(z,n)
    alpha = arctan2((l3*sin(theta3)),l2+l3*cos(theta3))

    theta2 = beta - alpha
    #print("ran")
    return [rad2deg(theta1),rad2deg(theta2),rad2deg(theta3)]
    #return rad2deg(theta1)
    #  


