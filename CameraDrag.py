###############################################################################
#             Camera Drag Controller | Template v 1.0 | UPBGE 0.2.3           #
###############################################################################
#                      Created by: Guilherme Teres Nunes                      #
#                       Access: youtube.com/UnidayStudio                      #
#                               github.com/UnidayStudio                       #
###############################################################################
# HOW TO USE IN YOUR PROJECTS:                                                #
# It's very easy to use: Just load this script into your .blend file (or paste#
# them in the same folder that your .blend is), select your camera (or an obj,#
# you decide) and attach them into the components (CameraDrag.CameraDrag).	  #
# 	It's very simple to configure:											  #
#	-> Show Mouse: Enable if you want to show the mouse						  #
#	-> Mouse Movement: Enable if you want to activate the mouse drag logic	  #
#	-> Keyboard Movement: Enable if you want to move the object using W,A,S,D #
#	-> Up Axis: Select the UP axis.											  #
#	-> Local Movement: Local or Global movement? You decide!				  #
#	-> Mouse Sensibility: The mouse sensibility! 							  #
#	-> Keyboard Speed: If you enabled the Keyboard Movement, control the speed#
#					   here!												  #
#	-> Limit Area: You can limit the area that the object can stay by playing #
#				   around with this values. If you don't want, just set to 0  #
###############################################################################
import bge
from mathutils import Vector

class CameraDrag(bge.types.KX_PythonComponent):
	args = {
		"Show Mouse"		: True,
		"Mouse Movement"	: True,
		"Keyboard Movement"	: True,
		"Up Axis"			: {"Z Axis", "Y Axis", "X Axis"},
		"Local Movement"	: False,
		"Mouse Sensibility"	: 10.5,
		"Keyboard Speed"	: 0.3,
		"Limit Area"		: Vector([0.0,0.0,0.0]),
	}

	# Start Function
	def start(self, args):
		self.hasMouseMovement = args["Mouse Movement"]
		self.hasKeyboardMovement = args["Keyboard Movement"]

		self.upAxis = {"X Axis":0, "Y Axis":1, "Z Axis":2}[args["Up Axis"]]
		self.localMovement = args["Local Movement"]
		self.sens = args["Mouse Sensibility"]*1000
		self.speed = args["Keyboard Speed"]

		self.hasAreaLimit = None
		if args["Limit Area"] != [0,0,0]:
			self.hasAreaLimit = args["Limit Area"]

		if args["Show Mouse"]:
			bge.render.showMouse(True)

		self.__lastMousePos = Vector([0,0])

	# Moves the object on the X axis (whatever axis this mean)
	def __moveX(self, value):
		vec = Vector([value,0,0])
		if self.upAxis == 0:
			vec = Vector([0, value, 0])
		self.object.applyMovement(vec*self.speed, self.localMovement)

	# Moves the object on the Y axis (whatever axis this mean)
	def __moveY(self, value):
		vec = Vector([0, value, 0])
		if self.upAxis == 0:
			vec = Vector([0, 0, value])
		self.object.applyMovement(vec * self.speed, self.localMovement)

	# Makes the object move with the keyboard (W,A,S,D keys)
	def keyboardMovement(self):
		keyboard = bge.logic.keyboard.inputs
		x = 0; y = 0

		if keyboard[bge.events.WKEY].values[-1]:	y = 1
		elif keyboard[bge.events.SKEY].values[-1]:	y = -1
		if keyboard[bge.events.AKEY].values[-1]:	x = -1
		elif keyboard[bge.events.DKEY].values[-1]:	x = 1

		self.__moveX(x)
		self.__moveY(y)

	# Makes the object move by clicking (LMB) and dragging the mouse
	def mouseMovement(self):
		mouse = bge.logic.mouse.inputs
		mPos = Vector(bge.logic.mouse.position)

		if mouse[bge.events.RIGHTMOUSE].values[-1]:
			# Mouse displacement since last frame
			mDisp = self.__lastMousePos - mPos
			mDisp *= self.sens # Apply Mouse sensibility
			self.__moveX(mDisp[0])
			self.__moveY(mDisp[1]*(-1))

		self.__lastMousePos = mPos

	# Limits the area that this object can stay. If you don't want this
	# limitation, just set the values to zero (0).
	def limitArea(self):
		for axis in range(3):
			if self.hasAreaLimit[axis] == 0:
				continue
			value = self.object.worldPosition[axis]
			if abs(value) > self.hasAreaLimit[axis]:
				final = self.hasAreaLimit[axis]*(value/abs(value))
				self.object.worldPosition[axis] = final

	# Update Function
	def update(self):
		if self.hasKeyboardMovement:
			self.keyboardMovement()
		if self.hasMouseMovement:
			self.mouseMovement()
		if self.hasAreaLimit != None:
			self.limitArea()