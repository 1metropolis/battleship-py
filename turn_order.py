import random 
def choose_starting_player(player1, player2):
    """
    Randomly choose which player goes first.
    Returns (current_player, waiting_player).
    """
    # Randomly pick 1 or 2 to decide who starts
    starter_number = random.randint(1, 2)

    print("Deciding who will go first...")
    print(f"Random generator picked the number: {starter_number}")

    if starter_number == 1:
        current_player = player1
        waiting_player = player2
    else:
        current_player = player2
        waiting_player = player1

    print(f">>> {current_player['name']} has been chosen to go first! <<<\n")
    return current_player, waiting_player