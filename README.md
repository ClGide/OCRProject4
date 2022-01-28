
# ♔ TinyDB for chess tournament management 

The following Python code is the project 4 of my Open ClassRooms path. It is designed to save and load data about a chess tournament in a TinyDB database. The program operates in two broad steps.

First, before the tournament starts, the program requests info about the tournament (venue, number of rounds, number of players...) and about each player (name, age, sex...). 

Second, throughout the tournament, the program requests match results and pairs the players according to the swiss-system algorithm. It also allows the user to override a player's ranking or the tournament's description at any time. Moreover, it enables the user to save or load data about the tournament between rounds.

### ❗ Important 

The rounds duration is dependent on the time control chosen by the user. If, for example, he chooses "bullet" the rounds will last 3 min. Now, for testing purposes, you may want to fast-forward the time each round would take. If that's the case, go to *file c_9_time_control.py line 31* and delete the 8 in the parantheses. Then, when asked by the program what time control you want for the tournament, choose bullet. The rounds will only take 10 sec, which is more convenient for testing purposes.

## 📄 Description 

The aim of the project is to respect the Model-View-Controller pattern. In order to do this, we splitted the code in three groups of files. 

The __model__ contains only one file. It defines four classes: Round, Player, Tournament, Matches. The methods defined inside each class computes only data about this particular class. In other words, no computation including data from two separate classes is done in the Model. 
E.g. methods that raise errors if the data inputted by the user isn't usable are defined in Model. However, methods that would return values about the tournament that is taking place aren't defined. 

The __view__ contains two files.  _view.py_ is responsible for taking info from the user. No typecasting is done in the file. All computations are either done in the model or the controller. Therefore, the view is dumb. _view_display.py_ is responsible for displaying data about the tournament progress to the user. 

The __controller__ contains ten files. Broadly speaking, it is responsible for: 
* Pairing players in each round.  
* Creating the tournament, match, player and round instances according to the data entered by the user. Storing the match, round and player instances in the tournament instance.
* Leveraging the methods defined in _model.py_ to serialize and save data in the database when the user needs it. 
* Retrieving and deserializing data from the database when the user needs it.
* Modifying a player's ranking or the tournament's description.
* Managing the flow of the program and updating the time-related tournament data according to the time control choosen by the manager.
* Mocking the tournament progress. 



## 🔧 VIRTUAL ENVIRONMENT

### standard library

dataclasses - The dataclass decorator is used to write three classes in models. I find it more convenient then the classic way of writing classes because it automatically writes the init and repr dunder methods. Moreover, when I started writing the program, I thought that having the eq dunder method automatically wrote might be useful later for sorting the player. Turned out I had to sort players otherwise. 

datetime, time - Mainly used to save the start and end datetime of each round. Also, more convenient for storing player's date of birth and the tournament date. 

itertools - Used once the zip_longest method to dynamically create the match instances for the subsequent rounds in the tournament. 

json - Used when serializing to transform the list of opponents faced by a player into json strings. Used when deserializing to load the table into the program. 

operator - attrgetter was used when I needed to sort on two criterias.

typing, __ future __ - The type annotation improves the readability of the code. 

### third-party 

tinyDB - Used to save data about the tournament or the players in the database and to 

# 👷‍♂️ Contributors

Gide Rutazihana, student, giderutazihana81@gmail.com 
Ashutosh Purushottam, mentor

# License

 There's no license 
