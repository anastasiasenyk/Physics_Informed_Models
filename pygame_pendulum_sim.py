import pygame
from math import sin, cos, pi, dist
# Reference code: https://github.com/achaval-tomas/Double-Pendulum-Chaos/
import math

class Pendulum:
    def __init__(self, g, m1, m2, r1, r2, a1, a2, v1, v2, color):
        # system parameters
        self.g = g
        self.m1 = m1
        self.m2 = m2
        self.r1 = r1
        self.r2 = r2
        self.color = color
        self.cvs = pygame.Surface((swidth, sheight))

        # modeling parameters
        self.a1 = a1
        self.a2 = a2
        self.v1 = v1
        self.v2 = v2

        # coordinates
        self.px2 = 0
        self.py2 = 0
        self.x1 = p + self.r1 * sin(self.a1)
        self.y1 = q + self.r1 * cos(self.a1)
        self.x2 = self.x1 + self.r2 * sin(self.a2)
        self.y2 = self.y1 + self.r2 * cos(self.a2)

    def update_positions(self):
        self.px2 = self.x2
        self.py2 = self.y2

        self.x1 = p + self.r1 * sin(self.a1)
        self.y1 = q + self.r1 * cos(self.a1)
        self.x2 = self.x1 + self.r2 * sin(self.a2)
        self.y2 = self.y1 + self.r2 * cos(self.a2)

    def update_accelerations(self):
        num1 = -1 * self.g * (2 * self.m1 + self.m2) * sin(self.a1)
        num2 = -1 * self.m2 * self.g * sin(self.a1 - 2 * self.a2)
        num3 = -2 * sin(self.a1 - self.a2) * self.m2
        num4 = self.v2 * self.v2 * self.r2 + self.v1 * self.v1 * self.r1 * cos(self.a1 - self.a2)
        den = self.r1 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.a1 - 2 * self.a2))
        acc1 = (num1 + num2 + num3 * num4) / den

        num1 = 2 * sin(self.a1 - self.a2)
        num2 = self.v1 * self.v1 * self.r1 * (self.m1 + self.m2)
        num3 = self.g * (self.m1 + self.m2) * cos(self.a1)
        num4 = self.v2 * self.v2 * self.r2 * self.m2 * cos(self.a1 - self.a2)
        den = self.r2 * (2 * self.m1 + self.m2 - self.m2 * cos(2 * self.a1 - 2 * self.a2))
        acc2 = (num1 * (num2 + num3 + num4)) / den

        self.v1 += acc1
        self.v2 += acc2
        self.a1 += self.v1
        self.a2 += self.v2

    def draw(self):
        # Clear the canvas
        self.cvs.set_colorkey((0, 0, 0))
        self.cvs.fill((0, 0, 0))

        # Draw the line connecting the previous position to the current position of the second mass
        pygame.draw.line(canvas, self.color, pygame.Vector2(self.px2, self.py2), pygame.Vector2(self.x2, self.y2), 2)
        screen.blit(canvas, (0, 0))  # Blit the canvas onto the screen

        # Calculate the intensity of the gradient color based on the distance traveled by the second mass
        intensity = min(255, max(0, 50 + int(dist((self.px2, self.py2), (self.x2, self.y2))) * 4))
        line_color = pygame.Color(intensity, intensity, intensity)

        # Draw the segments of the pendulum (rod) with gradient color
        pygame.draw.line(self.cvs, line_color, pygame.Vector2(p, q), pygame.Vector2(self.x1, self.y1), 5)
        pygame.draw.line(self.cvs, line_color, pygame.Vector2(self.x1, self.y1), pygame.Vector2(self.x2, self.y2), 5)

        # Draw masses of the pendulum
        pygame.draw.circle(self.cvs, self.color, pygame.Vector2(self.x1, self.y1), self.m1 / 4)
        pygame.draw.circle(self.cvs, self.color, pygame.Vector2(self.x2, self.y2), self.m2 / 4)

    def update(self):
        self.update_positions()
        self.draw()
        self.update_accelerations()




# Initialize pygame
pygame.init()

# Screen dimensions
swidth = 900
sheight = 800

# Initial conditions for the pendulum
p = swidth / 2
q = sheight / 2

# Create screen
screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('Double Pendulum Simulation in Python')
canvas = pygame.Surface((swidth, sheight))
canvas.fill("black")
# Clock
clock = pygame.time.Clock()

def is_space_pressed():
    keys = pygame.key.get_pressed()
    return keys[pygame.K_SPACE]


running = True
start = False

# Colors
black = (0, 0, 0)
tan4 = (139, 90, 43)
goldenrod1 = (255, 193, 37)

# Create pendulum instance
pendulum = Pendulum(
    g=1, # mousey: it's better to set g <= 1.3, otherwise it would be math domain error (NANs) after some time
    m1=50,
    m2=75,
    r1=100,
    r2=250,
    a1=3 * pi / 4,
    a2=3 * pi / 4,
    v1=0,
    v2=0,
    color=goldenrod1
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not start:
        start = is_space_pressed()
        continue

    screen.fill(black)

    pendulum.update()
    screen.blit(pendulum.cvs, (0, 0))

    pygame.draw.circle(screen, tan4, pygame.Vector2(p, q), 5)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
