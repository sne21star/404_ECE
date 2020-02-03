def getinput():
	gotNumber = False
	while not gotNumber:
		num = input("Enter a number: ")
		num = float(num)
		if num >= 50:
			print("Please enter an integer between 0 and 50")
		elif num < 0:
			print("Please enter an integer between 0 and 50")
		elif not num.is_integer():
			print("Number must be an Integer")
		else:
			gotNumber = True
	return int(num)


# return true or false
def isfield(num):
	return False


def main():
	num = getinput()
	isField = isfield(num)

	if isField:
		print(str(num) + " is a Field")
	else:
		print(str(num) + " is a Commutative Ring only")


if __name__ == "__main__":
	main()
