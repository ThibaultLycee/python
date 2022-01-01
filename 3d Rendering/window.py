import classes

A = [
	[-100],
	[-100],
	[-100]
]

B = [
	[100],
	[100],
	[100]
]

C = [
	[100],
	[100],
	[100]
]

D = [
	[200],
	[200],
	[300]
]

facesColor = [
	'red',
	'blue',
	'orange',
	'green',
	'yellow',
	'white'
]

cube1 = classes.Cube(classes.Matrice(A), classes.Matrice(B), pointsColor='red', facesColor=facesColor)
cube2 = classes.Cube(classes.Matrice(C), classes.Matrice(D), pointsColor='red', facesColor=facesColor)

w = classes.Window(1080, 740)
w.changeSetting('fillTriangles', True)
w.changeSetting('renderVertices', False)
w.changeSetting('renderLinks', False)
w.changeSetting('renderBoxesBoundaries', True)
w.changeSetting('showVerticesCoords', False)

#w.drawAxis()

w.translateCanvas(540, 360)
w.addToScene(cube1)
w.addToScene(cube2)

w.render()
w.mainloop()
