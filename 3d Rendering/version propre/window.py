import classes

A = [
	[-500],
	[-50],
	[-50]
]

B = [
	[500],
	[50],
	[50]
]

C = [
	[-500],
	[-75],
	[-75]
]

D = [
	[-600],
	[-75],
	[-75]
]

facesColor = [
	'brown',
	'brown',
	'brown',
	'brown',
	'brown',
	'brown'
]

cube1 = classes.Cube(classes.Matrice(A), classes.Matrice(B), pointsColor='red', facesColor=facesColor)
cube2 = classes.Cube(classes.Matrice(C), classes.Matrice(D), facesColor=facesColor)

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
