# Project
!!!!!!!PLEASE READ FOR END USER INSTRUCTIONS!!!!!!

Python Project - Network Programming
This project consists of three python scripts.
****************************************************************************************************************************************
First Script - > PythonScript.py.
PythonScript.py uses 4 files:
range.txt,
passwords.txt. 
For these 2 files, the end user should specify the full path of these files and denote it in the script.

iprange = open('Full path should be specified here, 'r').
passlist = open('Full path should be specified here', 'r').

PythonScript.py requires two other files which needs to be empty text file. One more time, the path for this text file needs to be specified in the script itself. Scripty writes the neighbors for each device in tempfile1. tempfile2 is used for getting the copy of the whole output of PythonScript.py 

tempfile1 = open('Full path should be specified here', 'w').
tempfile2 = open('Full path should be specified here', 'w').

With the file informations provided, end user can compile the PythonScript.py and after compiling end user should confirm the changes made in tempfile and click 'OK' so the necessary updates are loaded to tempfiles.

****************************************************************************************************************************************
Second Script - > DrawTopology.py

In order to successfully compile this script, the full path of the tempfile has to be written in the code like it's done in PythonScript.py.
tempfile = open('Full path should be specified here', 'w').

We should have had outputs in tempfile from running the first script properly. Before compiling DrawTopology.py let's make sure that we get the results we wanted from PythonScript.py 
When we open tempfile ( you will know the full path to open it), we should see an output similar to the structure below

router1,switch1
router2,switch1
router3,switch1
router4,switch1
router5,switch1
router6,switch1
router7,switch1
router8,switch1
switch1,router8
switch1,router7
switch1,router6
switch1,router5
switch1,router4
switch1,router3
switch1,router2
switch1,router1

where hostnames are separated by commas for each line.

DrawTopology.py will take the output above and will draw a topology graph using networkx and matplotlib modules and open the graph in a .png file.

****************************************************************************************************************************************
Third Script - > GETEol.py

This script is used for getting the information of LastDayofSupport for the given Product ID's (PID's)
PID's are obtained from devices by entering the show inventory command and using the regex 
pid_pattern = re.compile('(PID:)(.*?)\,') 

Using the URL, Client_id , Client_secret , we communicate with API and get the end of life information for platforms.

Thanks

