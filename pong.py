import pygame
import os
from button import Button
pygame.font.init()
pygame.display.init()
pygame.mixer.init()

size = pygame.display.get_desktop_sizes()
flags = pygame.FULLSCREEN | pygame.SCALED
WINDOW = pygame.display.set_mode((size[0]), flags)

WIDTH, HEIGHT = WINDOW.get_width(), WINDOW.get_height()

BUTTON_WIDTH, BUTTON_HEIGHT = 178, 46
NORMAL_BUTTON_W, NORMAL_BUTTON_H = WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2 + 100
HARD_BUTTON_W, HARD_BUTTON_H = WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2 + 200
EXIT_BUTTON_W, EXIT_BUTTON_H = WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 - BUTTON_HEIGHT//2 + 300

PADDLE_WIDTH, PADDLE_HEIGHT = 25, 150
BALL_WIDTH, BALL_HEIGHT = 25, 25

WHITE = (255, 255, 255)
GREEN = (57, 255, 20)

FPS = 60
VEL = 15
COM_VEL = 11

background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))
normal_button_img = pygame.image.load(os.path.join("Assets", "normal_button.png"))
normal_button_pressed_img = pygame.image.load(os.path.join("Assets", "normal_button_pressed.png"))
hard_button_img = pygame.image.load(os.path.join("Assets", "hard_button.png"))
hard_button_pressed_img = pygame.image.load(os.path.join("Assets", "hard_button_pressed.png"))
exit_button_img = pygame.image.load(os.path.join("Assets", "exit_button.png"))
exit_button_pressed_img = pygame.image.load(os.path.join("Assets", "exit_button_pressed.png"))
icon = pygame.image.load(os.path.join("Assets", "paddle_icon.png"))

pygame.display.set_icon(icon)

table = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "table2.png")), (WIDTH, HEIGHT)).convert_alpha()
paddle = pygame.image.load(os.path.join("Assets", "paddle.png")).convert_alpha()

paddle_sound = pygame.mixer.Sound(os.path.join("Assets", "paddle_hit.wav"))
paddle_sound.set_volume(.1)

title_font = pygame.font.SysFont("Impact", 200)
score_font = pygame.font.SysFont("Impact", 100)
subtitle_font = pygame.font.SysFont("Impact", 20)


normal_button = Button(normal_button_img, NORMAL_BUTTON_W, NORMAL_BUTTON_H, normal_button_pressed_img)
hard_button = Button(hard_button_img, HARD_BUTTON_W, HARD_BUTTON_H, hard_button_pressed_img)
exit_button = Button(exit_button_img, EXIT_BUTTON_W, EXIT_BUTTON_H, exit_button_pressed_img)



def main():

    while True:
        hard_mode = menu()
        pygame.mouse.set_visible(False)
        if hard_mode:
            global COM_VEL
            COM_VEL = 15
        elif not hard_mode:
            COM_VEL = 11

        player_score = 0
        computer_score = 0
        end_loop = 0
        
        player = pygame.Rect((WIDTH//16, HEIGHT//2 - PADDLE_HEIGHT//2), (PADDLE_WIDTH, PADDLE_HEIGHT))
        computer = pygame.Rect((((WIDTH//16) * 15) - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2), (PADDLE_WIDTH, PADDLE_HEIGHT))
        ball = pygame.Rect((WIDTH//2, HEIGHT//2), (BALL_WIDTH, BALL_WIDTH))
        
        BALL_VEL_X, BALL_VEL_Y = 10, 0

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        run = False
                    if event.key == pygame.K_ESCAPE:
                        back = pause()
                        if back:
                            run = False

            if ball.x < 0 or ball.x > WIDTH:
                if ball.x < 0:
                    computer_score += 1
                elif ball.x > WIDTH:
                    player_score += 1
                BALL_VEL_X, BALL_VEL_Y = reset_ball(ball, player, computer)

            if player_score >= 11 and player_score - computer_score >= 2:
                if end_loop == 1:
                    draw_end_screen("PLAYER WINS!")
                    break
                elif end_loop != 1:
                    end_loop += 1
            elif computer_score >= 11 and computer_score - player_score >= 2:
                if end_loop == 1:
                    draw_end_screen("COMPUTER WINS!")
                    break
                elif end_loop != 1:
                    end_loop += 1

                

            keys_pressed = pygame.key.get_pressed()
            handle_player_movement(keys_pressed, player)
            handle_computer_movement(computer, ball,  BALL_VEL_X)

            BALL_VEL_X, BALL_VEL_Y = handle_ball(player, computer, ball, BALL_VEL_X, BALL_VEL_Y, hard_mode)
            draw_scene(player, computer, ball, player_score, computer_score)



def draw_scene(player, computer, ball, player_score, computer_score):
    space = 140
    WINDOW.blit(table, (0, 0))
    #WINDOW.fill((0,0,0))

    p_score = score_font.render(f"{player_score}", 1, WHITE)
    WINDOW.blit(p_score, ((WIDTH//2 - p_score.get_width()/2) - space, 0))
    c_score = score_font.render(f"{computer_score}", 1, WHITE)
    WINDOW.blit(c_score, ((WIDTH//2 - c_score.get_width()/2) + space, 0))

    WINDOW.blit(paddle, (player.x, player.y))
    WINDOW.blit(paddle, (computer.x, computer.y))
    pygame.draw.rect(WINDOW, WHITE, ball)

    pygame.display.update()



def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_w] and (player.y - VEL) > 0:
        player.y -= VEL
    if keys_pressed[pygame.K_s] and (player.y + VEL) < (HEIGHT - PADDLE_HEIGHT):
        player.y += VEL



def handle_computer_movement(computer, ball, BALL_VEL_X):
    if (ball.y + ball.h/2) < (computer.y + computer.h/2) and (computer.y - COM_VEL > 0) and (BALL_VEL_X > 0 and ball.x > (WIDTH//2)):
        computer.y -= COM_VEL
    if (ball.y + ball.h/2) > (computer.y + computer.h/2) and (
        computer.y + COM_VEL < (HEIGHT - PADDLE_HEIGHT)) and (BALL_VEL_X > 0 and ball.x > (WIDTH//2)):
        computer.y += COM_VEL
    if BALL_VEL_X < 0 and ((computer.y + computer.h/2) < (HEIGHT//2)):
        computer.y += COM_VEL
    if BALL_VEL_X < 0 and ((computer.y + computer.h/2) > (HEIGHT//2)):
        computer.y -= COM_VEL
        


def handle_ball(player, computer, ball, BALL_VEL_X, BALL_VEL_Y, hard_mode):
    ball.x += BALL_VEL_X
    ball.y += BALL_VEL_Y
    #handle top and bottom of the screen
    if ball.y + BALL_VEL_Y > (HEIGHT - BALL_HEIGHT):
        BALL_VEL_Y = (BALL_VEL_Y * -1) - 1
    if ball.y + BALL_VEL_Y < 0:
        BALL_VEL_Y = (BALL_VEL_Y * -1) + 1
    #handle paddle collisions
    if player.colliderect(ball):
        paddle_sound.play()
        BALL_VEL_X = (BALL_VEL_X * -1) + 1
        BALL_VEL_Y = BALL_VEL_Y + set_y_vel(player, ball)

    if computer.colliderect(ball):
        paddle_sound.play()
        BALL_VEL_X = (BALL_VEL_X * -1) - 1
        BALL_VEL_Y = BALL_VEL_Y + set_y_vel(computer, ball)
    #print(BALL_VEL_X, BALL_VEL_Y)
    BALL_VEL_X, BALL_VEL_Y = cap_ball_vel(BALL_VEL_X, BALL_VEL_Y, hard_mode)
    return BALL_VEL_X, BALL_VEL_Y
    


def reset_ball(ball, player, computer):
    computer.y = HEIGHT//2 - PADDLE_HEIGHT//2
    player.y = HEIGHT//2 - PADDLE_HEIGHT//2
    if ball.x < 0:
        ball_vel_x = 10
        ball.x, ball.y = (player.x + PADDLE_WIDTH) + 1, HEIGHT//2 - ball.h/2
    elif ball.x > WIDTH:
        ball_vel_x = -10
        ball.x, ball.y = computer.x - ball.w - 1, HEIGHT//2 - ball.h/2
    
    return ball_vel_x, 0



def set_y_vel(paddle, ball):
    if (ball.y + ball.h//2) - paddle.y <= 25:
        BALL_VEL_Y = -5
    elif (ball.y + ball.h//2) - paddle.y <= 50:
        BALL_VEL_Y = -3
    elif (ball.y + ball.h//2) - paddle.y <=75:
        BALL_VEL_Y = -1
    elif (ball.y + ball.h//2) - paddle.y <= 100:
        BALL_VEL_Y = 1
    elif (ball.y + ball.h//2) - paddle.y <= 125:
        BALL_VEL_Y = 3
    elif (ball.y + ball.h//2) - paddle.y <= 150:
        BALL_VEL_Y = 5
    elif (ball.y + ball.h//2) - paddle.y > 150:
        BALL_VEL_Y = 5
    
    return BALL_VEL_Y



def cap_ball_vel(ball_vel_x, ball_vel_y, hard_mode):
    if hard_mode == False:
        if ball_vel_x > 15:
            ball_vel_x = 15
        elif ball_vel_x < -15:
            ball_vel_x = -15

        if ball_vel_y > 15:
            ball_vel_y = 15
        elif ball_vel_y < -15:
            ball_vel_y = -15

    elif hard_mode == True:
        if ball_vel_x > 20:
            ball_vel_x = 20
        elif ball_vel_x < -20:
            ball_vel_x = -20

        if ball_vel_y > 20:
            ball_vel_y = 20
        elif ball_vel_y < -20:
            ball_vel_y = -20
    
    return ball_vel_x, ball_vel_y



def draw_end_screen(text):
    end_text = score_font.render(text, 1, GREEN)
    WINDOW.blit(end_text, ((WIDTH//2 - end_text.get_width()//2), (HEIGHT//2 - end_text.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(3000)



def pause():
    clock = pygame.time.Clock()
    back = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_BACKSPACE:
                    back = True
                    run = False
        
        text = score_font.render("PAUSED.", 1, GREEN)
        text2 = score_font.render("PRESS ESC TO UNPAUSE.", 1, GREEN)
        WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 150))
        WINDOW.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2))
        pygame.display.update()
    return back




def menu():
    clock = pygame.time.Clock()
    pygame.mixer.music.load(os.path.join("Assets", "menu_music.mp3"))
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)
    play_clicked = True
    pygame.mouse.set_visible(True)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        if exit_button.clicked == True:
            exit_button.clicked = False
            run = False
            pygame.quit()
        if normal_button.clicked == True and play_clicked == False:
            normal_button.clicked = False
            hard = False
            run = False
        if hard_button.clicked == True and play_clicked == False:
            hard = True
            run = False

        WINDOW.blit(background, (0, 0))
        normal_button.draw(WINDOW)
        hard_button.draw(WINDOW)
        exit_button.draw(WINDOW)
        title = title_font.render("PONG", 1, WHITE)
        WINDOW.blit(title, (WIDTH//2 - title.get_width()/2, HEIGHT//2 - title.get_height()/2 - 200))
        subtitle = subtitle_font.render("PRESS ESC AT ANY TIME TO PAUSE.", 1, WHITE)
        WINDOW.blit(subtitle, (WIDTH//2 - subtitle.get_width()/2, HEIGHT//2 - subtitle.get_height()/2 - 20))
        subtitle2 = subtitle_font.render("PRESS BACKSPACE AT ANY TIME TO RETURN TO MENU.", 1, WHITE)
        WINDOW.blit(subtitle2, (WIDTH//2 - subtitle2.get_width()/2, HEIGHT//2 - subtitle2.get_height()/2 + 15))

        pygame.display.update()
        if play_clicked == True:
            play_clicked = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load(os.path.join("Assets", "game_music.mp3"))
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1, fade_ms=500)
    return hard



if __name__ == "__main__":
    main()