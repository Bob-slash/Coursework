 # Problem Set 4C
# Name: Bobby Albani
# Collaborators: None
# Time Spent: 1:00
# Late Days Used: 0

import json
import ps4b # Importing your work from Part B

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # inFile: file
    with open(file_name, 'r') as inFile:
        # wordlist: list of strings
        wordlist = []
        for line in inFile:
            wordlist.extend([word.lower() for word in line.split(' ')])
        return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"").lower()
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story[:-1]

def get_story_pads():
    with open('pads.txt') as json_file:
        return json.load(json_file)

WORDLIST_FILENAME = 'words.txt'
### END HELPER CODE ###

def decrypt_message_try_pads(ciphertext, pads):
    '''
    Given a string ciphertext and a list of possible pads
    used to create it find the pad used to create the ciphertext

    We will consider the pad used to create it the pad which
    when used to decrypt ciphertext results in a plaintext
    with the most valid English words. In the event of ties return
    the last pad that results in the maximum number of valid English words.

    ciphertext (EncryptedMessage): The ciphertext
    pads (list of lists of ints): A list of pads which might have been used
        to encrypt the ciphertext

    Returns: (PlaintextMessage) A message with the decrypted ciphertext and the best pad
    '''
    #Variables
    most_words = 0
    most_valid_words = ciphertext.decrypt_message(pads[0])
    plain_text = None
    valid_word_list = load_words(WORDLIST_FILENAME)
    
    #Finds pad that returns text with the most amound of valid words
    for pad in pads:
        plain_text = ciphertext.decrypt_message(pad)
        word_list = plain_text.get_text().split(" ")
        valid_word_count = 0
        #Count number of valid words
        for word in word_list:
            if is_word(valid_word_list, word):
                valid_word_count += 1
        
        #If there is a file with more valid words than the previous max
        #save the number of most words and the plaintext object
        if valid_word_count >= most_words:
            most_words = valid_word_count
            most_valid_words = plain_text
    
    return most_valid_words
        

def decode_story():
    '''
    Write your code here to decode Bob's story using a list of possible pads
    Hint: use the helper functions get_story_string and get_story_pads and your EncryptedMessage class.

    Returns: (string) the decoded story

    '''
    ciphertext = ps4b.EncryptedMessage(get_story_string())
    pads = get_story_pads()
    #Puts story and pads through decrypt_message_try_pads
    story = decrypt_message_try_pads(ciphertext, pads)
    return story.get_text()

if __name__ == '__main__':
    # # Uncomment these lines to try running decode_story()
    story = decode_story()
    print("Decoded story: ", story)

