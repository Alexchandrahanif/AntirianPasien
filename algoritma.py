def sequenceExists(main, seq):
    for i in range(len(main) - 1):
        if main[i] == seq[0] and main[i+1] == seq[1]:
            return True
    return False


main = [20, 7, 8, 10, 2, 5, 6]
print(sequenceExists(main, [7, 8]))
print(sequenceExists(main, [8, 7]))
print(sequenceExists(main, [7, 10]))
