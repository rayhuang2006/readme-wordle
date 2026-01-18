import os
import json
import re
import time
import glob
import random
from wordle import check_guess
from drawer import draw_game_state

STATE_FILE = "state.json"
README_FILE = "README.md"
TEMPLATE_FILE = "README.template"

WORD_LIST = ["SMART", "KIWIS", "APPLE", "GHOST", "START", "WORLD", "HELLO", "LINUX", "REACT"]

def pick_new_word():
    return random.choice(WORD_LIST)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"answer": pick_new_word(), "guesses": [], "status": "playing"}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def clean_old_images():
    for f in glob.glob("wordle_status_*.png"):
        try:
            os.remove(f)
            print(f"已刪除舊圖: {f}")
        except:
            pass

def update_readme_with_new_image(image_filename):
    if not os.path.exists(TEMPLATE_FILE):
        print("錯誤：找不到樣板檔")
        return

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_content = f.read()

    image_markdown = f"![Wordle Status](./{image_filename})"

    new_content = template_content.replace("{{WORDLE_STATUS}}", image_markdown)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"README 已更新指向新圖片: {image_filename}")

def main():
    issue_title = os.environ.get("ISSUE_TITLE", "")
    match = re.search(r"guess:\s*([a-zA-Z]{5})", issue_title, re.IGNORECASE)
    
    timestamp = int(time.time())
    new_image_filename = f"wordle_status_{timestamp}.png"
    
    if not match:
        print("未偵測到有效猜測，僅重繪。")
        state = load_state()
        clean_old_images()
        draw_game_state(state, new_image_filename)
        update_readme_with_new_image(new_image_filename)
        return

    guess_word = match.group(1).upper()
    state = load_state()


    if state["status"] != "playing":
        print("上一局已結束，開啟新局！")
        state["answer"] = pick_new_word()
        state["guesses"] = []
        state["status"] = "playing"

    target_word = state["answer"]
    
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
    
    clean_old_images()
    draw_game_state(state, new_image_filename)
    update_readme_with_new_image(new_image_filename)

if __name__ == "__main__":
    main()