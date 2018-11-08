#### TITLE
### META
__title__ = "DepCraw"
__author__ = "Conrad Großer"
__version__ = "0.01"
__branch__ = "DEVELOPMENT"

### HELP
## Startup Parameters
# --timer - Activate benchmark timer
# --input_path - Project path for dependency check
# --output_path - Path for requirements.txt storage
# --debug - Activate debug mode (No automatic error catching!)
# PARAMETER - FUNCTION

## Functionality/ Usage

## TODO

## Known Issues

### IMPORTS
# Importing sys for argument handling
import sys
# Importing time for benchmark
import time
# Importing default module argparse for argument parsing
import argparse

### HELPER FUNCTIONS

### FUNCTIONS

def writeDependencies(path, data):
	print('Writing requirements.txt...')
	# Open the file location
	file = open(path, 'w+')
	file.write('# Automatically generated requirements/ dependencies\n')
	# Write all the dependencies into the files
	for i in range(len(data)):
		file.write(data[i] + '\n')
	# Newline at end of file
	file.write('\n')
	file.close()
	return 0

### MAIN
def main(args):
	print('STATUS: ' + __title__ + ' started.')
	if args.timer: startTime = time.time()

	requirements = ['ye', 'ye', 'ye']

	writeDependencies((args.input_path + '/requirements.txt' if args.input_path else 'requirements.txt'), requirements)

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
