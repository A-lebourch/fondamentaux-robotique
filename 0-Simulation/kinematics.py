from math import pi,cos, sin, radians, sqrt, acos, degrees
from constants import *
# Dimensions used for the PhantomX robot :
# constL1 = 54.8
# constL2 = 65.3
# constL3 = 133

theta2Correction = 0  # A completer
theta3Correction = 0  # A completer
offsetP2 = radians(16)
offsetP3 = radians(43.76)

state = 0

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

    lenght = math.sqrt((0-x)**2 + (0-y)**2 + (0-z)**2)

    max_lenght = l1 + l2 + l3

    if lenght > max_lenght :
        print("position inateignable")

    return [theta1, -theta2, -theta3]   #gérer position inateignables + sense du coude + infinité de positions 

def alkashi (a,b,c, elbowup=True):
    test = (a**2 + b**2 - c**2) / (2*a*b)

    if test > 1:
        test = 1

    if test <-1:
        test = -1

    if elbowup:
        return math.acos(test)
    
    else :
        return -math.acos(test)
    
def circle(x, z, r, t, duration):
    angle = ((t * 2 * pi) / duration)
    dy = cos(angle) * r            
    dz = (sin(angle) * r) +z
    return computeIK(x, dy, dz)

def triangle(x, z, h, w, t):
    global state 
    
    pts = triangle_points(x,z, h, w)
    
    if state == 0 or round(dx,2)==pts[0][0] and round(dy,2)==pts[0][1] and round(dz,2)==pts[0][2]:
        dx, dy, dz = segment(pts[0][0],pts[0][1],pts[0][2],pts[1][0],pts[1][1],pts[1][2], t ,4)
    if state == 1 or round(dx,2)==pts[1][0] and round(dy,2)==pts[1][1] and round(dz,2)==pts[1][2]:
        state = 1
        dx, dy, dz = segment(pts[1][0],pts[1][1],pts[1][2],pts[2][0],pts[2][1],pts[2][2], t ,4)
    if state == 2 or round(dx,2)==pts[2][0] and round(dy,2)==pts[2][1] and round(dz,2)==pts[2][2]:
        state = 2 
        dx, dy, dz = segment(pts[2][0],pts[2][1],pts[2][2],pts[0][0],pts[0][1],pts[0][2], t ,4) 

    print("\ndx:")
    print(round(dx,2))
    print(round(pts[1][1],2))
    print("\ndy:")
    print(dy)
    print(pts[1][0])
    print("\ndz:")
    print(dz)
    print(pts[1][2])

    return (dx, dy, dz)


def segment(x1, y1, z1,x2, y2, z2, t, duration):
    # if t/duration > 1:
    #     return computeIK(x2, y2, z2)
    # else:
    #     x = t/duration * (x2-x1) + x1
    #     y = t/duration * (y2-y1) + y1
    #     z = t/duration * (z2-z1) + z1
    #     return computeIK(x, y, z)

    x = t%duration/3 * (x2-x1) + x1
    y = t%duration/3 * (y2-y1) + y1
    z = -t%duration/3 * (z2-z1) + z1
    return computeIK(x, y, z)

def triangle_points(x,z,h,w):
    coo_de_depart = [x,w*1/2,z]
    coo_de_hyp = [x,0, z+h]
    coo_de_fin = [x,-w*1/2,z]
    return [coo_de_depart, coo_de_hyp, coo_de_fin]

    

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
