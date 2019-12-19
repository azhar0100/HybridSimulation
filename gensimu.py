"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
"""
 
import pygame
from math import exp
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
 
def draw_stick_figure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1 + x, y, 10, 10], 0)
 
    # Legs
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [x, 27 + y], 2)
 
    # Body
    pygame.draw.line(screen, RED, [5 + x, 17 + y], [5 + x, 7 + y], 2)
 
    # Arms
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [1 + x, 17 + y], 2)
 
# Setup
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Hide the mouse cursor
pygame.mouse.set_visible(0)
 
# Speed in pixels per frame
x_speed = 0
y_speed = 0
 
# Current position
x_coord = 200
y_coord = 200

d2y = 0
dy = 25

fuel_intake = 0
force = 0
mass = 200
u_f = 0.7

def relu(x):
    if x >= 0:
        return x
    else:
        return 0

decelrating = False
engine_torque = 0
tyre_radius = 0.45
maximum_engine_torque = 100

battery_level = 1
battery_depletion_rate = 0.0001

engine_temperature = 0

starting_help = 0

tick_counter = 0
second_counter = 0

R_a = 0.1e-2
R_f = 200
Kphi = 60/7.0
battery_voltage = 12

def battery_speed_to_torque(speed, V_T = battery_voltage, Kphi=Kphi,R_a=R_a):
    return (V_T/Kphi - speed)*(Kphi**2/R_a)

def speed_to_dy_vv(dy=None,speed=None):
    ratio = 1/500.0
    if (dy==None and speed==None):
        return None
    elif dy == None:
        return speed * ratio
    elif speed == None:
        return dy / ratio


def engine_speed_to_torque(speed):
    if(speed < 1000):
        return (300.0/1000) * speed
    if(speed >= 1000 and speed <= 5000):
        return 300.0
    if(speed > 5000):
        return -0.3*speed + 1800

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key
 
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
                force = 141
                fuel_intake = 1
                print(fuel_intake)
            elif event.key == pygame.K_DOWN:
                y_speed = 3
            elif event.key == pygame.K_s:
                starting_help = 1
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
                fuel_intake = 0.1
                force = 0
            elif event.key == pygame.K_s:
                starting_help = 0
 
    # --- Game Logic

    # engine_starting_torque = -100*exp(second_counter/5)
 
    # Move the object according to the speed vector.
    
    maximum_engine_torque = engine_speed_to_torque(speed_to_dy_vv(dy=dy)) + starting_help * 100
    # maximum_engine_torque = 100
    engine_torque = maximum_engine_torque * fuel_intake
    # engine_torque += engine_starting_torque
    # total_torque = engine_torque
    # total_torque = engine_torque + battery_speed_to_torque(speed_to_dy_vv(dy=dy)) * fuel_intake
    force = engine_torque / tyre_radius
    d2y = (force - u_f*mass)/mass 
    x_coord = x_coord + x_speed
    dy += (d2y)
    dy = relu(dy)
    y_coord = y_coord - dy
    print(force,dy, u_f*mass,y_coord)
 
    # --- Drawing Code
 
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
 
    draw_stick_figure(screen, x_coord%size[0], y_coord%size[1])
 
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    tick_counter = tick_counter + 1
    second_counter += tick_counter / 60
    tick_counter = tick_counter % 60
    # Limit frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()

