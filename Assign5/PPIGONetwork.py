from CliqueNetwork import CliqueNetwork
from os.path import exists

class Protein:
	def __init__(self, name):
		self.name = name
		self.GOs = []
		
	def getName(self):
		return self.name
	
	def addGOTerm(self, term):
		self.GOs.append(term)
	
	def size(self):
		return len(self.GOs)

class PPIGONetwork:
	"""
	Comment
	"""
	def __init__(self, ppi_file, uniprot_file, go_file):
		self.ppi = CliqueNetwork(ppi_file, "")
		self.mapping = dict()
		self.initMapping(uniprot_file)

	def initMapping(self, uniprot_file):
		if exists(uniprot_file):
			# "with" closes the file again after reading 
			counter = 0
			with open(uniprot_file) as openfile:
				for line in openfile:
					# get entries of a line as list
					content = line[0:(len(line)-1)].split("\t")
					variants = content[4].split(" ")
					self.mapping[content[0]] = variants
					if (counter  < 10):
						print content[0]
						print variants
						counter = counter + 1
		else:
			print(filename, "does not exist")
		
	def assignGOTerms(self, go_file):
		if exists(go_file):
			# "with" closes the file again after reading 
			counter = 0
			with open(go_file) as openfile:
				for line in openfile:
					# get entries of a line as list
					content = line[0:(len(line)-1)].split("\t")
					#if content[0] == "UniProtKB" and len(content) >:
		
	def size(self):
		return self.ppi.size()
