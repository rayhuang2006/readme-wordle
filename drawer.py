import os
from PIL import Image, ImageDraw, ImageFont

COLOR_BG = (18, 18, 19)
COLOR_WRONG = (58, 58, 60)   
COLOR_PARTIAL = (181, 159, 59)  
COLOR_CORRECT = (83, 141, 78)   
COLOR_TEXT = (255, 255, 255)
COLOR_BORDER = (58, 58, 60)

def get_font():
    font_paths = [
        "arialbd.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "Arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            try: return ImageFont.truetype(path, 50)
            except: continue
    return ImageFont.load_default()

def draw_game_state(state):
    """
    state 格式: { "guesses": [ {"word": "APPLE", "result": [0,1,0,0,2]}, ... ] }
    """
    width, height = 500, 800
    img = Image.new('RGB', (width, height), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    font = get_font()

    box_size = 80
    gap = 10
    start_x = (width - (box_size * 5 + gap * 4)) // 2
    start_y = 50 


    for row in range(6):
        guess_data = state["guesses"][row] if row < len(state["guesses"]) else None
        
        y = start_y + row * (box_size + gap)

        for col in range(5):
            x = start_x + col * (box_size + gap)
            
            fill_color = COLOR_BG
            outline_color = COLOR_BORDER
            text = ""

            if guess_data:
                text = guess_data["word"][col]
                res = guess_data["result"][col]
                if res == 2: fill_color = COLOR_CORRECT
                elif res == 1: fill_color = COLOR_PARTIAL
                else: fill_color = COLOR_WRONG
                outline_color = fill_color 

            draw.rectangle([x, y, x + box_size, y + box_size], fill=fill_color, outline=outline_color, width=2)
            
            if text:
                draw.text((x + 25, y + 15), text, font=font, fill=COLOR_TEXT)

    img.save("wordle_status.png")
    print("遊戲盤面已更新：wordle_status.png")