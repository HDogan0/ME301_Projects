"""
Hasan Doğan
2627842
ME301 Project 1
"""

from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from numpy import linspace
from numpy import pi
from numpy import cos, sin, sqrt, arctan2


# gridspec - 2 rows, 1 column for top, then 1 row, 3 columns for bottom
fig = plt.figure(figsize=(12, 10))
gs = plt.GridSpec(2, 1, height_ratios=[2, 1])

# Top plot MECHANISM
mechanism = plt.subplot(gs[0])

# Bottom plots - create a nested gridspec for the 3 subplots
gs_bottom = gs[1].subgridspec(1, 4, wspace=0.5)
theta_12_drawing = plt.subplot(gs_bottom[0])
theta_14_drawing = plt.subplot(gs_bottom[1])
s_23 = plt.subplot(gs_bottom[2])
s_15 = plt.subplot(gs_bottom[3])

mechanism.set_title("MECHANISM")
mechanism.set_xlabel("x-axis (mm)")
mechanism.set_ylabel("y-axis (mm)")
mechanism.set_xlim(-200, 400)
mechanism.set_ylim(-10, 300)
mechanism.set_aspect('equal')


#   +1/-1 to switch solutions
sigma = -1

#   measurements
L_AB = 70
L_AG = 95
L_GC = 140
L_BD = 108.86
L_CD = 50
L_BE = 230
L_FE = 74
h5 = 245

link_f_height = 20
link_f_width = 30

circle_c_radius = L_CD + 15

#   Lets take the point A as our origin
# x-y
A = [0,0]   
B = [70,0]
C = [95,140]

#   Solution
rectangle = Rectangle(((0),(h5-link_f_height/2)), width=link_f_width, height=link_f_height, facecolor="purple" )

prismatic_upper = Line2D([-150, 300], [h5-link_f_height/2, h5-link_f_height/2], color='C8', linewidth=1)
prismatic_bottom = Line2D([-150, 300], [h5+link_f_height/2, h5+link_f_height/2], color='C8', linewidth=1)

#   Circle centered at point C 
circle_c = Circle((C[0], C[1]), circle_c_radius, fill=False, linewidth=2)

#   Patches
mechanism.add_patch(rectangle)
mechanism.add_patch(circle_c)
mechanism.add_line(prismatic_upper)
mechanism.add_line(prismatic_bottom)

#   Joints
joint_AB, = mechanism.plot([], [], 'b-', linewidth=3)
joint_BE, = mechanism.plot([], [], 'b-', linewidth=2)
joint_FE, = mechanism.plot([], [], 'r-', linewidth=2)
#joint_FE_2, = mechanism.plot([], [], 'b-', linewidth=2)

#   Points
point_A, = mechanism.plot([], [], 'bo', label='A')
label_A = mechanism.text(0, 0, "A", va='bottom', fontsize=15)

point_B, = mechanism.plot([], [], 'ro', label='B')
label_B = mechanism.text(0, 0, "B", va='bottom', fontsize=15)

point_C, = mechanism.plot([], [], 'yo', label='C')
label_C = mechanism.text(0, 0, "C", va='bottom', fontsize=15)

point_D, = mechanism.plot([], [], 'go', label='D')
label_D = mechanism.text(0, 0, "D", va='bottom', fontsize=15)

point_E, = mechanism.plot([], [], 'co', label='E')
label_E = mechanism.text(0, 0, "E", va='bottom', fontsize=15)

point_F, = mechanism.plot([], [], 'ro', label='F')
label_F = mechanism.text(0, 0, "F", va='bottom', fontsize=15)

#   Points for subplots
point_theta_12, = theta_12_drawing.plot([], [], '*b')
point_theta_14, = theta_14_drawing.plot([], [], '*C1')
point_s15, = s_15.plot([], [], '*r')
point_s23, = s_23.plot([], [], '*g')


def theta12(theta13, s23):
    y = (L_GC + L_CD * sin(theta13)) / s23
    x = (L_AG - L_AB + L_CD * cos(theta13)) / s23
    return arctan2(y, x)

def calculate_s15(theta_12):
    
    B = -2*L_AB - 2*L_BE*cos(theta_12)
    C = L_AB**2 + L_BE**2 - L_FE**2 + h5**2 + 2*L_AB*L_BE*cos(theta_12)-2*h5*L_BE*sin(theta_12)

    s15 = (-B + sigma * sqrt(B**2 - 4*C))/2

    return s15

def theta14(s15, theta12):
    
    return arctan2((L_BE*sin(theta12)-h5)/L_FE,(L_AB-s15+L_BE*cos(theta12))/L_FE)


def update(frame):
    angle = theta_13[frame]

    point_A.set_data([A[0]], [A[1]])
    label_A.set_position((A[0], A[1]))

    point_B.set_data([B[0]], [B[1]])
    label_B.set_position((B[0], B[1]))

    point_C.set_data([C[0]], [C[1]])
    label_C.set_position((C[0], C[1]))

    #   point D
    px = C[0] + L_CD * cos(angle)
    py = C[1] + L_CD * sin(angle)
    point_D.set_data([px], [py])
    label_D.set_position((px, py))

    s23 = sqrt((px - B[0])**2 + (py - B[1])**2)

    theta_12 = theta12(angle, s23)
    px_be = B[0] + L_BE * cos(theta_12)
    py_be = B[1] + L_BE * sin(theta_12)
    s15 = calculate_s15(theta_12)

    theta_14 = theta14(s15, theta_12)

    #   rectangle
    rectangle.set_x(s15-link_f_width/2)

    #   lines
    joint_AB.set_data([A[0],B[0]], [A[1],B[1]])
    joint_BE.set_data([B[0], px_be], [B[1],py_be])

    #   points
    point_E.set_data([px_be], [py_be])
    label_E.set_position((px_be, py_be))

    point_F.set_data([s15], [h5])
    label_F.set_position((s15, h5))

    px_fe = s15 + L_FE * cos(theta_14)
    py_fe = h5 + L_FE * sin(theta_14)
  
    joint_FE.set_data([s15, px_fe], [h5,py_fe])

    #   unknown plot points
    point_theta_12.set_data([angle*180/pi], [theta_12*180/pi])
    point_theta_14.set_data([angle*180/pi], [(theta_14+2*pi)*180/pi])
    point_s15.set_data([angle*180/pi], [s15])
    point_s23.set_data([angle*180/pi], [s23])

    return (point_A, point_B, point_C, point_D, point_E, point_F, 
            joint_AB, joint_BE, joint_FE, rectangle, 
            point_theta_12, point_theta_14, point_s15, point_s23)

#   Unknowns:
#       -s15
#       -theta_12
#       -theta_14

if __name__== "__main__":
    num_division = 1080
    
    theta_13 = linspace(0, 2*pi, num_division)

    s23_values = []
    theta_12_values = []
    theta_14_values = []
    s15_values = []
    for angle in theta_13:
        px = C[0] + L_CD * cos(angle)
        py = C[1] + L_CD * sin(angle)
        s23 = sqrt((px - B[0])**2 + (py - B[1])**2)
        theta_12 = theta12(angle, s23)
        s15 = calculate_s15(theta_12)
        theta_14 = theta14(s15, theta_12)

        s23_values.append(s23)
        theta_12_values.append(theta_12*180/pi)
        theta_14_values.append((theta_14+2*pi)*180/pi)
        s15_values.append(s15)

    s_23.plot(theta_13*180/pi, s23_values, '--g')
    s_23.set_title('$s_{23}$ vs $\\theta_{13}$')
    s_23.set_ylabel('$s_{23}$ (mm)')
    s_23.set_xlabel('$\\theta_{13}$ (degree)')
    s_23.grid('minor')

    s_15.plot(theta_13*180/pi, s15_values, '--r')
    s_15.set_title('$s_{15}$ vs $\\theta_{13}$')
    s_15.set_ylabel('$s_{15}$ (mm)')
    s_15.set_xlabel('$\\theta_{13}$ (degree)')
    s_15.grid('minor')

    theta_12_drawing.plot(theta_13*180/pi, theta_12_values, '--b')
    theta_12_drawing.set_title('$s_{12}$ vs $\\theta_{13}$')
    theta_12_drawing.set_ylabel('$s_{12}$ (degree)')
    theta_12_drawing.set_xlabel('$\\theta_{13}$ (degree)')
    theta_12_drawing.grid('minor')

    theta_14_drawing.plot(theta_13*180/pi, theta_14_values, '--C1')
    theta_14_drawing.set_title('$s_{14}$ vs $\\theta_{13}$')
    theta_14_drawing.set_ylabel('$s_{14}$ (degree)')
    theta_14_drawing.set_xlabel('$\\theta_{13}$ (degree)')
    theta_14_drawing.grid('minor')

    ani_mech = FuncAnimation(fig, update, frames=len(theta_13), interval=1, blit=False)

    
    plt.show()
