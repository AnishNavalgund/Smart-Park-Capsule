# Smart Park Capsule

Smart Park Capsule is an IOT based parking management system in a public building. This system provides an easy and time efficient parking solution which saves the user’s time and energy.

Project assignemnt as part of "Smart City and IOT" course at the University of Stuttgart

---------------- Team Members -----------
Sl.No   |           Names                
  1     |     Swathi Shridhar                      
  2     |     Badruddin Mukadam           
  3     |     Suraj Sakpal               
  4     |     Anish Krishna Navalgund   
-----------------------------------------

Project Files:

SPC_Subcriber.py - This is the main code to run in the project. This code connects to the Raspberry Pi through MQTT protocol and subscibes to the sensor data. This code also runs the AI-planner as and when the sensor data is subscribed. 

SPC_AIPlanner.py - This is the main code to perform AI-Planning. The code will generate the plan dynamically as the per the input sensor data.
                  
SPC_RunOnlineAIPlanner.py -  This is the code to run online planning editor.                 
                  
SPC_GUI.py - This code creates the real-time visualization window to monitor the required data in the project.

SPC_Problem.pddl and SPC_DomainFile.pddl - Input Files for AI-planning

SPC_GeneratedPlan.text - Text file which gets updated with the plan 

/****************************************************************************************************************/


                   


