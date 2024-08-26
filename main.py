import pygame
import time
import random
import math
from scipy.stats import norm

pygame.font.init()

#Define Screen Value
SCREEN_WIDTH = 1200
SCREEN_HIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
pygame.display.set_caption("Rock, Paper, Scissors Bot")
font = pygame.font.SysFont(None, 40)

#Define Colours
BG_colour = (130, 212, 232)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gray = (192, 192, 192)

#Define Varibles
clicked = False
past_moves = []
rounds = 0
bot_wins = 0
player_wins = 0
bot_p_win_num = "0.00"
player_p_win_num = "0.00"
expected_win_rate = 1/3
bot_chance = "100.00"

#Create Images and Text
image_rock = pygame.image.load("rock.png")
image_rock = pygame.transform.scale(image_rock, (250,250))
image_rock_rect = image_rock.get_rect()
image_rock_rect.topleft = (100, 50)

image_paper = pygame.image.load("paper.png")
image_paper = pygame.transform.scale(image_paper, (250,250))
image_paper_rect = image_paper.get_rect()
image_paper_rect.topleft = (475, 50)

image_scissors = pygame.image.load("scissors.png")
image_scissors = pygame.transform.scale(image_scissors, (250,250))
image_scissors_rect = image_scissors.get_rect()
image_scissors_rect.topleft = (850, 50)

def create_display(state):

    #Set Screen Backgroud
    if state == "win":
        screen.fill(green)
    elif state == "lose":
        screen.fill(red)
    elif state == "draw":
        screen.fill(gray)
    else:
        screen.fill(BG_colour)

    #Print Images
    screen.blit(image_rock, image_rock_rect)
    screen.blit(image_paper, image_paper_rect)
    screen.blit(image_scissors, image_scissors_rect)

    #Print outline for images
    size = 250
    create_square((100,50),size,5, "Rock")
    create_square((SCREEN_WIDTH-100-size,50),size,5, "Paper")
    create_square(((SCREEN_WIDTH - size) //2,50),size,5, "Scissors")

    #Print text
    rounds_text = "Rounds: " + str(rounds)
    rounds_img = font.render(rounds_text, True, black)
    screen.blit(rounds_img, (100, 320))

    bot_p_win_text = "Bot % winrate: " + str(bot_p_win_num) + "%"
    bot_p_win_img = font.render(bot_p_win_text, True, black)
    screen.blit(bot_p_win_img, (100, 370))

    player_p_win_text = "Player % winrate: " + str(player_p_win_num) + "%"
    player_p_win_img = font.render(player_p_win_text, True, black)
    screen.blit(player_p_win_img, (700, 370))

    bot_chance_text = "Two Tailed Test Chance: " + str(bot_chance) + "%"
    bot_chance_img = font.render(bot_chance_text, True, black)
    screen.blit(bot_chance_img, (100, 420))

def win_rate_test():
    global rounds
    global bot_wins

    #null hypothosis
    global expected_win_rate

    #Observed win rate
    observed_win_rate = bot_wins / rounds

    #Standered error of the proportion
    standard_error = math.sqrt((expected_win_rate * (1 - expected_win_rate)) / rounds)

    #Calculate the z-statistic
    z_score = (observed_win_rate - expected_win_rate) / standard_error

    #Two tailed test: Caculate p-value
    p_value = 200 * (1 - norm.cdf(abs(z_score)))

    return p_value

def effect(state):
    global bot_wins
    global player_wins

    if state == "win":
        create_display("win")
        player_wins += 1
        
    elif state == "lose":
        create_display("lose")
        bot_wins += 1
    else:
        create_display("draw")
    pygame.display.update()
    time.sleep(0.1)

def create_square(top_right_corner,size,width,thing):
    pygame.draw.line(screen,black,top_right_corner,(top_right_corner[0]+size,top_right_corner[1]),width)
    pygame.draw.line(screen,black,top_right_corner,(top_right_corner[0],top_right_corner[1]+size),width)
    pygame.draw.line(screen,black,(top_right_corner[0]+size,top_right_corner[1]),(top_right_corner[0]+size,top_right_corner[1]+size),width)
    pygame.draw.line(screen,black,(top_right_corner[0],top_right_corner[1]+size),(top_right_corner[0]+size,top_right_corner[1]+size),width)
    #print("===",thing,"===")
    #print("Top: ", top_right_corner[1])
    #print("Bottom: ", top_right_corner[1] + size)
    #print("Left: ", top_right_corner[0])
    #print("Right: ", top_right_corner[0] + size)
    
def get_move_from_location(position):
    cell_x = position[0]
    cell_y = position[1]
    if cell_y >= 50 and cell_y <= 300:
        if cell_x >= 100 and cell_x <= 350:
            return "rock"
        elif cell_x >= 475 and cell_x <= 725:
            return "paper"
        elif cell_x >= 850 and cell_x <= 1100:
            return "scissors"
        else:
            return False
    else:
        return False

def pick_move():
    global past_moves
    global rounds

    #initialise varibles
    rock_likleyhood = 0
    paper_likleyhood = 0
    scissors_likleyhood = 0

    if rounds == 0:
        #on round 0 always play rock as it is most likley
        rock_likleyhood = 1
    else:
        #add 1 points for every time played
        for i in range(len(past_moves)):
            if past_moves[i] == "rock":
                rock_likleyhood += (1 * ((i + 1) / rounds))
            elif past_moves[i] == "paper":
                paper_likleyhood += (1 * ((i + 1) / rounds))
            else:
                scissors_likleyhood += (1 * ((i + 1) / rounds))
        
        for depth in range(2,rounds):
            if rounds >= depth+1:
                latest_moves  = get_last_moves(depth)
                temp_list = []
                for i in range(len(past_moves)):
                    if not (i >= depth+1):
                        temp_list.append(past_moves[i])
                    else:
                        temp_list.pop(0)
                        temp_list.append(past_moves[i])
                        
                        if temp_list[0:depth] == latest_moves:
                            if temp_list[depth] == "rock":
                                rock_likleyhood += ((5 * (depth - 1)) * ((i + 1) / rounds))
                            elif temp_list[depth] == "paper":
                                paper_likleyhood += ((5 * (depth - 1)) * ((i + 1) / rounds))
                            else:
                                scissors_likleyhood += ((5 * (depth - 1)) * ((i + 1) / rounds))
                    



    print("Rock Weight: ", rock_likleyhood)
    print("Paper Weight: ", paper_likleyhood)
    print("Scissors Weight: ", scissors_likleyhood)
    
    #return counter
    if rock_likleyhood > paper_likleyhood and rock_likleyhood > scissors_likleyhood:
        return "paper"
    elif paper_likleyhood > scissors_likleyhood:
        return "scissors"
    else:
        return "rock"
            
def get_last_moves(count):
    global past_moves

    latest_moves  = []
    for i in range(len(past_moves)-count,len(past_moves)):
        latest_moves.append(past_moves[i])

    return latest_moves

Running = True
while Running:
    create_display("Normal")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()

            #Check Location
            player_move = get_move_from_location(pos)


            if player_move == "rock" or player_move == "paper" or player_move == "scissors":
                
                bot_move = pick_move()

                if bot_move == player_move:
                    effect("draw")
                elif player_move == "rock":
                    if bot_move == "scissors": effect("win")
                    else: effect("lose")
                elif player_move == "paper":
                    if bot_move == "rock": effect("win")
                    else: effect("lose")
                else: 
                    if bot_move == "paper": effect("win")
                    else: effect("lose")
                



                #update values
                rounds += 1

                if rounds != 0:
                    bot_p_win_num = "{:.2f}".format(((bot_wins / rounds) * 100))
                    player_p_win_num = "{:.2f}".format(((player_wins / rounds) * 100))
                    
                    bot_chance = "{:.2f}".format(win_rate_test())
                    if bot_chance == "0.00":
                        bot_chance = "{:.5f}".format(win_rate_test())


                past_moves.append(player_move)
                


    pygame.display.update()