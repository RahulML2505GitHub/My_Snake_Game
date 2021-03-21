import pygame
import random
import os

pygame.mixer.init()

pygame.init()



# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (50, 50, 50)
violet = (135, 130, 232)

# Creating window
screen_width = 750
screen_height = 850
screen_WHalf = screen_width*(0.5)
screen_HHalf = screen_height*(0.5)
gameWindow = pygame.display.set_mode((screen_width-200, screen_height))

#Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Mr_Snake🐍")
pygame.display.update()
clock = pygame.time.Clock()



def text_screen(text, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((232, 181, 214))
        text_screen("Welcome to Snakes", red, 100, 250, 80)
        Font = pygame.font.SysFont(None, 40)
        Pe = "Press Space Bar To Play"
        screentextPe = Font.render( Pe, True, gray)
        gameWindow.blit(screentextPe, [200,700])
       # text_screen("Press Space Bar To Play", black, 150, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if hiscore file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_WHalf)
    food_y = random.randint(20, screen_HHalf)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 30
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            text_screen("Game Over!", red, 240, 250, 60)
            Font = pygame.font.SysFont(None, 35)
            PE = "Press Enter To Continue"
            screentextPE = Font.render( PE, True, gray)
            gameWindow.blit(screentextPE, [220,300])
            text_screen(f"High Score: {hiscore}   Your Score: {score}", black, 100, 700, 55)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_0:
                        exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        welcome()

        else:

            for event in pygame.event.get():
                # Quit command
                if event.type == pygame.QUIT:
                        exit_game = True

                if event.type == pygame.KEYDOWN:
                    # Quit command by '0'
                    if event.type == pygame.K_0:
                        exit_game = True

                    # Going Right command
                    if event.key == pygame.K_6:
                        velocity_x = init_velocity
                        velocity_y = 0

                    # Going Left command
                    if event.key == pygame.K_4:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    # Going Up command
                    if event.key == pygame.K_2:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    # Going Down command
                    if event.key == pygame.K_8:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Increasing Score ( Cheating ) command
                    if event.key == pygame.K_KP_PLUS:
                        score = score + 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            if score>int(hiscore):
                hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+ str(hiscore), red, 5, 5, 60)
            # Drawing food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            # Drawing snake 🐍 hear
            plot_snake(gameWindow, violet, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
pygame.mixer.music.stop()
welcome()
