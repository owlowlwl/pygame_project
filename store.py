import pygame
import sys
import os
import random


WIDTH, HEIGHT = 600, 500
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["     Продуктовый магазин", "",
                  "Собери необходимые продукты"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 145
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    click_text = ["SPACE - пауза и список покупок", "",
                  "Кликните в любом месте для продолжения"]
    font2 = pygame.font.Font(None, 20)
    text_coord = 300
    for line in click_text:
        string_rendered = font2.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 2
        intro_rect.top = text_coord
        intro_rect.x = 145
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # txt = 'Кликните в любом месте для продолжения'
    # string = font.render(txt, 1, pygame.Color('white'))
    # screen.blit(string, (150, 320))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
play_fon = load_image('play_fon.jpg')
images = ['cab.png', 'chick.png', 'cheese.png']


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        image = load_image(images[random.randint(0, 2)])
        self.image = pygame.transform.scale(image, (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, 0)

    def update(self):
        if not pygame.sprite.collide_mask(self, player):
            self.rect = self.rect.move(0, 1)
        else:
            self.kill()


class Player(pygame.sprite.Sprite):
    image = pygame.Surface([70, 10])
    image.fill(pygame.Color((51, 45, 45)))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = 400
        self.rect.x = WIDTH // 2 - self.rect.width // 2

    def update(self, x):
        self.rect.x = x - self.rect.width // 2


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    player = Player(player_group)
    running = True
    score = 0
    food = Food()
    objects_amount = 50
    object_spawn_pause = 0
    while running:
        screen.blit(play_fon, (0, 0))  # корректировка фона
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                player.update(event.pos[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
        if objects_amount != 0 and object_spawn_pause <= 0:
            for i in range(3, 7):
                food = Food()
            objects_amount -= 1
            object_spawn_pause = 300
        if object_spawn_pause > 0:
            object_spawn_pause -= 1
        player_group.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()
