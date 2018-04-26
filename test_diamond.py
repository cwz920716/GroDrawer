from groDrawer import *

a = Point(1.0, 0)
b = Point(0, 1.0)
c = Point(-1.0, 0)
d = Point(0, -1.0)

drawer = Canvas()
drawer.drawLine(a, b)
drawer.drawLine(b, c)
drawer.drawLine(c, d)
drawer.drawLine(d, a)

p = drawer.codegen()

print(p)
