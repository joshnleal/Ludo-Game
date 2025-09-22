import random, os, file_saver as fs, board_printer as bp
PAWN_COUNT = 4
MIN_PLAYERS = 2
MAX_PLAYERS = 4
COLORS = ["red", "green", "yellow", "black"]
BOARD_SIZE = 40
STRT_SQR = 'starting_square'
APP = 'active_pawn_positions'

    
def main():
    print('*** Mens Erger Je Niet ***')
    temp_colors = COLORS[:]
    if fs.check_existing_game():
       players = fs.load_existing_game()
       print("Last session restored.")
    else:
        num_of_players = read_players()
        players = create_players(num_of_players, temp_colors)
    # old_pos = 50
    color_initials = get_initials(players)
    while True:
        for player in players:
            bp.print_board(players, color_initials, BOARD_SIZE)
            dice = roll_dice(player)
            if not give_start(player, players, dice):
                selection = check_num_pawns(player)
                move_pawn(player, players, dice, selection)
            fs.create_save_file(players)
            if check_win(player):
                bp.print_board(players, color_initials, BOARD_SIZE)
                os.remove("save_file.txt") 
                exit()
            else:
                continue 


def read_players():
    """Ask the user how many players want to participate. Returns the number of players."""
    while True:
        try:
            num_of_players = input("With how many players would you like to play [2-4]: ")
            if not num_of_players.isdigit:
                print("Input not a digit. Try again.")
                continue  
            elif int(num_of_players) > MAX_PLAYERS or int(num_of_players) < MIN_PLAYERS:
                print("Input is invalid. Try again.")
                continue
            else:
                num_of_players = int(num_of_players)
                return num_of_players
        except:
            print("Input invalid. Try again.")


def create_players(num_of_players, temp_colors):
    """Has the player choose their color and stores the color and other info into a dictionary. Returns the players' info as a list of dictionaries."""
    player_info = []
    for i in range(num_of_players):
        while True:
            player_color = input(f"Choose a color for player #{i + 1} {temp_colors}: ").lower()
            if player_color not in temp_colors:
                print("Invalid color!")
                continue
            else:
                for color in temp_colors:
                    if player_color.lower() == color: 
                        generic_start = {
                                        "color": player_color,
                                        "starting_square": i * 10,
                                        'active_pawn_positions': [], 
                                        "pawns_available": PAWN_COUNT, 
                                        "pawns_home": 0, 
                                        }
                        temp_colors.remove(color)
                        player_info.append(generic_start)
                        break
                break
    return player_info


# def display_player(players):
#     print("\nPlayers:")
#     for player_num, player in enumerate(players):
#         print(f"{player_num}. {player['color']} (starting square: {player[STRT_SQR]}, pawns available: {player['pawns_available']}, pawns home: {player['pawns_home']})")
#     return


# def display_gameboard(players, board):
#    """Displays a boring 'board' that shows the board position and the corresponding color to it."""
#     print("\nBoard:")
#     for position in board['square']:
#         for player in players:
#             if position in player[APP]:
#                 print(f"{position}: {player['color']}")
#                 continue
#     return 


def roll_dice(player):
    """Rolls a six-sided dice. Returns the value of the dice."""
    print(f"\nPlayer {player['color']}")
    while True:
        key = input("Press enter to roll the dice...")
        dice = random.randint(1, 6)
        if key == "":
            print(f"You rolled: {dice}!")
            return dice
        else:
            # dice = int(key) - Test code
            print("Try again.")
            continue


def give_start(player, players, dice):
    """Places player's pawn in start position. Returns boolean values."""
    if dice < 6:
        return False
    elif dice == 6 and player['pawns_available'] == 0:
        return False
    elif dice == 6 and player[STRT_SQR] in player[APP]:
        return True
    else:
        if player['pawns_available'] == 0:
            return False
        else:
            new_pos = player[STRT_SQR]
            if not check_collision(players, new_pos):
                player[APP].append(new_pos)
                player['pawns_available'] -= 1
                print("Placing a pawn on the starting square!")
                return True
            else:
                player[APP].append(new_pos)
                player['pawns_available'] -= 1
                return True


def check_num_pawns(player):
    """Moves player's pawn automatically if the player only has one on the board, checks to see if the player has any moveable pawns, and gives the player the option to pick which pawn they want to move (if applicable). Returns the value of selection."""
    if len(player[APP]) > 1:
        while True:
            try:
                selection = input(f"The pawn at which square would you like to move? ({', '.join(str(e) for e in player[APP])}): ")
                if not selection.isdigit():
                    print("Try again.")
                elif int(selection) not in player[APP]:
                    print("Try again.")
                    continue
                else:
                    selection = int(selection)
                    return selection
            except:
                print("Invalid input. Please try again.")
    elif len(player[APP]) == 0:
        print("No moveable pawns.")
        selection = None
        return selection
    else:
        selection = player[APP][0]
        return selection
        

def move_pawn(player, players, dice, selection):
    if selection is None:
        pass
    else:
        index = player.get(APP).index(selection)
        old_pos = player[APP][index]
        new_pos = old_pos + dice
        new_pos = new_pos % 40
        # check_if_passed(new_pos) implement this "someday"
        check_collision(players, new_pos)
        player[APP][index] = new_pos 
        if check_home_pos(player, players, dice, new_pos) == True:
            return 
        else:
            print_movement(old_pos, new_pos)     
            return 


def print_movement(old_pos, new_pos):
    print(f"Pawn moving from {old_pos} to {new_pos}.")


def check_collision(players, new_pos): 
    """Removes a pawn from the board when the current player places a pawn on the same exact spot."""
    for player in players:
        positions = player[APP]
        if new_pos in positions:
            index = positions.index(new_pos)   
            if player[APP][index] == (player[STRT_SQR]):
                player[APP].pop()
                player['pawns_available'] += 1     
            else:
                player[APP].pop(index)
                player['pawns_available'] += 1     
            return True
    return False


def check_home_pos(player, players, dice, new_pos):  
    if new_pos == player[STRT_SQR]:
        player['pawns_home'] += 1
        player[APP].remove(new_pos)
        print("Pawn has arrived home!")
        return True
    else: 
        pass


# def check_if_passed(home):
    # if home > player[STRT_SQR] and player[STRT_SQR] % home < 0:
    #     print("Pawn would go past home.")
    #     return 
    # else:
    #     pass


def check_win(player):
    if player['pawns_home'] == 4:
        print(f"Player {player['color']} has won the game!")
        return True
    else:
        return False


def get_initials(players):
    """Get the initials of each player's color"""
    player_initials = []
    for player in players:
        for index, letter in enumerate(player['color']):
            if index == 0:
                player_initials.append(letter)
            else:
                continue
    return player_initials
    
    
main()