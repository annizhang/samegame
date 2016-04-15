# hw10.py
# Anni Zhang + anniz + C

from __future__ import with_statement
import os
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
import copy

def rgbString(red, green, blue):
	# used to create custom colors
    return "#%02x%02x%02x" % (red, green, blue)

#custom colors
pastelGreen = rgbString(141,204,185)
pastelBlue = rgbString(171,225,253)
peachy = rgbString(254,209,190)
pastelSun = rgbString(255,234,155)
periwinkle = rgbString(222,222,255)
limeGreen = rgbString(188,240,162)
prettyBlue = rgbString(135,179,255)
pinkish = rgbString(242,156,151)
weirdPurple = rgbString(228,189,255)
rainGray = rgbString(200,194,204)
outlineColor = rgbString(47,47,47)
win = rgbString(251,173,227)
background = rgbString(255,245,231)
time = rgbString(165,216,153)

class sameGame(EventBasedAnimationClass):
	def __init__(self, rows, cols, numColors):
		super(sameGame, self).__init__(1000, 700)
		self.rows = rows
		self.cols = cols
		self.numColors = numColors 
		minSide = min(self.width,self.height)
		self.dotDiameter = minSide/((max(self.rows,self.cols))+1)
		self.xMargin = ((self.width)-(self.dotDiameter * self.cols))/2
		self.yMargin = ((self.height)-(self.dotDiameter * self.rows))/2
		#FROM LECTURE NOTES:
		# creates a tempDir if there's no tempdir and highScore is None
		# if theres a tempdir then the highScore is whatever is stored
		path = "tempDir" + os.sep + "sameGameHighScore.txt"
		if (not os.path.exists("tempDir")):
			os.makedirs("tempDir")
			contents = "None"
			self.writeFile(path, contents)
			self.highScore = self.readFile(path)
		elif (os.path.exists(path)):
			self.highScore = self.readFile(path)


	def onTimerFired(self):
		# self.time subtracts by 1 and once it reaches -1 it returns to 5
		# if game is over timer stops
		if self.gameOver == True:
			pass
		else:
			if self.time > -1:
				self.time -= 1
				if self.time == -1:
					self.time = 5
					if self.score >= 20:
						self.score -=20

	def onKeyPressed(self, event):
		# r to restart
		if event.char == "r":
			self.initAnimation()

	def onMousePressed(self, event):
		# the highlighted section gets set to none
		# cascade happens after mouse click
		(self.mouseX, self.mouseY) = (event.x, event.y)
		if (self.mouseX >= self.xMargin and 
			self.mouseX < self.width-self.xMargin and
			self.mouseY >= self.yMargin and 
			self.mouseY < self.height-self.yMargin):
			# if the clicked location is inside the board
			(clickedRow, clickedCol) = self.findDot()
			if (clickedRow, clickedCol) in self.selected:
				self.removeDots(clickedRow, clickedCol) #removes dots from board
				self.time = 5 # timer restarts
				self.cascade() # cascades
				self.gameOver = self.isFinished() 
				# checks if there are no more options
				if self.gameOver:
					# if game is over, compares high score to currentscore
					if (self.highScore == "None" or 
						self.score > int(self.highScore)):
						# then the high score file is replaced with a new file
						# that has the new high score and sets new high score
						path = "tempDir" + os.sep + "sameGameHighScore.txt"
						os.remove(path)
						contents = str(self.score)
						self.writeFile(path, contents)
						self.highScore = self.readFile(path)


	def isFinished(self):
		# checks if the board is finished and there are no more moves left
		result = []
		for row in xrange(self.rows):
			for col in xrange(self.cols):
				if self.board[row][col] != None:
					num = self.board[row][col]
					intermediate = self.selectGroup(row, col, num, [])
					result += [intermediate]
		for row in xrange(len(result)):
			if result[row] != []:
				return False
		return True

	def removeDots(self, row, col):
		# removes the highlighted dots and adds to score
		for dot in self.selected:
			row = dot[0]
			col = dot[1]
			self.board[row][col] = None
			# score is 3 times the amount of removed dots
			self.score += (len(self.selected))*3
		self.selected = []

	def removeRepitition(self, a):
		# specific helper function
		# looks in a 2D list and if an inner list is only composed of None,
		# removes the list
		# used in cascading
		b = copy.deepcopy(a)
		for item in a:
			count = 0 
			for num in item:
				if num == None:
					count += 1
			if count == len(item):
				# if all the items in the sublist is None
				b.remove(item)
				b.append([None] * self.cols)
		return b

	def cascade(self):
		# first cascades down then cascades left, looks through the board and 
		# if there is a col with Nones in it, adds the values of the col to a 
		# new list which is used to replace the col, similar with going left
		tempColList = []
		for col in xrange(self.cols):
			currentCol = []
			for row in xrange(self.rows):
				if self.board[row][col] != None:
					currentCol += [self.board[row][col]]
			tempColList += [currentCol]
		tempColList = self.removeRepitition(tempColList)
		for col in xrange(self.cols):
			for revIndex in xrange(self.rows-1,-1, -1):
				rdiff = self.rows - len(tempColList[col])
				if rdiff == 0:
					self.board[revIndex][col] = tempColList[col][revIndex]
				elif revIndex - rdiff >= 0:
					self.board[revIndex][col] = tempColList[col][revIndex-rdiff]
				else:
					self.board[revIndex][col] = None


	def onMotion(self, event):
		# when mouse over a group of same colors, they are added to a list
		# this list is later used to draw the highlight 
		(self.x, self.y) = (event.x, event.y)
		if (self.x >= self.xMargin and self.x < self.width-self.xMargin and
			self.y >= self.yMargin and self.y < self.height-self.yMargin):
			(dotRow, dotCol) = self.findDot()
			if self.board[dotRow][dotCol] != None:
				num = self.board[dotRow][dotCol]
				self.selected = self.selectGroup(dotRow, dotCol, num, [])
			elif self.board[dotRow][dotCol] ==None:
				self.selected = []
		else:
			self.selected = []
		self.redrawAll()
		
	def selectGroup(self, row, col, num, visited):
		# recursive function that looks for the same number in the board and
		# returns the list of their coordinates
		if (row, col) in visited:
			if len(visited) > 1:
				return visited
			else:
				return []
		elif (row >= 0 and row < self.rows and 
			col >= 0 and col < self.cols):
			if self.board[row][col] == num:
				# self.groupCoord += [(row, col)]
				visited += [(row, col)]
				self.selectGroup(row-1, col, num, visited)
				self.selectGroup(row+1, col, num, visited)
				self.selectGroup(row, col-1, num, visited)
				self.selectGroup(row, col+1, num, visited)
		if len(visited) > 1:
			return visited
		else: return []


	def findDot(self):
		# used to select dots
		# to find col:
		dotCol = int(float((self.x-self.xMargin)/self.dotDiameter))
		# to find row:
		dotRow = int(float((self.y-self.yMargin)/self.dotDiameter))
		return (dotRow, dotCol)

	def redrawAll(self):
		# redraws all
		self.canvas.delete(ALL)
		self.drawBoard()
		self.drawScore()
		self.drawTime()
		if self.gameOver == True:
			self.drawOverMsg()
		self.drawHighScore()
		self.drawInstruction()

	def drawHighScore(self):
		# draws the high score
		x0 = self.xMargin/2
		y0 = self.height/3
		y1 = self.height/3.5
		self.canvas.create_text(x0, y1, text="HIGH SCORE:",
			fill=win, font = "Arial 20 bold")
		self.canvas.create_text(x0,y0,text=self.highScore, 
			fill=win, font="Arial 20 bold")
	
	def drawTime(self):
		# draws the timer
		x0 = self.width-self.xMargin/2
		y0 = self.height/20
		x1 = x0
		y1 = self.height/12
		self.canvas.create_text(x0, y0, anchor=N,text="TIME:", 
			fill=time,font="Arial %s bold" % str(self.height/30))
		self.canvas.create_text(x1,y1,anchor=N, text=self.time,
			fill=time, font="Arial %s bold" % str(self.height/30))

	def drawInstruction(self):
		# draws the instruction on the side
		x0 = self.width-self.xMargin/2
		y0 = self.height/3.5
		self.canvas.create_text(x0,y0,text="PRESS R TO RESTART", fill=time, 
			font="Arial %s bold" % str(self.height/50))

	def drawScore(self):
		# draws the current score
		x0 = self.xMargin/2
		y0 = self.height/20
		x1 = self.xMargin/2
		y1 = self.height/12
		self.canvas.create_text(x0,y0,anchor=N, text="SCORE:", 
			fill=win,font="Arial %s bold" % str(self.height/30))
		self.canvas.create_text(x1, y1, anchor =N, text=self.score,
			fill=win, font="Arial %s bold" % str(self.height/30))

	def drawOverMsg(self):
		# draws the game over message
		x0 = self.width/2
		y0 = self.height/2
		self.canvas.create_text(x0, y0, text="GAME OVER", 
			fill=win, font="Arial %s bold" % str(self.height/5))

	def drawBoard(self):
		# draws the dots
		x0 = 0
		y0 = 0
		x1 = 1.1*self.width
		y1 = 1.1*self.height
		self.canvas.create_rectangle(x0,y0,x1,y1,fill=background, width=0)
		for row in xrange(self.rows):
			for col in xrange(self.cols):
				if (row, col) not in self.selected:
					self.drawDot(row, col)
				else:
					self.drawSelected(row, col)

	def drawSelected(self, row, col):
		# draws the highlight for the selected region
		x0 = (self.xMargin + col*self.dotDiameter) + self.dotDiameter/6
		y0 = (self.yMargin + row*self.dotDiameter) + self.dotDiameter/6
		x1 = (self.xMargin + (col+1)*self.dotDiameter) - self.dotDiameter/6
		y1 = (self.yMargin + (row+1)*self.dotDiameter) - self.dotDiameter/6
		colorIndex = self.board[row][col]
		if colorIndex != None:
			self.canvas.create_oval(x0, y0, x1, y1,fill=self.colors[colorIndex],
				width=self.dotDiameter/7, outline=outlineColor)

	def drawDot(self, row, col):
		# draws each dot, their number in the board is the color index
		x0 = self.xMargin + col*self.dotDiameter
		y0 = self.yMargin + row*self.dotDiameter
		x1 = self.xMargin + (col+1)*self.dotDiameter
		y1 = self.yMargin + (row+1)*self.dotDiameter
		colorIndex = self.board[row][col]
		if colorIndex != None:
			self.canvas.create_oval(x0, y0, x1, y1,fill=self.colors[colorIndex], 
				width=0)

	def readFile(self,filename, mode="rt"):
		# from notes in lecture
	    # rt = "read text"
	    with open(filename, mode) as fin:
	        return fin.read()

	def writeFile(self,filename, contents, mode="wt"):
		# from notes in lecture
	    # wt = "write text"
	    with open(filename, mode) as fout:
	        fout.write(contents)

	def initAnimation(self):
		self.timerDelay = 1000
		self.colors = [pastelGreen, pastelBlue, peachy, pastelSun, periwinkle,
		limeGreen, prettyBlue, pinkish, weirdPurple, rainGray]
		# the list of colors is shuffled so everytime random colors are selected
		random.shuffle(self.colors)
		self.selected = []
		self.board = []
		# we start with a 2D list of Nones
		for row in xrange(self.rows):
			self.board.append(self.cols * [None])
		self.setColors()
		self.gameOver = False
		self.canvas.bind("<Motion>", lambda event: self.onMotion(event))
		self.score = 0 
		self.time = 5
		
	def setColors(self):
		# for each dot in the board sets a number,which is used to set the color
		# of each dot
		for row in xrange(self.rows):
			for col in xrange(self.cols):
				self.board[row][col] = random.randint(0, self.numColors-1)

def playSameGame(rows, cols, numColors):
	Game = sameGame(rows,cols, numColors)
	Game.run()




 




