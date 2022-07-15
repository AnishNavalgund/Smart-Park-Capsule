"""
Project:    Smart Park Capsule

Course:     Smart City and IOT
Institute:  Service Computing Department, IAAS, University of Stuttgart

---------------- Team Members -----------

Sl.No   |           Names                   
  1     |     Swathi Shridhar               
  2     |     Badruddin Mukadam             
  3     |     Suraj Sakpal                  
  4     |     Anish Krishna Navalgund       
-----------------------------------------

File Description: SPC_RunOnlineAIPlanner.py is the main file to run online planning editor.

Timestamp: 10th July 2022

"""
# Import required python packages 
import requests, sys

print("--------------------------------")
print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
print("--------------------------------")

# Open the domain and problem file in read mode and store the data in dict format
data = {'domain': open(sys.argv[1], 'r').read(),
        'problem': open(sys.argv[2], 'r').read()}

# Pass the data file to online AI-Planning solver
resp = requests.post('http://solver.planning.domains/solve',
                     verify=False, json=data).json()

# Get the plan from the online solver 
with open(sys.argv[3], 'w') as f:
    f.write('\n'.join([act['name'] for act in resp['result']['plan']]))