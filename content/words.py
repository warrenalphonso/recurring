"""
Save words from Webster's 1913 dictionary which are also among the 10,000 most 
common words according to Google's n-gram. (Actually, I only save the 1,000 to 
10,000 most common because the top 1,000 most common are very simple words.) 
I use a .txt file of Webster's downloaded from Project Gutenberg: 
    http://www.gutenberg.org/cache/epub/29765/pg29765.txt
And the top 1/3 million common words downloaded from Peter Norvig's website: 
    https://norvig.com/ngrams/count_1w.txt
I'll save the words and their definitions to a CSV file, and then email myself 
one word every day. 

You can see how I came up with this code in the "ParseWebsters" Jupyter Notebook 
in this repository. 
"""
import string
import random
import csv

random.seed(123)

# Parse Webster's 1913
with open("websters1913.txt", "r") as f:
    lines = f.read().split("\n")


def is_word(w):
    # Webster's dictionary words are surrounded by \n and all uppercase
    return w and all(map(lambda c: c in string.ascii_uppercase, w))


definitions = {}
curr_word = None
for l in lines:
    if is_word(l):
        curr_word = l
        # String concatentation makes it O(N**2)
        definitions[curr_word] = definitions.get(curr_word, [])
    elif curr_word and l:
        definitions[curr_word].append(l)
# Join array of lines into one string
for k, v in definitions.items():
    definitions[k] = "\n".join(v)

n = 10_000  # Keep 1_000 to n most common words
with open("ngram_common.txt", "r") as f:
    lines = f.read().split("\n")[:-1]  # Last line is empty line
    # Separate word from freq
    lines = list(map(lambda l: l.split("\t"), lines))
    most_common = [w for w, f in lines][1_000:n]
    most_common = set(most_common)  # Constant lookup time


def is_common(w):
    # most_common dataset is all lowercase
    return w.lower() in most_common


frequent = {k: v for k, v in definitions.items() if is_common(k)}

# Save to CSV
with open("words.csv", "w") as f:
    w = csv.writer(f)
    # Save in random order
    for k in random.sample(list(frequent), len(frequent)):
        w.writerow([k, frequent[k]])
