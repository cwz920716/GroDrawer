from groDrawer import *

x = Point(0, 1.0)
y = Point(0, -1.0)

drawer = Canvas()
drawer.drawLine(y, x)

p = drawer.codegen()

print(p)
