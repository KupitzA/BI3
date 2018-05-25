from PPIGONetwork import PPIGONetwork

# 5.2 (a) (1)
print "Start program"
net = PPIGONetwork("pig_network.tsv", "pig_uniprot.tsv", "pig_GO.gaf")
net.overview()
