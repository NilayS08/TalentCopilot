text = input("Enter a String:")

words = text.split()
frequency = {}

for word in words:
    frequency[word] = frequency.get(word, 0) + 1

else:
    max_count = max(frequency.values())
    print(max_count)