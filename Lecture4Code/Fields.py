'''
Homework Number: 3
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/05/2020
'''
from sympy import *
def getinput():
	gotNumber = False
	while not gotNumber:
		given_num = input("Enter a number: ")
		given_num = float(given_num)
		if not given_num.is_integer():
			print("Number must be an Integer")
		else:
			gotNumber = True
	return int(given_num)

#Used fermat little primality, a probability test to check whether or not it is prime
def isPrime(given_num):
	return isprime(given_num)

def isfield(num):
	return isPrime(num)

def main():
	given_num = getinput()
	isField = isfield(given_num)
	for i in range(0, 100):
		isField = isfield(i)
		print(i)
		if isField:
			print("field")
		else:
			print("ring")

if __name__ == "__main__":
	main()