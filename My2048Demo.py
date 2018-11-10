
import pygame, sys
from pygame.locals import *
import random
import math
import time
import copy
import multiprocessing

LabelX = 0 #左上角的X座標
LabelY = 0 #左上角的Y座標

#FrontEnd TODO 
#把這些數值改成你想要的顏色跟位置
My2048Position = (50,80)
My2048Size = 55
backGroundColor = (55,57,58) #你想要的背景顏色
OutterGridColor = (113,117,119) #外圍的顏色
tileColor = (211,215,220) #每個方塊的顏色
TextColor = (155,61,18) #數字的顏色
HeaderTitleColor = (191,172,200) #標題的顏色(My2048的顏色)
TextFont = "Arial"

#可以上 https://coolors.co/ 找自己喜歡的顏色

#這四個參數是拿來紀錄上下左右鍵被按了幾次

Window_Width, Window_Height = (500,850)

text_size = 14
text_height = text_size
pygame.init()


DISPLAYSURF = pygame.display.set_mode((500, 850))
pygame.display.set_caption('2048')

class My2048:
	matrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	score = 0
	def __init__(self):
		
		numsToInsert = random.randint(1,2)
		if numsToInsert == 2:
			loc1 = random.randint(0,15)
			loc2 = random.randint(0,15)
			if loc2 == loc1:
				loc2 = random.randint(0,15)
			#print(loc2,"  ",loc1)
			for row in range(4):
				for col in range(4):
					if loc2 == 0:
						self.matrix[row][col] = random.randint(1,2) * 2
					if loc1 == 0:
						self.matrix[row][col] = random.randint(1,2) * 2
					loc2 -= 1
					loc1 -= 1
		if numsToInsert == 1:
			loc1 = random.randint(0,15)
			print(loc1)
			for row in range(4):
				for col in range(4):
					if loc1 == 0:
						self.matrix[row][col] = random.randint(1,2) * 2
					loc1 -= 1

	def align(self,direction):
		if direction == "left":
			for row in range(4):
				#to remove 0s in the array
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				for i in range(len(self.matrix[row])-1):
					if i < 0:
						break
					if self.matrix[row][i] == self.matrix[row][i+1]:
						#collapse
						self.matrix[row][i] += self.matrix[row][i]
						self.score += self.matrix[row][i]
						self.matrix[row][i+1] = 0
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				#insert back proper len
				for times in range(4-len(self.matrix[row])):
					self.matrix[row].append(0)
		if direction == "right":
			for row in range(4):
				#to remove 0s in the array
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				for i in range(len(self.matrix[row])-1,0,-1):
					if i < 0:
						break
					if self.matrix[row][i-1] == self.matrix[row][i]:
						self.score += self.matrix[row][i]
						#collapse
						self.matrix[row][i] += self.matrix[row][i]

						self.matrix[row][i-1] = 0
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				#insert back proper len
				for times in range(4-len(self.matrix[row])):
					self.matrix[row].insert(0,0)

		if direction == "up":
			TempMatrix = [[],[],[],[]]

			for col in range(3,-1,-1):
				for row in range(4):
					TempMatrix[3-col].append(self.matrix[row][col])
			for row in range(4):
				for col in range(4):
					self.matrix[row][col] = TempMatrix[row][col]
			for row in range(4):
				#to remove 0s in the array
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				for i in range(len(self.matrix[row])-1):
					if i < 0:
						break
					if self.matrix[row][i] == self.matrix[row][i+1]:
						self.score += self.matrix[row][i]
						#collapse
						self.matrix[row][i] += self.matrix[row][i]
						self.matrix[row][i+1] = 0
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				#insert back proper len
				for times in range(4-len(self.matrix[row])):
					self.matrix[row].append(0)
			for row in range(4):
				for col in range(4):
					TempMatrix[row][col] = self.matrix[row][col]

			for row in range(4):
				for col in range(4):
					self.matrix[col][row*(-1)+3] = TempMatrix[row][col]
		if direction == "down":
			TempMatrix = [[],[],[],[]]
			for col in range(3,-1,-1):
				for row in range(4):
					TempMatrix[3-col].append(self.matrix[row][col])
			for row in range(4):
				for col in range(4):
					self.matrix[row][col] = TempMatrix[row][col]
			for row in range(4):
				#to remove 0s in the array
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				for i in range(len(self.matrix[row])-1,0,-1):
					if i < 0:
						break
					if self.matrix[row][i-1] == self.matrix[row][i]:
						self.score += self.matrix[row][i]
						#collapse
						self.matrix[row][i] += self.matrix[row][i]
						self.matrix[row][i-1] = 0
				self.matrix[row] = [x for x in self.matrix[row] if x != 0]
				#insert back proper len
				for times in range(4-len(self.matrix[row])):
					self.matrix[row].insert(0,0)
			for row in range(4):
				for col in range(4):
					TempMatrix[row][col] = self.matrix[row][col]
			for row in range(4):
				for col in range(4):
					self.matrix[col][row*(-1)+3] = TempMatrix[row][col]
			#for row in range(4):
			#	for col in range(len(TempMatrix[row])):
			#		print(self.matrix[row][col], end=" ")
			#	print()
			#print("---------")
	def randomSpawn(self):
		# 如果想要一次有可能產生兩個數字，就把這段取消註解，還有適當的縮排
		# numsToInsert = random.randint(1,2)
		
		# if numsToInsert == 2:
		# 	emptyPos = []
		# 	for i in range(4):
		# 		for j in range(4):
		# 			if self.matrix[i][j] == 0 :
		# 				emptyPos.append(4*i+j)
		# 	loc1 = random.choice(emptyPos)
		# 	emptyPos.remove(loc1)
		# 	loc2 = random.choice(emptyPos)

		# 	for row in range(4):
		# 		for col in range(4):
		# 			if loc2 == 0:
		# 				self.matrix[row][col] = random.randint(1,2) * 2
		# 			if loc1 == 0:
		# 				self.matrix[row][col] = random.randint(1,2) * 2
		# 			loc2 -= 1
		# 			loc1 -= 1
		# if numsToInsert == 1:
		emptyPos = []
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 0 :
					emptyPos.append(4*i+j)
		if(len(emptyPos)==0):
			return
		loc1 = random.choice(emptyPos)

		for row in range(4):
			for col in range(4):
				if loc1 == 0:
					self.matrix[row][col] = random.randint(1,2) * 2
				loc1 -= 1
	def getScore(self):
		return self.score
	def checkGameOver(self):
		for i in range(4):
			for j in range(4):
				if(self.matrix[i][j]==0):
					return True
				if(i + 1 <=3):
					if(self.matrix[i][j]==self.matrix[i+1][j]):
						return True
				if(i-1 >=0):
					if(self.matrix[i][j]==self.matrix[i-1][j]):
						return True
				if(j+1 <= 3):
					if(self.matrix[i][j]==self.matrix[i][j+1]):
						return True
				if(j-1 >= 0):
					if(self.matrix[i][j]==self.matrix[i][j-1]):
						return True
		return False
	def checkMovable(self,dir):
		prev = copy.deepcopy(self)
		if(dir == 'l'):
			prev.align("left")
		if(dir == 'r'):
			prev.align("right")
		if(dir == 'u'):
			prev.align("up")
		if(dir == 'd'):
			prev.align("down")
		for i in range(4):
			for j in range(4):
				if(prev.matrix[i][j]!=self.matrix[i][j]):
					return True
		return False

X = My2048()


#----------這裡以下是拿來畫圖的function 不用會

def text_objects(text, font,color,BGC):
    textSurface = font.render(text, True, color,BGC)
    return textSurface, textSurface.get_rect()

def ClearText(Posx,Posy,rect):
	pygame.draw.rect(DISPLAYSURF,(155, 171, 198),(Posx,Posy,rect[2],rect[3])) #(x,y,width,height)

def ShowText(text,Posx,Posy,size,color,BGC):
	_MyFont = pygame.font.SysFont("Calibri",size)
	TextSurf, TextRect = text_objects(text,_MyFont,color,BGC)
	#print(TextRect)
	ClearText(Posx,Posy,TextRect)
	DISPLAYSURF.blit(TextSurf,(Posx,Posy))
	pygame.display.update()
	fontList = pygame.font.get_fonts()
	return TextSurf

	#(155, 171, 198)

DISPLAYSURF.fill(backGroundColor)
tilelist = [[],[],[],[]]


rect1 = Rect(Window_Width/2,Window_Height/2,Window_Width*7/8,Window_Height/2+5)
rect1.center = (Window_Width/2,Window_Height*5/8+25)
OutterGrid = pygame.draw.rect(DISPLAYSURF,OutterGridColor,rect1)

#this part is for drawing background grid



def drawGrid():
	line_Width = 5
	COLlist = []
	ROWlist = []
	COLlist.append(Rect(rect1[0]+math.ceil(rect1[3]/4)+1,rect1[1],line_Width,rect1[3]))
	COLlist.append(Rect(rect1[0]+math.ceil(rect1[3]/4)*2,rect1[1],line_Width,rect1[3]))
	COLlist.append(Rect(rect1[0]+math.ceil(rect1[3]/4)*3,rect1[1],line_Width,rect1[3]))
	ROWlist.append(Rect(rect1[0],rect1[1]+math.ceil(rect1[2]/4),rect1[2],line_Width))
	ROWlist.append(Rect(rect1[0],rect1[1]+math.ceil(rect1[2]/4)*2,rect1[2],line_Width))
	ROWlist.append(Rect(rect1[0],rect1[1]+math.ceil(rect1[2]/4)*3,rect1[2],line_Width))

	rect2 = Rect(Window_Width/2,Window_Height/2,Window_Width*7/8-20,Window_Height/2-13)
	rect2.center = (Window_Width/2,Window_Height*5/8+26)
	InnerGrid = pygame.draw.rect(DISPLAYSURF,tileColor,rect2)
	BAR1 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,ROWlist[0])
	BAR2 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,ROWlist[1])
	BAR3 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,ROWlist[2])
	BAR4 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,COLlist[0])
	BAR5 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,COLlist[1])
	BAR6 = pygame.draw.rect(DISPLAYSURF,OutterGridColor,COLlist[2])	
	#print_number()

	tileNumberColor = (104, 27, 18)
	tilelist[0].append(Rect(rect2.topleft[0]+(COLlist[0].topleft[0]-rect2.topleft[0])/2,rect2.topleft[1]+(ROWlist[0].topleft[1]-rect2.topleft[1])/2,4,4))
	for i in range(2):
		tilelist[0].append(Rect(COLlist[i].topright[0]+(COLlist[i+1].topright[0]-COLlist[i].topright[0])/2,rect2.topright[1]+(ROWlist[0].topleft[1]-rect2.topright[1])/2,4,4))
	tilelist[0].append(Rect(rect2.topright[0]-(rect2.topright[0]-COLlist[2].topright[0])/2,rect2.topright[1]+(ROWlist[0].topright[1]-rect2.topright[1])/2,4,4))

	tilelist[1].append(Rect(rect2.bottomleft[0]+(COLlist[0].topleft[0]-rect2.bottomleft[0])/2,ROWlist[0].bottomleft[1]+(ROWlist[1].topleft[1]-ROWlist[0].bottomleft[1])/2,4,4))
	for i in range(0,2):
		tilelist[1].append(Rect(COLlist[i].topright[0]+(COLlist[i+1].topleft[0]-COLlist[i].topright[0])/2,ROWlist[0].bottomleft[1]+(ROWlist[1].topleft[1]-ROWlist[0].bottomleft[1])/2,4,4))
	tilelist[1].append(Rect(rect2.topright[0]-(rect2.topright[0]-COLlist[2].topright[0])/2,ROWlist[0].bottomright[1]+(ROWlist[1].bottomright[1]-ROWlist[0].bottomright[1])/2,4,4))

	tilelist[2].append((rect2.bottomleft[0]+(COLlist[0].topleft[0]-rect2.bottomleft[0])/2,ROWlist[1].bottomleft[1]+(ROWlist[2].topleft[1]-ROWlist[1].bottomleft[1])/2,4,4))
	for i in range(0,2):
		tilelist[2].append(Rect(COLlist[i].topright[0]+(COLlist[i+1].topleft[0]-COLlist[i].topright[0])/2,ROWlist[1].bottomleft[1]+(ROWlist[2].topleft[1]-ROWlist[1].bottomleft[1])/2,4,4))
	tilelist[2].append(Rect(rect2.topright[0]-(rect2.topright[0]-COLlist[2].topright[0])/2,ROWlist[1].bottomright[1]+(ROWlist[2].bottomright[1]-ROWlist[1].bottomright[1])/2,4,4))

	tilelist[3].append(Rect(rect2.bottomleft[0]+(COLlist[0].topleft[0]-rect2.bottomleft[0])/2,rect2.bottomleft[1]-(rect2.bottomleft[1]-ROWlist[2].bottomleft[1])/2,4,4))
	for i in range(2):
		tilelist[3].append(Rect(COLlist[i].bottomright[0]+(COLlist[i+1].topright[0]-COLlist[i].topright[0])/2,rect2.bottomright[1]+(ROWlist[2].bottomleft[1]-rect2.bottomright[1])/2,4,4))
	tilelist[3].append(Rect(rect2.bottomright[0]-(rect2.bottomright[0]-COLlist[2].topright[0])/2,rect2.bottomright[1]+(ROWlist[2].bottomright[1]-rect2.bottomright[1])/2,4,4))
	
	scoreText = ShowText("SCORE",rect2.topright[0]-75,rect2.topright[1]-120,20,tileColor,backGroundColor)
	scoreBG = scoreText.get_rect()
	print(scoreBG.center)
	scoreBG[2] += 30
	scoreBG[3] += 20
	scoreBG.center = (rect2.topright[0]-90+scoreBG.center[0] , rect2.topright[1]-90 +scoreBG.center[1])
	hello = pygame.draw.rect(DISPLAYSURF,tileColor,scoreBG)	


	ShowText(str(X.score),scoreBG.center[0]-len(str(X.score))*7,scoreBG.center[1]-9,25,(0,0,0),tileColor)

drawGrid()
Numlist = [[],[],[],[]]
Numbers = []
for i in range(4):
	for j in range (4):
		Position = (tilelist[i][j][0]-4,tilelist[i][j][1]-4)
		Numlist[i].append(Position)
		if X.matrix[i][j] !=0:
			wordOffset = len(str(X.matrix[i][j]))*8.5
			Numbers.append(ShowText(str(X.matrix[i][j]),Numlist[i][j][0]-wordOffset,Numlist[i][j][1]-15,40,TextColor,tileColor))



def GameOver():
	_MyFont = pygame.font.SysFont(TextFont,90)
	textSurface = _MyFont.render("GAME OVER", True,(255,0,0) ,(tileColor))
	textSurface.set_alpha(200)
	DISPLAYSURF.blit(textSurface,(20,500))
	pygame.display.update()
	time.sleep(3)

def drawNumber():
	for i in range(4):
		for j in range (4):
			if X.matrix[i][j] !=0:
				wordOffset = len(str(X.matrix[i][j]))*8.5
				ShowText(str(X.matrix[i][j]),Numlist[i][j][0]-wordOffset,Numlist[i][j][1]-15,40,TextColor,tileColor)

ShowText("MY 2048 XD",My2048Position[0],My2048Position[1],My2048Size,HeaderTitleColor,(backGroundColor))


pygame.display.update()

#----------這裡以上是拿來畫圖的function 不用會

print(Window_Width,",",Window_Width)
NotGameOver = True
f = open("out.txt","w")

def forsee(mat,depth,lim):
	print(depth)
	dep = copy.deepcopy(depth)
	_limit = copy.deepcopy(lim)
	tempr = copy.deepcopy(mat)
	tempr.matrix = copy.deepcopy(mat.matrix)
	templ = copy.deepcopy(mat) 
	templ.matrix = copy.deepcopy(mat.matrix)
	tempu = copy.deepcopy(mat) 
	tempu.matrix = copy.deepcopy(mat.matrix)
	tempd = copy.deepcopy(mat) 
	tempd.matrix = copy.deepcopy(mat.matrix)

	templ.align("left")

	tempr.align("right")

	tempu.align("up")

	tempd.align("down")
	maxScore = 0
	direc = "n"
	direc2 = "n"
	if(dep >= _limit):
		dep -= 1
		return maxScore
	def probe(_matr,score):
		_scr = copy.deepcopy(score)
		for i in range(4):
			for j in range(4):
				if(_matr.matrix[i][j] == 0):
					_matr.matrix[i][j] = 2
					_scr = forsee(_matr,dep+1,_limit)
					if(_scr > maxScore):
						maxScore = _scr
						direc = "l"
					_matr.matrix[i][j] = 0
	probe(templ,maxScore)
	probe(tempr,maxScore)
	probe(tempu,maxScore)
	probe(tempd,maxScore)
	print("-----")

	if(dep == 1):
		print ("direction: ", direc)
		return direc
	return maxScore
	
while NotGameOver: # main game loop

	for getevent in pygame.event.get():
		pygame.event.pump()
		FORSEE = False
		keypress = False
		if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_RETURN:
    		
			DIR = forsee(X,1,3)
			FORSEE = True
			if DIR == "l":
				if(not X.checkMovable("l")):
					X.align("left")
					keypress = True
			if DIR == "r":
				if(not X.checkMovable("r")):
					X.align("right")
					keypress = True
			if DIR == "u":
				if(not X.checkMovable("u")):
					X.align("up")
					keypress = True
			if DIR == "d":
				if(not X.checkMovable("d")):
					X.align("down")
					keypress = True
		if getevent.type==QUIT:
			pygame.quit()
			sys.exit()
		
		if FORSEE == False:
			if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_LEFT:
				print("In left")
				if(not X.checkMovable("l")):
					X.align("left")
					keypress = True
			if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_RIGHT:
				if(not X.checkMovable("r")):
					X.align("right")
					keypress = True
			if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_UP:
				if(not X.checkMovable("u")):
					X.align("up")
					keypress = True
			if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_DOWN:
				if(not X.checkMovable("d")):
					X.align("down")
					keypress = True
		if(not X.checkGameOver()):
			GameOver()
			pygame.quit()
			sys.exit()
		if keypress == True:
			for row in range(4):
				for col in range(4):
					print(X.matrix[row][col], end = " " )
				print()
			print("---------")
			X.randomSpawn()
			drawGrid()
			drawNumber()
			pygame.display.update()
		if getevent.type == pygame.KEYDOWN and getevent.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()