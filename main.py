import pygame
from pygame.locals import *
import random



pygame.init()


width = 500
height = 500
screen_size = (width,height)
Screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game by Mr.M.N.A')


gray = (35,35,35)
green =(8,51,1)
red = (105,2,2)
white = (255,255,255)
yellow =(171, 159, 31)



Road_width = 300
Marker_Width = 10
Marker_Height = 50


road = (100 , 0 , Road_width , height)
Left_Edge_Marker = (95 , 0 , Marker_Width , height)
Right_Edge_Marker = (395 , 0 , Marker_Width , height)

Left_Lane = 150
Center_Lane = 250
Right_Lane = 350
Lanes = [Left_Lane , Center_Lane , Right_Lane]

Lane_Marker_Move_Y = 0


Player_X = 250
Player_Y = 400


Clock = pygame.time.Clock()
Fps = 120

GameOver = False
Speed = 2
Score = 0


class Vehicle(pygame.sprite.Sprite):
    
    
    def __init__(self, image ,x ,y ):
        pygame.sprite.Sprite.__init__(self)
        
        
        image_scale = 45 / image.get_rect().width
        New_width = image.get_rect().width * image_scale
        New_Height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image , (New_width , New_Height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x , y]
        
        
class PlayerVehicle(Vehicle):
    
    def __init__(self,  x, y):
        image = pygame.image.load('car.png')
        super().__init__(image, x, y)     
        
        



Player_Group = pygame.sprite.Group()
Player = PlayerVehicle(Player_X , Player_Y)
Player_Group.add(Player)
  
Image_FileNames = ['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
Vehicle_Images = []
for Image_FileName in Image_FileNames:
    image = pygame.image.load('' + Image_FileName)
    Vehicle_Images.append(image)
    
    
Vehicle_Group = pygame.sprite.Group()

crash = pygame.image.load('crash.png')
crash_rect = crash.get_rect()


Running = True
while Running:
    Clock.tick(Fps)
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
         
         
        if event.type == KEYDOWN:
            
            
            if event.key ==  K_LEFT and Player.rect.center[0] > Left_Lane:
                Player.rect.x -= 100 
            elif event.key ==  K_RIGHT and Player.rect.center[0] < Right_Lane:
                Player.rect.x += 100 

            for vehicle in Vehicle_Group:
                if pygame.sprite.collide_rect(Player , vehicle):
                    
                    GameOver = True
                    
                    if event.key == K_LEFT:
                        Player.rect.left == vehicle.rect.right
                        crash_rect.center == [Player.rect.left, (Player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        Player.rect.right = vehicle.rect.left
                        crash_rect.center = [Player.rect.right, (Player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
            
            
    Screen.fill(green)
    
    pygame.draw.rect(Screen , gray , road)
    
    pygame.draw.rect(Screen , yellow , Left_Edge_Marker)
    pygame.draw.rect(Screen , yellow , Right_Edge_Marker)
    
    Lane_Marker_Move_Y += Speed * 2
    if Lane_Marker_Move_Y >= Marker_Height *2:
        Lane_Marker_Move_Y = 0
    for y in range (Marker_Height * -2 , height , Marker_Height * 2):
        pygame.draw.rect(Screen , white , (Left_Lane + 45 ,y + Lane_Marker_Move_Y, Marker_Width , Marker_Height))
        pygame.draw.rect(Screen , white , (Center_Lane + 45 ,y + Lane_Marker_Move_Y, Marker_Width , Marker_Height))
    
    Player_Group.draw(Screen)
    
    if len(Vehicle_Group) < 2:
        
        
        add_vehicle = True
        for vehicle in Vehicle_Group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
                
        if add_vehicle :
            
            
            Lane = random.choice(Lanes)
            image = random.choice(Vehicle_Images)
            vehicle = Vehicle(image , Lane , height / -2)
            Vehicle_Group.add(vehicle)
            
            
    for vehicle in Vehicle_Group:
        vehicle.rect.y += Speed
        
        
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            
            Score += 1
            
            if Score > 0 and Score % 5 == 0 :
                Score += 1
    Vehicle_Group.draw(Screen)
    
    
    font = pygame.font.Font(pygame.font.get_default_font(),16)
    text = font.render('Score : ' + str(Score), True , white)
    text_rect = text.get_rect()
    text_rect.center = (50 , 450)
    Screen.blit(text , text_rect)
    
    if pygame.sprite.spritecollide(Player , Vehicle_Group , True):
        GameOver = True
        crash_rect.center = [Player.rect.center[0],Player.rect.top]
        
    if GameOver:
        Screen.blit(crash, crash_rect)
        
        pygame.draw.rect(Screen , red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game Over. Play Again? (Y or N)', True , white)
        text_rect = text.get_rect()
        text_rect.center = (width /2 , 100)
        Screen.blit(text , text_rect)
        
    pygame.display.update()
    
    
    while GameOver :
        
        
        Clock.tick(Fps)
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                GameOver = False
                Running = False
                
                
            if event.type == KEYDOWN:
                if event.key == K_y:
                    GameOver = False
                    Speed = 2
                    Score = 0
                    Vehicle_Group.empty()
                    Player.rect.center = [Player_X , Player_Y] 
                elif event.key == K_n:
                      GameOver = False
                      Running = False
                      
    
pygame.quit            
