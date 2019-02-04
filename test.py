import difflib

print (difflib.get_close_matches ('appel', ['ape', 'apple', 'peach', 'puppy']))
print (difflib.get_close_matches ('shami', ['sha', 'mi', 'shmikapoor', 'jack']))


collection = [1,2,3,4]
print (collection)

def test(word):
    if word in collection:
        return collection[word]

print (test(1))
print (test(5))