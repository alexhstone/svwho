def wildcard(name):
    # Split the name into a list of words
    words = name.split()

    # Loop through each word and replace the characters between the first and last letter with %
    for i in range(len(words)):
        for i in range(len(words)):
            if len(words[i]) > 3:
                words[i] = words[i][:2] + "%"*(len(words[i])-3) + words[i][-1]

    # Join the words back together into a sentence
    guess = " ".join(words)

    return guess