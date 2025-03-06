from machine import Pin, I2C
import ssd1306
import time
import random

# --- Globální inicializace OLED displeje ---
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Menu ---
menu = ["Snake", "Dodge the Blocks", "Catch the Dot", "Flappy Bird"]
menu_index = 0  # Počáteční výběr

def draw_menu():
    oled.fill(0)
    for i, option in enumerate(menu):
        if i == menu_index:
            oled.text("-> " + option, 0, i * 10)
        else:
            oled.text(option, 0, i * 10)
    oled.text("ESP game console", 0, 55)
    oled.show()

def change_selection(direction):
    global menu_index
    if direction == "UP" and menu_index > 0:
        menu_index -= 1
    elif direction == "DOWN" and menu_index < len(menu) - 1:
        menu_index += 1
    elif direction == "RIGHT":
        start_game(menu_index)

def start_game(game_index):
    if game_index == 0:
        play_snake()
    elif game_index == 1:
        play_dodge_the_blocks()
    elif game_index == 2:
        play_catch_game()
    elif game_index == 3:
        play_flappy_bird()

# Menu ovládání – využíváme tlačítka na pinech 12 (nahoru), 13 (dolu) a 14 (potvrdit)
menu_button_up = Pin(12, Pin.IN, Pin.PULL_UP)
menu_button_down = Pin(13, Pin.IN, Pin.PULL_UP)
menu_button_select = Pin(14, Pin.IN, Pin.PULL_UP)

def menu_loop():
    global menu_index
    while True:
        draw_menu()
        if menu_button_up.value() == 0:
            change_selection("UP")
            time.sleep(0.3)  # debounce
        if menu_button_down.value() == 0:
            change_selection("DOWN")
            time.sleep(0.3)
        if menu_button_select.value() == 0:
            change_selection("RIGHT")
            time.sleep(0.3)
        time.sleep(0.1)

# --- Hra Flappy Bird ---
from machine import Pin, I2C
import ssd1306
import time
import random

# --- Globální inicializace OLED displeje ---
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Flappy Bird Hra ---
from machine import Pin, I2C
import ssd1306
import time
import random

# --- Globální inicializace OLED displeje ---
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Flappy Bird Hra ---
from machine import Pin, I2C
import ssd1306
import time
import random

# --- Globální inicializace OLED displeje ---
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Flappy Bird Hra ---
def play_flappy_bird():
    bird_x = 20
    bird_y = 32
    bird_speed = 0
    gravity = 1
    jump_strength = -4
    score = 0
    gap_height = 30  # Výška mezery mezi překážkami

    # Počáteční překážky
    obstacles = []
    obstacle_width = 10
    obstacle_speed = 2  # Rychlost pohybu překážek
    min_obstacle_distance = 30  # Minimální horizontální vzdálenost mezi překážkami

    # Tlačítko pro skok
    btn_jump = Pin(12, Pin.IN, Pin.PULL_UP)

    def draw_game():
        oled.fill(0)
        oled.text("Score: {}".format(score), 0, 0)
        oled.rect(bird_x, bird_y, 5, 5, 1)  # Kreslí ptáčka

        # Kreslí překážky
        for obstacle in obstacles:
            oled.rect(obstacle[0], obstacle[1], obstacle_width, obstacle[2], 1)
            oled.rect(obstacle[0], obstacle[1] + obstacle[2] + gap_height, obstacle_width, 64 - obstacle[1] - obstacle[2] - gap_height, 1)

        oled.show()

    def update_obstacles():
        nonlocal obstacles, score
        # Pohyb překážek
        new_obstacles = []
        for obs in obstacles:
            if obs[0] + obstacle_width > 0:
                new_obstacles.append((obs[0] - obstacle_speed, obs[1], obs[2]))
            # Zkontroluj, zda překážka prošla obrazovkou
            elif obs[0] + obstacle_width == 0:
                score += 1  # Zvyš skóre
        obstacles = new_obstacles

        # Vytvoř novou překážku, pokud není v zorném poli
        if len(obstacles) == 0 or obstacles[-1][0] < 128 - min_obstacle_distance:
            # Náhodně generovaná výška horní překážky mezi 20% a 60% výšky obrazovky
            top_height = (random.getrandbits(6) % 25) + 5  # Horní překážka bude mít výšku mezi 5 a 30 pixely
            # Výška spodní překážky (výška obrazovky minus výška horní překážky minus mezera)
            bottom_height = 64 - top_height - gap_height

            # Pokud by výška spodní překážky byla menší než 0, nastaví ji na 0
            if bottom_height < 0:
                bottom_height = 0

            obstacles.append((128, 0, top_height))  # Horní překážka začíná na y = 0
            obstacles.append((128, 64 - bottom_height, bottom_height))  # Spodní překážka začíná na zemi

    def update_bird():
        nonlocal bird_y, bird_speed
        if btn_jump.value() == 0:
            bird_speed = jump_strength
        bird_speed += gravity
        bird_y += bird_speed

        # Kontrola kolize s horní a dolní hranicí
        if bird_y < 0:
            bird_y = 0
            bird_speed = 0
        if bird_y > 64 - 5:
            bird_y = 64 - 5
            bird_speed = 0

    def check_collision():
        # Pro každou dvojici překážek (horní a spodní)
        for i in range(0, len(obstacles), 2):
            top_obstacle = obstacles[i]
            bottom_obstacle = obstacles[i+1]
            # Kontrola, zda se ptáček nachází ve sloupci překážek
            if bird_x + 5 > top_obstacle[0] and bird_x < top_obstacle[0] + obstacle_width:
                # Pokud ptáček je výše než dolní hrana horní překážky, pak je v kolizi
                if bird_y < top_obstacle[2]:
                    return True
                # Pokud ptáček klesne pod horní hranu spodní překážky, pak je v kolizi
                if bird_y + 5 > bottom_obstacle[1]:
                    return True
        return False



    # Hlavní herní smyčka
    while True:
        update_bird()
        update_obstacles()
        draw_game()

        if check_collision():
            oled.fill(0)
            oled.text("Game Over", 30, 30)
            oled.show()
            time.sleep(2)
            break

        time.sleep(0.02)  # Zrychlení obnovy, aby hra byla plynulejší

    time.sleep(1)

# --- Hra Snake ---
def play_snake():
    # Lokální herní proměnné
    snake = [(30, 30)]
    food = ((random.getrandbits(7) % 25) * 5, (random.getrandbits(7) % 13) * 5)
    snake_dir = "RIGHT"
    score = 0
    player_speed = 5  # Mění se o tuto hodnotu

    # Nastavení tlačítek pro ovládání – piny: 12 (LEFT), 13 (RIGHT), 14 (UP), 0 (DOWN)
    btn_left  = Pin(12, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(13, Pin.IN, Pin.PULL_UP)
    btn_up    = Pin(14, Pin.IN, Pin.PULL_UP)
    btn_down  = Pin(0,  Pin.IN, Pin.PULL_UP)

    def draw_game():
        oled.fill(0)
        oled.text("Score: {}".format(score), 0, 0)
        for seg in snake:
            oled.rect(seg[0], seg[1], 5, 5, 1)
        # Ovocí vykreslené jako "*"
        oled.text('*', food[0], food[1])
        oled.show()

    def update_direction():
        nonlocal snake_dir
        if btn_left.value() == 0 and snake_dir != "RIGHT":
            snake_dir = "LEFT"
        elif btn_right.value() == 0 and snake_dir != "LEFT":
            snake_dir = "RIGHT"
        elif btn_up.value() == 0 and snake_dir != "DOWN":
            snake_dir = "UP"
        elif btn_down.value() == 0 and snake_dir != "UP":
            snake_dir = "DOWN"

    def move_snake():
        nonlocal snake, food, score, snake_dir, player_speed
        head_x, head_y = snake[0]
        if snake_dir == "UP":
            head_y -= player_speed
        elif snake_dir == "DOWN":
            head_y += player_speed
        elif snake_dir == "LEFT":
            head_x -= player_speed
        elif snake_dir == "RIGHT":
            head_x += player_speed
        new_head = (head_x, head_y)
        if new_head == food:
            score += 1
            food = ((random.getrandbits(7) % 25) * 5, (random.getrandbits(7) % 13) * 5)
        else:
            snake.pop()
        if head_x < 0 or head_x >= 128 or head_y < 0 or head_y >= 64 or new_head in snake:
            oled.fill(0)
            oled.text("Game Over", 30, 30)
            oled.show()
            time.sleep(2)
            return False
        else:
            snake.insert(0, new_head)
        return True

    while True:
        update_direction()
        if not move_snake():
            break
        draw_game()
        time.sleep(0.2)
    time.sleep(1)

# --- Hra Dodge the Blocks ---
def play_dodge_the_blocks():
    player_x = 64
    player_y = 58
    blocks = [((random.getrandbits(7) % 121), 0)]
    score = 0
    player_speed = 5  # Rychlost pohybu hráče
    block_speed = 3

    # Tlačítka pro ovládání (piny 12 a 13)
    btn_left  = Pin(12, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(13, Pin.IN, Pin.PULL_UP)

    while True:
        if btn_left.value() == 0:
            player_x -= player_speed
        if btn_right.value() == 0:
            player_x += player_speed
        if player_x < 0:
            player_x = 0
        if player_x > 123:
            player_x = 123

        new_blocks = []
        for (x, y) in blocks:
            new_y = y + block_speed
            if new_y < 64:
                new_blocks.append((x, new_y))
        blocks = new_blocks

        if (random.getrandbits(4) % 11) < 3:
            blocks.append(((random.getrandbits(7) % 121), 0))

        collision = False
        for (x, y) in blocks:
            if (x < player_x + 5 and x + 5 > player_x and
                y < player_y + 5 and y + 5 > player_y):
                collision = True
                break
        if collision:
            oled.fill(0)
            oled.text("Game Over", 30, 30)
            oled.show()
            time.sleep(2)
            break

        oled.fill(0)
        # Hráč vykreslený jako čtverec
        oled.rect(player_x, player_y, 5, 5, 1)
        for (x, y) in blocks:
            oled.text('*', x, y)
        oled.show()
        time.sleep(0.01)
    time.sleep(0.01)

# --- Hra Catch the Dot ---
def play_catch_game():
    player_x = 60
    player_y = 58
    dot_x = random.getrandbits(7) % 124
    dot_y = 0
    score = 0
    speed = 2
    player_speed = 5  # zrychlený pohyb hráče

    # Tlačítka pro ovládání (piny 12 a 13)
    btn_left  = Pin(12, Pin.IN, Pin.PULL_UP)
    btn_right = Pin(13, Pin.IN, Pin.PULL_UP)

    while True:
        if btn_left.value() == 0:
            player_x -= player_speed
        if btn_right.value() == 0:
            player_x += player_speed
        if player_x < 0:
            player_x = 0
        elif player_x > 123:
            player_x = 123

        dot_y += speed

        oled.fill(0)
        oled.text("Score: {}".format(score), 0, 0)
        # Hráč jako čtverec
        oled.rect(player_x, player_y, 5, 5, 1)
        # Padající tečka jako "*"
        oled.text('*', dot_x, dot_y)
        oled.show()

        if dot_y + 5 >= player_y and (dot_x + 5 > player_x and dot_x < player_x + 5):
            score += 1
            dot_x = random.getrandbits(7) % 124
            dot_y = 0

        if dot_y > 64:
            oled.fill(0)
            oled.text("Game Over", 30, 30)
            oled.show()
            time.sleep(2)
            break

        time.sleep(0.01)  # ještě rychlejší interval pro plynulejší pohyb
    time.sleep(1)


# --- Spuštění menu ---
menu_loop()

