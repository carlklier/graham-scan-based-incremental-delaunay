from point import *
from random import randrange
import pyglet
from pyglet import shapes
from pyglet.window import key,mouse
from grahamscandelaunay import *
W,H = 1280, 720
window =pyglet.window.Window(W,H)

def pt_1(p):
    shapes.Circle(p[0],p[1],5,segments=12,color=(100,0,0)).draw()
def pt_2(p):
    shapes.Circle(p[0],p[1],5,segments=12,color=(200,0,0)).draw()
def line(a,b):
    shapes.Line(a[0],a[1],b[0],b[1],width=4,color=(0,0,0)).draw()
def randpt():
    margin = 100
    return  Point(randrange(margin,W-margin),randrange(margin,H-margin))

V = []
ready=False

@window.event
def on_mouse_press(x,y,button,modifiers):
    if button == mouse.LEFT:
        V.append(Point(x,y))

@window.event
def on_key_press(symbol,modifiers):
    global state
    global ready
    global stepofthealgorithm
    if symbol == key.S:
        g = GrahamScanDelaunay(V)
        stepofthealgorithm = g.run()
        state = next(stepofthealgorithm)
        ready= True
    if symbol == key.SPACE:
        try:
            state = next(stepofthealgorithm)
            print("NEXT")
        except StopIteration:
            print("STOP")
            pass

@window.event
def on_draw():
    shapes.Rectangle(0,0,W,H,(255,255,255)).draw()
    for v in V:
        pt_1(v)
    if ready:
        for halfedge in state:
            pt_2(halfedge.point)
            line(halfedge.point,halfedge.link.point)

pyglet.app.run()
