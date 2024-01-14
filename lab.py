"""
6.101 Lab 9:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        # type check
        if type(key) != str:
            raise TypeError("Only strings allowed")

        cur_tree = self
        for i in range(1, len(key) + 1):
            new_key = key[i-1:i]
            new_tree = PrefixTree()
            if new_key not in cur_tree.children:
                cur_tree.children[new_key] = new_tree
            cur_tree = cur_tree.children[new_key]
        cur_tree.value = value

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if type(key) != str:
            raise TypeError("Only strings allowed")

        cur_tree = self
        for i in range(1, len(key) + 1):
            new_key = key[i-1:i]
            if new_key not in cur_tree.children:
                raise KeyError("key not in prefix tree")
            cur_tree = cur_tree.children[new_key]

        return cur_tree.value

    def get_children(self):
        return self.children

    def get_value(self):
        return self.value

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if type(key) != str:
            raise TypeError("Only strings allowed")
        cur_tree = self
        for i in range(1, len(key)):
            new_key = key[i-1:i]
            if new_key not in cur_tree.children:
                raise KeyError("key not in prefix tree")
            cur_tree = cur_tree.children[new_key]
        if cur_tree.children[key[-1]].children:
            cur_tree.children[key[-1]].value = None
        else:
            cur_tree.children.pop(key[-1])

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        if type(key) != str:
            raise TypeError("Only strings allowed")

        cur_tree = self
        for letter in key:
            if letter not in cur_tree.children:
                return False
            cur_tree = cur_tree.children[letter]
        if cur_tree.value == None:
            return False
        return True

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        # for key in cur_tree.children:
        #     if cur_tree.value != None:
        #         yield (key, cur_tree.value)
        #     cur_tree = cur_tree.children[key]
        visited = set()
        yet_to_visit = [(None, self)]
        while yet_to_visit:
            next_visit = yet_to_visit.pop(0)
            cur_tree = next_visit[1]
            cur_letter = next_visit[0]
            neighbors = cur_tree.get_neighbors()
            visited.add(cur_tree)
            for key, neighbor in neighbors:
                next_key = key
                if cur_letter != None:
                    next_key = cur_letter + next_key
                if neighbor.value != None:
                    yield (next_key, neighbor.value)
                yet_to_visit.append((next_key, neighbor))

    def get_neighbors(self):
        """
        Given a prefixtree, returns a list of tuples of the shape
        (key, prefixtree)
        """
        output = []
        for key in self.children:
            output.append((key, self.children[key]))
        return output


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    sentences = tokenize_sentences(text)
    words = []
    for sentence in sentences:
        words += sentence.split()
    frequencies = {}
    for word in words:
        if word not in frequencies:
            frequencies[word] = 1
        else:
            frequencies[word] += 1
    output = PrefixTree()
    for key in frequencies:
        output[key] = frequencies[key]
    return output


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if type(prefix) != str:
        raise TypeError("Only strings allowed")
    tree_vals = []
    cur_tree = tree
    for letter in prefix:
        if letter not in cur_tree.children:
            return []
        cur_tree = cur_tree.children[letter]

    if cur_tree.value != None:
        tree_vals.append(("", cur_tree.value))
    for val in cur_tree:
        tree_vals.append(val)

    output = []
    tree_vals.sort(key=lambda x: x[1], reverse=True)
    if max_count != None:
        for val in tree_vals[:max_count]:
            output.append(prefix + val[0])
    else:
        for val in tree_vals:
            output.append(prefix + val[0])
    return output


def edit_insert(prefix):
    alph = "abcdefghijklmnopqrstuvwxyz"
    output = set()
    for letter in alph:
        for i in range(len(prefix) + 1):
            output.add(prefix[0:i] + letter + prefix[i:])
    return list(output)


def edit_replace(prefix, rep_with=""):
    alph = "abcdefghijklmnopqrstuvwxyz"
    output = set()
    for i in range(len(prefix)):
        temp = ""
        for j in range(len(prefix)):
            if j != i:
                temp += prefix[j]
            if rep_with != "" and j == i:
                temp += rep_with
        output.add(temp)
    return list(output)


def edit_swap(prefix):
    alph = "abcdefghijklmnopqrstuvwxyz"
    output = set()
    for i in range(len(prefix) - 1):
        temp_list = [*prefix]
        temp = temp_list[i]
        temp_list[i] = temp_list[i + 1]
        temp_list[i + 1] = temp
        output.add("".join(temp_list))
    return list(output)


def edit(prefix):
    """
    Given a prefix, returns every possible correction to the prefix
    as a list
    """
    alph = "abcdefghijklmnopqrstuvwxyz"
    output = []
    output.extend(edit_insert(prefix))
    output.extend(edit_replace(prefix))
    for letter in alph:
        output.extend(edit_replace(prefix, letter))
    output.extend(edit_swap(prefix))

    return output


def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    complete = set(autocomplete(tree, prefix, max_count))
    edits = edit(prefix)

    valid = []
    for val in edits:
        if val in tree and val not in complete:
            valid.append(val)

    tree_vals = []
    for val in valid:
        tree_vals.append((val, tree[val]))

    tree_vals.sort(key=lambda x: x[1], reverse=True)
    if max_count != None:
        count = max_count - len(complete)
        for i in range(count):
            complete.add(tree_vals[i][0])
    else:
        for val in valid:
            complete.add(val)

    return list(complete)


def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    if len(pattern) == 0:
        if tree.value != None:
            return [("", tree.value)]
        else:
            return []

    output = []

    first_letter = pattern[0]

    if first_letter == "*":
        all_pattern = word_filter(tree, pattern[1:])

        for val in all_pattern:
            output.append((val[0], val[1]))

        for cur_tree in tree.children:
            new_tree = tree.children[cur_tree]
            all_pattern = word_filter(new_tree, pattern)

            for val in all_pattern:
                new_val = (cur_tree + val[0], val[1])
                output.append(new_val)

    elif first_letter == "?":
        for cur_tree in tree.children:
            new_tree = tree.children[cur_tree]
            all_pattern = word_filter(new_tree, pattern[1:])

            for val in all_pattern:
                new_val = (cur_tree + val[0], val[1])
                output.append(new_val)

    else:
        if first_letter in tree.children:
            new_tree = tree.children[first_letter]
            all_pattern = word_filter(new_tree, pattern[1:])

            for val in all_pattern:
                new_val = (first_letter + val[0], val[1])
                output.append(new_val)

    output = set(output)
    output = list(output)
    return output


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    doctest.testmod()
    with open("dracula.txt", encoding="utf-8") as f:
        text = f.read()
