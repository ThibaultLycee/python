import math
import tkinter as tk

##################################
#   KEYCODES
##################################

keyCodes = {
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    'arrow_up': 38,
    'arrow_down': 40,
    'arrow_left': 37,
    'arrow_right': 39
}

##################################
#   CLASSES
##################################

class Matrice:
    def __init__(self, matrice):
        self.matrice = matrice
    
    def __repr__(self):
        return str(self.matrice)

    def __getitem__(self, idx):
        return self.matrice[idx]
    
    def __mul__(self, other):
        if not self.isCompatible(other): return self

        width, height = len(other[0]), len(self)

        result = []

        for Y in range(height):
            line = []
            for X in range(width):
                val = 0
                for x in range(len(self[0])):
                    val += self[Y][x] * other[x][X]
                line.append(val)
            result.append(line)
        
        return Matrice(result)

    def __len__(self):
        return len(self.matrice)

    def isCompatible(self, other):
        return len(self[0]) == len(other)
    
    def getCoord2d(self):
        return {'x': self[0][0], 'y': self[1][0]}

    def getCoord3d(self):
        return {'x': self[0][0], 'y': self[1][0], 'z': self[2][0]}

class Stack:
    def __init__(self):
        self.stack = []
        self.index = -1
    
    def addElement(self, z, miniZ, val):
        self.stack.append((z, miniZ, val))
    
    def sort(self):
        self.stack = sorted(self.stack, key=lambda e: (e[0], -e[1]))
    
    def getElementsInOrder(self, sort=True):
        if sort: self.sort()
        return [val for idx, z, val in self.stack]
    
    def __getitem__(self, idx):
        return self.stack[idx][2]

    def __len__(self):
        return len(self.stack)

    def __iter__(self):
        return self
    
    def __next__(self):
        self.index += 1
        if self.index >= len(self):
            self.index = -1
            raise StopIteration
        else:
            return self[self.index]

class Window(tk.Tk):
    def __init__(self, width, height):
        tk.Tk.__init__(self)

        self.height = height
        self.width = width
        self.canvasOriginX = 0
        self.canvasOriginY = 0
        self.sceneScale = 1

        self.title('3d Rendering')
        self.geometry(f'{width}x{height}')

        self.objs = []
        self.renderingOrder = Stack()

        self.makeCanvas()

        self.bind("<Key>", self.keyListener)

        self.settings = {
            'fillTriangles': False,
            'areAxisDrawn': False,
            'renderVertices': True,
            'renderLinks': True,
            'showVerticesCoords': False,
            'renderBoxesBoundaries': False
        }

    def changeSetting(self, name, state):
        if name in self.settings.keys():
            self.settings[name] = state

    def keyListener(self, event):
        if event.keycode == keyCodes['arrow_up']: self.rotateScene(1, math.pi / 250)
        if event.keycode == keyCodes['arrow_down']: self.rotateScene(1, -math.pi / 250)
        if event.keycode == keyCodes['arrow_left']: self.rotateScene(2, -math.pi / 250)
        if event.keycode == keyCodes['arrow_right']: self.rotateScene(2, math.pi / 250)
        if event.keycode == keyCodes['z']: self.rescaleScene(.01)
        if event.keycode == keyCodes['s']: self.rescaleScene(-.01)

    def drawAxis(self):
        self.settings['areAxisDrawn'] = True
        for name, axis in Axis.items():
            self.objs.insert(0, axis)

    def rotateScene(self, axis, angle):
        if self.settings['areAxisDrawn']:
            for obj in self.objs[3:]:
                obj.rotate(axis, angle)
        else:
            for obj in self.objs:
                obj.rotate(axis, angle)
        self.render()
    
    def rescaleScene(self, scl):
        self.sceneScale += scl
        for obj in self.objs:
            obj.scale(self.sceneScale, self.sceneScale, self.sceneScale)
        self.render()

    def makeCanvas(self):
        self.canvas = tk.Canvas(self, bg='sky blue', height=self.height, width=self.width)
        self.canvas.pack(expand=True)
    
    def translateCanvas(self, x, y):
        self.canvasOriginX = x
        self.canvasOriginY = y
    
    def renderObj(self, obj):
        points, links, col, majorLinks = obj.calculateRendering()

        if isinstance(obj, Triangle) and self.settings['fillTriangles']:
            pts = []
            for name, coord in points.items():
                coord = coord.getCoord2d()
                pts.append((coord['x'] + self.canvasOriginX, coord['y'] + self.canvasOriginY))
            
            self.canvas.create_polygon(pts[0], pts[1], pts[2], fill=col['fill'], outline=None)

        if self.settings['renderLinks']:
            for link in links:
                self.canvas.create_line(
                    points[link[0]][0][0] + self.canvasOriginX, points[link[0]][1][0] + self.canvasOriginY,
                    points[link[1]][0][0] + self.canvasOriginX, points[link[1]][1][0] + self.canvasOriginY,
                    width=1, fill=col['links']
                )
        
        if isinstance(obj, Triangle) and self.settings['renderBoxesBoundaries']:
            for link in majorLinks:
                self.canvas.create_line(
                    points[link[0]][0][0] + self.canvasOriginX, points[link[0]][1][0] + self.canvasOriginY,
                    points[link[1]][0][0] + self.canvasOriginX, points[link[1]][1][0] + self.canvasOriginY,
                    width=1, fill=col['links']
                )

        if self.settings['renderVertices']:
            for name, coord in points.items():
                coord = coord.getCoord2d()
                self.canvas.create_oval(
                    coord['x'] - 3 + self.canvasOriginX, coord['y'] - 3 + self.canvasOriginY,
                    coord['x'] + 3 + self.canvasOriginX, coord['y'] + 3 + self.canvasOriginY,
                    outline=col['points'], fill=col['points']
                )
        
        if self.settings['showVerticesCoords']:
            for name, coord in points.items():
                coord = coord.getCoord2d()
                self.canvas.create_text(coord['x'] + self.canvasOriginX + 10, coord['y'] + self.canvasOriginY + 10, text=f'x:{int(coord["x"])}, y:{int(coord["y"])}')

    def render(self):
        self.canvas.delete('all')
        del self.renderingOrder
        self.renderingOrder = Stack()
        for obj in self.objs:
            if isinstance(obj, Line3):
                z, miniZ = obj.getMedianZ()
                self.renderingOrder.addElement(z, miniZ, obj)
            elif isinstance(obj, Cube):
                for triangle in obj.getTriangles():
                    z, miniZ = triangle.getMedianZ()
                    self.renderingOrder.addElement(z, miniZ, triangle)
        
        self.renderingOrder.sort()
        for obj in self.renderingOrder:
            self.renderObj(obj)
    
    def addToScene(self, obj):
        self.objs.append(obj)

class Line3:
    def __init__(self, a, b, linkColor='black', pointsColor=None, rotX=0, rotY=0, rotZ=0):
        self.points = {
            'a': a,
            'b': b
        }
        self.links = ['ab']
        self.linkColor = linkColor
        self.pointsColor = pointsColor
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scaleX = 1
        self.scaleY = 1
        self.scaleZ = 1

    def scale(self, x=1, y=1, z=1):
        self.scaleX = x
        self.scaleY = y
        self.scaleZ = z

    def getMedianZ(self):
        medianZ = 0
        miniZ = None
        for name, pt in self.points.items():
            rotX = makeRotationMatrice(self.rotX, 1)
            rotY = makeRotationMatrice(self.rotY, 2)
            rotZ = makeRotationMatrice(self.rotZ, 3)
            currentZ = (rotX * rotY * rotZ * pt).getCoord3d()['z']
            medianZ += currentZ
            if miniZ == None or currentZ < miniZ: miniZ = currentZ
        medianZ /= len(self.points)
        return medianZ, miniZ

    def calculateRendering(self):
        return {
            name: makeScaleMatrice(self.scaleX, self.scaleY, self.scaleZ) * makeRotationMatrice(self.rotX, 1) * makeRotationMatrice(self.rotY, 2) * makeRotationMatrice(self.rotZ, 3) * patternMatrice * point for name, point in self.points.items()
        }, self.links, {
            'links': self.linkColor, 'points': self.pointsColor, 'fill': None
        }

class Triangle:
    def __init__(self, a, b, c, linksColor='black', pointsColor='red', fillColor='black', rotX=0, rotY=0, rotZ=0):
        self.points = {
            'a': a,
            'b': b,
            'c': c
        }
        self.links = ['ab', 'ac', 'bc']
        self.linksColor = linksColor
        self.pointsColor = pointsColor
        self.fillColor = fillColor
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.medianZ = None
        self.scaleX = 1
        self.scaleY = 1
        self.scaleZ = 1
        self.majorLinks = ['ab', 'bc']

    def scale(self, x=1, y=1, z=1):
        self.scaleX = x
        self.scaleY = y
        self.scaleZ = z
    
    def getMedianZ(self):
        medianZ = 0
        miniZ = None
        for name, pt in self.points.items():
            rotX = makeRotationMatrice(self.rotX, 1)
            rotY = makeRotationMatrice(self.rotY, 2)
            rotZ = makeRotationMatrice(self.rotZ, 3)
            currentZ = (rotX * rotY * rotZ * pt).getCoord3d()['z']
            medianZ += currentZ
            if miniZ == None or currentZ < miniZ: miniZ = currentZ
        medianZ /= len(self.points)
        return medianZ, miniZ

    def rotate(self, axis, angle):
        if axis == 1: self.rotX = cap(self.rotX + angle, 4 * math.pi)
        elif axis == 2: self.rotY = cap(self.rotY + angle, 4 * math.pi)
        elif axis == 3: self.rotZ = cap(self.rotZ + angle, 4 * math.pi)

    def calculateRendering(self):
        return {
			name: makeScaleMatrice(self.scaleX, self.scaleY, self.scaleZ) * makeRotationMatrice(self.rotX, 1) * makeRotationMatrice(self.rotY, 2) * makeRotationMatrice(self.rotZ, 3) * patternMatrice * point for name, point in self.points.items()
		}, self.links, {
            'links': self.linksColor, 'points': self.pointsColor, 'fill': self.fillColor
        }, self.majorLinks

class Cube:
    def __init__(self, a, b, rotX=0, rotY=0, rotZ=0, linkColor='black', pointsColor=None, facesColor=None):
        self.linkColor = linkColor
        self.pointsColor = pointsColor

        if facesColor == None:
            self.facesColor = [
                'grey',
                'grey',
                'grey',
                'grey',
                'grey',
                'grey'
            ]
        else:
            self.facesColor = facesColor

        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ

        self.constructPoints(a, b)
        self.constructTriangles()

    def constructPoints(self, a, b):
        self.points = {
			'a': a,
			'b': Matrice([[a.getCoord3d()['x']], [a.getCoord3d()['y']], [b.getCoord3d()['z']]]),
			'c': Matrice([[a.getCoord3d()['x']], [b.getCoord3d()['y']], [a.getCoord3d()['z']]]),
			'd': Matrice([[a.getCoord3d()['x']], [b.getCoord3d()['y']], [b.getCoord3d()['z']]]),
			'e': Matrice([[b.getCoord3d()['x']], [a.getCoord3d()['y']], [a.getCoord3d()['z']]]),
			'f': Matrice([[b.getCoord3d()['x']], [a.getCoord3d()['y']], [b.getCoord3d()['z']]]),
			'g': Matrice([[b.getCoord3d()['x']], [b.getCoord3d()['y']], [a.getCoord3d()['z']]]),
			'h': b
		}
    
    def constructTriangles(self):
        self.triangles = {
            1:  Triangle(self.points['c'], self.points['a'], self.points['e'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[0]),
            2:  Triangle(self.points['c'], self.points['g'], self.points['e'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[0]),
			3:  Triangle(self.points['e'], self.points['g'], self.points['h'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[1]),
			4:  Triangle(self.points['e'], self.points['f'], self.points['h'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[1]),
			5:  Triangle(self.points['h'], self.points['f'], self.points['b'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[2]),
			6:  Triangle(self.points['h'], self.points['d'], self.points['b'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[2]),
			7:  Triangle(self.points['b'], self.points['d'], self.points['c'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[3]),
			8:  Triangle(self.points['b'], self.points['a'], self.points['c'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[3]),
			9:  Triangle(self.points['b'], self.points['a'], self.points['e'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[4]),
			10: Triangle(self.points['b'], self.points['f'], self.points['e'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[4]),
			11: Triangle(self.points['c'], self.points['d'], self.points['h'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[5]),
			12: Triangle(self.points['c'], self.points['g'], self.points['h'], rotX=self.rotX, rotY=self.rotY, rotZ=self.rotZ, linksColor=self.linkColor, pointsColor=self.pointsColor, fillColor=self.facesColor[5])
		}

    def scale(self, x=1, y=1, z=1):
        for name, triangle in self.triangles.items():
            triangle.scale(x, y, z)

    def getTriangles(self):
        return [triangle for name, triangle in self.triangles.items()]

    def printPointsCoord(self):
        for name, point in self.points.items():
            print(f'{name} :\t{point}')
            print('-------------------')
        
    def rotate(self, axis=1, angle=0):
        for name, triangle in self.triangles.items():
            triangle.rotate(axis, angle)

##################################
#   CONSTANTS
##################################

Axis = {
	'x': Line3(Matrice([[1000], [0], [0]]), Matrice([[0], [0], [0]]), linkColor='green'),
	'y': Line3(Matrice([[0], [1000], [0]]), Matrice([[0], [0], [0]]), linkColor='black'),
	'z': Line3(Matrice([[0], [0], [1000]]), Matrice([[0], [0], [0]]), linkColor='purple'),
}

patternMatrice = Matrice([
    [1, 0, 0],
    [0, 1, 0]
])

AxisNames = {
	'X': 1,
	'Y': 2,
	'Z': 3
}

##################################
#   FUNCTIONS
##################################

def makeRotationMatrice(angle, axis):
	if axis == 1:
		return Matrice([
					[1, 0, 0],
					[0, math.cos(angle), -math.sin(angle)],
					[0, math.sin(angle), math.cos(angle)]
				])
	if axis == 2:
		return Matrice([
					[math.cos(angle), 0, math.sin(angle)],
					[0, 1, 0],
					[-math.sin(angle), 0, math.cos(angle)]
				])
	if axis == 3:
		return Matrice([
					[math.cos(angle), -math.sin(angle), 0],
					[math.sin(angle), math.cos(angle), 0],
					[0, 0, 1]
				])

def makeScaleMatrice(x=1, y=1, z=1):
    return Matrice([
        [x, 0, 0],
        [0, y, 0],
        [0, 0, z]
    ])

def cap(x, maxi):
	return x % maxi