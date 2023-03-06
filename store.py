import pygame
import sys
import os
import random


WIDTH, HEIGHT = 626, 419
FPS = 50
# clock = pygame.time.Clock()
# TIMER_EVENT_TYPE = 20
# уровни и начальные данные
levels = {'1': ["     Список покупок", "", "1. Куриное филе", "2. Салат", "3. Сыр", "4. Помидоры"],
          '2': ["     Список покупок", "", "1. Спагетти", "2. Бекон", "3. Сливки", "4. Сыр", "5. Яйца"],
          '3': ["     Список покупок", "", "1. Картофель", "2. Морковь", "3. Яйца", "4. Колбаса", "5. Горох",
                "6. Майонез"]}
level = '1'
score = 0
hearts = 5


def terminate():
    pygame.quit()
    sys.exit()


# стартовый экран
def start_screen(final_text=None):
    if not final_text:
        intro_text = ["Grocery store", "",
                      "Собери необходимые продукты"]

        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font1 = pygame.font.SysFont('bahnschrift', 28)
        font2 = pygame.font.SysFont('bahnschrift', 23)
        string1 = font1.render(intro_text[0], 1, pygame.Color('black'))
        intro_rect = string1.get_rect()
        intro_rect.top = 150
        intro_rect.x = WIDTH // 2 - intro_rect.width // 2
        screen.blit(string1, intro_rect)
        string2 = font2.render(intro_text[2], 1, pygame.Color('black'))
        intro_rect = string2.get_rect()
        intro_rect.top = 200
        intro_rect.x = WIDTH // 2 - intro_rect.width // 2
        screen.blit(string2, intro_rect)

        click_text = ["SPACE - пауза и список покупок",
                      "Кликните в любом месте для продолжения"]
        font2 = pygame.font.SysFont('bahnschrift', 16)
        text_coord = 250
        for line in click_text:
            string_rendered = font2.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 2
            intro_rect.top = text_coord
            intro_rect.x = 145
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)
    # финальный экран
    else:
        fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.SysFont('bahnschrift', 30)
        text_coord = 150
        for line in final_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = WIDTH // 2 - intro_rect.width // 2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)


# экран во время паузы
def paused_screen():
    list_text = levels[level]
    fon = pygame.transform.scale(load_image('paused_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 80
    for line in list_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # выводим счёт
    screen.blit(font.render(f'Счёт: {score}', 1, pygame.Color('black')), (200, 370, 50, 20))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # продолжаем игру
        pygame.display.flip()
        clock.tick(FPS)


# загрузка изображений
def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
play_fon = load_image('fon2.jpg')
images = {'Салат': 'cab.png', 'Куриное филе': 'chick.png', 'Сыр': 'cheese.png', 'Бекон': 'bac.png',
          'Морковь': 'carr.png', 'Сливки': 'cream.png', 'Яйца': 'eggs.png', 'Горох': 'peas.png',
          'Картофель': 'pot.png', 'Колбаса': 'sausage.png', 'Спагетти': 'spag.png', 'Помидоры': 'tom.png'}


# класс с созданием падающих спрайтов
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.num = random.randint(0, 10)
        self.keys = list(images.keys())
        image = load_image(images[self.keys[self.num]])
        self.image = pygame.transform.scale(image, (55, 55))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.is_paused = False

    def update(self):
        if not pygame.sprite.collide_mask(self, player):
            # движение вниз
            self.rect = self.rect.move(0, 1)
        else:
            global score, hearts
            name_prod = self.keys[self.num]
            # проверка
            if name_prod in ' '.join(levels[level]):
                score += 1
                for i in range(len(levels[level])):
                    if name_prod in levels[level][i]:
                        levels[level][i] += ' +'  # отмечаются уже собранные продукты
            else:
                hearts -= 1
            self.kill()

    # проверка на выигрыш
    def check_win(self):
        return score == len(levels[level])


# класс игрока
class Player(pygame.sprite.Sprite):
    image = pygame.Surface([70, 10])
    image.fill(pygame.Color((51, 45, 45)))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = 390
        self.rect.x = WIDTH // 2 - self.rect.width // 2

    def update(self, x):
        # движение вместе соответственно курсору
        self.rect.x = x - self.rect.width // 2


# пауза
def switch_pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        paused_screen()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            paused = False


# основной игровой цикл
if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_screen()
    player = Player(player_group)
    running = True
    objects_amount = 100
    object_spawn_pause = 0
    game_over = False
    while running:
        screen.blit(play_fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # движение игрока
            if event.type == pygame.MOUSEMOTION and not game_over:
                player.update(event.pos[0])
            # нажатие на паузу
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    switch_pause()
        if not game_over:
            # произвольное создание спрайтов
            if objects_amount != 0 and object_spawn_pause <= 0:
                food = Food()
                objects_amount -= 1
                object_spawn_pause = random.randint(10, 100)
            if object_spawn_pause > 0:
                object_spawn_pause -= 1
            if objects_amount == 0:
                game_over = True
        player_group.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(120)
        # проверка на проигрыш
        if hearts == 0 or game_over:
            game_over = True
            text = ["     Вы проиграли!", "", "Результаты:", f"Счёт: {score}"]
            start_screen(final_text=text)
        # проверка на выигрыш
        if food.check_win():
            game_over = True
            text = ["     Вы выиграли!", "", "Результаты:", f"Счёт: {score}"]
            start_screen(final_text=text)
        pygame.display.flip()
    pygame.quit()
