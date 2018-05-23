net = open("human_network.tsv", "r")

line = net.readlines(1)
line = line[0]
line = line[0:len(line)-1]
line_list = line.split("\t")
with open("human_GO.gaf", "r") as gos:
    for go_line in gos:
        temp = go_line.split("\t")
        for i in range(0,len(temp)):
            if(temp[i] == line_list[0]):
                print(line_list[0] + "\t:\t" + str(i))
            if(temp[i] == line_list[1]):
                print(line_list[1] + "\t:\t" + str(i))


net.close()
gos.close()
