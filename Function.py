import os
import re
import sys
from Algorithms import *

class Process:
	arrivalTime = 0
	listTime = []
	countNotUseCPU = 0 #for conflict in the entrance of the Ready Queue
	turnaroundTime = 0
	waitingTime = 0
	def __init__(self, arrivalTime, listTime):
		self.arrivalTime = arrivalTime
		self.listTime = listTime

def readFileInput():
	i, j = 0, 0
	numOfAl = 0
	numOfRR = 0
	listOfProcess = []
	path = os.getcwd()
	path += "/Inputs/" + sys.argv[1]
	with open(path, 'r') as file:
		lines = file.readlines()

	numOfAl = int(lines[i].strip())
	i += 1
	if numOfAl == 2:
		numOfRR = int(lines[i].strip())
		i += 1
	numOfProcess = lines[i].strip()
	i += 1

	while j < int(numOfProcess):
		detail = lines[i].strip()
		i += 1

		arrivalTime = int(detail[0])
		detail = detail[2:len(detail)]
		listTime = []
		elements = re.findall(r'(\d+)(?:\((R\d+)\))?', detail)
		for value, res in elements:
			if res:
				listTime.append((int(value), res))
			else:
				listTime.append((int(value), "CPU"))

		listOfProcess.append(Process(arrivalTime, listTime))
		j += 1

	return numOfAl, numOfRR, listOfProcess

def solve():
	numOfAl, numOfRR, listOfProcess = readFileInput()
	match numOfAl:
		case 1:
			FCFS_solve(listOfProcess)
		case 2:
			RR_solve(listOfProcess, numOfRR)
		case 3:
			SJF_solve(listOfProcess)
		case 4:
			SRTN_solve(listOfProcess)