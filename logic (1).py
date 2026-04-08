import random

def run_simulation(ai, subjects, difficulty, scores, slots=6, explore=True):
    current_scores = scores.copy()
    history = []
    last_choice = -1
    recent_choices = []          # track last N picks for cooldown
    subject_counts = {s: 0 for s in subjects}
    n = len(subjects)

    # Ensure slots >= number of subjects so every subject gets at least one slot
    slots = max(slots, n)

    for slot in range(slots):
        weakest_idx = min(range(n), key=lambda i: current_scores[subjects[i]])

        # --- Cooldown mask: block subjects picked in last (n-1) turns ---
        cooldown = max(1, n - 1)
        blocked = set(recent_choices[-cooldown:]) if len(subjects) > 1 else set()

        # Force-include any subject that has had zero slots so far
        unvisited = [i for i in range(n) if subject_counts[subjects[i]] == 0]
        if unvisited:
            # Pick the weakest unvisited subject
            choice = min(unvisited, key=lambda i: current_scores[subjects[i]])
        else:
            # Let AI choose, but mask out recently used subjects
            raw_choice = ai.choose(slot, weakest_idx, explore)
            if raw_choice in blocked:
                # Fall back to weakest subject not on cooldown
                available = [i for i in range(n) if i not in blocked]
                if not available:
                    available = list(range(n))   # safety valve
                choice = min(available, key=lambda i: current_scores[subjects[i]])
            else:
                choice = raw_choice

        subj = subjects[choice]
        subject_counts[subj] += 1

        # --- Gain: diminishing returns as score rises ---
        gap = 1.0 - current_scores[subj]
        gain = gap * difficulty[subj] * random.uniform(0.12, 0.22)
        current_scores[subj] = min(1.0, current_scores[subj] + gain)

        # --- Reward shaping ---
        reward = gain * 20
        if choice == weakest_idx:
            reward += 5                          # good: tackled weakest
        if choice == last_choice:
            reward -= 15                         # strong repetition penalty
        if subject_counts[subj] > slots // n + 1:
            reward -= 10                         # penalise over-concentration

        ai.learn(slot, weakest_idx, choice, reward, slot + 1, weakest_idx)
        history.append({"subj": subj, "score": current_scores[subj], "gain": gain})

        recent_choices.append(choice)
        last_choice = choice

    return history