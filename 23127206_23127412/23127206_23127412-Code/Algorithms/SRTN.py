import os
import sys
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Function

def makeOutput(listOfCPU, listOfR, listOfProcess):
	path = os.getcwd() + '/' + sys.argv[2]
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

def normalize(listStr):
	while listStr and listStr[-1] == '_':
		listStr.pop()
	return listStr

def checkAndAddToQ_CPU(q_CPU, list_Temp, listOfProcess, countTime):
	for index in range(0, len(listOfProcess)):
		if listOfProcess[index].arrivalTime == countTime:
			list_Temp.append(index+1)
	if len(list_Temp) == 0:
		return q_CPU, list_Temp, listOfProcess

	while len(q_CPU) != 0:
		list_Temp.append(q_CPU.popleft())	

	n = len(list_Temp)
	for i in range(0, n - 1):
		for j in range(0, n - 1 - i):
			if listOfProcess[list_Temp[j]-1].listTime[0][0] >= listOfProcess[list_Temp[j + 1]-1].listTime[0][0]:  
				if listOfProcess[list_Temp[j]-1].listTime[0][0] == listOfProcess[list_Temp[j + 1]-1].listTime[0][0]:
					if listOfProcess[list_Temp[j]-1].countNotUseCPU < listOfProcess[list_Temp[j + 1]-1].countNotUseCPU:  
						list_Temp[j], list_Temp[j + 1] = list_Temp[j + 1], list_Temp[j]
				else:
					list_Temp[j], list_Temp[j + 1] = list_Temp[j + 1], list_Temp[j]  

    #add to queue
	for index in list_Temp:
		q_CPU.append(index)
	list_Temp.clear()

	return q_CPU, list_Temp, listOfProcess

def checkEnd(listOfProcess, q_CPU, q_R1, q_R2):
	if len(q_CPU) != 0 or len(q_R1) != 0 or len(q_R2) != 0:
		return False
	for process in listOfProcess:
		if process.turnaroundTime == 0:
			return False
	return True

def SRTN(listOfProcess):
	listOfCPU = []
	listOfR = []
	R1 = []
	R2 = []
	list_Temp = []
	q_CPU = deque()
	q_R1 = deque()
	q_R2 = deque()
	countTime = 0
	countTime_R1 = 0
	countTime_R2 = 0
	flagUseCPU = False
	flagUseR1 = False
	flagUseR2 = False

	curProcess_CPU = 0
	curProcess_R1 = 0
	curProcess_R2 = 0
	while True:
		
		if flagUseR1 == False:
			if len(q_R1) != 0:
				curProcess_R1 = q_R1.popleft()
				countTime_R1 = 1
				R1.append(str(curProcess_R1))
				flagUseR1 = True
			else:
				R1.append('_')
		else:
			if countTime_R1 == listOfProcess[curProcess_R1-1].listTime[0][0]:
				countTime_R1 = 0
				listOfProcess[curProcess_R1-1].listTime.pop(0)	
				flagUseR1 = False	
				if len(listOfProcess[curProcess_R1-1].listTime) == 0: #count turn around time
					listOfProcess[curProcess_R1-1].turnaroundTime = countTime - listOfProcess[curProcess_R1-1].arrivalTime
				else:
					list_Temp.append(curProcess_R1)

				if len(q_R1) != 0:
					curProcess_R1 = q_R1.popleft()
					R1.append(str(curProcess_R1))
					flagUseR1 = True
				else:
					if checkEnd(listOfProcess, q_CPU, q_R1, q_R2) == True:
						break
					else:					
						R1.append('_')
			else:
				R1.append(str(curProcess_R1))
			countTime_R1 += 1

		if flagUseR2 == False:
			if len(q_R2) != 0:
				curProcess_R2 = q_R2.popleft()
				countTime_R2 = 1
				R2.append(str(curProcess_R2))
				flagUseR2 = True
			else:
				R2.append('_')
		else:
			if countTime_R2 == listOfProcess[curProcess_R2-1].listTime[0][0]:
				countTime_R2 = 0
				listOfProcess[curProcess_R2-1].listTime.pop(0)	
				flagUseR2 = False	
				if len(listOfProcess[curProcess_R2-1].listTime) == 0: #count turn around time
					listOfProcess[curProcess_R2-1].turnaroundTime = countTime - listOfProcess[curProcess_R2-1].arrivalTime
				else:
					list_Temp.append(curProcess_R2)

				if len(q_R2) != 0:
					curProcess_R2 = q_R2.popleft()
					R2.append(str(curProcess_R2))
					flagUseR2 = True
				else:
					if checkEnd(listOfProcess, q_CPU, q_R1, q_R2) == True:
						break
					else:
						R2.append('_')
			else:
				R2.append(str(curProcess_R2))
			countTime_R2 += 1

		q_CPU, list_Temp, listOfProcess = checkAndAddToQ_CPU(q_CPU, list_Temp, listOfProcess, countTime)
		#CPU
		if len(q_CPU) != 0:
			flagUseCPU = True
			curProcess_CPU = q_CPU.popleft()
			listOfCPU.append(str(curProcess_CPU))
			listOfProcess[curProcess_CPU-1].countNotUseCPU = 0
			listOfProcess[curProcess_CPU-1].listTime[0][0] -= 1
		else:
			listOfCPU.append('_')

		if flagUseCPU == True and listOfProcess[curProcess_CPU-1].listTime[0][0] == 0:
			flagUseCPU = False
			listOfProcess[curProcess_CPU-1].listTime.pop(0)	
			if len(listOfProcess[curProcess_CPU-1].listTime) == 0: #count turn around time
				listOfProcess[curProcess_CPU-1].turnaroundTime = countTime - listOfProcess[curProcess_CPU-1].arrivalTime + 1
			else:
				temp = listOfProcess[curProcess_CPU-1].listTime[0][1]
				if temp == "R1":
					q_R1.append(curProcess_CPU)
				elif temp == "R2":
					q_R2.append(curProcess_CPU)
			curProcess_CPU = -1
		elif curProcess_CPU != -1:
			flagUseCPU = False
			list_Temp.append(curProcess_CPU)
		if checkEnd(listOfProcess, q_CPU, q_R1, q_R2) == True:
			break

		for index in q_CPU: #counting waiting time
			listOfProcess[index-1].waitingTime += 1

		for index in range(0, len(listOfProcess)): #counting time not use CPU
			if listOfProcess[index].arrivalTime <= countTime:
				if curProcess_CPU != index+1:
					listOfProcess[index].countNotUseCPU += 1
		countTime += 1

	listOfCPU = normalize(listOfCPU)
	if not all(item == '_' for item in R1):
		R1 = normalize(R1)
		listOfR.append(R1) 
	if not all(item == '_' for item in R2):
		R2 = normalize(R2)
		listOfR.append(R2) 
	return listOfProcess, listOfCPU, listOfR

def SRTN_solve(listOfProcess):
	listOfProcess, listOfCPU, listOfR = SRTN(listOfProcess)
	makeOutput(listOfCPU, listOfR, listOfProcess)