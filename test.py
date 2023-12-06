CURVE = 0.4
MIN_BRIGHT = 15
LUX = 200

for x in range(401):

  print(int(((255-MIN_BRIGHT)*((x/400)**CURVE))+MIN_BRIGHT))