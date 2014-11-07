#! /usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import time
import AlienTilesProblem

class Tile(Button) :
#η κλάση που θα αναπαριστά κάθε tile στο παράθυρο
	def __init__(self, master, maxcolor = 4):
		self.maxcolor = maxcolor
		self.b_isenabled = True
		Button.__init__(self, master)

	def advcolor(self):
		#με κάθε κλικ το χρώμα θα αυξάνεται κατά ένα, ώστε να μπορούμε να ορίσουμε ό,τι καταστάσεις αρχής και στόχου θέλουμε
		self.setcolor((self.color + 1 ) % self.maxcolor)
		
	def setcolor(self, color):
		self.color = color
		self["bg"] = ["red","green","blue","purple"][color]
		#ορισμός χρώματος
		
	def reset(self):
		self["state"] = "normal"
		self.setcolor(0)
		self.b_isenabled = True
		
	def disable(self):
		self["state"] = "disabled"
		self["bg"] = "grey"
		self.b_isenabled = False
		#απενεργοποίηση του κουμπιού
		
	def getcolor(self):
		return self.color
		
	def isenabled(self):
		return self.b_isenabled

class Application(Frame):
	def createWidgets(self):
		#άδεια label για να δημιουργούνται κενά μεταξύ των στοιχείων του παραθύρου
		Label(self, width = 1).grid(column = 0, row = 0, columnspan = 1)
		Label(self, width = 1).grid(column = 0, row = 10, columnspan = 1)
		Label(self, height = 1).grid(column = 0, row = 180, rowspan = 1)
		Label(self, height = 1).grid(column = 0, row = 200, rowspan = 1)
		Label(self, width = 1).grid(column = 159, row = 0, rowspan = 1)
		Label(self, width = 1).grid(column = 170, row = 0, rowspan = 1)
		Label(self, width = 10).grid(column = 100, row = 0, columnspan = 3)
		Label(self, text = "Start state").grid(column = 50, row = 40, columnspan = 3)
		Label(self, text = "End state").grid(column = 150, row = 40, columnspan = 3)
		Label(self, text = "    Presets:    ").grid(column = 160, row = 50, columnspan = 3)
		Button(self, width = 8, text = "About", command = lambda: tkMessageBox.showinfo("About","""
Created by sdi1000103 using Tkinter, tkMessageBox and time libraries
Click on the tiles to define a start and end state
and click "Run A* search" to start the algorithm
Symmetric states will not be checked if the checkbox is checked
Main loop will be blocked while the search is running
Once a solution is found it will be displayed
on the bottom of the window
and the start state will change to match the end state
while simulating the steps taken
A click will be simulated every second
Each click will be displayed in the format (x,y) (meaning we clicked on the x-th tile from the left, y-th tile from the top)
You can change the problem size by resetting the problem with a new size (default size 3)
Click on the preset buttons to change the end state to one of the presets
AI is hard
""")).grid(column = 160, row = 1, columnspan = 3)
		#κουμπί about
		self.useheuristic = StringVar(self)
		self.useheuristic.set("Heuristic 1")
		OptionMenu(self, self.useheuristic, "Heuristic 1", "Heuristic 2", "Heuristic 3").grid(column = 70, row = 1, columnspan = 5)
		Button(self, width = 12, text = "Run A* search", command = self.run).grid(column = 50, row = 1, columnspan = 5)
		#κουμπί που τρέχει τον αλγόριθμο
		Button(self, width = 8, text = "All Green", command = lambda: self.setpreset(0)).grid(column = 160, row = 51, columnspan = 3)
		Button(self, width = 8, text = "All Blue", command = lambda: self.setpreset(1)).grid(column = 160, row = 52, columnspan = 3)
		Button(self, width = 8, text = "All Purple", command = lambda: self.setpreset(2)).grid(column = 160, row = 53, columnspan = 3)
		#κουμπιά που αλλάζουν την κατάσταση στόχου σε προκαθορισμένες καταστάσεις
		Label(self, text = "Reset with size: ").grid(column = 150, row = 1, columnspan = 4)
		self.symmchecked = BooleanVar()
		chkb = Checkbutton(self, width = 18, text = "Use symmetry breaking", onvalue = True, offvalue = False, variable = self.symmchecked)
		chkb.select()
		chkb.grid(column = 50, row = 10, columnspan = 18)
		self.es = Entry(self, width = 2)
		self.es.insert(0,'3')
		self.es.grid(column = 154, row = 1, columnspan = 1)
		self.solsteps = Entry(self, width = 100)
		self.solsteps.grid(column = 50, row = 190, columnspan = 110)
		#entry όπου θα γράφεται η λύση αφού βρεθεί
		Button(self, text = "Reset", command = self.resetproc).grid(column = 155, row = 1, columnspan = 2)
		#κουμπί που κάνει reset (και αλλάζει το μέγεθος του προβλήματος)
		
		for i in range(0,7):
			for l in range(0,7):
				t = Tile(self)
				if i > 2 or l > 2:
					t.disable()
				else:	
					t.setcolor(0)
				t["command"] = t.advcolor
				t["padx"] = 14
				t.grid(column = i + 50,row = l + 50)
				self.startstate[i].append(t)
				#δημιουργία κουμπιών που απεικονίζουν την αρχική κατάσταση
		
		for i in range(0,7):
			for l in range(0,7):
				t = Tile(self)
				if i > 2 or l > 2:
					t.disable()
				else:	
					t.setcolor(1)
				t["command"] = t.advcolor
				t["padx"] = 14
				t.grid(column = i + 150, row = l + 50)
				self.endstate[i].append(t)
				#δημιουργία κουμπιών που απεικονίζουν την κατάσταση στόχου

	def __init__(self, master=None):
		Frame.__init__(self, master)
		master.title("Alien Tiles")
		self.startstate = [[] for i in range(0,7)]
		self.endstate = [[] for i in range(0,7)]
		self.pack()
		self.probsize = 3
		self.createWidgets()
	
	def resetproc(self):
		if not self.es.get().isdigit():
			tkMessageBox.showinfo("Error", "Size needs to be a number")
		else:
			newsize = int(self.es.get())
			if newsize not in range(1,8):
				tkMessageBox.showinfo("Error", "Size needs to be between 1 and 7")
			else:
				self.probsize = newsize
				for i in range(0,7):
					for l in range(0,7):
						#κάνουμε reset όλα τα tiles
						if i < newsize and l < newsize:
							self.startstate[i][l].reset()
							self.endstate[i][l].reset()
						else:
							#αν τα tiles είναι εκτός του πίνακα με μέγεθος newsize τα απενεργοποιούμε
							self.startstate[i][l].disable()
							self.endstate[i][l].disable()
							
	def run(self):
		startstate = [[] for i in range(0, self.probsize)]
		endstate = [[] for i in range(0, self.probsize)]
		for i in range(0, self.probsize):
			for l in range(0, self.probsize):
				startstate[i].append(self.startstate[i][l].getcolor())
				endstate[i].append(self.endstate[i][l].getcolor())
				#φτιάχνουμε τις λίστες που θα περάσουμε στον αλγόριθμο του BlocksWorldProblem.py
		started = time.clock()
		#μετράμε την ώρα εκκίνησης
		if self.useheuristic.get() == "Heuristic 1" :
			heuristic = 0
		elif self.useheuristic.get() == "Heuristic 2" :
			heuristic = 1
		else :
			heuristic = 2
		#επιλέγουμε ευρετική ανάλογα με την επιλογή στο OptionMenu
		solution = AlienTilesProblem.SolveProblem(startstate, endstate, self.probsize, usesymmetry = [False, True][self.symmchecked.get()], useheuristic = heuristic)
		#καλούμε τον αλγόριθμο
		if solution is None:
			tkMessageBox.showinfo("Alien Tiles", "No solution found! Target must be unreachable")
		else:
			self.solsteps.delete(0, END)
			self.solsteps.insert(0, "Clicks to solution: " + str(solution.solution()))
			#γράφουμε την λύση στο entry field του παραθύρου
			tkMessageBox.showinfo("Alien Tiles", "Solution found in " + str(time.clock() - started) + " seconds! Steps will now be simulated")
			self.simulation(solution.path(), 0)
			#ξεκινάμε την προσομοίωση
	
	def simulation(self, solutionnodes, stepnum):
		#θα απεικονίσουμε την κατάσταση στη θέση stepnum της λίστας solutionnodes, η οποία περιέχει τις καταστάσεις προς τη λύση
		for i in range(0, self.probsize):
			for l in range(0, self.probsize):
				self.startstate[i][l].setcolor(solutionnodes[stepnum].state[i][l])
				#αλλάζουμε τον αριστερό πίνακα του παραθύρου για να δείξουμε τη μετάβαση απ την αρχική κατάσταση στο στόχο
		if (stepnum < len(solutionnodes) - 1):
			self.after(1000, lambda: self.simulation(solutionnodes, stepnum + 1))
		#λέμε στο παράθυρο να ξανακαλέσει αυτή τη συνάρτηση μετά από 1000 ms με το stepnum αυξημένο κατά 1
		#(αν δεν έχουμε φτάσει στο τέλος)
	
	def setpreset(self, presetnum):
		if presetnum >= 0 and presetnum <= 2:
			for i in range(0,7):
				for l in range(0,7):
					if self.endstate[i][l].isenabled():
						self.endstate[i][l].setcolor(presetnum + 1)
						#αλλάζουμε τα χρώματα των κουμπιών σε presetnum + 1
						#(αφού η παράμετρος που περνιέται απ το κουμπί είναι 0 για όλα πράσινα, 1 για μπλε, 2 για μωβ)
						
root = Tk()
app = Application(master=root)
#δημιουργία παραθύρου
app.mainloop()
#message loop παραθύρου
root.destroy()
