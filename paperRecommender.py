import xlrd
import networkx as nx
from node2vec import Node2Vec
import math
import random

def buildAugGraph():
	G_Augmented = nx.DiGraph()
	locTopic = ("topic.xlsx")
	locPapers = ("papers.xlsx")
	wbTopic = xlrd.open_workbook(locTopic)
	wbPapers = xlrd.open_workbook(locPapers)
	sheetTopic = wbTopic.sheet_by_index(0)
	sheetPapers = wbPapers.sheet_by_index(0)
	for i in range(sheetTopic.nrows):
	    G_Augmented.add_edge(int(sheetTopic.cell_value(i,0)), str(sheetTopic.cell_value(i,3)))
	    G_Augmented.add_edge(int(sheetTopic.cell_value(i,0)), str(sheetTopic.cell_value(i,6)))
	for j in range(sheetPapers.nrows):
	    G_Augmented.add_edge(int(sheetPapers.cell_value(j,0)), int(sheetPapers.cell_value(j,1)))
	return G_Augmented
def buildGraph():
	G= nx.DiGraph()
	locPapers = ("papers.xlsx")
	wbPapers = xlrd.open_workbook(locPapers)
	sheetPapers = wbPapers.sheet_by_index(0)
	for j in range(sheetPapers.nrows):
	    G.add_edge(int(sheetPapers.cell_value(j,0)), int(sheetPapers.cell_value(j,1)))
	return G    
def knn(input, knn, filename):
	#filename = "EMBEDDING_FILENAME.emb"
	filehandle = open(filename, 'r')
	#print(filehandle.readline())
	dict1={}
	#print(knn)
	#input="DEXA Workshop"
	#knn=10
	while True:
	    line = filehandle.readline()
	    if not line:
	        break
	    lis1=line.split()
	    lis2=lis1[-64:]
	    key_list=lis1[0:len(lis1)-64]
	    key= " ".join(str(x) for x in key_list)
	    #print(str(key))
	    dict1[str(key)]= lis2

	filehandle.close()
	distList=[]
	distdict={}
	#print(str('44')==str(input))
	#print(float(dict1[str(input)][0]))
	for i in dict1.keys():
	    dist=0
	    if(i==''):
	    	continue
	    if(str(i)!=str(input)):
	        for j in range(64):
	            dist= dist+math.pow((float(dict1[str(i)][j])-float(dict1[str(input)][j])),2)

	    dist=math.sqrt(dist)
	    distdict[i]=dist
	    

	sort_distdict= sorted(distdict.items(), key = lambda kv:(kv[1], kv[0]))
	#print(sort_distdict[0])
	count=0
	for i in sort_distdict:
	    if(count>knn):
	        break;
	    distList.append(i[0])
	    count+=1
	return (distList[1:])

def createembeddings(Graph_data, filename):
	node2vec = Node2Vec(Graph_data, dimensions=64, walk_length=30, num_walks=200, workers=1)  # Use temp_folder for big graphs

	# Embed nodes
	model = node2vec.fit(window=10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)

	# Look for most similar nodes
	model.wv.most_similar('2')  # Output node names are always strings
	#filename="EMBEDDING_FILENAME.emb"

	# Save embeddings for later use
	model.wv.save_word2vec_format(filename)
QueryList= random.sample(range(0, 2554), 100)
print(QueryList)

//acc=0
for Pi in QueryList:
	print("running node"+str(Pi))
	L1= list(buildGraph().successors(Pi))
	L2=list(buildGraph().predecessors(Pi))
	#print(L2)
	count=0
	Li= L1+L2
	Li= list(dict.fromkeys(Li))
	print(Li)
	A= len(Li)
	#print(A)
	#print(A/2)
	k=0
	random_k=[3,5,10,15]
	gr= buildGraph()
	gr_emb= buildAugGraph()
	while (len(Li)>= A/2 ):
		print("entered")
		pn= random.choice(Li)
		print("random node selected"+ str(pn))
		Li.remove(pn)
		if gr.has_edge(pn,Pi):
			gr.remove_edge(pn,Pi)
		else:
			gr.remove_edge(Pi, pn)
		if gr_emb.has_edge(pn,Pi):
			gr_emb.remove_edge(pn,Pi)
		else:
			gr_emb.remove_edge(Pi, pn)
		print("check if node is present"+str(gr.has_node(Pi)))
		print("check if node is present"+str(gr_emb.has_node(Pi)))
		createembeddings(gr, "EMBEDDING_FILENAME.emb")
		createembeddings(gr_emb, "EMBEDDING_FILENAME_AUG.emb")
		l_knn=knn(str(Pi),15,"EMBEDDING_FILENAME.emb")
		l_knn_emb=knn(str(Pi),15,"EMBEDDING_FILENAME_AUG.emb")

		acc=[0,0, 0, 0]
		acc_emb=[0,0,0,0]
		if (str(pn) in l_knn):
			knn_index= l_knn.index(str(pn))

			for ind in range(len(random_k)):
				if(ind>=knn_index):
					acc[ind]+=1
					#"acc"+str(ind)="acc"+str(ind)+1

		print(acc[0])
		print(acc[1])
		print(acc[2])
		print(acc[3])
		if (str(pn) in l_knn_emb):
			knn_index_emb= l_knn_emb.index(str(pn))

			for ind_emb in range(len(random_k)):
				if(ind_emb>=knn_index_emb):
					acc_emb[ind]+=1
					#("acc"+str(ind)+"emb")=("acc"+str(ind)+"emb")+1
		print(acc_emb[0])
		print(acc_emb[1])
		print(acc_emb[2])
		print(acc_emb[3])




	
