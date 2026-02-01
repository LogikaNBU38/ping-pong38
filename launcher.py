import sys

import pygame
from pygame import *
WIDTH, HEIGHT = 500, 500

mixer.init()
clicksound = pygame.mixer.Sound("hitsound4.mp3")
def launcher():
    init()
    screen = display.set_mode((WIDTH, HEIGHT))
    display.set_caption("Pong Launcher")

    font_title = font.Font(None, 56)
    font_btn = font.Font(None, 42)
    font_input = font.Font(None, 36)

    backgroundskin = "1"
    turnonmusic = True
    input_text = ""
    active_input = False
    mode = "Main"

    while True:
        if mode == "Main":
            screen.fill((70, 70, 70))

            title = font_title.render("PING PONG 38", True, (0, 200, 255))
            screen.blit(title, title.get_rect(center=(WIDTH / 2, 40)))

            play_btn = Rect(100, 100, 300, 70)
            settings_btn = Rect(100, 200, 300, 70)
            exit_btn = Rect(100, 300, 300, 70)

            input_box = Rect(100, 400, 300, 50)

            draw.rect(screen, (0, 180, 0), play_btn, border_radius=12)
            draw.rect(screen, (18, 180, 0), settings_btn, border_radius=12)
            draw.rect(screen, (180, 0, 0), exit_btn, border_radius=12)

            draw.rect(screen, (255, 255, 255), input_box, 2, border_radius=8)

            screen.blit(font_btn.render("ГРАТИ", True, (0, 0, 0)),
                        font_btn.render("ГРАТИ", True, (0, 0, 0)).get_rect(center=play_btn.center))
            screen.blit(font_btn.render("НАЛАШТУВАННЯ", True, (0, 0, 0)),
                        font_btn.render("НАЛАШТУВАННЯ", True, (0, 0, 0)).get_rect(center=settings_btn.center))
            screen.blit(font_btn.render("ВИХІД", True, (0, 0, 0)),
                        font_btn.render("ВИХІД", True, (0, 0, 0)).get_rect(center=exit_btn.center))

            screen.blit(font_input.render("Ім'я гравця:", True, (255, 255, 255)), (100, 370))
            screen.blit(font_input.render(input_text, True, (255, 255, 255)), (110, 410))

            for e in event.get():
                if e.type == QUIT:
                    quit()

                if e.type == MOUSEBUTTONDOWN:
                    if play_btn.collidepoint(e.pos):
                        clicksound.play()
                        return input_text, backgroundskin, turnonmusic

                    if exit_btn.collidepoint(e.pos):
                        quit()

                    if settings_btn.collidepoint(e.pos):
                        clicksound.play()
                        mode = "Settings"

                    if input_box.collidepoint(e.pos):
                        clicksound.play()
                        active_input = True
                    else:
                        active_input = False

                if e.type == KEYDOWN and active_input:
                    if e.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 13:
                        clicksound.play()
                        input_text += e.unicode

            display.update()
        elif mode == "Settings":
            screen.fill((60, 60, 60))

            title = font_title.render("НАЛАШТУВАННЯ", True, (180, 50, 0))
            screen.blit(title, title.get_rect(center=(WIDTH / 2, 40)))

            exitsettings_btn = Rect(100, 100, 300, 70)

            skin1_btn = Rect(100, 225, 150, 70)
            skin2_btn = Rect(250, 225, 150, 70)
            skin3_btn = Rect(100, 300, 150, 70)
            skin4_btn = Rect(250, 300, 150, 70)

            volume_btn = Rect(150, 400, 200, 70)

            draw.rect(screen, (180, 80, 0), exitsettings_btn, border_radius=12)

            draw.rect(screen, (150, 10, 150), skin1_btn, border_radius=12)
            draw.rect(screen, (0, 150, 10), skin2_btn, border_radius=12)
            draw.rect(screen, (100, 120, 30), skin3_btn, border_radius=12)
            draw.rect(screen, (0,0,0), skin4_btn, border_radius=12)

            if turnonmusic == True:
                draw.rect(screen, (150, 0, 0), volume_btn, border_radius=12)
            else:
                draw.rect(screen, (0, 150, 0), volume_btn, border_radius=12)

            screen.blit(font_btn.render("ПОВЕРНУТИСЯ", True, (0, 0, 0)),
                        font_btn.render("ПОВЕРНУТИСЯ", True, (0, 0, 0)).get_rect(center=exitsettings_btn.center))

            screen.blit(font_btn.render("1", True, (0, 0, 0)),
                        font_btn.render("1", True, (0, 0, 0)).get_rect(center=skin1_btn.center))
            screen.blit(font_btn.render("2", True, (0, 0, 0)),
                        font_btn.render("2", True, (0, 0, 0)).get_rect(center=skin2_btn.center))
            screen.blit(font_btn.render("3", True, (0, 0, 0)),
                        font_btn.render("3", True, (0, 0, 0)).get_rect(center=skin3_btn.center))
            screen.blit(font_btn.render("4", True, (255,255,255)),
                        font_btn.render("4", True, (255,255,255)).get_rect(center=skin4_btn.center))
            if turnonmusic == True:
                screen.blit(font_btn.render("ВИКЛЮЧИТИ", True, (0, 0, 0)),
                            font_btn.render("ВИКЛЮЧИТИ", True, (0, 0, 0)).get_rect(center=volume_btn.center))
            else:
                screen.blit(font_btn.render("УВІМКНУТИ", True, (0, 0, 0)),
                            font_btn.render("УВІМКНУТИ", True, (0, 0, 0)).get_rect(center=volume_btn.center))

            screen.blit(font_input.render("Вигляд мапи:", True, (255, 255, 255)), (100, 175))
            screen.blit(font_input.render(backgroundskin, True, (255, 255, 255)), (340, 175))

            tc = 0, 150, 0
            tt = "Аудіо: Увімкнено"
            if turnonmusic == False:
                tc = 150, 0, 0
                tt = "Аудіо: Вимкнено"

            screen.blit(font_input.render(tt, True, tc), (100, 370))

            for e in event.get():
                if e.type == QUIT:
                    quit()

                if e.type == MOUSEBUTTONDOWN:
                    if exitsettings_btn.collidepoint(e.pos):
                        clicksound.play()
                        mode = "Main"

                    if skin1_btn.collidepoint(e.pos):
                        clicksound.play()
                        backgroundskin = "1"
                    if skin2_btn.collidepoint(e.pos):
                        clicksound.play()
                        backgroundskin = "2"
                    if skin3_btn.collidepoint(e.pos):
                        clicksound.play()
                        backgroundskin = "3"
                    if skin4_btn.collidepoint(e.pos):
                        clicksound.play()
                        backgroundskin = "4"

                    if volume_btn.collidepoint(e.pos):
                        clicksound.play()
                        if turnonmusic == True:
                            turnonmusic = False
                        else:
                            turnonmusic = True

            display.update()


