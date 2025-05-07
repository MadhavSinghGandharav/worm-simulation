import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LIFE")

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Particle class
class Particle():
    def __init__(self, color):
        self.color = color
        self.position = [random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)]
        self.velocity = [0.0, 0.0]

    def draw(self):
        pygame.draw.circle(screen, colors[self.color], (int(self.position[0]), int(self.position[1])), 2)
    
    def update_position(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Wrap around screen
        self.position[0]%= SCREEN_WIDTH
        self.position[1] %= SCREEN_HEIGHT

# Helper Functions
def render(particles):
    for particle in particles:
        particle.draw()

def create_particles(color, quantity):
    p = []
    for _ in range(quantity):
        a = Particle(color)
        p.append(a)
        particles.append(a)
    return p

def simulate(particles):
    for i in particles:
        vec = [0.0, 0.0]
        for j in particles:
            if i is not j:
                dxy = [i.position[0] - j.position[0], i.position[1] - j.position[1]]
                distance = math.sqrt(dxy[0]**2 + dxy[1]**2)
                attraction = relation[i.color][j.color]
                if distance > 80:
                    continue
                elif distance <= 15:
                    force = -(0.05*distance - 1)
                else:
                    force  = attraction * math.exp(-distance / 20)  
                vec[0] += force * dxy[0] / distance
                vec[1] += force * dxy[1] / distance
        
        i.velocity[0] = vec[0]
        i.velocity[1] = vec[1]
        
        i.velocity[0] = max(min(i.velocity[0], 3), -3)
        i.velocity[1] = max(min(i.velocity[1], 3), -3)
        i.update_position()

def display_fps(screen, clock):
    # Calculate FPS
    fps = str(int(clock.get_fps()))
    
    # Render the FPS text
    fps_text = font.render(fps, True, pygame.Color('white'))
    
    # Blit the FPS text onto the screen
    screen.blit(fps_text, (10, 10))

# Variables
colors = [(43, 207, 255), (179, 251, 50), (255, 50, 155)]  # blue, green, pink
font = pygame.font.SysFont(None, 30)
particles = []
relation = [
    [-3, -0.5, -1],  # Particle Type 0 blue
    [0.5, 1, -1.5],  # Particle Type 1 green
    [-1, 1,-3]   # Particle Type 2 pink
]

# Create particles
create_particles(0, 100)
create_particles(1, 100)
create_particles(2, 100)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    screen.fill(BLACK)
    simulate(particles)
    render(particles)
    display_fps(screen, clock)
    pygame.display.update()

    clock.tick(FPS)

# Clean up
pygame.quit()
sys.exit()
