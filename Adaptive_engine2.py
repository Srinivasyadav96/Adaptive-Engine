import time
import random

# --- 1. PUZZLE GENERATOR 
class PuzzleGenerator:
    def __init__(self):
        # Ranges for Easy (1-10), Medium (10-50), Hard (50-100) 
        self.levels = {
            "Easy": (1, 10),
            "Medium": (10, 50),
            "Hard": (50, 100)
        }

    def generate(self, difficulty):
        low, high = self.levels[difficulty]
        a, b = random.randint(low, high), random.randint(low, high)
        op = random.choice(['+', '-'])
        
        # Ensure no negative results for children 
        if op == '-' and a < b: a, b = b, a
        
        question = f"{a} {op} {b}"
        answer = eval(question)
        return question, answer

# --- 2. PERFORMANCE TRACKER 
class PerformanceTracker:
    def __init__(self):
        self.history = []

    def log(self, difficulty, is_correct, response_time):
        self.history.append({
            "level": difficulty,
            "correct": is_correct,
            "time": response_time
        })

# --- 3. ADAPTIVE ENGINE (Rule-Based Logic)
class AdaptiveEngine:
    def __init__(self):
        self.levels = ["Easy", "Medium", "Hard"]

    def update_difficulty(self, current_diff, history):
        if not history: return current_diff
        
        idx = self.levels.index(current_diff)
        last_result = history[-1]
        
        # LOGIC: IF STRUGGLING -> DECREASE 
        if not last_result['correct']:
            if idx > 0:
                print(f"  >>> [ADAPTIVE SYSTEM]: Struggling detected. Moving to {self.levels[idx-1]}...")
                return self.levels[idx-1]
        
        # LOGIC: IF DOING WELL -> INCREASE 
        # "Doing well" = 2 correct in a row AND fast response (< 6 seconds)
        if len(history) >= 2:
            recent = history[-2:]
            all_correct = all(h['correct'] for h in recent)
            avg_time = sum(h['time'] for h in recent) / 2
            
            if all_correct and avg_time < 6.0:
                if idx < 2:
                    print(f"  >>> [ADAPTIVE SYSTEM]: Mastery detected! Moving to {self.levels[idx+1]}...")
                    return self.levels[idx+1]
                    
        return current_diff

# --- 4. MAIN SYSTEM 
def start_app():
    gen = PuzzleGenerator()
    tracker = PerformanceTracker()
    engine = AdaptiveEngine()
    
    print("--- Math Adventures Prototype ---")
    user_name = input("Enter student name: ")
    current_lvl = input("Choose starting level (Easy/Medium/Hard): ").capitalize()
    
    if current_lvl not in ["Easy", "Medium", "Hard"]: current_lvl = "Easy"

    # Run for 6 rounds to see transitions
    for i in range(6):
        print(f"\nRound {i+1} | Level: {current_lvl}")
        problem, correct_ans = gen.generate(current_lvl)
        
        start = time.time()
        try:
            ans = int(input(f"Question: {problem} = "))
        except:
            ans = None
        elapsed = round(time.time() - start, 2)
        
        is_correct = (ans == correct_ans)
        if is_correct:
            print(f"Correct! Time: {elapsed}s")
        else:
            print(f"Incorrect. The answer was {correct_ans}.")
            
        # Log performance 
        tracker.log(current_lvl, is_correct, elapsed)
        
        # SYSTEM ADAPTS AUTOMATICALLY HERE [cite: 13]
        current_lvl = engine.update_difficulty(current_lvl, tracker.history)

    # SESSION SUMMARY 
    print("\n" + "="*30)
    print(f"SESSION SUMMARY FOR {user_name.upper()}")
    total_correct = sum(1 for h in tracker.history if h['correct'])
    print(f"Final Accuracy: {total_correct}/6")
    print(f"Final Recommended Level: {current_lvl}")
    print("="*30)

if __name__ == "__main__":
    start_app()
