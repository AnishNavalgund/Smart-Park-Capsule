#pc
import requests, sys
print("--------------------------------")
print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
print("--------------------------------")

data = {'domain': open(sys.argv[1], 'r').read(),
        'problem': open(sys.argv[2], 'r').read()}

resp = requests.post('http://solver.planning.domains/solve',
                     verify=False, json=data).json()

with open(sys.argv[3], 'w') as f:
    f.write('\n'.join([act['name'] for act in resp['result']['plan']]))