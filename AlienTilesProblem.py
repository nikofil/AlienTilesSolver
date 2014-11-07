#! /usr/bin/python
# -*- coding: utf-8 -*-

from search import *

class tuple_sym(tuple) :
	def __init__(self, listp) :
		counter = 0
		for i in self:
			for l in i:
				counter += 50**l
		#για hash ενός πίνακα, αθροίζουμε 50 υψωμένο στην τιμή κάθε tile
		#έτσι, ακόμα και ένας πίνακας με 49 άσους θα έχει μικρότερη τιμή από έναν με ένα δυάρι
		#και τα hash 2 πινάκων με διαφορετικά στοιχεία θα είναι πιο δύσκολα ίδια
		self.hashv = counter
		#το αποθηκέυουμε για να μην χρειάζεται να το ξαναυπολογίσουμε
		super(tuple_sym, self).__init__(listp)
	
	def __hash__(self) :
		return self.hashv
	
	def allsort(self) :
		sortedlist = zip(*sorted(zip(*self)))
		#δίνοντας στη zip πχ 2 λίστες με ν στοιχεία αυτή θα μας δώσει ένα tuple που μέσα θα έχει ν λίστες, η καθεμία με 2 στοιχεία
		#τα οποία θα είναι τα στοιχεία που βρίσκονταν στις ίδιες θέσεις στις 2 λίστες που δώσαμε
		#οπότε κάνοντας zip(*self) δημιουργείται ένα tuple από λίστες που ουσιαστικά είναι η αντανάκλαση του tuple που περάσαμε
		#κάνοντάς sort αυτό, ουσιαστικά έχουμε κάνει sort τις σειρές του tuple που δώσαμε
		#μετά ξανακάνουμε zip για να ξαναγίνει η ανάκλαση
		return sorted(sortedlist)
		#κάνουμε sort ώστε να σορταριστούν και οι στήλες
	
	def __eq__(self, other) :
		#στο πρόβλημα alien tiles πολλές καταστάσεις είναι συμμετρικές, δηλαδή φτάνουν στη λύση με παρόμοιες κινήσεις
		#η σειρά των στήλων και των γραμμών δεν έχει σημασία, αφού αν τους αλλάξουμε θέσεις η λύση είναι παρόμοια
		#το να κάνουμε πχ κλικ στο στοιχείο (χ,ψ) είναι ισοδύναμο του να ανταλλάξουμε τη γραμμή ψ με μια άλλη γραμμή ζ
		#και να κάνουμε κλικ στο στοιχείο (χ,ζ)
		#παρόμοια με τις στήλες
		#επομένως 2 καταστάσεις που έχουν ίδιες γραμμές ή στήλες αλλά σε άλλη σειρά θέλουν ίδιο αριθμό κλικ για να φτάσουν το στόχο
		#απλώς τα κλικ θα πρέπει να είναι στις αντίστοιχες γραμμές και στήλες κάθε κατάστασης
		#γι αυτό το λόγο μπορούμε να χρησιμοποιήσουμε την allsort
		#για να κάνουμε sort πρώτα τις γραμμές και μετά τις στήλες μιας κατάστασης
		#και να ελέγξουμε αν είναι ισοδύναμη με μια άλλη
		#στην περίπτωση που είναι δεν χρειάζεται να ελέγξουμε και τις 2 οπότε μπορούμε να τις θεωρήσουμε ίσες
		if hash(self) != hash(other):
			return False
		sortedself = self.allsort()
		sortedother = other.allsort()
		if sortedself == sortedother or zip(*sortedself) == sortedother:
			#παρόμοια 2 καταστάσεις που η μία είναι αντανάκλαση της άλλης πάνω από τη διαγώνιο
			return True
		return False

class AlienTilesProblem(Problem) :
	def __init__(self, startarray, endarray, probsize, colornumber, usesymmetry) :
		self.colornumber = colornumber
		self.probsize = probsize
		self.usesymm = usesymmetry
		startstate = [tuple(x) for x in startarray]
		endstate = [tuple(x) for x in endarray]
		#κάνουμε tuple τα startarray, endarray
		if usesymmetry:
			super(AlienTilesProblem, self).__init__(tuple_sym(startstate), tuple_sym(endstate))
			#αν θέλουμε να μην υπολογίζονται συμμετρικές καταστάσεις χρησιμοποιούμε την tuple_sym που ορίζεται παραπάνω
		else:
			super(AlienTilesProblem, self).__init__(tuple(startstate), tuple(endstate))
			#αλλιώς χρησιμοποιούμε κανονική tuple
		
	def actions(self, state) :
		for x in range(0, self.probsize) :
			for y in range(0, self.probsize) :
				yield (x,y)
				#δίνουμε όλα τα πιθανά κλικ
					
	def result(self, state, action) :
		x, y = action
		newstate = []
		for i in range(0,self.probsize):
			#περνάμε από κάθε στήλη
			if i == x:
				#αν είναι η στήλη που έγινε το κλικ αυξάνουμε όλα τα στοιχεία κατά 1
				newstate.append( tuple( [(c + 1) % self.colornumber for c in state[i]] ) )
			else:
				#αν είναι άλλη στήλη ενώνουμε τα στοιχεία πριν τη γραμμή του κλικ, το στοιχείο στη γραμμή που έγινε κλικ + 1
				#και τα στοιχεία μετά τη γραμμή του κλικ για να φτιάξουμε ένα νέο tuple
				newstate.append( state[i][:y] + tuple([(state[i][y] + 1) % self.colornumber],) + state[i][y+1:] )
		if self.usesymm:
			return tuple_sym(newstate)
		else:
			return tuple(newstate)
	
	def h1(self, node) :
		crossx, crossy = (0,0)
		counter = 0
		diff = [[(self.goal[i][l] - node.state[i][l]) % 4 for l in range(0, self.probsize)] for i in range(0, self.probsize)]
		#διαφορά μεταξύ κατάστασης και στόχου
		while True:
			bestcrossvalue = 0
			bestnonzerovalue = 0
			for i in range(0,self.probsize):
				for l in range(0,self.probsize):
					temp, tempnonzero = self.findcrossval(diff, i, l)
					if tempnonzero > bestnonzerovalue or (tempnonzero == bestnonzerovalue and temp > bestcrossvalue):
						#σε κάθε επανάληψη βρίσκουμε το κλικ που αλλάζει τα περισσότερα κουτιά με τιμή > 0
						#σε περίπτωση ισοπαλίας διαλέγουμε αυτό που αλλάζει τα κουτιά με μεγαλύτερη συνολική τιμή
						bestcrossvalue = temp
						bestnonzerovalue = tempnonzero
						crossx = i
						crossy = l
			counter += 1
			
			if bestnonzerovalue == 0:
				break
			#αν ο πίνακας diff είναι μηδενικός
			diff[crossx][crossy] += 1
			for x in range(0, self.probsize):
				if diff[x][crossy] > 0:
					diff[x][crossy] -= 1
				if diff[crossx][x] > 0:
					diff[crossx][x] -= 1
				#μειώνουμε τα κουτιά στη γραμμή και τη στήλη του κάθε κλικ
		
		return counter
		
	def h2(self, node) :
		diff = [[(self.goal[i][l] - node.state[i][l]) % 4 for l in range(0, self.probsize)] for i in range(0, self.probsize)]
		counter = 0
		for i in range(0, self.probsize) :
			for l in range(0, self.probsize) :
				counter += diff[i][l]
				#προσθέτουμε τη διαφορά κάθε tile από το στόχο του
		if counter % (2 * self.probsize - 1) == 0 :
			return counter / (2 * self.probsize - 1)
		else :
			return counter / (2 * self.probsize - 1) + 1
			#αν κάθε κλικ είναι βέλτιστο και αλλάζει όσα περισσότερα κουτάκια γίνεται προς το καλύτερο, θα χρειαστούν counter/(2n-1) (στρογγυλοποιημένο προς τα πάνω)
	
	def h3(self, node) : #πιο γρήγορη αλλά μη παραδεκτή
		crossx, crossy = (0,0)
		counter = 0
		diff = [[(self.goal[i][l] - node.state[i][l]) % 4 for l in range(0, self.probsize)] for i in range(0, self.probsize)]
		#παρομοίως με την h1
		while True:
			bestcrossvalue = 0
			bestnonzerovalue = 0
			for i in range(0,self.probsize):
				for l in range(0,self.probsize):
					temp, tempnonzero = self.findcrossval(diff, i, l)
					if tempnonzero > bestnonzerovalue or (tempnonzero == bestnonzerovalue and temp > bestcrossvalue):
						bestcrossvalue = temp
						bestnonzerovalue = tempnonzero
						crossx = i
						crossy = l
			counter += 1
			
			if bestnonzerovalue < self.probsize:
				break
			#δε σταματάμε όταν ο πίνακας diff είναι μηδενικός, αλλά όταν ένα κλικ έχει περισσότερα μηδενικά παρά μη-μηδενικά στην ίδια γραμμή και στήλη
			
			diff[crossx][crossy] += 1
			for x in range(0, self.probsize):
				if diff[x][crossy] > 0:
					diff[x][crossy] -= 1
				if diff[crossx][x] > 0:
					diff[crossx][x] -= 1
		
		for i in range(0,self.probsize):
			for l in range(0,self.probsize):
				counter += diff[i][l]
			#αφού σταματήσουμε την επανάληψη, μετράμε πόσα κουτιά είναι μη μηδενικά και προσθέτουμε ένα κλικ για καθένα
			#με αυτόν τον τρόπο μπορεί να υπερεκτιμήσουμε τα κλικ, αλλά συνήθως η εκτίμηση είναι πιο κοντά στην πραγματικότητα
		return counter
		
	def findcrossval(self, diff, i, l):
		val = 0
		nonzero = 0
		for x in range(0, self.probsize):
			if diff[x][l] > 0:
				val += diff[x][l]
				nonzero += 1
			else:
				val -= 1
				
			if diff[i][x] > 0:
				val += diff[i][x]
				nonzero += 1
			else:
				val -= 1
				
			#βρίσκουμε πόσα μη-μηδενικά και το άθροισμα των κουτιών σε μια γραμμή και στήλη
		if diff[i][l] > 0:
			nonzero -= 1
		val -= diff[i][l]
		#έχουμε προσθέσει το diff[i][l] 2 φορές, οπότε το αφαιρούμε μία
		return (val, nonzero)

def SolveProblem(start, end, probsize, colornumber = 4, usesymmetry = True, useheuristic = 0):
	if usesymmetry :
		for i in range(0, probsize) :
			for l in range(0, probsize) :
				if start[i][l] != start[0][0] or end[i][l] != end[0][0] :
					usesymmetry = False
					break
	#δεν μπορούμε να χρησιμοποιήσουμε συμμετρία αν δεν είναι ίδια όλα τα χρώματα στις καταστάσεις αρχής και τέλους
	print "\nSize = ", probsize, " - Symmetry = ", usesymmetry, " - Heuristic = ", useheuristic
	p = AlienTilesProblem(start, end, probsize, colornumber, usesymmetry)
	return astar_search(p, [p.h1, p.h2, p.h3][useheuristic])