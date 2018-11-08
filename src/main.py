#### TITLE
### META
__title__ = "DepCraw"
__author__ = "Conrad Grosser"
__version__ = "1.1"
__branch__ = "STABLE"

### HELP
## Startup Parameters
# --timer - Activate benchmark timer
# --input_path - Project path for dependency check
# --output_path - Path for requirements.txt storage
# --debug - Activate debug mode (No automatic error catching!)
# PARAMETER - FUNCTION

## Functionality/ Usage
# -> readme.md

## TODO

## Known Issues
# - If a file imports only modules already considered in the requirements it will still show up in the final file

### IMPORTS
# Importing sys for argument handling
import sys
# Importing time for benchmark
import time
# Importing default module argparse for argument parsing
import argparse
# Importing os for file handling
import os

### HELPER FUNCTIONS
def splitter(string):
	split = []
	word = ''
	for i in range(len(string)):
		if string[i] == ' ' or string[i] == '.':
			split.append(word)
			word = ''
		else:
			word += string[i]
	return split

def deleteIfExist(fileName):
	# Deletes a file with given path if it exists
	if os.path.isfile(fileName):
		os.remove(fileName)

### FUNCTIONS
def writeDependencies(fileName, data):
	print('Writing requirements.txt...')
	deleteIfExist(fileName)
	# Open the file location
	file = open(fileName, 'w+')
	file.write('# Automatically generated requirements/ dependencies\n')
	# Write all the dependencies into the files
	for i in range(len(data)):
		file.write(data[i])
	# Newline at end of file
	file.write('\n')
	file.close()
	return 0

def readFile(fileName):
	dependencies = []
	# Read the file and store it in a cache
	file = open(fileName, 'r')
	code = file.readlines()
	file.close()

	# Search the cache for code lines that start with an import or from statement
	for i in range(len(code)):
		if code[i].startswith('import') or code[i].startswith('from'):
			dependencies.append('-' + str(code[i].split()[1].split('.')[0]) + '\n')

	if len(dependencies) != 0:
		#message = '# From file ' + fileName + ' the following dependencies were initially added:\n'
		#return [message] + dependencies
		return dependencies
	return ''

### MAIN
def main(args):
	print('STATUS: ' + __title__ + ' started.')
	if args.timer: startTime = time.time()

	requirements = []

	for root, subdirs, files in os.walk(args.input_path):
		for filename in files:
			if filename.endswith('.py'):
				requirements += readFile(os.path.join(root, filename))

	writeDependencies((args.output_path + '/requirements.txt' if args.output_path else 'requirements.txt'), list(set(requirements)))

	if args.timer: print('BENCHMARK: ' + __title__ + ' took ' + str((time.time() - startTime) * 1000) + ' seconds for executing.')
	print('STATUS: ' + __title__ + ' ended.')
	return

### CALL
# Argument parsing definition
parser = argparse.ArgumentParser()
parser.add_argument('--timer', nargs='?', const=True, default=False, type=bool)
parser.add_argument('--input_path', nargs='?', const=True, default='', type=str)
parser.add_argument('--output_path', nargs='?', const=True, default='', type=str)
parser.add_argument('--debug', nargs='?', const=True, default=False, type=bool)
args = parser.parse_args()

if args.debug:
	main(args)
else:
	try:
		main(args)
	except:
		print('ERROR: Something went wrong. Thanks Microsoft!')
