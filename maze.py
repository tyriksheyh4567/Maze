import pygame as pg

pg.init()
pg.font.init()

class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        """
        Initializes the player with the given image, position, speed, width, and height.
        
        Parameters:
            player_image (str): The path to the player's image file.
            player_x (int): The initial x-coordinate of the player.
            player_y (int): The initial y-coordinate of the player.
            player_speed (int): The speed of the player.
            width (int): The width of the player's image.
            height (int): The height of the player's image.
        """
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        """
        Reset the position of the object and redraw it on the window.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        """
        Update the position of the object based on the pressed keys.
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class NPC(GameSprite):
    direction = "left"
    def update(self):
        """
        Update the position of the object based on its current direction and speed.
        """
        if self.rect.x <= 390:
            self.direction = "right"
        if self.rect.x >= 570:
            self.direction = "left"
        #...
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(pg.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        """
        Initializes the wall with the given color and position.
        
        Parameters:
            color_1 (int): The first color of the wall.
            color_2 (int): The second color of the wall.
            color_3 (int): The third color of the wall.
            wall_x (int): The x-coordinate of the wall.
            wall_y (int): The y-coordinate of the wall.
            wall_width (int): The width of the wall.
            wall_height (int): The height of the wall.
        """
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        """
        Draws a wall on the window at the specified position.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))

class Treasure(GameSprite):
    pass #в этом классе ничего нет, так как это просто финиш, а всё необходимое уже есть в классе GameSprite.

Hero = Player(player_image="hero.png", player_x=100, player_y=350, player_speed=5, width=90, height=90)
Enemy = NPC(player_image="cyborg.png", player_x=390, player_y=370, player_speed=2, width=90, height=90)

w1 = Wall(color_1=97, color_2=174, color_3=31, wall_x=70, wall_y=25, wall_width=750, wall_height=15)
w2 = Wall(color_1=97, color_2=174, color_3=31, wall_x=70, wall_y=25, wall_width=15, wall_height=450)
w3 = Wall(color_1=97, color_2=174, color_3=31, wall_x=200, wall_y=140, wall_width=15, wall_height=450)
w4 = Wall(color_1=97, color_2=174, color_3=31, wall_x=350, wall_y=25, wall_width=15, wall_height=380)
w5 = Wall(color_1=97, color_2=174, color_3=31, wall_x=650, wall_y=135, wall_width=350, wall_height=15)
w6 = Wall(color_1=97, color_2=174, color_3=31, wall_x=650, wall_y=135, wall_width=15, wall_height=350)

Final = Treasure(player_image="treasure.png", player_x=600, player_y=45, player_speed=0, width=80, height=80)

pg.mixer.init()

win_width = 700
win_height = 500

window = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Лабиринт")
bg = pg.transform.scale(pg.image.load("background.jpg"), (win_width, win_height))

pg.mixer.music.load("jungles.ogg")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play()

money = pg.mixer.Sound("money.ogg")
kick = pg.mixer.Sound("kick.ogg")
money.set_volume(0.5)
kick.set_volume(1)

finish = False
game = True #флаг продолжения игры
FPS = 60
clock = pg.time.Clock()

font = pg.font.Font('Anta/Anta-Regular.ttf', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

while game:
    for e in pg.event.get(): #условие закрытия окна
        if e.type == pg.QUIT:
            game = False
    if finish is not True:
        window.blit(bg, (0, 0))
        Hero.update()
        Enemy.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        Hero.reset()
        Enemy.reset()
        Final.reset()
        if pg.sprite.collide_rect(Hero, Final):
            finish = True
            pg.mixer.music.stop()
            money.play()
            window.blit(win, (200, 200))
        if pg.sprite.collide_rect(Hero, Enemy) or pg.sprite.collide_rect(Hero, w1) or pg.sprite.collide_rect(Hero, w2) or pg.sprite.collide_rect(Hero, w3) or pg.sprite.collide_rect(Hero, w4) or pg.sprite.collide_rect(Hero, w5):
            finish = True
            pg.mixer.music.stop()
            kick.play()
            window.blit(lose, (180, 200))
    pg.display.update()
    clock.tick(FPS)