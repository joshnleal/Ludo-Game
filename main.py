import random
import os
import file_saver as fs
import board_printer as bp


PAWNS_PER_PLAYER = 4
MIN_PLAYERS = 2
MAX_PLAYERS = 4
COLORS = ["red", "green", "yellow", "black"]
BOARD_SIZE = 40
START_SQUARE = 'starting_square'
APP = 'active_pawn_positions'

    
def main():
    print('*** Mensch ärgere Dich nicht ***')
    available_colors = COLORS[:]
    if fs.check_existing_game():
       players = fs.load_existing_game()
       print("Last session restored.")
    else:
        num_of_players = read_players()
        players = create_players(num_of_players, available_colors)
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
            num_of_players = int(input("With how many players would you like to play [2-4]: "))
            if  MIN_PLAYERS <= num_of_players <= MAX_PLAYERS:
                return num_of_players
            print(f"Input invalid. Enter a number betwee {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Input invalid. Input a digit.")


def create_players(num_of_players, available_colors):
    """The player chooses their color and stores the color and other info into a dictionary. Returns the players' info as a list of dictionaries."""
    player_info = []
    for i in range(num_of_players):
        while True:
            player_color = input(f"Choose a color for player #{i + 1} {available_colors}: ").lower()
            if player_color in available_colors:
                generic_start = {
                                "color": player_color,
                                "starting_square": i * 10,
                                'active_pawn_positions': [], 
                                "pawns_available": PAWNS_PER_PLAYER, 
                                "pawns_home": 0, 
                                }
                player_info.append(generic_start)
                available_colors.remove(player_color)
                break
            print("Invalid color! Please select one of the available colors.")
    return player_info


def roll_dice(player):
    """Rolls a six-sided dice. Returns the value of the dice."""
    print(f"\nPlayer {player['color']}")
    while True:
        key = input("Press enter to roll the dice...")
        if key == "":
            dice = random.randint(1, 6)
            print(f"You rolled: {dice}!")
            return dice
        print("Just press Enter.")


def give_start(player, players, dice):
    """Places player's pawn in start position. Returns boolean values."""
    if dice < 6:
        return False
    elif dice == 6 and player['pawns_available'] == 0:
        return False
    elif dice == 6 and player[START_SQUARE] in player[APP]:
        return True
    else:
        if player['pawns_available'] == 0:
            return False
        else:
            new_pos = player[START_SQUARE]
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
        new_pos = new_pos % BOARD_SIZE
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
            if player[APP][index] == (player[START_SQUARE]):
                player[APP].pop()
                player['pawns_available'] += 1     
            else:
                player[APP].pop(index)
                player['pawns_available'] += 1     
            return True
    return False


def check_home_pos(player, players, dice, new_pos):  
    if new_pos == player[START_SQUARE]:
        player['pawns_home'] += 1
        player[APP].remove(new_pos)
        print("Pawn has arrived home!")
        return True
    else: 
        pass


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
        player_initials.append(player['color'][0])
    return player_initials


if __name__ == "__main__":   
    main()