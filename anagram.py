#!/usr/bin/python

"""
This module provides a function that anagrams a given sentence, based on a
dictionary of acceptable words. It ignores spaces, and the anagrams it returns
may have more than one constituent word.

The way it does this is by first constructing a trie from your dictionary.
Because this can take a long time, it is recommended that you do this yourself
first, using build_trie(), so you can reuse the same trie across multiple
calls of anagram(). The anagramming itself is pretty fast.

MIN_WORD_SIZE controls the minimum length of the words added to the trie.
WORDS_FILE is the default dictionary used.
"""

MIN_WORD_SIZE = 3
WORDS_FILE = "/usr/share/dict/words"

class TrieNode(object):
    """Basically a standard trie."""

    def __init__(self, value=''):
        """Creates a new non-terminal trie node, with no children."""
        self.value = value
        self.children = {}
        self.terminal = False

    def add(node, letters):
        """Add letters to the trie, depthwise."""
        for letter in letters:
            if letter not in node.children:
                node.children[letter] = TrieNode(letter)
            node = node.children[letter]
        node.terminal = True

    def _anagram(self, tiles, path, root, sentence_length):
        if self.terminal:
            ana = ''.join(path)
            if len(ana.replace(' ', '')) == sentence_length:
                # Our path is as long as the entire sentence we were
                # anagramming, so we've completed a valid anagram.
                yield ana
            else:
                # Not done yet. Anagram the remaining letters.
                path.append(' ')
                for ana in root._anagram(tiles, path, root, sentence_length):
                    yield ana
                path.pop()
        # Terminal nodes can have children too.
        for letter, node in self.children.iteritems():
            count = tiles.get(letter, 0)
            if count == 0:
                # Don't need more of this letter.
                continue
            tiles[letter] = count - 1
            path.append(letter)
            for ana in node._anagram(tiles, path, root, sentence_length):
                yield ana
            path.pop()
            tiles[letter] = count


def build_trie(words=None, words_file=None):
    """
    Builds a trie from a given list of words, or (if no words are given) a
    given or default words_file.
    """
    if words is None:
        words = open(words_file or WORDS_FILE)

    trie, chars = TrieNode(), set()
    for word in words:
        word = word.strip().lower()
        if len(word) >= MIN_WORD_SIZE:
            chars |= set(word)
            trie.add(word)

    if words is None: words.close()
    trie.chars = chars
    return trie


def anagram(sentence, words=None, words_file=None, trie=None):
    """
    Returns an iterator of anagram sentences for a given sentence.
    If no trie is given, build_trie(words, words_file) is called first.
    """
    if trie is None:
        trie = build_trie(words, words_file)
    if any(map(lambda c: c not in trie.chars, sentence.lower())):
        # Easy.
        return []
    tiles = {}
    for letter in sentence.lower():
        tiles[letter] = tiles.get(letter, 0) + 1
    return trie._anagram(tiles, [], trie, len(sentence))


def _main():
    import sys
    from time import time

    sentence = ''.join(sys.argv[1:])
    if len(sentence) == 0:
        print >> sys.stderr, "Usage: %s WORDS" % sys.argv[0]
        sys.exit(1)

    s = time()
    words = sys.stdin if not sys.stdin.isatty() else None
    trie = build_trie(words)
    print >> sys.stderr, "Loaded dictionary in %f seconds." % (time() - s)
    
    s = time()
    count = 0
    for a in anagram(sentence, trie=trie):
        print a
        count += 1
    print >> sys.stderr, "Found %d anagrams in %f seconds." % (count,
                                                               time() - s)


if __name__ == '__main__':
    _main()
