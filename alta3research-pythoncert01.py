#!/usr/bin/env python3


""" Created: Brent Reich
    This is a silly little game called "Bork", based on old text based games.
    Just run the command, nothing special is needed. should be self-explanatory.
    """

import sys
from random import randint #needed for dice rolling
from time import sleep  #needed for pause between combat, so it doesnt scroll by a million MPH.

#define character
player = {'name':'Player','cur_health':50,'max_health':50,'weapon':'kung-fu','min_damage':1,'max_damage':8,'att_type':'chop'}

# dictionary of monsters
monsters = {1:{'name':'Gnoll','cur_health':10,'max_health':10,'weapon':'sword','min_damage':1,'max_damage':6,'att_type':'stabs'},
            2:{'name':'Goblin','cur_health':10,'max_health':10,'weapon':'axe','min_damage':1,'max_damage':6,'att_type':'swings'},
            3:{'name':'Werechicken','cur_health':10,'max_health':10,'weapon':'beak','min_damage':2,'max_damage':8,'att_type':'pecks'},
            4:{'name':'Orc','cur_health':10,'max_health':10,'weapon':'spear','min_damage':1,'max_damage':10,'att_type':'thrust'},
            5:{'name':'Boss','cur_health':20,'max_health':20,'weapon':'Flaming Sword of Doom','min_damage':2,'max_damage':12,'att_type':'swings'}
           }

# the location dict describes the game map. its a single corridor with a with a room in the middle and end.
location = {1:{'name':'Entrance','enemy':'no','description':'You see an old, crumbling, stone staircase leading down into a mysterious crypt','exits':['down','q to exit']},
            2:{'name':'South Hallway','enemy':'no','description':'You are in a dark, gloomy corrider, there are spider webs everywhere. ick!','exits':['north','up','q to exit']},
            3:{'name':'Monster Room 1','enemy':'yes','description':'You are in a large circular room','exits':['north','south','q to exit']},
            4:{'name':'North Hallway','enemy':'no','description':'You are in a dark, gloomy corrider, there is glowing slime oozing down the walls.','exits':['north','south','q to exit']},
            5:{'name':'Boss Room','enemy':'yes','description':'You are in an immense room with large stalagtites hanging almost to the floor','exits':['south','q to exit']}
           }

#set initial player location
PLAYER_LOC = location[1]   #made all caps for pylint recommendation, also its set to global later.

def move_handler():
    """ this func takes care of moving around in the map, describing your location and taking input from user. """

    global PLAYER_LOC #I read this is discouraged, but i ran into alot of issues returning something like myloc = PLAYER_LOC back to main. this worked.

    # get user input for where to go
    direction = input(f"Which way would you like to go? {PLAYER_LOC['exits']}: ")
    print("")

    #evaluate location and direction and move accordingly
    if direction.lower() == "q":
        print("Exiting game .....")
        sys.exit()
    if (PLAYER_LOC == location[1]) and (direction.lower() == "down"):
        PLAYER_LOC = location[2]
    elif (PLAYER_LOC == location[2]) and (direction.lower() == "up"):
        PLAYER_LOC = location[1]
    elif (PLAYER_LOC == location[2]) and (direction.lower() == "north"):
        PLAYER_LOC = location[3]
    elif (PLAYER_LOC == location[3]) and (direction.lower() == "north"):
        PLAYER_LOC = location[4]
    elif (PLAYER_LOC == location[3]) and (direction.lower() == "south"):
        PLAYER_LOC = location[2]
    elif (PLAYER_LOC == location[4]) and (direction.lower() == "north"):
        PLAYER_LOC = location[5]
    elif (PLAYER_LOC == location[4]) and (direction.lower() == "south"):
        PLAYER_LOC = location[3]
    elif (PLAYER_LOC == location[5]) and (direction.lower() == "south"):
        PLAYER_LOC = location[4]
    else:
        print("Invalid input....") # informs user they didnt use a valid input. this exits the func and main will plop them right back here for another try.

#print game start dialogue.  only used at startup
print("The masters at the ancient Shao-Lin monastary have requested you investigate a crypt to the north, reports have been given that it has been taken over by monsters.")
print("")
print("you proceed north to investigate...")
print("")

def combat():
    """ set up vars needed for combat and resolves combat """
    print("Entering combat ...")

    # checks to see if boss room or not to pick the right type of monster
    if PLAYER_LOC != location[5]:
        my_random_int = randint(1,4)
        this_monster = monsters[my_random_int]
    else:
        this_monster = monsters[5]

    #sets vars for combat. rolls dmg, applies dmg, checks health conditions.
    while True: #set loop condition
	# factor dmg and apply to player and monster health
        player_dmg_done = randint(player['min_damage'], player['max_damage'])
        this_monster_dmg_done = randint(this_monster['min_damage'], this_monster['max_damage'])
        this_monster['cur_health'] = this_monster['cur_health'] - player_dmg_done
        player['cur_health'] = player['cur_health'] - this_monster_dmg_done
        print("")

        #this if/else is needed to distinguish random monsters vs boss.
        if PLAYER_LOC != location[5]:
            print(f"You use your {player['weapon']} to deliver a mighty {player['att_type']} to the {this_monster['name']} and deliver {player_dmg_done} dmg! {this_monster['cur_health']}/{monsters[my_random_int]['max_health']}")
        else:
            print(f"You use your {player['weapon']} to deliver a mighty {player['att_type']} to the {this_monster['name']} and deliver {player_dmg_done} dmg! {this_monster['cur_health']}/{monsters[5]['max_health']}")
       
        #evalute player and monster health to determin win/loss of combat 
        if this_monster["cur_health"] <= 0: #evaluate monster health
            #this if/else is needed to resolve random monsters vs boss and gives outcome messages.
            if this_monster != monsters[5]:
                print(f"You have slain the {this_monster['name']}!!") #victory is sweet!
            else:
                print("You have slain the Boss!! Folk across the country will sing your name in praise and heap wealth and glory upon you! congratulations you have won the game!!") #victory is sweet!
                sys.exit()
            print("")
            break
        print(f"The {this_monster['name']} {this_monster['att_type']} with his {this_monster['weapon']} and delivers {this_monster_dmg_done} dmg to you! {player['cur_health']}/{player['max_health']}")
        if player["cur_health"] <= 0: #evaluate the player health
            print("You have died ......") #game over, man. game over.
            sys.exit()
        sleep(2)

# game engine
def main():
    """ main engine of the game """
    #start game loop
    while True:
        global PLAYER_LOC
        if PLAYER_LOC["enemy"] == "yes":   #hallways and entrance do not have monsters. if i had more time i would add a % chance for random encounter.
            #describe the new location. 
            print(f"You have arrived at the {PLAYER_LOC['name']}. {PLAYER_LOC['description']}. There are exits to the {PLAYER_LOC['exits']}.")
            print("There is a monster here")

            # fleeing results in returning to the previous location. fighting will engage the monster.
            answer = input("Do you want to fight or flee?: ")
            while (answer.lower() != "fight") and (answer.lower() != "flee"):
                print(answer.lower())
                answer = input("Invalid input. Do you want to fight or flee?: ")
            if answer.lower() == "fight":
                combat()
                if PLAYER_LOC == location[3]:
                    location[3]['enemy'] = 'no'
            elif answer.lower() == "flee":
                if PLAYER_LOC == location[3]:
                    PLAYER_LOC = location[2]
                    print("")
                elif PLAYER_LOC == location[5]:
                    PLAYER_LOC = location[4]
                    print("")
            else:
                print("Game Error. something unexpected happened ... Exiting")
        print(f"You have arrived at the {PLAYER_LOC['name']}. {PLAYER_LOC['description']}. There are exits to the {PLAYER_LOC['exits']}.")
        
        # throw to the move_handler function
        move_handler()

if __name__ == "__main__":
    main()
