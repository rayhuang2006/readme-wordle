import os
import json
import re
from wordle import check_guess
from drawer import draw_game_state

STATE_FILE = "state.json"

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def main():
    issue_title = os.environ.get("ISSUE_TITLE", "")
    print(f"收到輸入: {issue_title}")

    match = re.search(r"guess:\s*([a-zA-Z]{5})", issue_title, re.IGNORECASE)
    
    if not match:
        print("格式錯誤或找不到 5 個字母的猜測。")
        state = load_state()
        draw_game_state(state)
        return

    guess_word = match.group(1).upper()
    print(f"玩家猜測: {guess_word}")

    state = load_state()
    target_word = state["answer"]

    if state["status"] != "playing":
        print("遊戲已經結束！")
        draw_game_state(state)
        return

    result = check_guess(guess_word, target_word)
    
    new_record = {
        "word": guess_word,
        "result": result
    }
    state["guesses"].append(new_record)

    if guess_word == target_word:
        state["status"] = "won"
        print("恭喜贏了！")
    elif len(state["guesses"]) >= 6:
        state["status"] = "lost"
        print("很遺憾，輸了...")

    save_state(state)
    draw_game_state(state)

if __name__ == "__main__":
    main()