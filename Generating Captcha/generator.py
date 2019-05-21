from random_word import RandomWords
import oxford as dictionary
import random
r = RandomWords()

def generate_captcha():
    success = False

    # some words are not found in the Oxford Dictionary API
    # loop until there is a match
    while not success:
        try:
            word = r.get_random_word(hasDictionaryDef="true", minCorpusCount=7, minDictionaryCount=5, maxLength=6)
            info = dictionary.Word.get(word)
            success = True
            print("Random word: ", word)
        except:
            pass

    # get a list of example sentences using the given word
    # and choose a random one from the list to use 
    sentences = dictionary.Word.examples()
    randomNum = random.randint(0, len(sentences)-1)
    sentence = sentences[randomNum]

    print("Sentence: ", sentence)

generate_captcha()
