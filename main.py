import pygame
import os
pygame.font.init()
pygame.mixer.init()
#drawing the main areas
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceship game by shyskill')

#easy to change variables


BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
BLACK4 =  (0,0,0)


SIUU = pygame.mixer.Sound(os.path.join('Spaceship trap game', 'SIUUAYE.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Spaceship trap game', 'Grenade+1.mp3'))
BULLET_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Spaceship trap game', 'Gun+Silencer.mp3'))
MUSIC = pygame.mixer.Sound(os.path.join('Spaceship trap game', 'Prodbydines_beat.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
MUSIC_FONT = pygame.font.SysFont('sansserif', 30)

FPS = 60
VEL = 5
BULLET_VEL = 7 
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 155, 140


YELLOW = (255 , 255 , 0)
RED = (255 , 0 , 0)
COLORET = (255,255,255)

BLACK_HIT = pygame.USEREVENT + 1
WHITE_HIT = pygame.USEREVENT + 2

SPONGE_IMAGE = pygame.image.load(
    os.path.join('Spaceship trap game', 'sponge-final.png'))


#black ship testing and drawing
BLACK_SHIP_IMAGE = pygame.image.load(
    os.path.join('Spaceship trap game', 'black-ship.png'))
BLACK_SHIP = pygame.transform.rotate(pygame.transform.scale(
    BLACK_SHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT )),180)

SPACE_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Spaceship trap game', 'galaxy.jpg')),  (900, 500))


#white ship testing and drawing
WHITE_SHIP_IMAGE = pygame.image.load(
    os.path.join('Spaceship trap game', 'white-ship.png'))
WHITE_SHIP = pygame.transform.rotate(pygame.transform.scale(
    WHITE_SHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT )),360)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, COLORET)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, 
                        HEIGHT/2 - draw_text.get_height()/2 ))
    pygame.display.update()
    pygame.time.delay(3500)
#window drawer
def draw_window(black, white, black_bullets, white_bullets, white_health, black_health):
    WIN.blit(SPACE_IMAGE, (0,0))
    pygame.draw.rect(WIN, BLACK4, BORDER)
    music_text = MUSIC_FONT.render("Click M to start the music, and N to stop!", 1, COLORET)
    white_health_text = HEALTH_FONT.render("Black Health: " + str(white_health), 1, COLORET)
    black_health_text = HEALTH_FONT.render("White Health: " + str(black_health), 1, COLORET)
    WIN.blit(white_health_text, (WIDTH - black_health_text.get_width() - 10, 10))
    WIN.blit(black_health_text, (10, 10))
    WIN.blit(music_text, (260,60))
    WIN.blit(BLACK_SHIP, (black.x, black.y))
    WIN.blit(WHITE_SHIP, (white.x, white.y))


    for bullet in white_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in black_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#black movement

black_bullets = []
white_bullets = []

def black_handle_movement(keys_pressed, black):
        if keys_pressed[pygame.K_a] and black.x - VEL > 0:  #LEFT KEY BTW
            black.x -= VEL
        if keys_pressed[pygame.K_d] and black.x + VEL + black.width < BORDER.x:  #RIGHT KEY BTW
            black.x += VEL
        if keys_pressed[pygame.K_s] and black.y + VEL + black.height < HEIGHT + 40:  #DOWN KEY BTW
            black.y += VEL
        if keys_pressed[pygame.K_w] and black.y - VEL > -20:  #UP KEY BTW
            black.y -= VEL

#white movement

def white_handle_movement(keys_pressed, white):
        if keys_pressed[pygame.K_LEFT] and white.x - VEL > BORDER.x + BORDER.width:  #LEFT KEY BTW
            white.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and white.x + VEL + white.width < WIDTH:  #RIGHT KEY BTW
            white.x += VEL
        if keys_pressed[pygame.K_DOWN] and white.y + VEL + white.height < HEIGHT + 40:  #DOWN KEY BTW
            white.y += VEL
        if keys_pressed[pygame.K_UP] and white.y - VEL > -20:  #UP KEY BTW
            white.y -= VEL

#if white gets hit

def handle_bullets(black_bullets, white_bullets, black, white):
    for bullet in black_bullets:
        bullet.x += BULLET_VEL
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))
            black_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            black_bullets.remove(bullet)
        
            #if black gets hit
    for bullet in white_bullets:
        bullet.x -= BULLET_VEL
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            white_bullets.remove(bullet)
        elif bullet.x < 0:
            white_bullets.remove(bullet)

#main function (important asf)
def main():
    global main
    black = pygame.Rect(100, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    white = pygame.Rect(700, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    
    black_health = 10
    white_health = 10 

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            #white bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(black_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        black.x + black.width, black.y + black.height/2 - 2, 10, 5)
                    black_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()
             #black bullets
                if event.key == pygame.K_m:
                    MUSIC.play()
                if event.key == pygame.K_n:
                    MUSIC.stop()
                if event.key == pygame.K_RCTRL and len(white_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        white.x, white.y + white.height/2 - 2, 10, 5)
                    white_bullets.append(bullet)
                    BULLET_SHOOT_SOUND.play()

            if event.type == WHITE_HIT:
                white_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BLACK_HIT:
                black_health -= 1
                BULLET_HIT_SOUND.play()

                
        winner_text = ""
        if white_health <= 0:
            winner_text = "White Wins! SEWEY!"
            MUSIC.stop()
            SIUU.play()
        if black_health <= 0:
            winner_text = "Black Wins! SEWEY!"
            MUSIC.stop()       
            SIUU.play()
        if winner_text != "":
            draw_winner(winner_text)
            break
                
        #KEY PRESSING EVENTS YAY! # Black is to yellow as white is to red
        
        keys_pressed = pygame.key.get_pressed()
        black_handle_movement(keys_pressed, black)
        white_handle_movement(keys_pressed, white)

        handle_bullets(black_bullets, white_bullets, black, white)
       
        draw_window(white, black, white_bullets, black_bullets, white_health, black_health)


    main()

if __name__ == "__main__":
    main()

