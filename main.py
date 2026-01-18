from wordle import check_guess
from drawer import draw_wordle_result

ANSWER = "KIWIS"  
GUESS = "SKILL"   

print(f"答案: {ANSWER}, 猜測: {GUESS}")
result = check_guess(GUESS, ANSWER)
print(f"邏輯結果: {result}") 

draw_wordle_result(ANSWER, GUESS, result)