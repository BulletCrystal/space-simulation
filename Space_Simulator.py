#Librarys
import pygame
import sys
import random
import math
import keyboard
#Init And Window And Clock
pygame.init()
Clock = pygame.time.Clock()
window_height = 720
window_weight = 1080
window = pygame.display.set_mode((window_weight,window_height))
font = pygame.font.Font(size=50)

pygame.display.set_caption('Space Simulator v1.0')

#Classes
class Background:
    def __init__(self,n_stars):
        self.n_stars = n_stars
        self.x = []
        self.y = []
        self.z = []
        for i in range(0,self.n_stars):
            self.x.append(random.randrange(0,window_weight))
            self.y.append(random.randrange(0,window_height))
            self.z.append(random.randrange(1,2))
    def update(self):
        for a,b,c in zip(self.x,self.y,self.z):
            pygame.draw.circle(window,(255,255,255),(a,b),c)

class Planet:

    AU = 149.6e6 * 1000 #in m
    G = 6.67428e-11
    SCALE = 120/ AU #1AU = 100 pixels
    TIMESTEP = 3600*24

    def __init__(self,x,y,radius,mass,color):
        
        self.x = x #in KM
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.x_vel = 0
        self.y_vel = 0
        self.distance = 0
        self.trac = []

    def draw(self,win):
        x = self.x * self.SCALE + window_weight/2
        y = self.y * self.SCALE + window_height/2

        for i in self.trac :
            pygame.draw.circle(win,self.color,i,1)
        if len(self.trac)>2000:
            self.trac.reverse()
            self.trac.pop()
            self.trac.reverse()
            

        pygame.draw.circle(win,self.color,(x,y),self.radius)
    def attraction(self,other):
        other_x,other_y = other.x,other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        self.distance = math.sqrt(distance_x**2+distance_y**2) 

        force = self.G * self.mass * other.mass / self.distance**2
        theta = math.atan2(distance_y,distance_x)

        force_X = math.cos(theta) * force
        force_Y = math.sin(theta) * force

        if abs(self.distance)<3*10**10:
            force_X,force_Y = 0,0
            if self.mass>other.mass:
                planets.remove(other)
                self.mass += other.mass
                self.x_vel = 0
                self.y_vel = 0

        return force_X , force_Y
    
    def update(self,planets):
        total_fx = total_fy = 0
        if keyboard.is_pressed('q'):
            if self.SCALE!=0:
                self.SCALE += 1/self.AU
                self.radius += 0.1
                self.trac.clear()
        if keyboard.is_pressed('d'):
            if self.SCALE-1/self.AU>0:
                self.SCALE -= 1/self.AU
                self.radius -=0.1
                self.trac.clear()
        for planet in planets:
            if self == planet:
                continue
            fx,fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.trac.append((self.x* self.SCALE + window_weight/2,self.y* self.SCALE + window_height/2))
        


sun = Planet(0,0,20,1.98892*10**30,(255,255,50))

earth = Planet(-Planet.AU,0,7,5.9742*10**23,(0,100,200))
earth.y_vel = 30.789*1000
mars = Planet(-1.524*Planet.AU,0,7,10.39*10**23,(250,100,0))
mars.y_vel = 24.077*1000
mercury = Planet(0.387*Planet.AU,0,3,3.30*10**23,(100,100,100))
mercury.y_vel = -47.4*1000


planet_1 = Planet(-2*Planet.AU,0,10,3.30*10**23,(250,130,130))
planet_1.y_vel = 24.077*1000
planet_2 = Planet(-2.5*Planet.AU,0,10,3.30*10**23,(250,0,100))
planet_2.y_vel = 20.077*1000
planets = [sun,earth,mars,mercury,planet_1,planet_2]

background = Background(100)

#Main Loop
running = True
while running :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            pygame.quit()
            sys.exit()
    #Window Color
    window.fill((12,11,18))

    background.update()

    text = font.render('^Earth',True,(255,255,255))
    window.blit(text,(earth.x * earth.SCALE+ window_weight/2,earth.y*earth.SCALE+window_height/2))
    #Main
    for planet in planets :
        planet.update(planets)
        planet.draw(window)
















    Clock.tick(60)
    pygame.display.update()
