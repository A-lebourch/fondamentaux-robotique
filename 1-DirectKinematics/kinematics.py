from math import pi,cos, sin, radians

# Dimensions used for the PhantomX robot :
constL1 = 54.8
constL2 = 65.3
constL3 = 133
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
    theta1 = radians(theta1)
    theta2 = radians(theta2)
    theta3 = radians(theta3)

    x = cos(theta1) * (l1*cos(theta1)+l2*cos(theta2-offsetP2)+l3*cos(theta2+theta3-(offsetP3+offsetP2)))
    y = sin(theta1) * (l1*sin(theta1)+l2*cos(theta2-offsetP2)+l3*cos(theta2+theta3-(offsetP3+offsetP2)))
    z = sin(theta2-offsetP2)*l2 + l3*sin(theta2+theta3-(offsetP3+offsetP2))


    return [x, y, z]

def computeDKsimple(theta1, theta2, theta3, l1=constL1, l2=constL2, l3=constL3):
    theta1 = radians(theta1)
    theta2 = radians(theta2)
    theta3 = radians(theta3)

    x = cos(theta1) * (l1*cos(theta1)+l2*cos(theta2)+l3*cos(theta2+theta3))
    y = sin(theta1) * (l1*sin(theta1)+l2*cos(theta2)+l3*cos(theta2+theta3))
    z = sin(theta2)*l2 + l3*sin(theta2+theta3)


    return [x, y, z]


def computeIK(x, y, z, l1=constL1, l2=constL2, l3=constL3):
    theta1 = 0
    theta2 = 0
    theta3 = 0

    return [theta1, theta2, theta3]


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
