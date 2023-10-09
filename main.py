import pygame
import random
import pygame.time
from player import Player
from enemy import Enemy
from databasemanager import DatabaseManager

def gameRules():
    global rule1_surface
    global rule1_rect
    global rule2_surface
    global rule2_rect
    global rule3_surface
    global rule3_rect
    global rule4_surface
    global rule4_rect
    global rule5_surface
    global rule5_rect
    rule1 = "1. Введите имя персонажа и нажмите Enter."
    rule2 = "2. Управление персонажем на стрелочки."
    rule3 = "3. За отведенное время нужно есть фрукты."
    rule4 = "4. Если съедите меньше тридцати, то проиграете."
    rule5 = "5. Больше двигаешься - больше фруктов."
    rule1_surface = font.render(rule1, True, (255, 255, 255))
    rule1_rect = pygame.Rect(170, 200, 500, 36)
    rule2_surface = font.render(rule2, True, (255, 255, 255))
    rule2_rect = pygame.Rect(170, 250, 500, 36)
    rule3_surface = font.render(rule3, True, (255, 255, 255))
    rule3_rect = pygame.Rect(170, 300, 500, 36)
    rule4_surface = font.render(rule4, True, (255, 255, 255))
    rule4_rect = pygame.Rect(170, 350, 500, 36)
    rule5_surface = font.render(rule5, True, (255, 255, 255))
    rule5_rect = pygame.Rect(170, 400, 500, 36)

def show_result_message(message, top_players):
    # Создайте текстовый объект для сообщения
    result_font = pygame.font.Font(None, 36)
    result_text = result_font.render(message, True, (255, 255, 255))  # Белый текст
    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Центрирование текста

    # Очистите экран
    screen.fill((0, 0, 0))

    # Отобразите сообщение на экране
    screen.blit(result_text, result_rect)

    # Отображение списка топ-5 игроков
    y_offset = result_rect.bottom + 20  # Начальная вертикальная позиция для списка игроков
    for rank, (player_name, player_score) in enumerate(top_players, start=1):
        player_text = result_font.render(f"{rank}. {player_name}: {player_score}", True, (255, 255, 255))
        player_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(player_text, player_rect)
        y_offset += player_rect.height + 10  # Увеличиваем вертикальную позицию для следующего игрока

    # Обновите экран
    pygame.display.flip()

    # Ждите, пока игрок не нажмет клавишу для начала новой игры
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_key = False

def initialize(): 

    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global running
    global clock
    global enemies
    global db_manager
    global font
    global screen
    global start_time
    global game_duration
    global background
    global player
    global score
    global game_over
    global text
    global input_active

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Основной игровой цикл
    running = True
    clock = pygame.time.Clock()

    # Создание группы спрайтов для врагов
    enemies = pygame.sprite.Group()

    db_manager = DatabaseManager("scores.db")
    db_manager.connect()
    db_manager.create_scores_table() # Создание таблицы, если она не существует

    font = pygame.font.Font(None, 36)
    # Создание окна игры
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MangoCrab")

    # Время начала игры (в миллисекундах)
    start_time = pygame.time.get_ticks()

    # Продолжительность игры (в миллисекундах)
    game_duration = 60000

    # Загрузка изображения заднего фона
    background = pygame.image.load("images/background.jpg")

    player = Player()

    score = 0
    game_over = False

    # Запрос имени пользователя
    text = "Введите имя"
    input_active = True  # Флаг активности поля ввода

def waitForName():

    global input_active
    global spawn_enemies
    global text_surface
    global input_rect
    global screen
    global clock
    global text

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if text.strip() != "":
                    input_active = False
                    spawn_enemies = True
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отображение заднего фона
    screen.blit(background, (0, 0))

    # Отображение поля ввода имени
    text_surface = font.render(text, True, (255, 255, 255))
    input_rect = pygame.Rect(50, 50, 200, 36)  # Позиция и размер поля ввода
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Отображение текста правил игры
    screen.blit(rule1_surface, rule1_rect)
    screen.blit(rule2_surface, rule2_rect)
    screen.blit(rule3_surface, rule3_rect)
    screen.blit(rule4_surface, rule4_rect)
    screen.blit(rule5_surface, rule5_rect)

    # Обновление дисплея
    pygame.display.flip()

    # Ограничение частоты обновления экрана
    clock.tick(60)

def mainGame():

    global running
    global score
    global game_over
    global start_time
    global text
    global input_active

    current_time = pygame.time.get_ticks()  # Получение текущего времени

    # Оставшееся время в миллисекундах
    remaining_time = max(0, game_duration - (pygame.time.get_ticks() - start_time))

    # Преобразование времени в секунды
    remaining_seconds = remaining_time // 1000

    # Создание текстового объекта для отображения времени
    time_text = font.render(f"Time: {remaining_seconds} s", True, (255, 255, 255))
    time_rect = time_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))  # Позиция времени в верхнем правом углу

    if game_over:
        enemies.empty()
        text = ""  # Сброс поля ввода имени
        input_active = True  # Включение ввода имени
        game_over = False

    # Проверка завершения игры
    if current_time - start_time >= game_duration:
        if score >= 30:
            message = "You WIN!"
            db_manager.insert_score(text, score) # Вставка результата в базу данных
        else:
            message = "You DIED!"

        # Получение топ-5 игроков
        top_players = db_manager.get_top_players()

        show_result_message(message, top_players)

        # Сброс счета и других переменных для начала новой игры
        score = 0
        player.rect.centerx = SCREEN_WIDTH // 2
        player.rect.bottom = SCREEN_HEIGHT - 10
        start_time = pygame.time.get_ticks()
        game_over = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # Обработка клавиш для управления персонажем
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()
        
        # Создание новых врагов
        if not input_active and random.randrange(100) < 15:
            new_enemy = Enemy()
            enemies.add(new_enemy)  # Добавление врага в группу спрайтов

    # Обновление позиции персонажа и врага
    player.update()
    enemies.update()

    # Проверка столкновения с врагами
    hits = pygame.sprite.spritecollide(player, enemies, True)
        
    # Если есть столкновения, увеличьте счет и выведите его
    if hits:
        score += len(hits)
    
    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отображение заднего фона
    screen.blit(background, (0, 0))

    # Отображение времени на экране
    screen.blit(time_text, time_rect)

    # Отображение персонажа на экране
    screen.blit(player.image, player.rect)

    # Отображение поля ввода имени
    text_surface = font.render(text, True, (255, 255, 255))
    input_rect = pygame.Rect(50, 50, 200, 36)  # Позиция и размер поля ввода
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Отображение счета на экране
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Отображение врагов
    enemies.draw(screen)

    # Обновление дисплея
    pygame.display.flip()

    # Ограничение частоты обновления экрана
    clock.tick(60)

# Инициализация PyGame
pygame.init()

initialize()

gameRules()

while input_active:
    waitForName()

while running:
    mainGame()
    
# Завершение PyGame
pygame.quit()