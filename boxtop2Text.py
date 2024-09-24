# ===============================================================
# 
# boxtop2Text.py
#
# (c) 2024 Michael Hamel
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit # http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
#
# Version history
# 08/11/2024  1.1  MH  Update formats for 1970's NCAA games.
# 07/04/2024  1.0  MH  Initial version, based on box2text.pl from the Larry Bird/ISU project.
#
# ===============================================================

import argparse, csv, re
from collections import defaultdict

# ===============================================================

# store data split in this dictionary
info = defaultdict(dict)

# store data as lists in these dictionaries, indexed by hteam and rteam
coaches = defaultdict(dict)
team_stats = defaultdict(dict)
linescores = defaultdict(dict)
team_technicals = defaultdict(dict)

# store data as lists in these dictionaries, indexed by player id
road_player_stats = defaultdict(dict)
home_player_stats = defaultdict(dict)

last_names_dict = defaultdict(dict)

game_count = 1
ref_count = 1
player_count = 0

# ===============================================================

# Determines if a numerial string contains a non-zero number
def is_nonzero(the_string):
    if len(the_string) > 0:
       if int(the_string) > 0:
           return True
           
    return False

def dump_team_to_file(team,team_name,header,boxscore_type_for_this_game):
    if team == "hteam":
        player_stats = home_player_stats
    else:
        player_stats = road_player_stats
    
    # stats go here in simple .csv tables...
    output_file.write("%s" % (team_name.upper()))
    output_file.write("%s" % (header))
    

    # 0    1           2      3  4         5        6   7   8   9   10  11   12   13  14   15  16  17 18     19        20     21
    # stat,rteam|hteam,player,ID,FIRSTNAME,LASTNAME,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PTS,OREB,REB,AST,PF,BLOCKS,TURNOVERS,STEALS,TECHNICALFOUL
        
    for p in player_stats:

        if len(player_stats[p][4]) > 0: # first name included
            player_name = player_stats[p][4] + " " + player_stats[p][5]
        else:
            player_name = player_stats[p][5]
        
        if boxscore_type_for_this_game == "deluxe":
            #  First Name      Last Name      MIN            FGM            FGA            FTM            FTA            REB             AST             STL             BLK             TOV              PF              PTS
            output_file.write( "%s,%s,%s-%s,%s-%s,%s,%s,%s,%s,%s,%s,%s\n" % (player_name,player_stats[p][6],player_stats[p][7],player_stats[p][8],player_stats[p][9],player_stats[p][10],player_stats[p][15],player_stats[p][16],player_stats[p][20],player_stats[p][18],player_stats[p][19],player_stats[p][17],player_stats[p][13]))
            
        elif boxscore_type_for_this_game == "minutes":
            #  First Name      Last Name     MIN             FGM            FGA            FTM            FTA             REB             AST             PF              PTS
            output_file.write( "%s,%s,%s-%s,%s-%s,%s,%s,%s,%s\n" % (player_name,player_stats[p][6],player_stats[p][7],player_stats[p][8],player_stats[p][9],player_stats[p][10],player_stats[p][15],player_stats[p][16],player_stats[p][17],player_stats[p][13]))
            
        elif boxscore_type_for_this_game == "standard":
            # First Name      Last Name     FGM            FGA            FTM            FTA             REB             AST             PF              PTS
            output_file.write( "%s,%s-%s,%s-%s,%s,%s,%s,%s\n" % (player_name,player_stats[p][7],player_stats[p][8],player_stats[p][9],player_stats[p][10],player_stats[p][15],player_stats[p][16],player_stats[p][17],player_stats[p][13]))

        elif boxscore_type_for_this_game == "noassists":
            # First Name      Last Name     FGM            FGA            FTM            FTA             REB             PF              PTS
            output_file.write( "%s,%s-%s,%s-%s,%s,%s,%s\n" % (player_name,player_stats[p][7],player_stats[p][8],player_stats[p][9],player_stats[p][10],player_stats[p][15],player_stats[p][17],player_stats[p][13]))
            
        elif boxscore_type_for_this_game == "basic":
            #                        First Name      Last Name     FGM         FTM            FTA             PTS
            output_file.write( "%s,%s,%s-%s,%s\n" % (player_name,player_stats[p][7],player_stats[p][9],player_stats[p][10],player_stats[p][13]))

        elif boxscore_type_for_this_game == "freshmen":
            #                        First Name      Last Name     PTS
            output_file.write( "%s,%s\n" % (player_name,player_stats[p][13]))
    
    # Add rebounds + teamrebounds together to match usual boxscore format
    # If no rebounds available, then print a blank
    
    if is_nonzero(team_stats[team][17]): # team rebounds
        if is_nonzero(team_stats[team][11]): # rebounds
            rebounds = str(int(team_stats[team][11]) + int(team_stats[team][17]))
        else:
            rebounds = ""
    elif is_nonzero(team_stats[team][11]):
        rebounds = team_stats[team][11]
    else:
        rebounds = ""
 
    # 0     1           2   3   4   5   6   7    8    9   10   11  12  13 14     15        16     17           18
    # tstat,rteam|hteam,MIN,FGM,FGA,FTM,FTA,FG3M,FG3A,PTS,OREB,REB,AST,PF,BLOCKS,TURNOVERS,STEALS,TEAMREBOUNDS,TECHNICALFOUL
    
    if boxscore_type_for_this_game == "deluxe":
        # MIN     FGM                  FGA                FTM                 FTA                 REB       AST             STL             BLK             TOV              PF              PTS
        output_file.write( "TOTALS,%s,%s-%s,%s-%s,%s,%s,%s,%s,%s,%s,%s\n" % (team_stats[team][2],team_stats[team][3],team_stats[team][4],team_stats[team][5],team_stats[team][6],team_stats[team][11],team_stats[team][12],team_stats[team][16],team_stats[team][14],team_stats[team][15],team_stats[team][13],team_stats[team][9]))

        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))

    elif boxscore_type_for_this_game == "minutes":
        # MIN                      FGM                  FGA                FTM                 FTA                 REB       AST                  PF                   PTS
        output_file.write( "TOTALS,%s,%s-%s,%s-%s,%s,%s,%s,%s\n" % (team_stats[team][2],team_stats[team][3],team_stats[team][4],team_stats[team][5],team_stats[team][6],team_stats[team][11],team_stats[team][12],team_stats[team][13],team_stats[team][9]))

        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))

    elif boxscore_type_for_this_game == "standard":
        # FGM                  FGA                FTM                 FTA                 REB       AST                  PF                   PTS
        output_file.write( "TOTALS,%s-%s,%s-%s,%s,%s,%s,%s\n" % (team_stats[team][3],team_stats[team][4],team_stats[team][5],team_stats[team][6],team_stats[team][11],team_stats[team][12],team_stats[team][13],team_stats[team][9]))

        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))
    
    elif boxscore_type_for_this_game == "noassists":
        # FGM                  FGA                FTM                 FTA                 REB       PF                   PTS
        output_file.write( "TOTALS,%s-%s,%s-%s,%s,%s,%s\n" % (team_stats[team][3],team_stats[team][4],team_stats[team][5],team_stats[team][6],team_stats[team][11],team_stats[team][13],team_stats[team][9]))

        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))
            
    elif boxscore_type_for_this_game == "basic":
        # FGM                 FTM                 FTA                 PTS
        output_file.write( "TOTALS,%s,%s-%s,%s\n" % (team_stats[team][3],team_stats[team][5],team_stats[team][6],team_stats[team][9]))
        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))
        if is_nonzero(team_stats[team][13]):
            output_file.write( "Team Fouls: %s\n" % (team_stats[team][13]))

    elif boxscore_type_for_this_game == "freshmen":
        # PTS
        output_file.write( "TOTALS,%s\n" % (team_stats[team][9]))
        if is_nonzero(team_stats[team][17]):
            output_file.write( "Team Rebounds: %s\n" % (team_stats[team][17]))
    
    extra_stats = defaultdict()
    
    extra_stats["ThreePointFG"] = ""
    extra_stats["TechnicalFouls"] = "" # TBD: I ported this from the perl version, but the Bird files never filled in technical fouls for individual players and coaches. So this was never used with that data set. Instead, info["techs"] was used to track technical fouls. But in the boxtopNCAA.py file I am trying to collect technical fouls for players and coaches as I originally intended.
    extra_stats["Blocks"] = ""
    extra_stats["Steals"] = ""
    extra_stats["Turnovers"] = ""


    for p in player_stats:
        last_name = player_stats[p][5]
        # if (last_names_dict[last_name] > 1):
            # there's more than one player in this boxscore with this last name, so prepend first initial
            # last_name = player_stats[p][4][0] + ". " + last_name
        
        # TBD: In theory, we could have games with rebounds/assists for just a few players, and it would
        #      be nice to add those to "basic" and "freshmen" box scores, but for the UCLA Walton case,
        #      that use case does not exist.
        if boxscore_type_for_this_game != "deluxe":
            if is_nonzero(player_stats[p][11]) or is_nonzero(player_stats[p][12]):
                if len(extra_stats["ThreePointFG"]) > 0:
                    extra_stats["ThreePointFG"] = extra_stats["ThreePointFG"] + ", "
                
                if is_nonzero(player_stats[p][12]):
                    temp = last_name + " " + player_stats[p][11] + "-" + player_stats[p][12]

                else: # omit 3FGA because they are missing
                    temp = last_name + " " + player_stats[p][11]

                extra_stats["ThreePointFG"] = extra_stats["ThreePointFG"] + temp

            if is_nonzero(player_stats[p][18]):
                if len(extra_stats["Blocks"]) > 0:
                    extra_stats["Blocks"] = extra_stats["Blocks"] + ", "
                
                temp = last_name
                if (int(player_stats[p][18]) > 1): 
                    temp = temp + " " + player_stats[p][18]
                extra_stats["Blocks"] = extra_stats["Blocks"] + temp

            if is_nonzero(player_stats[p][19]):
                if len(extra_stats["Turnovers"]) > 0:
                    extra_stats["Turnovers"] = extra_stats["Turnovers"] + ", "
                
                temp = last_name
                if (int(player_stats[p][19]) > 1):
                    temp = temp + " " + player_stats[p][19]
                extra_stats["Turnovers"] = extra_stats["Turnovers"] + temp
                
            if is_nonzero(player_stats[p][20]):
                if len(extra_stats["Steals"]) > 0:
                    extra_stats["Steals"] = extra_stats["Steals"] + ", "
                                
                temp = last_name
                if (int(player_stats[p][20]) > 1):
                    temp = temp + " " + player_stats[p][20]
                extra_stats["Steals"] = extra_stats["Steals"] . temp
    
    
        # Technical foul handling for players
        if is_nonzero(player_stats[p][21]):
            if len(extra_stats["TechnicalFouls"]) > 0:
                print("Hot here")
                extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + ", "
                        
            temp = last_name
            if (int(player_stats[p][21]) > 1):
                temp = temp + " " + player_stats[p][21] + " "

            extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + temp

#        else:
#            extra_stats["TechnicalFouls"] = ""
    
    # Technical foul handling for coaches and teams
    if is_nonzero(coaches[team][5]):
        if len(extra_stats["TechnicalFouls"]) > 0:
            extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + ", "
                        
        temp = coaches[team][4]
        
        # This should be safe to do because we checked this value using is_nonzero()
        if (int(coaches[team][5]) > 1):
            temp = temp + " " + coaches[team][5] + " "

        extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + temp
    
    if is_nonzero(team_technicals[team]):
        if len(extra_stats["TechnicalFouls"]) > 0:
            extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + ", "
                        
        extra_stats["TechnicalFouls"] = extra_stats["TechnicalFouls"] + team_technicals[team]
    
    # prepend team totals and then list individual players
    if boxscore_type_for_this_game != "deluxe":
        if len(extra_stats["ThreePointFG"]) > 0:
            if is_nonzero(team_stats[team][8]):
                extra_stats["ThreePointFG"] = team_stats[team][7] + "-" + team_stats[team][8] + " (" + extra_stats["ThreePointFG"] + ")"

            else: # 3FGA missing
                extra_stats["ThreePointFG"] = team_stats[team][7] + " (" + extra_stats["ThreePointFG"] + ")"

        if len(extra_stats["Blocks"]) > 0:
            extra_stats["Blocks"] = team_stats[team][14] + " (" + extra_stats["Blocks"] + ")"

        if len(extra_stats["Turnovers"]) > 0:
            extra_stats["Turnovers"] = team_stats[team][15] + " (" + extra_stats["Turnovers"] + ")"

        if len(extra_stats["Steals"]) > 0:
            extra_stats["Steals"] = team_stats[team][16] + " (" + extra_stats["Steals"] + ")"
    
    # print any non-empty fields
    
    if len(extra_stats["ThreePointFG"]) > 1:
        output_file.write( "3-point FG: %s.\n" % (extra_stats["ThreePointFG"]))

    if len(extra_stats["TechnicalFouls"]) > 1:
        output_file.write( "Technical Fouls: %s.\n" % (extra_stats["TechnicalFouls"]))

    if len(extra_stats["Blocks"]) > 1:
        output_file.write( "Blocks: %s.\n" % (extra_stats["Blocks"]))
    
    if len(extra_stats["Steals"]) > 1:
        output_file.write( "Steals: %s.\n" % (extra_stats["Steals"]))
    
    if len(extra_stats["Turnovers"]) > 1:
        output_file.write( "Turnovers: %s.\n" % (extra_stats["Turnovers"]))

    output_file.write( "\n" )


def dump_textdata_to_file(boxscore_type,game_count):

    # derive boxscore_type for this game if not set by user
    if (boxscore_type == "derive"):
        
        # 0     1           2   3   4   5   6   7    8    9   10   11  12  13 14     15        16     17           18
        # tstat,rteam|hteam,MIN,FGM,FGA,FTM,FTA,FG3M,FG3A,PTS,OREB,REB,AST,PF,BLOCKS,TURNOVERS,STEALS,TEAMREBOUNDS,TECHNICALFOUL
        
        if (team_stats["hteam"][14] != "") and (team_stats["hteam"][15] != "") and (team_stats["hteam"][16] != ""):
            # found blocks, turnovers, steals
            boxscore_type_for_this_game = "deluxe"
        
        elif (team_stats["hteam"][2] != "") and (team_stats["hteam"][12] != ""):
            # found minutes and assists
            boxscore_type_for_this_game = "minutes"

        elif (team_stats["hteam"][12] != ""):
            # found assists
            boxscore_type_for_this_game = "standard"

        elif (team_stats["hteam"][11] != ""):
            # found rebounds
            boxscore_type_for_this_game = "noassists"

        elif (team_stats["hteam"][3] != ""):
            # found FGM
            boxscore_type_for_this_game = "basic"

        else:
            boxscore_type_for_this_game = "freshmen"

    else:
        boxscore_type_for_this_game = boxscore_type

    header = stat_headers[boxscore_type_for_this_game]
    
    output_file.write("Game %d\n" % (game_count))

    output_file.write("%s vs. %s\n" % (info["rteam"],info["hteam"]))
    output_file.write("%s\n%s %s at %s\n%s, %s, %s\n" % (info["title"], info["dayofweek"], info["date"], info["arena"], info["city"], info["state"], info["country"]))

    #
    # Road Team
    #
    output_file.write( "\n%s\n\n" % (info["rteam"]))
    dump_team_to_file("rteam",info["rteam"],header,boxscore_type_for_this_game)
    
    #
    # Home Team
    #
    output_file.write( "\n%s\n\n" % (info["hteam"]))
    dump_team_to_file("hteam",info["hteam"],header,boxscore_type_for_this_game)
           
    #        
    # linescores in a table
    #
    column_count = len(linescores["rteam"]) # assume both the same length for now
    
    # columns 0 and 1 are 'linescore' and 'rteam/hteam'
    # last column is final score, even if there is no information for quarters/halves
    # could be a colon before the final score
    
    # extra column in first line to provide space for team name
    output_file.write("\n,")
    cc = 2
    period_count = 0
    while cc < column_count-1:
        if linescores["rteam"][cc] != ":":
            period_count += 1
            if period_count == 3:
                period = "OT"
            elif period_count >= 4:
                period = "O" + str(period_count-2)
            else:
                period = period_count
            
            output_file.write("%s," % (period))
            
        cc += 1
    
    output_file.write("F\n")

    output_file.write("%s," % (info["rteam"].upper()))
    cc = 2
    while cc < column_count-1:
        if linescores["rteam"][cc] != ":":
            output_file.write("%s," % (linescores["rteam"][cc]))
        cc += 1
    # print("%s %s" % (cc,linescores["rteam"]))
    output_file.write("%s\n" % (linescores["rteam"][cc])) # was +1
    
    output_file.write("%s," % (info["hteam"].upper()))
    cc = 2
    while cc < column_count-1:
        if linescores["hteam"][cc] != ":":
            output_file.write("%s," % (linescores["hteam"][cc]))
        cc += 1
    output_file.write("%s\n" % (linescores["hteam"][cc])) # was +1

    output_file.write("\nHead Coaches: ")
    output_file.write("%s - %s %s" % (info["rteam"], coaches["rteam"][3], coaches["rteam"][4]))
    output_file.write(", ")
    output_file.write("%s - %s %s" % (info["hteam"], coaches["hteam"][3], coaches["hteam"][4]))
    output_file.write("\n\n")
        
    # Omit the following fields if they are empty
    if "techs" in info:
        if len(info["techs"]) > 0:
            output_file.write("Technical Fouls (other): %s\n" % (info["techs"]))
            
    if "attendance" in info:
        if len(info["attendance"]) > 0:
            output_file.write("Attendance: %s\n" % (info["attendance"]))
            
    if "starttime" in info:
        if len(info["starttime"]) > 0 and info["starttime"] != "00:00PM":
            output_file.write("Start Time: %s %s\n" % (info["starttime"],info["timezone"]))
           
    if "ref3" in info and len(info["ref3"]) > 0:
        output_file.write("Referees: %s, %s, %s\n" % (info["ref1"], info["ref2"], info["ref3"]))
    elif "ref1" in info:
        if len(info["ref1"]) > 0:
            output_file.write("Referees: %s, %s\n" % (info["ref1"], info["ref2"]))

    if "note" in info:
        if len(info["note"]) > 0:
            output_file.write("Game Notes: %s\n\n" % (info["note"]))
    
    output_file.write("\n==============================\n")



#########################################################################
#
# Main program starts here
#    

# Frequently used headers for NCAA games in the mid-1970s. 
# 3-point field goal rule was not in effect, so skip those.
stat_headers = { "freshmen" : ",PTS\n", "basic" : ",FG,FT-A,PTS\n", "noassists" : ",FG-A,FT-A,RB,PF,PTS\n", "standard" : ",FG-A,FT-A,RB,A,PF,PTS\n", "minutes" : ",M,FG-A,FT-A,RB,A,PF,PTS\n", "deluxe" : ",M,FG-A,FT-A,RB,A,STL,BLK,TOV,PF,PTS\n"};

# No command-line arguments are needed, but argparse will automatically print this
# help message and then exit.
parser = argparse.ArgumentParser(description='Convert a boxtop-format file into a single text file suitable for pasting into a word processor program.')
parser.add_argument('boxtop_filename', help="Boxtop file") 
parser.add_argument('output_filename', help="Output filename")
parser.add_argument('-format', help="Default format is derived for each game, but can override with: %s" % list(stat_headers.keys())) 
args = parser.parse_args()

boxscore_option = "derive"
if args.format:
    if args.format in stat_headers:
        boxscore_option = args.format

output_file = open(args.output_filename,'w')

start_of_boxscore = "gamebxt"
first_gamebxt_read = False

with open(args.boxtop_filename,'r') as csvfile:
    items = csv.reader(csvfile)
    for row in items:    
        if len(row) > 0:
            save_this_line = row
            
            if not first_gamebxt_read:
                if row[0] == start_of_boxscore:
                    first_gamebxt_read = True
                    
            elif row[0] == start_of_boxscore:
                dump_textdata_to_file(boxscore_option,game_count)
                ref_count = 1
                player_count = 0
                game_count += 1
                
                # clear all hashes
                info.clear()
                coaches.clear()
                team_stats.clear()
                team_technicals.clear()
                linescores.clear()
                road_player_stats.clear()
                home_player_stats.clear()
                last_names_dict.clear()
                
            elif row[0] == "info":
                # special handling for referees
                if row[1] == "ref":
                    key = "ref%s" % str(ref_count)
                    info[key] = row[2]
                    ref_count += 1
                
                # special handling for notes
                elif row[1] == "note" or row[1] == "event" or row[1] == "prelim":
                    key = row[1]
                    complete_note = ''.join(row[2:]).strip() # combine the rest of the line into a single string with no extra space in between
                    if key in info:
                        # Add to output
                        info[key] = info[key] + "..." + complete_note
                    else:
                        info[key] = complete_note
                elif row[1] == "techs":
                    key = row[1]
                    complete_note = ','.join(row[2:]).strip() # combine the rest of the line into a single string with comma in between
                    if key in info:
                        # Add to output
                        info[key] = info[key] + "..." + complete_note
                    else:
                        info[key] = complete_note
                else:
                    info[row[1]] = row[2]
                    
                    
            elif row[0] == "coach":
                coaches[row[1]] = row # TBD the original script stored the entire line as a list, this should be the same
                
            elif row[0] == "stat":
                key = "player-" + str(player_count) # TBD the goal is to keep the players in the order as shown in BOXTOP file. Not sure if this is needed, since dictionaries are supposed to maintain their order. Might need to use a letter scheme like "A", followed by "AA", followed by "AAA".
                if row[1] == "rteam":
                    road_player_stats[key] = row
                else:
                    home_player_stats[key] = row
                player_count += 1
                
                last_name = row[5]
                if last_name in last_names_dict:
                    last_names_dict[last_name] += 1
                else:
                    last_names_dict[last_name] = 1

            elif row[0] == "tstat":
                team_stats[row[1]] = row
                
            elif row[0] == "linescore":
                linescores[row[1]] = row

# end of main loop

dump_textdata_to_file(boxscore_option,game_count) # dump the last game

output_file.close()

print("File %s created. %s games scanned." % (args.output_filename,game_count))



