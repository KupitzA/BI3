from CliqueNetwork import CliqueNetwork
from os.path import exists
import sys

class Protein:
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
	def __init__(self):
		# key:name  = Protein
		self.mapping = dict()
	
	def existsAccession(self, accession):
		if accession in self.mapping.keys():
			return True
		else:
			return False
	def existsName(self, name):
		if name in self.mapping.keys():
			return True
		else:
			return False
	
	def getMainName(self, variant):
		for i in self.mapping.keys():
			if variant in self.mapping[i].getAlternatives():
				return i
		return variant
	
	def addProtein(self, name):
		self.mapping[name] = Protein(name)
		
	def addAlternatives(self, name, alternatives):
		if self.existsName(name):
			self.mapping[name].addAlternatives(alternatives)
	
	def addGOTerm(self, name, goterm):
		if self.existsName(name):
			self.mapping[name].addGOTerm(goterm)
			
	def show(self):
		counter = 1
		for i in self.mapping.keys():
			print str(counter) + ".\t-------------------------------------"
			self.mapping[i].show()
			counter = counter + 1
	
	def addAccession(self, name, accession):
		if self.existsName(name):
			self.mapping[name].setAccessionNumber(accession)
	
	
	def getKeys(self):
		return self.mapping.keys
		
	def sumNoAnnotation(self):
		summ = 0
		for i in self.mapping.keys():
			if len(self.mapping[i].getGOTerms()) == 0:
				summ = summ + 1
		return summ
	
	def rawDistribution(self):
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
		summ = dict()
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				summ[j] = 0
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				summ[j] = summ[j] + 1
		
		values = [sys.maxint,0,0]
		for i in summ.keys():
			temp = summ[i]
			if temp < values[0]:
				values[0] = temp
			if temp > values[2]:
				values[2] = temp
			values[1] = values[1] + temp
		
		values[1] = float(values[1])/float(len(summ.keys()))
		return values
	
	def extendedNumber(self, length, number):
		while len(number) < length:
			number = "0" + number
		return number
	
	def nMostFewestAnnotations(self, n):
		summ = dict()
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				summ[j] = 0
		for i in self.mapping.keys():
			terms = self.mapping[i].getGOTerms()
			for j in terms:
				summ[j] = summ[j] + 1
		
		sorter = dict()
		for i in summ.keys():
			key = self.extendedNumber(10, str(summ[i])) + i
			sorter[key] = [i, summ[i]]
		
		helping = []
		#fewest = []
		for i in sorter.keys():
			helping.append(i) ####[0]
		helping.sort()
		
		high = []
		low = []
		for i in helping[0:n]:
			low.append(sorter[i])
		for i in helping[(len(helping)-n):len(helping)]:
			high.append(sorter[i])
		return [high, low]
			
	
class PPIGONetwork:
	"""
	Comment
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
		self.assignGOTerms(go_file)

	def initializeMapping(self):
		for n in self.ppi.nodes:
			self.mapping.addProtein(n)
	
	def updateMappingNames(self, uniprot_file):
		if exists(uniprot_file):
			# "with" closes the file again after reading 
			counter = 0
			with open(uniprot_file) as openfile:
				for line in openfile:
					counter = counter + 1
					if counter% 10000 == 0:
						print "Reading line " + str(counter)
					# get entries of a line as list
					content = line[0:(len(line)-1)].split("\t")
					if len(content) >= 4:
						variants = content[4].split(" ")
						for temp in variants:
							self.mapping.addAlternatives(temp, variants)
		else:
			print(filename, "does not exist")
		
	def assignGOTerms(self, go_file):
		if exists(go_file):
			# "with" closes the file again after reading 
			counter = 0
			with open(go_file) as openfile:
				for line in openfile:
					counter = counter + 1
					if counter%10000 == 0:
						print "Reading line " + str(counter)
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
