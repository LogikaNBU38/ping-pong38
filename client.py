from pygame import *
import socket
import json
from threading import Thread
import pygame

from launcher import launcher

player_name, backgroundskin = launcher()
print("Ім'я гравця: ", player_name)

# ---ПУГАМЕ НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")
# ---СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('localhost', 8080)) # ---- Підключення до сервера
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass


def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)
font_nickname = font.Font(None, 50)
# --- ЗОБРАЖЕННЯ ----
background = pygame.image.load("background1.png").convert()
if backgroundskin == "2":
    background = pygame.image.load("background2.png").convert()
elif backgroundskin == "3":
    background = pygame.image.load("background3.png").convert()
elif backgroundskin == "4":
    background = pygame.image.load("background4.png").convert()
background = transform.scale(background, (WIDTH, HEIGHT))
# --- ЗВУКИ ---
hitsound = pygame.mixer.Sound("hitsound1.mp3")
if backgroundskin == "2":
    hitsound = pygame.mixer.Sound("hitsound2.mp3")
elif backgroundskin == "3":
    hitsound = pygame.mixer.Sound("hitsound3.mp3")
elif backgroundskin == "4":
    hitsound = pygame.mixer.Sound("hitsound4.mp3")
# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if "countdown" in game_state and game_state["countdown"] > 0:
        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue  # Не малюємо гру до завершення відліку

    if "winner" in game_state and game_state["winner"] is not None:
        screen.fill((20, 20, 20))

        if you_winner is None:  # Встановлюємо тільки один раз
            if game_state["winner"] == my_id:
                you_winner = True
            else:
                you_winner = False

        if you_winner:
            text = "Ти переміг!"
        else:
            text = "Пощастить наступним разом!"

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render('К - рестарт', True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue  # Блокує гру після перемоги

    if game_state:
        screen.blit(background, (0, 0))
        colorP1 = 0, 30, 255
        colorP2 = 255, 30, 0
        if backgroundskin == "2":
            colorP1 = 200, 20, 200
            colorP2 = 0, 150, 0
        elif backgroundskin == "3":
            colorP1 = 255, 30, 0
            colorP2 = 0, 30, 255
        elif backgroundskin == "4":
            colorP1 = 255,255,255
            colorP2 = 255,255,255
        draw.rect(screen, colorP1, (20, game_state['paddles']['0'], 20, 100))
        draw.rect(screen, colorP2, (WIDTH - 40, game_state['paddles']['1'], 20, 100))
        draw.circle(screen, (255, 255, 255), (game_state['ball']['x'], game_state['ball']['y']), 10)
        score_text = font_main.render(f"{game_state['scores'][0]} : {game_state['scores'][1]}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 -25, 20))

        playername_text = font_nickname.render(player_name, True, (255, 255, 255))
        screen.blit(playername_text, (WIDTH // 2 -25 , 50))

        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                if backgroundskin != "1":
                    hitsound.play()

            if game_state['sound_event'] == 'platform_hit':
                hitsound.play()


    else:
        wating_text = font_main.render(f"Очікування гравців...", True, (255, 255, 255))
        screen.blit(wating_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")