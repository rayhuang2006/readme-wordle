import os
from PIL import Image, ImageDraw, ImageFont

COLOR_BG = (18, 18, 19)        
COLOR_WRONG = (58, 58, 60)     
COLOR_PARTIAL = (181, 159, 59) 
COLOR_CORRECT = (83, 141, 78)  
COLOR_TEXT = (255, 255, 255)  
COLOR_EMPTY = (18, 18, 19)  
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
            try:
                return ImageFont.truetype(path, 50) 
            except:
                continue
                
    print("Warning: Custom font not found, using default.")
    return ImageFont.load_default()

def draw_wordle_result(target_word, guess_word, result_list):

    width, height = 500, 100
    img = Image.new('RGB', (width, height), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    font = get_font()

    box_size = 80
    gap = 10
    total_width = (box_size * 5) + (gap * 4)
    start_x = (width - total_width) // 2 
    start_y = (height - box_size) // 2  

    for i in range(5):
        x0 = start_x + i * (box_size + gap)
        y0 = start_y
        x1 = x0 + box_size
        y1 = y0 + box_size
        
        status = result_list[i]
        if status == 2:
            fill_color = COLOR_CORRECT
        elif status == 1:
            fill_color = COLOR_PARTIAL
        else:
            fill_color = COLOR_WRONG
            
        draw.rectangle([x0, y0, x1, y1], fill=fill_color)
        
        char = guess_word[i].upper()
        
        try:
            draw.text((x0 + box_size/2, y0 + box_size/2), char, font=font, fill=COLOR_TEXT, anchor="mm")
        except:
            draw.text((x0 + 25, y0 + 15), char, font=font, fill=COLOR_TEXT)

    output_filename = "wordle_status.png"
    img.save(output_filename)
    print(f"圖片已生成: {output_filename}")

if __name__ == "__main__":
    print("Testing drawer...")
    draw_wordle_result("APPLE", "PARTY", [1, 0, 0, 0, 0])