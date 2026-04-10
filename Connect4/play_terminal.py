from Connect4.AI_cpu.agent import QLearningAgent
from Connect4.AI_cpu.game_logic import (CPU_PIECE, PLAYER_PIECE, check_winner, create_board, drop_piece,
                                        get_valid_moves, is_valid_move, print_board, convert_board)
from Connect4.AI_cpu.train_data import DEFAULT_ALPHA, DEFAULT_GAMMA, QTABLE_FILES
from Connect4.AI_cpu.config import get_epsilon

DIFFICULTY_NAMES = {
    "1": "easy",
    "2": "normal",
    "3": "hard",
}


def play_menu():
    while True:
        print("\n=== Select Difficulty ===")
        print("1) Easy")
        print("2) Normal")
        print("3) Hard")
        print("4) Return")
        choice = input("Choose a difficulty: ").strip()

        if choice == "4":
            return
        if choice in DIFFICULTY_NAMES:
            play_vs_cpu(DIFFICULTY_NAMES[choice])
        else:
            print("<Invalid option>")

def play_vs_cpu(difficulty):
    epsilon = get_epsilon()
    agent = QLearningAgent(DEFAULT_ALPHA, DEFAULT_GAMMA, epsilon)
    load_table = agent.load_q_table(QTABLE_FILES[difficulty])
    if not load_table:
        print(f"Error: Could not load {difficulty} Q-table.")
        return
    agent.set_epsilon(epsilon)
    board = create_board()
    player_turn = True
    print(f"\nStarting game vs {difficulty.upper()} CPU")

    while True:
        print_board(board)
        if player_turn:
            try:
                col = int(input("Choose a column (0-6): ").strip())
            except ValueError:
                print("Please enter a valid number.")
                continue
            if not is_valid_move(board, col):
                print("Please enter a valid number.")
                continue

            drop_piece(board, col, PLAYER_PIECE)
            if check_winner(board, PLAYER_PIECE):
                print_board(board)
                print("You win!")
                return

        else:
            valid_moves = get_valid_moves(board)
            state = convert_board(board)
            col = agent.choose_action(state, valid_moves)
            drop_piece(board, col, CPU_PIECE)
            print(f"CPU chose column {col}.")
            if check_winner(board, CPU_PIECE):
                print_board(board)
                print("CPU wins!")
                return

        if not get_valid_moves(board):
            print_board(board)
            print("Draw!")
            return

        player_turn = not player_turn
