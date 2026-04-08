import numpy as np
import json
import os

class StudyAI:
    def __init__(self, subjects, slots=6):
        self.subjects = subjects
        self.q = np.zeros((slots + 1, len(subjects), len(subjects)))

    def choose(self, slot, weakest_idx, explore=True):
        import random
        if explore and random.random() < 0.2:
            return random.randint(0, len(self.subjects) - 1)
        return int(np.argmax(self.q[slot][weakest_idx]))

    def learn(self, slot, weakest, choice, reward, next_slot, next_weakest):
        cur = self.q[slot][weakest][choice]
        best = np.max(self.q[next_slot][next_weakest])
        self.q[slot][weakest][choice] += 0.1 * (reward + 0.9 * best - cur)

    def save(self, file="q_table.json"):
        with open(file, "w") as f: json.dump(self.q.tolist(), f)

    def load(self, file="q_table.json"):
        if os.path.exists(file):
            with open(file) as f: self.q = np.array(json.load(f))
            return True
        return False