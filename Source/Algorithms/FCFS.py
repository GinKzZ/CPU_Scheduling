import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Function

def makeOutput(listOfCPU, listOfR, listOfProcess):
	path = os.getcwd() + "/Outputs/" + sys.argv[2]
	with open(path, 'w') as file:
	    file.write(" ".join(map(str, listOfCPU)) + "\n")

	    for RP in listOfR:
		    file.write(" ".join(map(str, RP)) + "\n")

		listOfTT = []
		listOfWT = []
		for process in listOfProcess:
			listOfTT.append(process.turnaroundTime)
			listOfWT.append(process.waitingTime)
	    file.write(" ".join(map(str, listOfTT)) + "\n")
	    file.write(" ".join(map(str, listOfWT)) + "\n")

def FCFS(listOfProcess, numOfRUsing):
	listOfCPU = []
	listOfR = []
	return listOfProcess, listOfCPU, listOfR

def FCFS_solve(listOfProcess):
	numOfRUsing = 0
	for process in listOfProcess:
		if numOfRUsing != 0:
			break

		for num in process.listTime:
			if num[1] == "R":
				numOfRUsing = 1
				break
			elif num[1] == "CPU":
				continue
			else:
				numOfRUsing = 2
				break

	listOfProcess, listOfCPU, listOfR = FCFS(listOfProcess, numOfRUsing)
	makeOutput(listOfCPU, listOfR, listOfProcess)