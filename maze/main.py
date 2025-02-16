from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 15:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, direction, pos):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = direction
        self.target = pos
    def update(self):
        if self.direction in ["left", "right"]:
            if self.rect.x <= self.target[0]:
                self.direction = "right"
            if self.rect.x >= self.target[1]:
                self.direction = "left"

            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed
        elif self.direction in ["up", "down"]:
            if self.rect.y <= self.target[0]:
                self.direction = "down"
            if self.rect.y >= self.target[1]:
                self.direction = "up"

            if self.direction == "up":
                self.rect.y -= self.speed
            if self.direction == "down":
                self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, wall_pos, wall_size):
        super().__init__()
        self.color_1 = color[0]
        self.color_2 = color[1]
        self.color_3 = color[2]
        self.width = wall_size[0]
        self.height = wall_size[1]
        self.image = Surface((self.width, self.height))
        self.image.fill((color[0], color[1], color[2]))
        self.rect = self.image.get_rect()
        self.rect.x = wall_pos[0]
        self.rect.y = wall_pos[1]
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

player = Player('hero.png', 5, win_height-80, 4)
final = GameSprite('treasure.png', win_width-120, win_height-80, 0)

monsters = (Enemy('cyborg.png', win_width-80, 280, 2, "left", (500, win_width-65)),
            Enemy('cyborg.png', win_width-300, 280, 2, "up", (200, 400)),)

walls = [Wall((154, 205, 50), (100, 20), (450, 10)),
         Wall((154, 205, 50), (100, 480), (350, 10)),
         Wall((154, 205, 50), (100, 20), (10, 380)),
         Wall((154, 205, 50), (200, 150), (200, 10)),
         Wall((154, 205, 50), (250, 250), (10, 250)),
         Wall((154, 205, 50), (250, 50), (10, 100)),
         Wall((154, 205, 50), (500, 150), (10, 300))]

game = True
finish = False

clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 80)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.blit(background, (0, 0))
        player.update()

        final.reset()
        player.reset()
        
        for m in monsters:
            m.update()
            m.reset()
        
        for w in walls:
            w.draw_wall()
    
    if any([sprite.collide_rect(player, m) for m in monsters]) or any([sprite.collide_rect(player, w) for w in walls]):
        finish = True
        window.blit(lose, (200, 200))
        kick.play()
        
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200, 200))
        money.play()
    
    display.update()
    clock.tick(FPS)
