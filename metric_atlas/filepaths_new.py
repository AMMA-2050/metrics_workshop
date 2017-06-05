

def main(string):

	if string == 'outp':
		string = 'D://CMIP5/save_files'
	elif string == 'inp':
		string = 'D://CMIP5/CMIP5_Africa'
	return(string)


if "__name__" == "__main__":
	main(string)
