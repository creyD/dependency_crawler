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
# --git_ignore - Path of the gitignore file (if existend)
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

def chrossCheck(listInner, listOuter):
	# Crosschecking a list with another list
	result = []
	for i in range(len(listInner)):
		if not listInner[i] in listOuter:
			result.append(listInner[i])
	return result

def readFile(filePath):
	file = open(filePath, 'r')
	content = file.readlines()
	file.close()
	return content

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

def readDependenciesFromFile(fileName):
	dependencies = []
	# Read the file and store it in a cache
	code = readFile(fileName)

	# Search the cache for code lines that start with an import or from statement
	for i in range(len(code)):
		if code[i].startswith('import') or code[i].startswith('from'):
			newDep = str(code[i].split()[1].split('.')[0])
			if len(newDep) > 1:
				dependencies.append(newDep)
	return list(set(dependencies))

def readGitIgnoresFromFile(fileName):
	ignoredFiles = []
	ignoredFolders = []

	ignored = readFile(fileName)

	for i in range(len(ignored)):
		if not (ignored[i].startswith('#') or len(ignored[i]) <= 2):
			if ignored[i].endswith('/'):
				ignoredFolders.append(ignored[i])
			else:
				ignoredFiles.append(ignored[i])

	return ignoredFiles

def getPythonDefaultLibary():
	# Thanks to Stackoverflow user Caspar (https://stackoverflow.com/users/775982/caspar)
	libary, std_lib = [], sysconfig.get_python_lib(standard_lib=True)
	for top, dirs, files in os.walk(std_lib):
		for fileName in files:
			if fileName != '__init__.py' and fileName[-3:] == '.py':
				package = os.path.join(top, fileName)[len(std_lib)+1:-3].replace('\\','.')
				if not ('site-package' in package):
					# Adding the pip styling for comparability
					libary.append(package)
	# Manually adding, bcs they don't count as as standard modules
	libary.append('sys')
	libary.append('time')
	libary.append('urllib')
	return libary

### MAIN
def main(args):
	print('STATUS: ' + __title__ + ' started.')
	if args.timer: startTime = time.time()

	requirements = []
	gitIgnoredFiles = readGitIgnoresFromFile(args.git_ignore)
	print(gitIgnoredFiles)

	for root, subdirs, files in os.walk(args.input_path):
		for filename in files:
			if filename.endswith('.py') and not filename == '__init__.py' and not filename in gitIgnoredFiles:
				print('Checking ' + str(filename) + '...')
				requirements += readDependenciesFromFile(os.path.join(root, filename))

	writeDependencies(os.path.join(args.output_path + args.output_name), chrossCheck(list(set(requirements)), getPythonDefaultLibary()), args.project_name)

	if args.timer: print('BENCHMARK: ' + __title__ + ' took ' + str((time.time() - startTime) * 1000) + ' seconds for executing.')
	print('STATUS: ' + __title__ + ' successfully .')
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
parser.add_argument('--git_ignore', nargs='?', const=True, default='', type=str)

args = parser.parse_args()

if args.debug:
	main(args)
else:
	try:
		main(args)
	except:
		print('ERROR: Something went wrong. Thank you Microsoft!')
