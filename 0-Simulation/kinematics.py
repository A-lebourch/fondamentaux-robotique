from math import pi,cos, sin, radians
from constants import *
# Dimensions used for the PhantomX robot :
# constL1 = 54.8
# constL2 = 65.3
# constL3 = 133

theta2Correction = 0  # A completer
theta3Correction = 0  # A completer
offsetP2 = radians(16)
offsetP3 = radians(43.76)

# Dimensions used for the simple arm simulation
# bx = 0.07
# bz = 0.25
# constL1 = 0.085
# constL2 = 0.185
# constL3 = 0.250

def computeDK(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # theta1 = radians(theta1)
    # theta2 = radians(theta2)
    # theta3 = radians(theta3)

    x = cos(theta1) * (l1*cos(theta1)+l2*cos(theta2-offsetP2)+l3*cos(theta2+theta3-(offsetP3+offsetP2)))    
    y = sin(theta1) * (l1*sin(theta1)+l2*cos(theta2-offsetP2)+l3*cos(theta2+theta3-(offsetP3+offsetP2)))
    z = sin(theta2-offsetP2)*l2 + l3*sin(theta2+theta3-(offsetP3+offsetP2)) 
    return [x, y, z]
    
def computeDKsimple(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # theta1 = radians(theta1)
    # theta2 = radians(theta2)
    # theta3 = radians(theta3)

    x = cos(theta1) * (l1+l2*cos(theta2)+l3*cos(theta2+theta3))
    y = sin(theta1) * (l1+l2*cos(theta2)+l3*cos(theta2+theta3))
    z = -sin(theta2)*l2 + -l3*sin(theta2+theta3)


    return [x, y, z]

def computeDKP1(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # theta1 = radians(theta1)
    # theta2 = radians(theta2)
    # theta3 = radians(theta3)

    x = l1*cos(theta1)
    y = l1*sin(theta1)
    z = 0

    return [x, y, z]

def computeDKP2(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    # theta1 = radians(theta1)
    # theta2 = radians(theta2)
    # theta3 = radians(theta3)

    x = (cos(theta1) * (l1+l2*cos(theta2)))
    y = (sin(theta1) * (l1+l2*cos(theta2)))
    z = -sin(theta2)*l2 

    return [x, y, z]

def computeIK(x, y, z, l1=constL1, l2=constL2, l3=constL3):
    
    theta1 = math.atan2(y,x)
    
    dproj = math.sqrt(x**2 + y**2)

    d13 = dproj - l1 

    d = math.sqrt(d13**2 + z**2)

    a = math.atan2(z,d13)

    b = alkashi(l2,d, l3)

    theta2 = a + b

    theta3 = alkashi(l2, l3, d) + math.pi

    return [theta1, -theta2, -theta3]   #gérer position inateignables + sense du coude + infinité de positions 

def alkashi (a,b,c):
    test = (a**2 + b**2 - c**2) / (2*a*b)
    print(test)
    if test > 1:
        test = 1

    if test <-1:
        test = -1

    return(math.acos(test))

def main():
    
    print("\n ComputeDK :")
    print(computeDK(0, 0, 0, l1=constL1, l2=constL2, l3=constL3))
    print(computeDK(90, 0, 0, l1=constL1, l2=constL2, l3=constL3))
    print(computeDK(30, 30, 30, l1=constL1, l2=constL2, l3=constL3))

    print("\n ComputeDK simple :")
    print(computeDKsimple(0, 0, 0, l1=constL1, l2=constL2, l3=constL3))
    print(computeDKsimple(90, 0, 0, l1=constL1, l2=constL2, l3=constL3))
    print(computeDKsimple(30, 30, 30, l1=constL1, l2=constL2, l3=constL3))


if __name__ == "__main__":
    main()
