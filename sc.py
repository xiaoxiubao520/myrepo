with open("1.txt") as f:
    for i in f.read().splitlines():
        par = i.strip().split("&")[2]
        task = par[7:]
        print(task)