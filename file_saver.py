def create_save_file(players):
    SAVE_GAME = "save_file.txt"
    with open(SAVE_GAME, 'w') as s_f:
        save_game(players, s_f)


def save_game(players, s_f):
    """Saves the current session by storing player info into the save file."""
    for player in players: 
        returned_players = []  
        for key, value in player.items(): 
            if key == 'starting_square':
                continue
            elif key == 'active_pawn_positions':
                active_pawns = value
            elif key == 'pawns_available':
                for index,i in enumerate(range(value)):
                    if index + 1 < 4:
                        s_f.write("a" + "/")
                    else:
                        s_f.write("a")
            elif key == 'pawns_home':
                for i in range(value):
                    s_f.write("h" + "/")
            else:
                s_f.write(value + "/")
                continue
        if active_pawns == 0:
            pass
        else:
            for index, pawn in enumerate(active_pawns):
                if index + 1 < len(active_pawns):
                    s_f.write(str(pawn) + "/")
                else:
                    s_f.write(str(pawn))
            s_f.write("\n")


def check_existing_game():
    try:
         with open("save_file.txt") as s_f:
            return True
    except:
        return False


def load_existing_game():
    """When existing save file found, creates a dictionary of the players current info. Returns list of dictionaries."""
    player_info = []
    with open("save_file.txt") as s_f:
        for i, line in enumerate(s_f):
            line = line.rstrip("\n")
            line = line.split("/")
            generic_start = {"color": "",
                            "starting_square": i * 10,
                            'active_pawn_positions': [], 
                            "pawns_available": 0, 
                            "pawns_home": 0, 
                            }
            for index, item in enumerate(line):
                if index == 0:
                    generic_start['color'] = item
                elif item == "a":
                    generic_start['pawns_available'] += 1
                elif item == "h":
                    generic_start['pawns_home'] += 1
                elif item == "":
                    continue
                else:
                    generic_start['active_pawn_positions'].append(int(item))
            player_info.append(generic_start)
        return player_info
