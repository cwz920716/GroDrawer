from groDrawer import *

x = Point(-0.667, 0.333)
y = Point(0.333, -0.667)
z = Point(0.333, 0.333)

drawer = Canvas()
drawer.drawLine(y, x, color="cyan", die_outer=True)
drawer.drawLine(z, y, color="red", die_outer=True)
drawer.drawLine(x, z, die_outer=True)

p = drawer.codegen()

print(p)
