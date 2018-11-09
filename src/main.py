#### TITLE
### META
__title__ = "DepCraw"
__author__ = "Conrad Grosser"
__version__ = "1.5"
__branch__ = "STABLE"

### HELP
## Startup Parameters
# --timer - Activate benchmark timer
# --input_path - Project path for dependency check
# --output_path - Path for requirements.txt storage
# --debug - Activate debug mode (No automatic error catching!)
# --output_name - Name of output file (default: requirements.txt)
# --project_name - Name of project, used for comments
# PARAMETER - FUNCTION

## Functionality/ Usage
# -> readme.md

### IMPORTS
# Importing time for benchmark
import time
# Importing default module argparse for argument parsing
import argparse
# Importing os for file handling
import os
# Importing module for getting the default libary modules
import distutils.sysconfig as sysconfig

### HELPER FUNCTIONS
def deleteIfExist(fileName):
	# Deletes a file with given path if it exists
	if os.path.isfile(fileName):
		os.remove(fileName)

### FUNCTIONS
def writeDependencies(fileName, data, projectName):
	deleteIfExist(fileName)
	# Open the file location
	file = open(fileName, 'w+')
	file.write('# Project: ' + projectName + '\n')
	file.write('# Automatically generated requirements/ dependencies\n')
	# Write all the dependencies into the files
	for i in range(len(data)):
		file.write(data[i] + '\n')
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
			newDep = str(code[i].split()[1].split('.')[0])
			if len(newDep) > 1:
				dependencies.append(newDep)
	return list(set(dependencies))

def getDefaults():
	libary = []
	std_lib = sysconfig.get_python_lib(standard_lib=True)
	for top, dirs, files in os.walk(std_lib):
		for nm in files:
			if nm != '__init__.py' and nm[-3:] == '.py':
				package = os.path.join(top, nm)[len(std_lib)+1:-3].replace('\\','.')
				if not ('site-package' in package):
					# Adding the pip styling for comparability
					libary.append(package)
	# Manually adding, bcs they don't count as as standard modules
	libary.append('sys')
	libary.append('time')
	libary.append('urllib')
	libary.append('HDB')
	return libary

def checkStandard(requirementsList, defaultList):
	requirements = []
	for i in range(len(requirementsList)):
		if not requirementsList[i] in defaultList:
			requirements.append(requirementsList[i])
	return requirements

### MAIN
def main(args):
	print('STATUS: ' + __title__ + ' started.')
	if args.timer: startTime = time.time()

	requirements = []

	for root, subdirs, files in os.walk(args.input_path):
		for filename in files:
			print('Checking ' + str(filename) + '...')
			if filename.endswith('.py') and not filename == '__init__.py':
				requirements += readFile(os.path.join(root, filename))

	writeDependencies(os.path.join(args.output_path + args.output_name), checkStandard(list(set(requirements)), getDefaults()), args.project_name)

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
parser.add_argument('--project_name', nargs='?', const=True, default='No Name Given', type=str)
parser.add_argument('--output_name', nargs='?', const=True, default='requirements.txt', type=str)

args = parser.parse_args()

if args.debug:
	main(args)
else:
	try:
		main(args)
	except:
		print('ERROR: Something went wrong. Thanks Microsoft!')
