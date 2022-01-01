import subprocess

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

wifis = [line.split(':')[1][1:-1] for line in data if 'All user Profile' in line]

for wifi in wifis:
	results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear']).decode('utf-8').split('\n')
	results = [line.split(':')[1][1:-1] for line in results if 'Key Content' in line]

	try:
		print(f'Nom : {wifi}, Mdp = {results[0]}')
	except IndexError:
		print(f'Pas de mdp pour {wifi}')