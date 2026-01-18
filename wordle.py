def check_guess(guess_word, target_word):

    guess_word = list(guess_word.upper())
    target_word = list(target_word.upper())

    result = [0] * 5

    for i in range(5):
        if guess_word[i] == target_word[i]:
            result[i] = 2
            guess_word[i] = None
            target_word[i] = None

    for i in range(5):
        now = guess_word[i]
        if now is not None and now in target_word:
            result[i] = 1
            target_word[target_word.index(now)] = None        

    return result