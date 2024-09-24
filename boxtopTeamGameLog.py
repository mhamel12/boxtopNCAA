# ===============================================================
# 
# boxtopTeamGameLog.py
#
# CC License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
# https://creativecommons.org/licenses/by-nc/4.0/
#
# Version history
# 08/10/2024  1.0  MH  Initial version
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
parser = argparse.ArgumentParser(description='Create a game log for a specific team from a BOXTOP file.')
parser.add_argument('boxtop_filename', help="Boxtop file") 
parser.add_argument('team_id', help="Team name") 
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

            elif row[0] == "tstat":
                if row[1] == "rteam":
                    tm_str = road_team_name
                    tm_code_str = "R"
                    opponent_tm_str = home_team_name
                    
                    if tm_str == args.team_id:
                        team_fgm = row[3]
                        team_ftm = row[5]
                        team_fta = row[6]
                        team_fgm3 = row[7]
                        team_fga3 = row[8]
                        team_pts = row[9]
                        team_pf = row[13]
                        
                        team_min = row[2]
                        team_fga = row[4]
                        team_oreb = row[10]
                        team_reb = row[11]
                        team_ast = row[12]
                        team_blocks = row[14]
                        team_turnovers = row[15]
                        team_steals = row[16]   
                        
                        # output_file.write("DATE,TEAM,OPPONENT,H/R,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PF,BLOCKS,TURNOVERS,STEALS,AST,REB,OREB,PTS,NOTE\n")
                        output_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (game_date,tm_str,opponent_tm_str,tm_code_str,team_min,team_fgm,team_fga,team_ftm,team_fta,team_fgm3,team_fga3,team_pf,team_blocks,team_turnovers,team_steals,team_ast,team_reb,team_oreb,team_pts,game_title))
                    
                else:
                    tm_str = home_team_name
                    tm_code_str = "H"
                    opponent_tm_str = road_team_name
                    
                    if tm_str == args.team_id:
                        team_fgm = row[3]
                        team_ftm = row[5]
                        team_fta = row[6]
                        team_fgm3 = row[7]
                        team_fga3 = row[8]
                        team_pts = row[9]
                        team_pf = row[13]
                        
                        team_min = row[2]
                        team_fga = row[4]
                        team_oreb = row[10]
                        team_reb = row[11]
                        team_ast = row[12]
                        team_blocks = row[14]
                        team_turnovers = row[15]
                        team_steals = row[16]   
                        
                        # output_file.write("DATE,TEAM,OPPONENT,H/R,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PF,BLOCKS,TURNOVERS,STEALS,AST,REB,OREB,PTS,NOTE\n")
                        output_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (game_date,tm_str,opponent_tm_str,tm_code_str,team_min,team_fgm,team_fga,team_ftm,team_fta,team_fgm3,team_fga3,team_pf,team_blocks,team_turnovers,team_steals,team_ast,team_reb,team_oreb,team_pts,game_title))                    
                    

output_file.close()

print("File %s created." % (args.output_filename))
