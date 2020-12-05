file = open("log.txt", "r+")

lines = file.readlines()
data = []
for line in lines:
    parts = line.split(";")
    time = float(parts[0])
    x,y = parts[1].split(",")
    vis = {"x":float(x), "y":float(y)}
    h,v = parts[2].split(",")
    hat = {"h":int(h), "v":int(v)}
    cir,squ,tri,dx = parts[3].split(",")
    dpad= {"circle":int(cir),
           "square":int(squ),
           "triangle":int(tri),
           "x":int(dx)}
    hL, hR, hD = parts[4].split(",")
    held = {"heldL":int(hL),
            "heldR":int(hR),
            "heldD":int(hD)}
    val = {"time":time,
           "vis":vis,
           "hat": hat,
           "dpad": dpad,
           "held": held}
    data.append(val)

print(data)