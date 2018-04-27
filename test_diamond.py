from groDrawer import *

a = Point(0, -1.0)
b = Point(-1.0, 0)
c = Point(0, 1.0)
d = Point(1.0, 0)

drawer = Canvas()
drawer.drawLine(a, b, die_outer=True)
drawer.drawLine(b, c, die_outer=True)
drawer.drawLine(c, d, die_outer=True)
drawer.drawLine(d, a, die_outer=True)

p = drawer.codegen()

print(p)
