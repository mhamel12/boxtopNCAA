# ===============================================================
# 
# boxtopGameLog.py
#
# CC License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
# https://creativecommons.org/licenses/by-nc/4.0/
#
# Version history
# 07/02/2024  1.0  MH  Initial version
#
# ===============================================================

import argparse, csv, re
from collections import defaultdict

def safeint(string):
    if len(string) > 0:
        return int(string)
    return 0

#########################################################################
#
# Main program starts here
#    

# No command-line arguments are needed, but argparse will automatically print this
# help message and then exit.
parser = argparse.ArgumentParser(description='Create a game log for a specific player from a BOXTOP file.')
parser.add_argument('boxtop_filename', help="Boxtop file") 
parser.add_argument('player_id', help="Player id") 
parser.add_argument('output_filename', help="Output filename")
args = parser.parse_args()

output_file = open(args.output_filename,'w')

output_file.write("DATE,TEAM,OPPONENT,H/R,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PF,BLOCKS,TURNOVERS,STEALS,AST,REB,OREB,PTS,NOTE\n")

start_of_boxscore = "gamebxt"
inventory_logging_on = False

game_count = 0
first_gamebxt_read = False

with open(args.boxtop_filename,'r') as csvfile:
    items = csv.reader(csvfile)
    for row in items:    
        if len(row) > 0:
            if row[0] == "info":
                # IMPORTANT
                # We make the assumption that the rteam/hteam is declared in the boxtop file first.
                
                if row[1] == "rteam":
                    road_team_name = row[2]

                elif row[1] == "hteam":
                    home_team_name = row[2]

                # Also grab some game info so we can track what we are missing
                elif row[1] == "date":
                    game_date = row[2]

                elif row[1] == "title":
                    game_title = row[2]

            elif row[0] == "stat":
                if row[1] == "rteam":
                    tm_str = road_team_name
                    tm_code_str = "R"
                    opponent_tm_str = home_team_name
                else:
                    tm_str = home_team_name
                    tm_code_str = "H"
                    opponent_tm_str = road_team_name
                    
                player_id = row[3]
                    
                if player_id == args.player_id:
                    player_first_name = row[4]
                    player_last_name = row[5]
                
                    player_fgm = row[7]
                    player_ftm = row[9]
                    player_fta = row[10]
                    player_fgm3 = row[11]
                    player_fga3 = row[12]
                    player_pts = row[13]
                    player_pf = row[17]
                    
                    player_min = row[6]
                    player_fga = row[8]
                    player_oreb = row[14]
                    player_reb = row[15]
                    player_ast = row[16]
                    player_blocks = row[18]
                    player_turnovers = row[19]
                    player_steals = row[20]   
                    
                    # output_file.write("DATE,TEAM,OPPONENT,H/R,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PF,BLOCKS,TURNOVERS,STEALS,AST,REB,OREB,PTS,NOTE\n")
                    output_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (game_date,tm_str,opponent_tm_str,tm_code_str,player_min,player_fgm,player_fga,player_ftm,player_fta,player_fgm3,player_fga3,player_pf,player_blocks,player_turnovers,player_steals,player_ast,player_reb,player_oreb,player_pts,game_title))

output_file.close()

print("File %s created." % (args.output_filename))
