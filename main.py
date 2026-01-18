import os
import json
import re
import time
from wordle import check_guess
from drawer import draw_game_state

STATE_FILE = "state.json"
README_FILE = "README.md"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"answer": "SMART", "guesses": [], "status": "playing"}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def update_readme():

    if not os.path.exists(README_FILE):
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    timestamp = int(time.time())
    
    repo_url = "https://raw.githubusercontent.com/rayhuang2006/readme-wordle/main/wordle_status.png"
    
    new_content = re.sub(
        r"\!\[Wordle Status\]\(.*?\)",
        f"![Wordle Status]({repo_url}?v={timestamp})",
        content
    )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README 已更新 (使用 Raw URL 強制刷新)")

def main():
    issue_title = os.environ.get("ISSUE_TITLE", "")
    match = re.search(r"guess:\s*([a-zA-Z]{5})", issue_title, re.IGNORECASE)
    
    if not match:
        print("未偵測到有效猜測，僅重繪圖片。")
        state = load_state()
        draw_game_state(state)
        return

    guess_word = match.group(1).upper()
    state = load_state()
    target_word = state["answer"]

    if state["status"] != "playing":
        draw_game_state(state)
        return

    result = check_guess(guess_word, target_word)
    
    state["guesses"].append({
        "word": guess_word,
        "result": result
    })

    if guess_word == target_word:
        state["status"] = "won"
    elif len(state["guesses"]) >= 6:
        state["status"] = "lost"

    save_state(state)
    draw_game_state(state)
    
    update_readme()

if __name__ == "__main__":
    main()