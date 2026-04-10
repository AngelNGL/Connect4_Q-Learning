import json
import os
import random


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.visit_counts = {}

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def state_exists(self, state, valid_moves):
        if state not in self.q_table:
            self.q_table[state] = {str(move): 0.0 for move in valid_moves}
        else:
            for move in valid_moves:
                self.q_table[state].setdefault(str(move), 0.0)
        self.visit_counts.setdefault(state, 0)

    def choose_action(self, state, valid_moves):
        self.state_exists(state, valid_moves)
        self.visit_counts[state] += 1
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        return self.best_action(state, valid_moves)

    def best_action(self, state, valid_moves):
        self.state_exists(state, valid_moves)
        best_value = max(self.q_table[state][str(move)] for move in valid_moves)
        best_moves = [move for move in valid_moves if self.q_table[state][str(move)] == best_value]
        return random.choice(best_moves)

    def update_q_value(self, state, action, reward, next_state, next_valid_moves, done):
        current_q = self.q_table[state][str(action)]

        if done or not next_valid_moves:
            target = reward
        else:
            self.state_exists(next_state, next_valid_moves)
            future_q = max(self.q_table[next_state][str(move)] for move in next_valid_moves)
            target = reward + self.gamma * future_q

        self.q_table[state][str(action)] = current_q + self.alpha * (target - current_q)

    def save_q_table(self, file_path):
        payload = {
            "alpha": self.alpha,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "q_table": self.q_table,
            "visit_counts": self.visit_counts,
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def load_q_table(self, file_path):
        if not os.path.exists(file_path):
            return False
        with open(file_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
        self.alpha = payload.get("alpha", self.alpha)
        self.gamma = payload.get("gamma", self.gamma)
        self.epsilon = payload.get("epsilon", self.epsilon)
        self.q_table = payload.get("q_table", {})
        self.visit_counts = payload.get("visit_counts", {})
        return True
