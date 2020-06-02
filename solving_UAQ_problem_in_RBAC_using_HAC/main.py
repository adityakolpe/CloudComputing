import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
print("Reading Dataset...")
print
dataset = pd.read_csv('gData.csv')
print(dataset)
X = dataset.iloc[:, 1:].values
print(X)
print
print("Creating Dendrogram...")
import scipy.cluster.hierarchy as sch

dendrogram = sch.dendrogram(sch.linkage(X, method  = "ward"))
plt.title('Dendrogram')
plt.xlabel('Roles')
plt.ylabel('Euclidean distances')
plt.show()

from sklearn.cluster import AgglomerativeClustering 
roles=[]
print
print("AgglomerativeClustering...")
print
for i in range(len(X),1,-1):
	hc = AgglomerativeClustering(n_clusters = i, affinity = 'euclidean', linkage ='ward')
	y_hc=hc.fit_predict(X)
	listy_hc = y_hc.tolist()
	roles.append(listy_hc)
	print(y_hc)

clubbedRoles = []
clubbedPerm = []

for i in roles:
	for c in range(0,len(i)):
		club1 = ''
		cluba = []
		club2 = ''
		clubb = []
		for j in range(0,len(i)):
			if i[j]==c:
				if j<8:
					#print(j)
					club1 = club1+str(j)+","
					cluba.append(j)
				else:
					club2 = club2+str(j)+","
					clubb.append(j)
		temp = []

		print('club1 = ',club1)
		print('cluba = ',cluba)
		print('club2 = ',club2)
		print('clubb = ',clubb)
		for k in cluba:
			if k == ',':
				continue
			else:
				ele = int(k)
				if len(temp)==0:
					temp.extend(X[ele])
					print("temp exten  = ",temp)
				else:
					temp = np.bitwise_or(temp,X[ele])
					temp = list(temp)
					print("temp = ",temp)

		if temp not in clubbedPerm:
			clubbedPerm.append(temp)
			clubbedRoles.append(club1)
		temp = []
		print(club2)
		for k in clubb:
			if k == ',':
				continue
			else:
				#print(k)
				ele = int(k)
				if len(temp)==0:
					temp.extend(X[ele])
					#print("X[ele] = ",X[ele])
					#print("temp extended = ",temp)
				else:
					#print("temp = ",temp)
					temp = np.bitwise_or(temp,X[ele])
					temp = list(temp)
					

		if temp not in clubbedPerm:
			clubbedPerm.append(temp)
			clubbedRoles.append(club2)

clubbedPerm = [ele for ele in clubbedPerm if ele != []]
clubbedRoles =  [ele for ele in clubbedRoles if ele != '']
print
print("List of Permissions...")
print(clubbedPerm)
print
print("And their respective Roles...")
print(clubbedRoles)
print
roleAssigned = []
print("Which Permissions do you want? ("+str(len(X))+")")
x = raw_input().split()
x = [int(i) for i in x]

y = []
for i in range(1,len(X[0])+1):
	if i in x:
		y.append(1)
	else:
		y.append(0)
#print(y)
for i in range(0,len(clubbedPerm)):
	temp2 = np.bitwise_and(y,clubbedPerm[i])
	temp2 = list(temp2)
	
	if temp2==y: 
		roleAssigned = clubbedRoles[i]
		break

if len(roleAssigned)==0:
	print("No such role found!")
else:
	print("Role(s) assigned:")
	print(roleAssigned)
