xmax = 1200.0
xmin = 550.0
xdiff = xmax-xmin

ymax = 600.0
ymin = 0.0
ydiff = 600
def translate_x(x):
    return (x-xmin) / xdiff

def translate_y(y):
    return (y-ymin) / ydiff

print(translate_x(1140))