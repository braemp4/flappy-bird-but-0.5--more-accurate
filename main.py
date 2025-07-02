import pygame #type: ignore - run in terminal to test
import random

pygame.init()
screen_w = 500
screen_l = 500

win = pygame.display.set_mode((screen_l, screen_w))
pygame.display.set_caption("flappybird")

     
GRAVITY= -10 #subtract this from height to get falling
FLAP_POWER = -13 #add to get upwards motion

test_image = pygame.image.load("flappy-bird.png")  #must go into spawnbird method

test_image = pygame.transform.scale(test_image, (50,50)).convert_alpha()

running = True

def calculate_pipe_space():
    width = 50
    height = random.randrange(35, 100) #min size for bird and up
    x = 450
    y = random.randrange(100,400) #min-max based on height of rectangle space taking into account window size

    return {"xcoord":x,"ycoord":y,"w":width,"h":height}

def calculate_pipe_spawn(pipe_params):
    #calculate thwere the two pipes will spawn based on calculate_pipe_space() as params
    top_x = pipe_params["xcoord"] 
    bottom_x = pipe_params["xcoord"]

    #top_y should probably be a constant 500
    top_y = pipe_params["ycoord"] - pipe_params["h"] - 100 #might have to be +
    bottom_y = pipe_params["ycoord"] + pipe_params["h"] + 100

    #pipe size should be: (total height - rectangle height)/2 and width is constant 
    #we should also calculate and return that in dict instead of "spacing"

    pipe_width = pipe_params["w"]
    pipe_height = (500 - pipe_params["h"])/2 


    return {"top_pipe":(top_x, top_y, pipe_width, pipe_height), "bottom_pipe":(bottom_x, bottom_y, pipe_width, pipe_height)}

def calculate_pipe_vertical(pipe_params):
    top_y = 0
    #I forgot top of screen = 0, bottom = 500 

    bottom_y = pipe_params["ycoord"] + pipe_params["h"] #set to top of "rectangle space" 
    pipe_width = pipe_params["w"]
    #height of top pipe = top y value of random rectangle
    #height of bottom pipe = bottom y value of the random rectangle
    top_pipe_height = pipe_params["h"]
    
    bottom_pipe_height = 500 - top_pipe_height - pipe_params["h"]
    return {"top_y": top_y, "bottom_y" : bottom_y, "pipe_width" : pipe_width, "top_pipe_height": top_pipe_height, "bottom_pipe_height" : bottom_pipe_height}

class pipe:
    def __init__(self, x):
        self.x = x
        self.random_rectangle = calculate_pipe_space()
        self.pipe_vertical = calculate_pipe_vertical(self.random_rectangle) 

    def get_width(self):
        return self.pipe_vertical["pipe_width"]

    def get_top_y(self):
        return self.pipe_vertical["top_y"]
    def get_bot_y(self):
        return self.pipe_vertical["bottom_y"]

    def get_top_h(self):
        return self.pipe_vertical["top_pipe_height"]
    def get_bot_h(self):
        return self.pipe_vertical["bottom_pipe_height"]

    def draw(self):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.get_top_y(), self.get_width(), self.get_top_h()))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.get_bot_y(), self.get_width(), self.get_bot_h()))
    
x = 450
y = 50




#new_pipes = calculate_pipe_vertical(calculate_pipe_space())
new_pipe_obj = pipe(x)


old_pipe = pipe(510)
lead_pipe = new_pipe_obj
 
current_pipes = [lead_pipe]

points = 0

while running:

    win.fill((0,55, 200))
    
    pygame.draw.rect(win, (255,255,0), (50,y, 25, 25))
    #win.blit(test_image, (50,y))

    y += 0.1
         
    x -= 0.05

    

    for p in current_pipes:
        p.x -= 0.05 
        p.draw()
    if current_pipes[0].x < 10:
        current_pipes.pop(0)
    
    if current_pipes[0].x < 50:     
        points += 1/800  
       
        print(points)

    if current_pipes[0].x <= 75 and current_pipes[0].x >= 50:
        if y <= (current_pipes[0].get_top_h()) or y >= (current_pipes[0].get_bot_y()): 
            print("collision possible")
            running = False

    if y <= 0:
        print("collision possible")
        running = False

    if lead_pipe.x <= 300:
        old_pipe = lead_pipe
        lead_pipe = pipe(500)
        current_pipes.append(lead_pipe)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
                
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space is being clicked")
                
                y -= 100
    

    

    pygame.display.update()

pygame.quit()