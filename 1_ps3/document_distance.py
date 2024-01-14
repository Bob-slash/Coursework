# 6.100A Spring 2023
# Problem Set 3
# Name: Bobby Albani
# Collaborators: None

"""
Description:
    Computes the similarity between two texts using two different metrics:
    (1) shared words, and (2) term frequency-inverse document
    frequency (TF-IDF).
"""

import string
import math
import re

### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 0: Prep Data ###
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    return input_text.split()


### Problem 1: Get Frequency ###
def get_frequencies(word_list):
    """
    Args:
        word_list: list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a word in l and the corresponding int
        is the frequency of the word in l
    """
    res = {}
    #iterates through list of words
    for word in word_list:
        # creates new dictionary with frequency of each word
        # adds to existing word frequency, otherwise making a new one
        if word in res.keys():
            res[word] += 1
        elif word not in res.keys():
            res[word] = 1
            
    return res


### Problem 2: Get Words Sorted by Frequency
def get_words_sorted_by_frequency(frequencies_dict):
    """
    Args:
        frequencies_dict: dictionary that maps a word to its frequency
    Returns:
        list of words sorted by increasing frequency with ties broken
        by alphabetical order
    """
    rep = frequencies_dict.copy()
    sort_list = []
    
    #sorts list by increasing frequencies
    while len(rep) > 0:
        keys = list(rep.keys())
        values = list(rep.values())
        least = keys[0]
        #finds word with smallest frequency
        for key in rep:
            if rep[key] < rep[least]:
                least = key
        
        #if there are multiple words with the same frequency...
        if values.count(rep[least]) > 1:
            #saves a list of all of them
            alph = []
            for key in rep:
                if rep[key] == rep[least]:
                    alph.append(key)
            #sorts list
            alph.sort()
            #puts it into the sorted list and reoves it from the dictionary
            for val in alph:
                sort_list.append(val)
                rep.pop(val)
        
        #if there is only one word with the frequency
        else:
            sort_list.append(least)
            rep.pop(least)
            
            
        
    return sort_list
    


### Problem 3: Most Frequent Word(s) ###
def get_most_frequent_words(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          frequencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """
    #Variables
    highest = 0
    dict_total = dict1.copy()

    #fills dict_total with frequencies of words from both dictionaries and finds highest value
    for key in dict2:
        if key in dict_total.keys():
            dict_total[key] += dict2[key]

        else:
            dict_total[key] = dict2[key]
            
        if dict_total[key] > highest:
            highest = dict_total[key]
    
    #looks for instances of highest in dict_total 
    most_frequent = []
    for key in dict_total:
        #puts highest valued keys into list
        if dict_total[key] == highest:
            most_frequent.append(key)
    
    #sorts list alphabetically
    most_frequent.sort()
    
    return most_frequent


### Problem 4: Similarity ###
def calculate_similarity_score(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary of words of text1
        dict2: frequency dictionary of words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums words
        from these three scenarios:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    #Variables
    diff = 0
    ALL = 0
    
    #Iterates through dict1
    for e1 in dict1:
        #adds all frequencies to ALL
        ALL += dict1[e1]
        #if element is in both dictionaries, take the absolute value of difference 
        #else just add frequency
        if e1 in dict2:
            diff += abs(dict1[e1] - dict2[e1])
        elif e1 not in dict2:
            diff += dict1[e1]

    #iterate through dict2
    for e2 in dict2:
        #adds to all and adds unique frequencies to diff
        ALL += dict2[e2]
        if e2 not in dict1:
            diff += dict2[e2]

    #Returns rounded number
    return round(1-(diff/ALL),2)
                


### Problem 5: Finding TF-IDF ###
def get_tf(text_file):
    """
    Args:
        text_file: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculatd as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """
    #Loads and preps data
    words = load_file(text_file)
    word_list = prep_data(words)
    
    #Modifies frequency dict
    TF = get_frequencies(word_list)
    for key in TF:
        #frequency / total number of words
        TF[key] = TF[key] / len(word_list)
    
    return TF

def get_idf(text_files):
    """
    Args:
        text_files: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()

    """
    #Variables
    IDF = {}
    words_total = {}
    
    #Iterate through files
    for file in text_files:
        #loads and preps data
        words = load_file(file)
        word_list = prep_data(words)
        frequencies = get_frequencies(word_list)
        
        #Makes a dict showing how many files each word appears in
        for key in frequencies:
            if key not in words_total:
                words_total[key] = 1
            else:
                words_total[key] += 1
    
    #Fills IDF dictionary using IDF equation
    for key in words_total:
        IDF[key] = math.log10(len(text_files)/words_total[key])
    
    return IDF
        
        
            
def get_tfidf(text_file, text_files):
    """
    Args:
        text_file: name of file in the form of a string (used to calculate TF)
        text_files: list of names of files, where each file name is a string
        (used to calculate IDF)
    Returns:
       a sorted list of tuples (in increasing TF-IDF score), where each tuple is
       of the form (word, TF-IDF). In case of words with the same TF-IDF, the
       words should be sorted in increasing alphabetical order.

    * TF-IDF(i) = TF(i) * IDF(i)
    """
    #Variables
    TF = get_tf(text_file)
    IDF = get_idf(text_files)
    TFIDF = {}
    sorted_list = []

    #Fills TFIDF dict
    for key in TF:
        TFIDF[key] = TF[key] * IDF[key]
    
    #uses get_words_sorted_by_frequency with TFIDF to get list of sorted words
    words_sorted = get_words_sorted_by_frequency(TFIDF)
    
    #fills sorted_list with tuple of (word, TFIDF score) in order from word_sorted
    for word in words_sorted:
        sorted_list.append((word, TFIDF[word]))
    
    return sorted_list


if __name__ == "__main__":
    pass
    # ##Uncomment the following lines to test your implementation
    # ## Tests Problem 1: Prep Data
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    print(world) ## should print ['hello', 'world', 'hello', 'there']
    print(friend) ## should print ['hello', 'friends']

    # ## Tests Problem 2: Get Frequencies
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    print(world_word_freq) ## should print {'hello': 2, 'world': 1, 'there': 1}
    print(friend_word_freq) ## should print {'hello': 1, 'friends': 1}

    # ## Tests Problem 3: Get Words Sorted by Frequency
    world_words_sorted_by_freq = get_words_sorted_by_frequency(world_word_freq)
    friend_words_sorted_by_freq = get_words_sorted_by_frequency(friend_word_freq)
    print(world_words_sorted_by_freq) ## should print ['there', 'world', 'hello']
    print(friend_words_sorted_by_freq) ## should print ['friends', 'hello']

    # ## Tests Problem 4: Most Frequent Word(s)
    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
    most_frequent = get_most_frequent_words(freq1, freq2)
    print(most_frequent) ## should print ["hello", "world"]

    # ## Tests Problem 5: Similarity
    word_similarity = calculate_similarity_score(world_word_freq, friend_word_freq)
    print(word_similarity) ## should print 0.33

    # ## Tests Problem 6: Find TF-IDF
    text_file = 'tests/student_tests/hello_world.txt'
    text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(text_file)
    idf = get_idf(text_files)
    tf_idf = get_tfidf(text_file, text_files)
    print(tf) ## should print {'hello': 0.5, 'world': 0.25, 'there': 0.25}
    print(idf) ## should print {'there': 0.3010299956639812, 'world': 0.3010299956639812, 'hello': 0.0, 'friends': 0.3010299956639812}
    print(tf_idf) ## should print [('hello', 0.0), ('there', 0.0752574989159953), ('world', 0.0752574989159953)]
