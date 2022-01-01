def param_log_decorator(string : str):
	def decorator(function):
		def wrapper(*args, **kwargs):
			val = function(*args, **kwargs)
			print(string.format(function.__name__, val))
			return val
		return wrapper
	return decorator



@param_log_decorator('La fonction {} à retourné le résultat : {}')
def addition(a : int, b : int) -> int:
	return a + b

addition(int(input("A : ")), int(input("B : ")))
input()