
# Import and initialize the pygame library
import pygame
import math

pygame.init()

# Set up the drawing window
HEIGHT = 800
WIDTH = 1200
SPEED = 10
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0, 135, 159)
ORANGE = (153, 49, 0)

class Node():
    def __init__(self, x=0,y=0, next_node=None, chain_length=30,size=20):
        self.x=x
        self.y=y
        self.next_node = next_node
        self.size=size
        self.chain_length = chain_length

    def update(self):
        if self.next_node:
            # Calculate vector and distance
            vector = [self.x - self.next_node.x, self.y - self.next_node.y]
            distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

            # Normalize vector and scale it to chain_length
            if distance > self.chain_length:
                direction = [vector[0] / distance, vector[1] / distance]
                self.next_node.x = self.x - direction[0] * self.chain_length
                self.next_node.y = self.y - direction[1] * self.chain_length

            if self.next_node.next_node:
                vector2 = [self.next_node.next_node.x - self.next_node.x,
                           self.next_node.next_node.y - self.next_node.y]



                angle1 = math.atan2(vector[1], vector[0])  # Angle of current vector
                angle2 = math.atan2(vector2[1], vector2[0])  # Angle of next vector
                    # Difference between the angles


                angle_diff = angle2 - angle1
                angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi

                if abs(angle_diff  )< 2.75:
                    rotation_step = 0.1 # Adjust this value for smoother/slower rotation
                    cos = math.cos(rotation_step)
                    sin = math.sin(rotation_step)
                    if angle_diff >=0:


                        # Apply rotation
                        new_x = vector2[0] * cos - vector2[1] * sin
                        new_y = vector2[0] * sin + vector2[1] * cos
                    else:

                        new_x = vector2[0] * cos + vector2[1] * sin
                        new_y = -vector2[0] * sin + vector2[1] * cos
                        # Update next_node.next_node position incrementally
                    self.next_node.next_node.x = self.next_node.x + new_x
                    self.next_node.next_node.y = self.next_node.y + new_y





    def draw(self):

        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.size)


chain=[]
def create_chain(nodes,size):
    global chain
    chain = [Node(size=size[0])]
    for i in range(nodes-1):
        n=Node(next_node=chain[0],size=size[i+1])
        chain.insert(0,n)

create_chain(20,size=[i for i in range(10,50,2)]) # size should be from tail to head

eyes_size = chain[0].size
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    anchor = list(pygame.mouse.get_pos())
    vector = [anchor[0]-chain[0].x ,anchor[1]- chain[0].y]
    distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if distance >10:
        direction = [vector[0] / distance, vector[1] / distance]
        chain[0].x += direction[0] *SPEED
        chain[0].y += direction[1] *SPEED


    for node in chain:
        node.draw()
        node.update()

    eyes_pos = math.atan2(chain[0].y-chain[0].next_node.y,chain[0].x-chain[0].next_node.x)
    pygame.draw.circle(screen,WHITE, [chain[0].x+eyes_size*math.cos(eyes_pos+0.5),chain[0].y+eyes_size*math.sin(eyes_pos+0.5)],10)
    pygame.draw.circle(screen,WHITE, [chain[0].x+eyes_size*math.cos(eyes_pos-0.5),chain[0].y+eyes_size*math.sin(eyes_pos-0.5)],10)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
