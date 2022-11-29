import pygame
import sys

pygame.mixer.init() #initialize mixer to load clicking sound 
clickSound = pygame.mixer.Sound("click.mp3") # load the click sound

class button():
	'''Creates an interactive button in pygame. Inspired by/references the button class
	made by Tech with Tim [https://www.youtube.com/watch?v=4_9twnEduFA] '''
        
	def __init__(self, x,y,width,height, text=''):
		'''Creates a button using the parameters of desired x and y positions for location of
		the button, width of the surface to draw onto, height of the surface to draw onto, and an optional
		parameter of text label. This does not draw the button onto the surface. Does not return.'''
		self.color = (106,90,205) # color RGB values 
		self.color2 = (72, 209, 204)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text

	def draw(self, screen, outline=True):
		'''Draws the constructed button onto the surface. Takes the parameter of surface to draw onto and
		an optional parameter of outlining the button, which is defaulted to True. Does not return.'''
                #Call this method to draw the button on the screen
		if outline: 
			pygame.draw.rect(screen, (255,255,255), (self.x-2,self.y-2,self.width+4,self.height+4),0,10) # creates the outline for the button (white)

		pygame.draw.rect(screen, self.color,(self.x,self.y,self.width,self.height),0,10)

		if self.text != '':
			font = pygame.font.SysFont('Corbel', 45)
			text = font.render(self.text, 1, (255,255,255)) # white color 
			screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))) # draw onto the screen
			# this line of code is set up such that the text will be centered inside the button 

	def isOver(self, screen, event, pos):
		'''Makes the drawn button responsive to user activity. If the coordinates of the user's mouse
		is over the button, the color will change, and then return to the original color once the mouse
		is no longer over the button. Takes the parameters of surface to draw onto, pygame event, and position
		of mouse. Does not return.'''
			#Pos is the mouse position or a tuple of (x,y) coordinates
		if event.type == pygame.MOUSEMOTION: # if the event type is the mouse moving then: 
			if (self.x < pos[0] < self.x + self.width) and (self.y < pos[1] < self.y + self.height):
				self.color = ((0,0,0)) # if the mouse is over the button, then change the color to black
				
			else:
				self.color = (106,90,205)
				
			self.draw(screen)

	def isClicked(self, screen, event, pos):
		'''Registers if the user clicks on the button. Has a clicking sound effect if the button is clicked.
		Takes the parameters of surface the button is drawn on, pygame event, and mouse position.
		Returns true if clicked. Returns false is not clicked. '''
		#Pos is the mouse position or a tuple of (x,y) coordinates
		if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse is clicked 
			if (self.x < pos[0] < self.x + self.width) and (self.y < pos[1] < self.y + self.height): # if the click position 
				self.color = ((255,130,255)) # change the color to pink 
				self.draw(screen)
				clickSound.play() # play the click sound 
				return True # returns True if clicked 

			return False # return False if clicked but not within the button 

