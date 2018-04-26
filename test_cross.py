from groDrawer import *

x = Point(0, 1.0)
y = Point(0, -1.0)
z = Point(1.0, 0)
w = Point(-1.0, 0)

drawer = Canvas()
drawer.drawLine(y, x)
drawer.drawLine(z, w)

p = drawer.codegen()

print(p)
