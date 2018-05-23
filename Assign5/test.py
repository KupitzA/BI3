from PPIGONetwork import PPIGONetwork

# 5.2 (a) (1)
net = PPIGONetwork("human_network.tsv", "human_uniprot.tsv", "go")
print net.size()
