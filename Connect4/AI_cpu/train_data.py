import json
import os
import random
from Connect4.AI_cpu.agent import QLearningAgent
from Connect4.AI_cpu.game_logic import (CPU_PIECE, PLAYER_PIECE, check_winner, create_board,
                                        drop_piece, get_winning_moves, get_valid_moves, is_draw, convert_board)
from pathlib import Path

DEFAULT_ALPHA = 0.1
DEFAULT_GAMMA = 0.9
DEFAULT_EPSILON = 0.1

BASE_DIR = Path(__file__).resolve().parent.parent
QTABLE_DIR = BASE_DIR/"Data"/"Qtables"
QTABLE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = BASE_DIR/"Data"/"Reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

DIFFICULTY_REWARDS = {
    "easy": {"win":1.0, "lose":-1.0, "draw":0.0, "block":0.0},
    "normal": {"win":1.5, "lose":-2.0, "draw":0.5, "block":1.0},
    "hard": {"win":2.0, "lose":-3.0, "draw":1.0, "block":1.5},
}

QTABLE_FILES = {
    "easy": str(QTABLE_DIR/"qtable_easy.json"),
    "normal": str(QTABLE_DIR/"qtable_normal.json"),
    "hard": str(QTABLE_DIR/"qtable_hard.json"),
}

def qtables_exist():
    missing = [name for name, path in QTABLE_FILES.items() if not os.path.exists(path)]
    if not missing:
        return
    print("Missing q-table files, training CPU using default values")
    for difficulty in missing:
        agent = QLearningAgent(DEFAULT_ALPHA, DEFAULT_GAMMA, DEFAULT_EPSILON)
        train_agent(agent, difficulty, 10000)
        agent.save_q_table(QTABLE_FILES[difficulty])

def train_agent(agent, difficulty, times):
    rewards = DIFFICULTY_REWARDS[difficulty]
    for _ in range(times):
        board = create_board()
        done = False

        if times%2 == 0:
            opponent_valid_moves = get_valid_moves(board)
            opponent_action = random.choice(opponent_valid_moves)
            drop_piece(board, opponent_action, PLAYER_PIECE)
            if check_winner(board, PLAYER_PIECE):
                done = True

        while not done:
            valid_moves = get_valid_moves(board)
            if not valid_moves:
                break

            state = convert_board(board)
            threat_before_turn = set(get_winning_moves(board, PLAYER_PIECE))
            action = agent.choose_action(state, valid_moves)
            drop_piece(board, action, CPU_PIECE)
            reward = 0.0

            if check_winner(board, CPU_PIECE):
                reward += rewards["win"]
                next_state = convert_board(board)
                agent.update_q_value(state, action, reward, next_state, [], True)
                done = True
                continue
            if is_draw(board):
                reward += rewards["draw"]
                next_state = convert_board(board)
                agent.update_q_value(state, action, reward, next_state, [], True)
                done = True
                continue
            threat_after_turn = set(get_winning_moves(board, PLAYER_PIECE))
            if threat_before_turn and len(threat_after_turn) < len(threat_before_turn):
                reward += rewards["block"]

            opponent_valid_moves = get_valid_moves(board)
            if not opponent_valid_moves:
                next_state = convert_board(board)
                agent.update_q_value(state, action, reward, next_state, [], True)
                done = True
                continue
            opponent_action = random.choice(opponent_valid_moves)
            drop_piece(board, opponent_action, PLAYER_PIECE)

            if check_winner(board, PLAYER_PIECE):
                reward += rewards["lose"]
                next_state = convert_board(board)
                agent.update_q_value(state, action, reward, next_state, [], True)
                done = True
                continue
            if is_draw(board):
                reward += rewards["draw"]
                next_state = convert_board(board)
                agent.update_q_value(state, action, reward, next_state, [], True)
                done = True
                continue

            next_state = convert_board(board)
            next_valid_move = get_valid_moves(board)
            agent.update_q_value(state, action, reward, next_state, next_valid_move, False)

def evaluate_agent(agent, games):
    original_epsilon = agent.epsilon
    agent.set_epsilon(0.0)
    results = {"wins":0, "losses":0, "draws":0}

    for _ in range(games):
        board = create_board()
        done = False

        while not done:
            valid_moves = get_valid_moves(board)
            if not valid_moves:
                results["draws"] += 1
                break

            state = convert_board(board)
            action = agent.choose_action(state, valid_moves)
            drop_piece(board, action, CPU_PIECE)

            if check_winner(board, CPU_PIECE):
                results["wins"] += 1
                done = True
                continue
            if is_draw(board):
                results["draws"] += 1
                done = True
                continue

            opponent_action = random.choice(get_valid_moves(board))
            drop_piece(board, opponent_action, PLAYER_PIECE)
            if check_winner(board, PLAYER_PIECE):
                results["losses"] += 1
                done = True
                continue
            if is_draw(board):
                results["draws"] += 1
                done = True

    agent.set_epsilon(original_epsilon)
    return results

def get_top_q_states(agent, top_n=5):
    scored_states = []
    for state, actions in agent.q_table.items():
        if actions:
            scored_states.append((state, max(actions.values()), actions))
    scored_states.sort(key=lambda item: item[1], reverse=True)
    top_states = []
    for state, best_value, actions in scored_states[:top_n]:
        top_states.append({
            "state": state,
            "best_q_value": best_value,
            "actions": actions,
            "visits": agent.visit_counts.get(state, 0),
        })
    return top_states

def generate_reports():
    os.makedirs(REPORT_DIR, exist_ok=True)
    checkpoints = [10, 1000, 10000]
    for difficulty in DIFFICULTY_REWARDS:
        agent = QLearningAgent(DEFAULT_ALPHA, DEFAULT_GAMMA, DEFAULT_EPSILON)
        prev = 0

        for games in checkpoints:
            train_agent(agent, difficulty, games - prev)
            prev = games

            summary = {
                "difficulty": difficulty,
                "games_trained": games,
                "alpha": agent.alpha,
                "gamma": agent.gamma,
                "epsilon": agent.epsilon,
                "evaluation": evaluate_agent(agent, games),
                "top_states": get_top_q_states(agent, top_n=5),
                "qtable_size": len(agent.q_table),
            }
            report_path = os.path.join(REPORT_DIR, f"report_{difficulty}_{games}.json")
            with open(report_path, "w", encoding="utf-8") as file:
                json.dump(summary, file, indent=2)

        agent.save_q_table(QTABLE_FILES[difficulty])


if __name__ == "__main__":
    qtables_exist()
    generate_reports()
