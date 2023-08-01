s = open("data/data.txt", "r")

s = s.read().replace("\n", "")

with open("data/new_data.txt", "w") as x:
    x.write(s)
