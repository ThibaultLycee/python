# library grouping a few usefull decorator

import time
import datetime
import functools

def Log(
		file : str,
		funcName : bool = True,
		executionTime : bool = False,
		Args : bool = False,
		Kwargs : bool = False,
		timer : bool = False,
		output : bool = False,
		outputType : bool = False
	):
	def manager(function):
		@functools.wraps(function)
		def wrapper(*args, **kwargs):
			before = time.time()
			returnedValue = function(*args, **kwargs)
			after = time.time()
			with open(file, "a+") as logFile:
				if funcName: logFile.write(f'[{function.__name__}]\n')
				if executionTime: logFile.write(f'\tExecution time : {datetime.datetime.now()}\n')
				if Args: logFile.write(f'\tArguments to the function : {args}\n')
				if Kwargs: logFile.write(f'\tKwarguments to the function : {kwargs}\n')
				if timer: logFile.write(f'\tTime to execute : {after - before} seconds\n')
				if output: logFile.write(f'\tOutput : {returnedValue}\n')
				if outputType: logFile.write(f'\tOutput type : {type(returnedValue)}\n')
			return returnedValue
		return wrapper
	return manager


def ErrorHandler(file : str):
	def manager(function):
		@functools.wraps(function)
		def wrapper(*args, **kwargs):
			try:
				val = function(*args, **kwargs)
			except Exception as e:
				with open(file, "a+") as logFile:
					logFile.write(f'Function {function.__name__} got an error : {str(e)}\n')
			return val
		return wrapper
	return manager


def Debbug(
		printFuncName=False,
		printTime=False,
		printDoc=False,
		printArgs=False,
		printKwargs=False,
		printOutput=False,
		printError=False
	):
	def manager(function):
		#@functools.wraps(function)
		def wrapper(*args, **kwargs):
			error = "No Error"
			before = time.time()
			try:
				val = function(*args, **kwargs)
			except Exception as e:
				error = str(e)
				val = None
			after = time.time()
			if printFuncName: print(f'[{function.__name__}]')
			if printTime: print(f'Execution took {after - before} seconds')
			if printDoc: print(f'Function doccumentation : {function.__doc__}')
			if printArgs: print(f'Function arguments : {args}')
			if printKwargs: print(f'Function kwarguments : {kwargs}')
			if printOutput: print(f'Output : {val}')
			if printError: print(f'Error : {error}')
			return val
		return wrapper
	return manager


def ShowOutput(baseString='Function output : '):
	def manager(function):
		@functools.wraps(function)
		def wrapper(*args, **kwargs):
			val = function(*args, **kwargs)
			print(f'{baseString} {val}')
			return val
		return wrapper
	return manager


def ReturnDocIfError(stopCode=False, addFuncNameToString=True, returnError=False):
	def manager(function):
		@functools.wraps(function)
		def wrapper(*args, **kwargs):
			error = ""
			val = ""
			try: val = function(*args, **kwargs)
			except Exception as e:
				error = str(e)
				print(f'{f"[{function.__name__ }]" if addFuncNameToString else ""}\n\tDoc : {function.__doc__}\n\tError : {error if returnError else ""}')
				if stopCode: function(*args, **kwargs)
			return val
		return wrapper
	return manager

def UniqueSignature(function):
	@functools.wraps(function)
	def wrapper(*args, **kwargs):
		signature = function.__annotations__
		for arg in args: