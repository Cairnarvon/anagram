## Mr. Aaron's friend Vic rang Ana.

### Usage

Standalone usage:

>     $ ./anagram.py cairnarvon
>     Loaded dictionary in 3.543153 seconds.
>     acorn invar
>     air corn van
>     (...)
>     vic roar ann
>     vic roar nan
>     Found 360 anagrams in 0.260907 seconds.

Or with a custom dictionary:

>     $ ./anagram.py cairnarvon </usr/share/dict/nederlands
>     Loaded dictionary in 37.050658 seconds.
>     aan nrc ivor
>     aio anvr nrc
>     (...)
>     vin rna caro
>     vin rna cora
>     Found 1188 anagrams in 0.706538 seconds.

For usage as a Python module, just `help(anagram)` after loading it.

### How work?

It constructs a (case-insensitive) trie holding all of the words in your dictionary, and then performs a depth-first search for matching words, jumping back to the root when it reaches the end of a word but still has characters left.

Concretely, suppose you have a dictionary containing the words "able", "ably", "ace", "aces", "aced", "babe", "baby", "bad", and "back". We will then construct the following trie:

![trie](http://i.imgur.com/ACkHF.png "Example trie")

The grey nodes are terminal nodes; that is, nodes that lie on the end of a word. Note that the E in "ace" is a terminal node, but that it still has children.

Suppose we want to anagram the word "Abby". Taking a letter at a time, we notice that it contains an A, so we proceed down that branch in the trie. The next letter is B, and our A node has a B child. However, none of the remaining letters is an L, so this is a dead end. We backtrack one level, and as none of the remaining letters is a C either, we backtrack again and go down the B branch. Then we proceed accordingly and follow A, B, and E which doesn't match, so we backtrack and go to Y which does. This is a terminal node and we have used all of the letters in our target phrase, so we have found a valid anagram: "baby".

Since there might be more anagrams hiding in the trie, we backtrack and continue on, but we quickly find that there are none, and we're done.

If we had letters left upon reaching a terminal node (for example, if our target phrase had been "abbey lab"), we could, as said, have tried jumping back to the root node after finding "baby" and continued on trying to find another word to match our remaining letters (ELAB), though in this example we wouldn't have found any.

Additionally, we keep track of which characters we've seen during the construction of the trie, so we can return immediately if the target phrase contains anything that will never match.
