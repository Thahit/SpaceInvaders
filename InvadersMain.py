import pygame
print("imports complete.")

pygame.init()
# game window
pygame.display.set_caption("Space Invaders")
width=800
hight=600
screen= pygame.display.set_mode(((width,hight)))
pygame.display.set_icon(pygame.image.load("img/ufo.png"))# mini icon on top left

#load img.    images are from https://www.flaticon.com/
P1Img=pygame.image.load("img/player.png")
enemy1Img=pygame.image.load("img/enemy.png")
bullet1Img=pygame.image.load("img/bullet.png")

#______________________________classes_______________________________________
class player():
    def __init__(self, x, y, array=[]):
        self.x=x
        self.y=y
        self.array=array #for bullets


    def move(self,x):
        if x=="l":
            if self.x >=15:
                self.x -=15
        else:
            if self.x <=(width-90):
                self.x += 15

    def show(self):
        screen.blit(P1Img,(self.x,self.y))

    def shoot(self):#create bullet
        if len(self.array)<5: #limit bullet nr.
            b=bullet(self.x,self.y)
            self.array.append(b)

class bullet():
    def __init__(self, x,y):
        self.x=x+16
        self.y=y+10

    def move(self):
        self.y -= 20


    def show(self):
        screen.blit(bullet1Img,(self.x,self.y))

class enemy():
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.dir=0

    def move(self):
        if self.dir == 0:#left
            if self.x >= 10:
                self.x -= 15
            else:#change dir
                self.dir = 1
                self.y += 25

        else:#right
            if self.x <= (width - 90):
                self.x += 15
            else:#change dir
                self.dir = 0
                self.y += 25

    def show(self):
        screen.blit(enemy1Img,(self.x,self.y))

font = pygame.font.Font('freesansbold.ttf', 20)
def scoreText(score):
    scorescreen=font.render("Score: "+ str(score), True, (150,0,0))
    screen.blit(scorescreen,(0,0))
def spawn(enemies):
    for i in range(50,700,90):
        enemies.append(enemy(i , 50))
    for i in range(50,700,90):
        enemies.append(enemy(i , 120))
#_____________________________main game__________________________________
def game():
    p = player(380, 500)
    #spawn enemies
    enemies=[]
    score=0
    shooting=False
    alive=True
    move=0
    while alive:
        screen.fill((5, 20, 20))
        p.show()
        scoreText(score)
        if len(enemies)<1:
            spawn(enemies)
        pygame.time.Clock().tick(15) # short delay to prevent hyperspeed

        #keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#stop game
                alive=False

            if event.type == pygame.KEYDOWN:  #press button
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move="l"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move="r"
                if event.key == pygame.K_SPACE:
                    shooting=True
            if event.type == pygame.KEYUP:  # unpress button
                if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move=0

        #player actions
        if move=="l":
            p.move("l")
        elif move=="r":
            p.move("r")
        if shooting:# to limit the amount of bullets
            p.shoot()
        shooting = False

        #enemy movement
        for e in enemies:
            e.move()
            e.show()

        #bullet movement and collision
        array=p.array
        for b in array:
            for e in enemies:
                if (abs(e.x - b.x)<16) and abs(b.y - e.y) <8:
                    enemies.remove(e)
                    array.remove(b)
                    score +=1
                    break # only remove 1 enemy
            b.move()
            b.show()
            if b.y<0:# remove bullets that are out of vision
                array.remove(b)
            for e in enemies:
                if (abs(e.x - b.x)<20) and abs(b.y - e.y) <12:
                    enemies.remove(e)
                    array.remove(b)
                    score +=1
                    break # only remove 1 enemy

        for e in enemies:#game over
            if e.y >350:
                endscreen = font.render(("Your score is: "+ str(score) + "   Gametime: "+ str(pygame.time.get_ticks()/1000)+" Game Over"), True, (255, 0, 0))
                screen.fill((5, 20, 20))
                screen.blit(endscreen, (100, 200))
                pygame.display.update()
                pygame.time.wait(10000)
                alive=False

        pygame.display.update()

game()#play
