from PPIGONetwork import PPIGONetwork

# 5.2 (a) (1)
print "Start program"
net = PPIGONetwork("human_network.tsv", "human_uniprot.tsv", "human_GO.gaf")
net.overview()
