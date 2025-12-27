import pygame
import random

pygame.init()
pygame.mixer.init()
game_over_sfx = pygame.mixer.Sound("game_over.wav")

font = pygame.font.SysFont("arial", 30)

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa's Gift Catcher")
clock = pygame.time.Clock()

player_image = pygame.image.load("Santa's Sleigh.png").convert_alpha()
player_image = pygame.transform.smoothscale(player_image, (100, 100))

red = pygame.image.load("red_gift.png").convert_alpha()
red = pygame.transform.smoothscale(red, (90, 90))
green = pygame.image.load("green_gift.png").convert_alpha()
green = pygame.transform.smoothscale(green, (90, 90))
blue = pygame.image.load("blue_gift.png").convert_alpha()
blue = pygame.transform.smoothscale(blue, (90, 90))
gift_images = [red, green, blue]

candy_image = pygame.image.load("candy_cane.png").convert_alpha()
candy_image = pygame.transform.smoothscale(candy_image, (90, 90))

snowball_image = pygame.image.load("Snowball.png").convert_alpha()
snowball_image = pygame.transform.smoothscale(snowball_image, (120, 120))
class Player:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.speed = speed
        self.image = player_image
        self.direction = "right"

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rect.x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.rect.x += self.speed
            self.direction = "right"

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def reset(self):
        self.rect.x = 365

    def draw(self):
        if self.direction == "left":
            img = pygame.transform.flip(self.image, True, False)
            mask = pygame.mask.from_surface(img)
        else:
            img = self.image
            mask = pygame.mask.from_surface(img)
        window.blit(img, self.rect)
        self.mask = mask

class Gift:
    def __init__(self, x, speed):
        self.rect = pygame.Rect(x, -40, 90, 90)
        self.speed = speed
        self.image = random.choice(gift_images)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        window.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, speed):
        self.image = snowball_image
        self.rect = pygame.Rect(x, -40, 120, 120)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        window.blit(self.image, self.rect)

class Candy:
    def __init__(self, x, speed):
        self.rect = pygame.Rect(x, -40, 90, 90)
        self.speed = speed
        self.image = candy_image
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        window.blit(self.image, self.rect)

background = pygame.image.load("christmasBG.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_speed = 10
gift_speed = 5
normal_gift_speed = gift_speed
player = Player(360, 500, player_speed)

gifts = []
enemy = []
candies = []

game_speedup = 0.002
max_speedup = 25

spawn_timer = 0
spawn_delay = 40
minimum_delay = 20
delay_decrease = 0.002

game_over = False
score = 0
startup = True
running = True
music_off = False

active_speed_buff = False
active_points_buff = False
speed_buff_end = 0
points_buff_end = 0
points_multiplier = 1
buff_duration = 5999

while running:
    while startup:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                startup = False
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            startup = False
            ticks = pygame.time.get_ticks()

        window.blit(background, (0, 0))
    
        title_text = font.render("Santa's Gift Catcher", True, (255, 0, 0))
        window.blit(title_text, (400 - title_text.get_width() / 2, 250))
    
        instruction_lines = [
            "In this game, your job is to catch Santa's gifts and avoid Snowballs.",
            "There are rare Candy Canes that give you Slow-Motion or Points Buffs.",
            "The game gets faster as you play.",
            "Press Space to start!"
        ]
    
        text_y = 310
        for line in instruction_lines:
            line_surface = font.render(line, True, (0, 0, 0))
            window.blit(line_surface, (400 - line_surface.get_width() / 2, text_y))
            text_y += 30
            # This is for the instruction lines to fit on screen
        pygame.display.update()

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    if not game_over:
        if not music_off:
            pygame.mixer.music.load("Jingle Bell.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
            music_off = True

        if not active_speed_buff:
            player_speed += game_speedup
        if not active_speed_buff:
            normal_gift_speed += game_speedup
            if normal_gift_speed > max_speedup:
                normal_gift_speed = max_speedup
        if player_speed > max_speedup:
            player_speed = max_speedup
        if normal_gift_speed > max_speedup:
            normal_gift_speed = max_speedup

        if not active_speed_buff:
            player.speed = player_speed
            gift_speed = normal_gift_speed

        if spawn_delay > minimum_delay:
            spawn_delay -= delay_decrease

        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            x = random.randint(0, WIDTH - 80)
            if random.randint(1, 20) == 1:
                candies.append(Candy(x, gift_speed))
            else:
                if random.choice([True, False]):
                    gifts.append(Gift(x, gift_speed))
                else:
                    enemy.append(Enemy(x, gift_speed))
            spawn_timer = 0

        player.update()
        player_mask = pygame.mask.from_surface(player.image)
        # im not using colliderect because hitboxes were inaccurate with the images in testing, this makes it pixel perfect
        for gift in gifts[:]:
            gift.update()
            offset = (player.rect.x - gift.rect.x, player.rect.y - gift.rect.y)
            if gift.mask.overlap(player.mask, offset):
                score += int(1 * points_multiplier)
                pygame.mixer.Sound("pickup_sound.wav").play()
                gifts.remove(gift)
            elif gift.rect.y > HEIGHT:
                gifts.remove(gift) 

        for e in enemy[:]:
            e.update()
            offset = (player.rect.x - e.rect.x, player.rect.y - e.rect.y)
            if e.mask.overlap(player.mask, offset):
                game_over_sfx.play()
                game_over = True
            elif e.rect.y > HEIGHT:
                enemy.remove(e)

        for candy in candies[:]:
            candy.update()
            offset = (player.rect.x - candy.rect.x, player.rect.y - candy.rect.y)
            if candy.mask.overlap(player.mask, offset):
                pygame.mixer.Sound("eating_candycane.wav").play()
                now = pygame.time.get_ticks()
                chosen_buff = random.choice(['speed', 'points'])

                if chosen_buff == 'speed':
                    if active_speed_buff:
                        speed_buff_end += buff_duration
                    else:
                        active_speed_buff = True
                        speed_buff_end = now + buff_duration
                        gift_speed = normal_gift_speed / 2
                        for object in gifts + enemy + candies:
                            object.speed /= 2

                else:
                    if active_points_buff:
                        points_buff_end += buff_duration
                    else:
                        active_points_buff = True
                        points_buff_end = now + buff_duration
                        points_multiplier = 2

                candies.remove(candy)

            elif candy.rect.y > HEIGHT:
                candies.remove(candy)

        now = pygame.time.get_ticks()
        if active_speed_buff and now >= speed_buff_end:
            active_speed_buff = False
            gift_speed = normal_gift_speed
            for obj in gifts + enemy + candies:
                obj.speed *= 2

        if active_points_buff and now >= points_buff_end:
            active_points_buff = False
            points_multiplier = 1

    secs = (pygame.time.get_ticks() - ticks) // 1000
    time_text = font.render(f"Time: {secs}", True, (255, 255, 255))
    time_text.set_alpha(175)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_text.set_alpha(175)

    window.blit(background, (0, 0))
    player.draw()
    window.blit(time_text, (10, 10))
    window.blit(score_text, (10, 50))

    for gift in gifts:
        gift.draw()
    for e in enemy:
        e.draw()
    for candy in candies:
        candy.draw()

    text_y = 90
    if active_speed_buff:
        seconds_left = (speed_buff_end - now) // 1000
        if seconds_left < 0:
            seconds_left = 0
        window.blit(font.render("Slow-Motion: " + str(seconds_left) + "s", True, (255, 255, 0)), (10, text_y))
        text_y += 30

    if active_points_buff:
        seconds_left = (points_buff_end - now) // 1000
        if seconds_left < 0:
            seconds_left = 0
        window.blit(font.render("2X Points Buff: " + str(seconds_left) + "s", True, (255, 255, 0)), (10, text_y))

    while game_over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                game_over = False
        pygame.mixer.music.stop()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            gifts.clear()
            enemy.clear()
            candies.clear()
            player.reset()
            player_speed = 10
            normal_gift_speed = 5
            gift_speed = normal_gift_speed
            score = 0
            spawn_delay = 40
            spawn_timer = 0
            ticks = pygame.time.get_ticks()
            active_speed_buff = False
            active_points_buff = False
            speed_buff_end = 0
            points_buff_end = 0
            points_multiplier = 1
            player.speed = player_speed
            game_over = False
            game_over_sfx.stop()
            pygame.mixer.music.play(-1)

        game_over_text = font.render("You got hit!", True, (255, 0, 0))
        game_over_text2 = font.render("Press R to play again.", True, (0, 0, 0))
        window.blit(game_over_text, (400 - game_over_text.width / 2, 300))
        window.blit(game_over_text2, (400 - game_over_text2.width / 2, 330))
        pygame.display.update()

    pygame.display.update()

pygame.quit()
