# SI508 final project py Pengyu Yang<br />
Dota2 banpick helper<br />
<br />
Get Started:<br />
Required packages:ast, tkinter & requests.<br />
<br />
<br />
To get your own API keys, go to https://steamcommunity.com/dev/apikey and signin with your steam account. Then replace the API keys.<br />
To run the program, open “Starter.py” with python.py or use command line python3 final_project.py<br />
To use the program, simply press the buttons to load or get the records. Use the drop-down menu to select the Heroes and see their counter results.<br />
<br />
<br />
how to interact:<br />
- Get new records from API: press button “getMatchesSteam” or “getMatchesOpenDota” depending on which sources you want. To get very large number of records, use the scale to set the number and press “getLargeMatchesSteam”
* Load the cached records: press button “load from file” or “load from OpenDotaAPI” depending on which sources you want.
+ Use the drop-down menu to select the Hero. The program will show the counter Heroes. Click on the counter Hero jumps to provide counters for that counter Hero.
* save the results: press: press ”save to file” button. Then press “STOP” to exit

Graph Structure<br />
For each game from the API, heroes and their win and loss will be store in a graph shown as below. The heroes are represented by the node and the edge is the win rate against other heroes.<br />
![Graph Structure](Picture1.png)<br />
The program finds the five heroes that has the lowest win rate as the “highlighted counter heroes” and displays to the client. This node and edge combination applies to other Heroes as well to form a large graph. 
