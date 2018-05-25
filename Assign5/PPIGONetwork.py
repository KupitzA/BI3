from CliqueNetwork import CliqueNetwork
from os.path import exists
import sys

class Protein:
	"""
	Protein class: Storage for protein specific informations
	obtained by the network, uniprot and go-term-file
	"""
	def __init__(self, name):
		# storage for protein name (from PPI)
		self.name = name
		# storage for accession number from Go file
		self.accession = ""
		# storage for alternative names (uniprot)
		self.alternatives = set([name])
		# storage for go terms from go file
		self.GOs = set()
		
	# Getter
	def getName(self):
		return self.name
	def getAccessionNumber(self):
		return self.accession
	def getAlternatives(self):
		return self.alternatives
	def getGOTerms(self):
		return self.GOs
		
	# Setter
	def setName(self, name):
		self.name = name
	def setAccessionNumber(self, accession):
		self.accession = accession
	def addAlternatives(self, alternatives):
		for a in alternatives:
			self.alternatives.add(a)
	def addGOTerm(self, go):
		self.GOs.add(go)
	
	# terminal visualization
	def show(self):
		print "Name:\t\t" + self.name
		print "Accession Number:\t" + self.accession
		print "Alternative Names:"
		counter = 1
		for i in self.alternatives:
			print "\t" + str(counter) + "\t" + i
			counter = counter + 1
		print "GO Term Annotations:"
		counter = 1
		for i in self.GOs:
			print "\t" + str(counter) + "\t" + i
			counter = counter + 1


class Mapping:
	"""
	Mapping class: Stores protein objects and provides
	further functionality
	"""
	def __init__(self):
		"""
		key: protein name = Protein
		"""
		self.mapping = dict()
	
	def existsAccession(self, accession):
		"""
		Returns true if the mapping contains a protein with
		the given accession number
		"""
		for name in self.mapping.keys():
			if self.mapping[name].getAccessionNumber() == accession:
				return True
		return False
		
	def existsName(self, name):
		"""
		Returns true if the mapping contains a protein with
		the given name
		"""
		if name in self.mapping.keys():
			return True
		else:
			return False
	
	def getMainName(self, variant):
		"""
		Return the name of a protein for a given alternative name
		"""
		if self.existsName(variant):
			return variant
		for i in self.mapping.keys():
			if variant in self.mapping[i].getAlternatives():
				return i
		return variant
	
	def addProtein(self, name):
		"""
		Expand mapping by one protein with the given name
		"""
		self.mapping[name] = Protein(name)
		
	def addAlternatives(self, name, alternatives):
		"""
		Add an alternative name to the protein with the given name
		Return without action if the protein name does not exist
		"""
		if self.existsName(name):
			self.mapping[name].addAlternatives(alternatives)
	
	def addGOTerm(self, name, goterm):
		"""
		Add a go term to the protein with the given name.
		Return without action if the protein name does not exist
		"""
		if self.existsName(name):
			self.mapping[name].addGOTerm(goterm)
			
	def addAccession(self, name, accession):
		"""
		Add an accession number to the protein with the given name
		Return without action if the protein name does not exist
		"""
		if self.existsName(name):
			self.mapping[name].setAccessionNumber(accession)
	
	def show(self):
		"""
		Write proteines into the terminal
		"""
		counter = 1
		for i in self.mapping.keys():
			print str(counter) + ".\t-------------------------------------"
			self.mapping[i].show()
			counter = counter + 1
	
	def getKeys(self):
		"""
		Return mapping keys (in the end, these are the protein names)
		"""
		return self.mapping.keys
	
	# Exercise specific functions
		
	def sumNoAnnotation(self):
		"""
		Count proteins without go annotations
		"""
		summ = 0
		for i in self.mapping.keys():
			if len(self.mapping[i].getGOTerms()) == 0:
				summ += 1
		return summ
	
	def rawDistribution(self):
		"""
		Compute the minimal, average and maximal number
		of go annotations per gene
		"""
		values = [sys.maxint,0,0]
		for i in self.mapping.keys():
			annotations = len(self.mapping[i].getGOTerms())
			if annotations < values[0]:
				values[0] = annotations
			if annotations > values[2]:
				values[2] = annotations
			values[1] = values[1] + annotations
		values[1] = float(values[1])/float(len(self.mapping.keys()))
		return values
	
	def rawReverseDistribution(self):
		"""
		Compute the minimal, average and maximal number
		of proteins per go annotations
		"""
		# initialize dict (key: GO term, value: occurrence)
		# store it as field of the class to allow later access
		self.revsum = dict()
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				self.revsum[j] = 0
		# count occurrences
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				self.revsum[j] += + 1
		
		# evaluate minimum, average and maximum
		values = [sys.maxint,0,0]
		for i in self.revsum.keys():
			temp = self.revsum[i]
			if temp < values[0]:
				values[0] = temp
			if temp > values[2]:
				values[2] = temp
			values[1] = values[1] + temp
		values[1] = float(values[1])/float(len(self.revsum.keys()))
		return values
	
	def extendedNumber(self, length, number):
		"""
		Append zeros in front of a string, allows a lexicographical
		sorting of different sized numbers
		"""
		while len(number) < length:
			number = "0" + number
		return number
	
	def nMostFewestAnnotations(self, n):
		"""
		Returns the n most and n fewest annotated GO terms
		"""
		# create a dict, where the keys are a combination of occurrences
		# and GO terms (as string - allows easy sorting)
		sorter = dict()
		for i in self.revsum.keys():
			key = self.extendedNumber(10, str(self.revsum[i])) + i
			sorter[key] = (i, self.revsum[i])
		
		# sort the keys of the sorter dict in lexicographically increaing
		# order, at the same time the most occurring terms come to the end
		helping = []
		for i in sorter.keys():
			helping.append(i)
		helping.sort()
		
		# extract the n most and fewest common GO annotations
		high = []
		low = []
		for i in helping[0:n]:
			low.append(sorter[i])
		for i in helping[(len(helping)-n):len(helping)]:
			high.append(sorter[i])
		return [high, low]
			
	
class PPIGONetwork:
	"""
	Performs part a b c of exercise 5.2
	"""
	def __init__(self, ppi_file, uniprot_file, go_file):
		# read in ppi network
		print "1. Create Network"
		self.ppi = CliqueNetwork(ppi_file, "")
		# create mapping of protein informations
		print "2. Initialize Mapping"
		self.mapping = Mapping()
		self.initializeMapping()
		print "3. Assign Alternative Names"
		self.updateMappingNames(uniprot_file)
		print "4. Assign Go terms"
		self.assignGOTerms(go_file)
		print "Initialization completed"

	def initializeMapping(self):
		"""
		Transfere network proteins into mapping
		"""
		for n in self.ppi.nodes:
			self.mapping.addProtein(n)
	
	def updateMappingNames(self, uniprot_file):
		"""
		Read in uniprot file to extend mapping with alternative
		protein names
		"""
		if exists(uniprot_file):
			with open(uniprot_file) as openfile:
				for line in openfile:
					# get entries of a line as list
					content = line[0:(len(line)-1)].split("\t")
					if len(content) >= 4:
						variants = content[4].split(" ")
						for temp in variants:
							self.mapping.addAlternatives(temp, variants)
		else:
			print(filename, "does not exist")
		
	def assignGOTerms(self, go_file):
		"""
		Extend mapping with GO terms of GO term file
		Add accession number to proteins
		"""
		if exists(go_file):
			# "with" closes the file again after reading 
			with open(go_file) as openfile:
				for line in openfile:
					# get entries of a line as list
					content = line[0:(len(line)-1)].split("\t")
					#content = [x for x in content if x != ""]
					if content[0] == "UniProtKB" and len(content) > 8:
						if content[8] == "P":
							temp = self.mapping.getMainName(content[2])
							self.mapping.addGOTerm(temp, content[4])
							self.mapping.addAccession(temp, content[1])
							
	def size(self):
		return self.ppi.size()

	def overview(self):
		"""
		Output information required for subtasks a b c
		"""
		print "--------------------- Overview ---------------------"
		print "Total number of proteins:\t\t\t" + str(self.ppi.size())
		print "Total number of protein interactions:\t\t" + str(self.ppi.numLinks())
		no = self.mapping.sumNoAnnotation()
		percent = (float(no)/float(self.ppi.size()))*100.0
		print "Number of proteines without GO annotation:\t" + str(no) + " (" + str(percent) + "%)"
		distr = self.mapping.rawDistribution()
		print "Smallest number of GO annotations per protein\t" + str(distr[0])
		print "Average number of GO annotations per protein\t" + str(distr[1])
		print "Highest number of GO annotations per protein\t" + str(distr[2])
		distr = self.mapping.rawReverseDistribution()
		print "Smallest number of proteins per GO annotations\t" + str(distr[0])
		print "Average number of proteins per GO annotations\t" + str(distr[1])
		print "Highest number of proteins per GO annotations\t" + str(distr[2])
		temp = self.mapping.nMostFewestAnnotations(5)
		print "5 most annotated GO terms:\t" + str(temp[0])
		print "5 fewest annotated GO terms:\t" + str(temp[1])
