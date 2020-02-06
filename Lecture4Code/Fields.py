'''
Homework Number: 3
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/05/2020
'''
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

def isPrime(given_num):
	isprimeX = True
	if(given_num < 2):
		return False
	elif(given_num == 2):
		return True
	elif(given_num % 2 == 0):
		return False
	else:
		for factor in range(2, given_num):
			if(given_num % factor) == 0:
				isprimeX = False
				break
	return isprimeX

def isfield(num):
	return isPrime(num)

def main():
	given_num = getinput()
	isField = isfield(given_num)
	if isField:
		print("field")
	else:
		print("ring")
if __name__ == "__main__":
	main()