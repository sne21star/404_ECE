'''
Homework Number: 3
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 02/03/2020
'''
# Constants
prime50 = dict({2: 1, 3: 1, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1, 29: 1, 31: 1, 37: 1, 41: 1, 43: 1, 47: 1})


def getinput():
	gotNumber = False
	while not gotNumber:
		num = input("Enter a number: ")
		num = float(num)
		if num >= 50:
			print("Please enter an integer [0,50)")
		elif num < 0:
			print("Please enter an integer [0,50)")
		elif not num.is_integer():
			print("Number must be an Integer")
		else:
			gotNumber = True
	return int(num)


def isprime(num):
	return prime50.get(num)


def isfield(num):
	return isprime(num)


def main():
	num = getinput()
	isField = isfield(num)

	if isField:
		print("field")
	else:
		print("ring")

if __name__ == "__main__":
	main()
