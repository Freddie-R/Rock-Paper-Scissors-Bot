import pickle
import random
import time

time_running = 1800

# Function to load all lists from the file
def load_all_lists():
    lists = []
    try:
        with open('past_games.pkl', 'rb') as file:
            while True:  # Continue until EOFError is raised
                lists.append(pickle.load(file))
    except EOFError:
        pass  # End of file reached
    return lists

# Retrieve and print all lists
loaded_lists = load_all_lists()

print("There are", len(loaded_lists), "sets to learn of")

def pick_move(rounds, past_moves, test_value_1, test_value_2, test_value_3):

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
                rock_likleyhood += (test_value_1 * ((i + 1) / rounds))
            elif past_moves[i] == "paper":
                paper_likleyhood += (test_value_1 * ((i + 1) / rounds))
            else:
                scissors_likleyhood += (test_value_1 * ((i + 1) / rounds))
        
        for depth in range(2,rounds):
            if rounds >= depth+1:
                latest_moves  = get_last_moves(depth, past_moves)
                temp_list = []
                for i in range(len(past_moves)):
                    if not (i >= depth+1):
                        temp_list.append(past_moves[i])
                    else:
                        temp_list.pop(0)
                        temp_list.append(past_moves[i])
                        
                        if temp_list[0:depth] == latest_moves:
                            if temp_list[depth] == "rock":
                                rock_likleyhood += ((test_value_2 * (depth - 1)) * (((i + 1) / rounds) * test_value_3))
                            elif temp_list[depth] == "paper":
                                paper_likleyhood += ((test_value_2 * (depth - 1)) * (((i + 1) / rounds) * test_value_3))
                            else:
                                scissors_likleyhood += ((test_value_2 * (depth - 1)) * (((i + 1) / rounds) * test_value_3))
    #return counter
    if rock_likleyhood > paper_likleyhood and rock_likleyhood > scissors_likleyhood:
        return "paper"
    elif paper_likleyhood > scissors_likleyhood:
        return "scissors"
    else:
        return "rock"

def get_last_moves(count, past_moves):

    latest_moves  = []
    for i in range(len(past_moves)-count,len(past_moves)):
        latest_moves.append(past_moves[i])

    return latest_moves

def get_wins(test_value_1, test_value_2, test_value_3):
    bot_wins = 0
    rounds = 0

    for set in loaded_lists:
        value = test_set(test_value_1, test_value_2, test_value_3, set)
        bot_wins += value[0]
        rounds += value[1]

    return bot_wins, rounds

def test_set(test_value_1, test_value_2, test_value_3, set):
    bot_wins = 0
    past_moves = []
    rounds = 0
    for i in range(len(set)):
        player_move = set[i]
        bot_move = pick_move(i, past_moves, test_value_1, test_value_2, test_value_3)
        value = check_win(player_move, bot_move)
        bot_wins += value[0]
        rounds += value[1]
        past_moves.append(player_move)

    return [bot_wins, rounds]

def check_win(player_move, bot_move):
    if player_move == bot_move: return [0,0]
    if player_move == "rock":
        if bot_move == "paper": return [1,1]
        else: 
            return [0,1]
    if player_move == "paper":
        if bot_move == "rock": 
            return [0,1]
        else: return [1,1]
    if bot_move == "rock": return [1,1]
    return [0,1]

start_time = time.time()

list_of_runs = []

while True:
    #run for 2 minuits
    current_time = time.time()
    if current_time - start_time > time_running:
        print("Done")
        break
    
    test_value_1 = random.uniform(-1, 1)
    test_value_2 = random.uniform(-1, 1)
    test_value_3 = random.uniform(-1, 1)
    win_count, rounds = get_wins(test_value_1, test_value_2, test_value_3)
    list_of_runs.append([test_value_1, test_value_2, test_value_3, win_count, rounds])

list_of_runs.sort(key=lambda x: x[3])

for i in list_of_runs:
    print(i[0:3], "It won", i[3],"/",i[4], " With a winrate of: ", "{:.2f}".format(((i[3] / i[4]) * 100)),"%")

