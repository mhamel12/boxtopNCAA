# ===============================================================
# 
# boxtopcheck.py
#
# CC License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
# https://creativecommons.org/licenses/by-nc/4.0/
#
# Version history
# 06/21/2024  1.0  MH  Initial version
#
# ===============================================================

import argparse, csv, re
from collections import defaultdict

game_count = 0

log_dump = ""

def log_it(string_to_print):
    print(string_to_print)
    global log_dump
    log_dump = log_dump + "\n" + string_to_print
    

# Set to True to print games where a stat is missing; especially useful for cases like FGM, 
# FTM, PTS where we should have these stats for EVERY game but can be useful for any stat.
# BE SURE TO TURN ON THE ONES YOU WANT TO USE by searching the code
verbose_print = True

# Use dictionaries for players - one entry per player, covers current game
player_games_played = defaultdict()
player_fgm = defaultdict()
player_ftm = defaultdict()
player_fta = defaultdict()
player_fgm3 = defaultdict()
player_fga3 = defaultdict()
player_pf = defaultdict()
player_pts = defaultdict()
player_first_names = defaultdict()
player_last_names = defaultdict()
player_min = defaultdict()
player_fga = defaultdict()
player_reb = defaultdict()
player_ast = defaultdict()
player_oreb = defaultdict()
player_blocks = defaultdict()
player_turnovers = defaultdict()
player_steals = defaultdict()

# Use dictionaries for player stats totals - one entry per team, covers current game
player_totals_for_current_game_fgm = defaultdict()
player_totals_for_current_game_ftm = defaultdict()
player_totals_for_current_game_fta = defaultdict()
player_totals_for_current_game_fgm3 = defaultdict()
player_totals_for_current_game_fga3 = defaultdict()
player_totals_for_current_game_pf = defaultdict()
player_totals_for_current_game_pts = defaultdict()
player_totals_for_current_game_min = defaultdict()
player_totals_for_current_game_fga = defaultdict()
player_totals_for_current_game_reb = defaultdict()
player_totals_for_current_game_ast = defaultdict()
player_totals_for_current_game_oreb = defaultdict()
player_totals_for_current_game_blocks = defaultdict()
player_totals_for_current_game_turnovers = defaultdict()
player_totals_for_current_game_steals = defaultdict()

# Use dictionaries for players - one entry per team, covers current game
team_fgm = defaultdict()
team_ftm = defaultdict()
team_fta = defaultdict()
team_fgm3 = defaultdict()
team_fga3 = defaultdict()
team_pf = defaultdict()
team_pts = defaultdict()
team_first_names = defaultdict()
team_last_names = defaultdict()
team_min = defaultdict()
team_fga = defaultdict()
team_reb = defaultdict()
team_team_reb = defaultdict()
team_ast = defaultdict()
team_oreb = defaultdict()
team_blocks = defaultdict()
team_turnovers = defaultdict()
team_steals = defaultdict()

current_game_counters = {"minutes" : int(0), "fgm" : int(0), "fga" : int(0), "ftm" : int(0), "fta" : int(0), "fgm3" : int(0), "fga3" : int(0), "pf" : int(0), "pts" : int(0), "min" : int(0), "reb" : int(0), "ast" : int(0), "team_reb" : int(0), "games" : int(0), "oreb" : int(0), "blocks" : int(0), "steals" : int(0), "turnovers" : int(0)};

season_player_games_played = defaultdict()
season_player_fgm = defaultdict()
season_player_ftm = defaultdict()
season_player_fta = defaultdict()
season_player_fgm3 = defaultdict()
season_player_fga3 = defaultdict()
season_player_pf = defaultdict()
season_player_pts = defaultdict()
season_player_first_names = defaultdict()
season_player_last_names = defaultdict()
season_player_min = defaultdict()
season_player_fga = defaultdict()
season_player_reb = defaultdict()
season_player_ast = defaultdict()
season_player_oreb = defaultdict()
season_player_blocks = defaultdict()
season_player_turnovers = defaultdict()
season_player_steals = defaultdict()

season_team_games_played = defaultdict()
season_team_fgm = defaultdict()
season_team_ftm = defaultdict()
season_team_fta = defaultdict()
season_team_fgm3 = defaultdict()
season_team_fga3 = defaultdict()
season_team_pf = defaultdict()
season_team_pts = defaultdict()
season_team_min = defaultdict()
season_team_fga = defaultdict()
season_team_reb = defaultdict()
season_team_team_reb = defaultdict()
season_team_ast = defaultdict()
season_team_oreb = defaultdict()
season_team_blocks = defaultdict()
season_team_turnovers = defaultdict()
season_team_steals = defaultdict()

season_stat_counters_games_played = defaultdict()
season_stat_counters_fgm = defaultdict()
season_stat_counters_ftm = defaultdict()
season_stat_counters_fta = defaultdict()
season_stat_counters_fgm3 = defaultdict()
season_stat_counters_fga3 = defaultdict()
season_stat_counters_pf = defaultdict()
season_stat_counters_pts = defaultdict()
season_stat_counters_min = defaultdict()
season_stat_counters_fga = defaultdict()
season_stat_counters_reb = defaultdict()
season_stat_counters_team_reb = defaultdict()
season_stat_counters_ast = defaultdict()
season_stat_counters_oreb = defaultdict()
season_stat_counters_blocks = defaultdict()
season_stat_counters_turnovers = defaultdict()
season_stat_counters_steals = defaultdict()

# missing = stat is completely missing from the box score
missing_stat_list_fgm = []
missing_stat_list_ftm = []
missing_stat_list_fta = []
missing_stat_list_fgm3 = []
missing_stat_list_fga3 = []
missing_stat_list_pf = []
missing_stat_list_pts = []
missing_stat_list_min = []
missing_stat_list_fga = []
missing_stat_list_reb = []
missing_stat_list_team_reb = []
missing_stat_list_ast = []
missing_stat_list_oreb = []
missing_stat_list_blocks = []
missing_stat_list_turnovers = []
missing_stat_list_steals = []

# incomplete = stat is partially missing from the box score - could indicate a problem while entering data
incomplete_stat_list_fgm = []
incomplete_stat_list_ftm = []
incomplete_stat_list_fta = []
incomplete_stat_list_fgm3 = []
incomplete_stat_list_fga3 = []
incomplete_stat_list_pf = []
incomplete_stat_list_pts = []
incomplete_stat_list_min = []
incomplete_stat_list_fga = []
incomplete_stat_list_reb = []
incomplete_stat_list_team_reb = []
incomplete_stat_list_ast = []
incomplete_stat_list_oreb = []
incomplete_stat_list_blocks = []
incomplete_stat_list_turnovers = []
incomplete_stat_list_steals = []

def update_season_stat_counters(r,h,date):
    
    if r not in team_list and h not in team_list:
        return
        
    game_info_string = "%s %s at %s" % (date,r,h)

    if r in team_list:
        season_stat_counters_games_played[r] += 1
    if h in team_list:
        season_stat_counters_games_played[h] += 1
        
    # If the counters are all at zero, this game probably does not have any stats at all, so skip the analysis
    
    if ((current_game_counters["minutes"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_min[r] += 1
        if h in team_list:
            season_stat_counters_min[h] += 1
    elif current_game_counters["minutes"] > 0:
        incomplete_stat_list_min.append(game_info_string)
    else:
        missing_stat_list_min.append(game_info_string)

    if ((current_game_counters["fgm"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_fgm[r] += 1
        if h in team_list:
            season_stat_counters_fgm[h] += 1
    elif current_game_counters["fgm"] > 0:
        incomplete_stat_list_fgm.append(game_info_string)
        # This stat should always be complete, but not for freshman scores
        # print("%s FGM incomplete" % (game_info_string))
    else:
        missing_stat_list_fgm.append(game_info_string)
        # This stat should always be complete, but not for freshman scores
        # print("%s FGM missing" % (game_info_string))
    
    if ((current_game_counters["fga"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_fga[r] += 1
        if h in team_list:
            season_stat_counters_fga[h] += 1
    elif current_game_counters["fga"] > 0:
        incomplete_stat_list_fga.append(game_info_string)
    else:
        missing_stat_list_fga.append(game_info_string)
        
    if ((current_game_counters["ftm"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_ftm[r] += 1
        if h in team_list:
            season_stat_counters_ftm[h] += 1
    elif current_game_counters["ftm"] > 0:
        incomplete_stat_list_ftm.append(game_info_string)
        # This stat should always be complete, but not for freshman scores
        # print("%s FTM incomplete" % (game_info_string))        
    else:
        missing_stat_list_ftm.append(game_info_string)
        # This stat should always be complete, but not for freshman scores
        # print("%s FTM missing" % (game_info_string))
        
    if ((current_game_counters["fta"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_fta[r] += 1
        if h in team_list:
            season_stat_counters_fta[h] += 1
    elif current_game_counters["fta"] > 0:
        incomplete_stat_list_fta.append(game_info_string)
    else:
        missing_stat_list_fta.append(game_info_string)            

    if ((current_game_counters["fgm3"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_fgm3[r] += 1
        if h in team_list:
            season_stat_counters_fgm3[h] += 1
    elif current_game_counters["fgm3"] > 0:
        incomplete_stat_list_fgm3.append(game_info_string)
    else:
        missing_stat_list_fgm3.append(game_info_string)
        
    if ((current_game_counters["fga3"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_fga3[r] += 1
        if h in team_list:
            season_stat_counters_fga3[h] += 1
    elif current_game_counters["fga3"] > 0:
        incomplete_stat_list_fga3.append(game_info_string)
    else:
        missing_stat_list_fga3.append(game_info_string)
        
    if ((current_game_counters["pf"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_pf[r] += 1
        if h in team_list:
            season_stat_counters_pf[h] += 1
    elif current_game_counters["pf"] > 0:
        incomplete_stat_list_pf.append(game_info_string)
    else:
        missing_stat_list_pf.append(game_info_string)
        
    if ((current_game_counters["pts"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_pts[r] += 1
        if h in team_list:
            season_stat_counters_pts[h] += 1
    elif current_game_counters["pts"] > 0:
        incomplete_stat_list_pts.append(game_info_string)
        # This stat should always be complete
        print("%s PTS incomplete" % (game_info_string))
    else:
        missing_stat_list_pts.append(game_info_string)
        # This stat should always be complete
        print("%s PTS missing" % (game_info_string))
    
    if ((current_game_counters["oreb"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_oreb[r] += 1
        if h in team_list:
            season_stat_counters_oreb[h] += 1

    if ((current_game_counters["reb"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_reb[r] += 1
        if h in team_list:
            season_stat_counters_reb[h] += 1
    elif current_game_counters["reb"] > 0:
        incomplete_stat_list_reb.append(game_info_string)
    else:
        missing_stat_list_reb.append(game_info_string)

    # Special case - "team rebounds" only appear in the box score one time per TEAM
    if current_game_counters["team_reb"] == 2:
        if r in team_list:
            season_stat_counters_team_reb[r] += 1
        if h in team_list:
            season_stat_counters_team_reb[h] += 1
    elif current_game_counters["team_reb"] > 0:
        incomplete_stat_list_team_reb.append(game_info_string)
    else:
        missing_stat_list_team_reb.append(game_info_string)
        
    if ((current_game_counters["ast"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_ast[r] += 1
        if h in team_list:
            season_stat_counters_ast[h] += 1
    elif current_game_counters["ast"] > 0:
        incomplete_stat_list_ast.append(game_info_string)
    else:
        missing_stat_list_ast.append(game_info_string)
        
    if ((current_game_counters["blocks"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_blocks[r] += 1
        if h in team_list:
            season_stat_counters_blocks[h] += 1
    elif current_game_counters["blocks"] > 0:
        incomplete_stat_list_blocks.append(game_info_string)
    else:
        missing_stat_list_blocks.append(game_info_string)
        
    if ((current_game_counters["steals"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_steals[r] += 1
        if h in team_list:
            season_stat_counters_steals[h] += 1
    elif current_game_counters["steals"] > 0:
        incomplete_stat_list_steals.append(game_info_string)
    else:
        missing_stat_list_steals.append(game_info_string)
        
    if ((current_game_counters["turnovers"] == current_game_counters["games"]) and (current_game_counters["games"] > 0)):
        if r in team_list:
            season_stat_counters_turnovers[r] += 1
        if h in team_list:
            season_stat_counters_turnovers[h] += 1
    elif current_game_counters["turnovers"] > 0:
        incomplete_stat_list_turnovers.append(game_info_string)
    else:
        missing_stat_list_turnovers.append(game_info_string)
    
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
parser = argparse.ArgumentParser(description='Check a BOXTOP file for problems and compile composite stats for players with valid player ids.')
parser.add_argument('boxtop_filename', help="Boxtop file") 
parser.add_argument('output_filename', help="Output file to store issues and stats")
args = parser.parse_args()

team_list = ["UCLA Bruins"]
for tm in team_list:
    season_team_games_played[tm] = 0
    season_team_fgm[tm] = 0
    season_team_ftm[tm] = 0
    season_team_fta[tm] = 0
    season_team_fgm3[tm] = 0
    season_team_fga3[tm] = 0
    season_team_pf[tm] = 0
    season_team_pts[tm] = 0

    season_team_min[tm] = 0
    season_team_fga[tm] = 0
    season_team_reb[tm] = 0
    season_team_team_reb[tm] = 0
    season_team_ast[tm] = 0
    season_team_oreb[tm] = 0
    season_team_blocks[tm] = 0
    season_team_turnovers[tm] = 0
    season_team_steals[tm] = 0    
    
    season_stat_counters_games_played[tm] = 0
    season_stat_counters_fgm[tm] = 0
    season_stat_counters_ftm[tm] = 0
    season_stat_counters_ftm[tm] = 0
    season_stat_counters_fta[tm] = 0
    season_stat_counters_fgm3[tm] = 0
    season_stat_counters_fga3[tm] = 0
    season_stat_counters_pf[tm] = 0
    season_stat_counters_pts[tm] = 0
    season_stat_counters_min[tm] = 0
    season_stat_counters_fga[tm] = 0
    season_stat_counters_reb[tm] = 0
    season_stat_counters_team_reb[tm] = 0
    season_stat_counters_ast[tm] = 0
    season_stat_counters_oreb[tm] = 0
    season_stat_counters_blocks[tm] = 0
    season_stat_counters_turnovers[tm] = 0
    season_stat_counters_steals[tm] = 0
    
    
output_file = open(args.output_filename,'w')

start_of_boxscore = "gamebxt"
inventory_logging_on = False

game_count = 0
game_ref_count = 0
first_gamebxt_read = False

with open(args.boxtop_filename,'r') as csvfile:
    items = csv.reader(csvfile)
    for row in items:    
        if len(row) > 0:
            # read until we read a "gamebxt" which tells us to loop back around to the next boxscore
            # but skip everything until after we read the first one
            if not first_gamebxt_read:
                if row[0] == start_of_boxscore:
                    # flip the flag, but ignore this line
                    first_gamebxt_read = True
                    game_count += 1
                # else just skip the line

            elif row[0] == start_of_boxscore:

                # We're finished with the previous box score, so determine if we need to increment our team stat counters
                # Note that the "games" field is set equal to the number of players in this game; the other values
                # will be <= that number.
                        
                # The current game counters are no longer needed, so clear them to get ready for the next game
                for key, value in current_game_counters.items():
                    current_game_counters[key] = 0            
              
                game_count += 1
                game_ref_count = 0
                
                # Clear all dictionaries that track a single game
                player_first_names.clear()
                player_last_names.clear()
            
                player_games_played.clear()
                player_fgm.clear()
                player_ftm.clear()
                player_fta.clear()
                player_fgm3.clear()
                player_fga3.clear()
                player_pts.clear()
                player_pf.clear()
                player_min.clear()
                player_fga.clear()
                player_oreb.clear()
                player_reb.clear()
                player_ast.clear()
                player_blocks.clear()
                player_turnovers.clear()
                player_steals.clear()
                
                team_fgm.clear()
                team_ftm.clear()
                team_fta.clear()
                team_fgm3.clear()
                team_fga3.clear()
                team_pf.clear()
                team_pts.clear()
                team_first_names.clear()
                team_last_names.clear()
                team_min.clear()
                team_fga.clear()
                team_reb.clear()
                team_team_reb.clear()
                team_ast.clear()
                team_oreb.clear()
                team_blocks.clear()
                team_turnovers.clear()
                team_steals.clear()
                
                player_totals_for_current_game_fgm.clear()
                player_totals_for_current_game_ftm.clear()
                player_totals_for_current_game_fta.clear()
                player_totals_for_current_game_fgm3.clear()
                player_totals_for_current_game_fga3.clear()
                player_totals_for_current_game_pf.clear()
                player_totals_for_current_game_pts.clear()
                player_totals_for_current_game_min.clear()
                player_totals_for_current_game_fga.clear()
                player_totals_for_current_game_reb.clear()
                player_totals_for_current_game_ast.clear()
                player_totals_for_current_game_oreb.clear()
                player_totals_for_current_game_blocks.clear()
                player_totals_for_current_game_turnovers.clear()
                player_totals_for_current_game_steals.clear()                
                
            elif row[0] == "version":
                # ignore
                pass

            elif row[0] == "sources":
                game_sources = row[1]
                
                # Because this is always the last row in a box score, this is a good place to 
                # cross-check player totals (for this game) vs. team totals
                #
                # TBD - could also check the two linescores for the same number of periods... but this would require adding them to the dictionaries.

                update_season_stat_counters(road_team_name,home_team_name,game_date)
                
            elif row[0] == "info":
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

                elif row[1] == "arena":
                    game_arena = row[2]

                elif row[1] == "attendance":
                    game_attendance = row[2]

                elif row[1] == "starttime":
                    game_starttime = row[2]

                elif row[1] == "ref":
                    if len(row[2]) > 0:
                       game_ref_count += 1

            elif row[0] == "coach":
                # ignore
                pass

            elif row[0] == "stat":
                if row[1] == "rteam":
                    tm_str = road_team_name
                else:
                    tm_str = home_team_name
                    
                # Append the team name at the end of the player id to reduce the chances of
                # being confused by a duplicate name, and to allow us to select only the 
                # players from the "team_list" when we are printing the team table(s) later.
                player_id = row[3] + "-" + tm_str    
                    
                # current game
                player_first_names[player_id] = row[4]
                player_last_names[player_id] = row[5]
            
                player_games_played[player_id] = 1
                player_fgm[player_id] = safeint(row[7])
                player_ftm[player_id] = safeint(row[9])
                player_fta[player_id] = safeint(row[10])
                player_fgm3[player_id] = safeint(row[11])
                player_fga3[player_id] = safeint(row[12])
                player_pts[player_id] = safeint(row[13])
                player_pf[player_id] = safeint(row[17])
                if player_pf[player_id] > 5:
                    log_it("ERROR: (%s at %s %s) %s More than 5 fouls is likely wrong (%s)" % (road_team_name,home_team_name,game_date,player_id,player_pf[player_id]))

                
                player_min[player_id] = safeint(row[6])
                player_fga[player_id] = safeint(row[8])
                player_oreb[player_id] = safeint(row[14])
                player_reb[player_id] = safeint(row[15])
                player_ast[player_id] = safeint(row[16])
                player_blocks[player_id] = safeint(row[18])
                player_turnovers[player_id] = safeint(row[19])
                player_steals[player_id] = safeint(row[20])   
                
                if tm_str not in player_totals_for_current_game_pts: # was fgm but freshman file will not contain FGM
                    # initialize all of these dictionaries
                    player_totals_for_current_game_fgm[tm_str] = 0
                    player_totals_for_current_game_ftm[tm_str] = 0
                    player_totals_for_current_game_fta[tm_str] = 0
                    player_totals_for_current_game_fgm3[tm_str] = 0
                    player_totals_for_current_game_fga3[tm_str] = 0
                    player_totals_for_current_game_pf[tm_str] = 0
                    player_totals_for_current_game_pts[tm_str] = 0
                    player_totals_for_current_game_min[tm_str] = 0
                    player_totals_for_current_game_fga[tm_str] = 0
                    player_totals_for_current_game_reb[tm_str] = 0
                    player_totals_for_current_game_ast[tm_str] = 0
                    player_totals_for_current_game_oreb[tm_str] = 0
                    player_totals_for_current_game_blocks[tm_str] = 0
                    player_totals_for_current_game_turnovers[tm_str] = 0
                    player_totals_for_current_game_steals[tm_str] = 0                    
                    
                player_totals_for_current_game_fgm[tm_str] += safeint(row[7])
                player_totals_for_current_game_ftm[tm_str] += safeint(row[9])
                player_totals_for_current_game_fta[tm_str] += safeint(row[10])
                player_totals_for_current_game_fgm3[tm_str] += safeint(row[11])
                player_totals_for_current_game_fga3[tm_str] += safeint(row[12])
                player_totals_for_current_game_pf[tm_str] += safeint(row[17])
                player_totals_for_current_game_pts[tm_str] += safeint(row[13])
                player_totals_for_current_game_min[tm_str] += safeint(row[6])
                player_totals_for_current_game_fga[tm_str] += safeint(row[8])
                player_totals_for_current_game_reb[tm_str] += safeint(row[15])
                player_totals_for_current_game_ast[tm_str] += safeint(row[16])
                player_totals_for_current_game_oreb[tm_str] += safeint(row[14])
                player_totals_for_current_game_blocks[tm_str] += safeint(row[18])
                player_totals_for_current_game_turnovers[tm_str] += safeint(row[19])
                player_totals_for_current_game_steals[tm_str] += safeint(row[20])
                

                # TBD - this could be separate road and home dictionaries in order to accurately reflect each team, 
                # but for now let's keep it this way and treat a stat as complete for both or neither
                
                current_game_counters["games"] +=1
                if len(row[6]) > 0:
                    current_game_counters["minutes"] +=1

                if len(row[7]) > 0:
                    current_game_counters["fgm"] +=1
                    points_from_shots = (2 * player_fgm[player_id]) + player_ftm[player_id] + player_fgm3[player_id]
                    if points_from_shots != player_pts[player_id]:
                        log_it("ERROR: (%s at %s %s) %s Points do not match FG + FT math %s != %s" % (road_team_name,home_team_name,game_date,player_id,player_pts[player_id],points_from_shots))
                        
                if len(row[8]) > 0:
                    current_game_counters["fga"] +=1
                    if (player_fgm[player_id] > player_fga[player_id]):
                        log_it("ERROR: (%s at %s %s) %s More FGM than FGA %s > %s" % (road_team_name,home_team_name,game_date,player_id,player_fgm[player_id],player_fga[player_id]))
                        
                if len(row[9]) > 0:
                    current_game_counters["ftm"] +=1

                if len(row[10]) > 0:
                    current_game_counters["fta"] +=1
                    if (player_ftm[player_id] > player_fta[player_id]):
                        log_it("ERROR: (%s at %s %s) %s More FTM than FTA %s > %s" % (road_team_name,home_team_name,game_date,player_id,player_ftm[player_id],player_fta[player_id]))

                if len(row[11]) > 0:
                    current_game_counters["fgm3"] +=1

                if len(row[12]) > 0:
                    current_game_counters["fga3"] +=1
                    if (player_fgm3[player_id] > player_fga3[player_id]):
                        log_it("ERROR: (%s at %s %s) %s More FGM3 than FGA3 %s > %s" % (road_team_name,home_team_name,game_date,player_id,player_fgm3[player_id],player_fga3[player_id]))

                if len(row[13]) > 0:
                    current_game_counters["pts"] +=1

                if len(row[17]) > 0:
                    current_game_counters["pf"] +=1

                if len(row[14]) > 0:
                    current_game_counters["oreb"] +=1

                if len(row[15]) > 0:
                    current_game_counters["reb"] +=1

                if len(row[16]) > 0:
                    current_game_counters["ast"] +=1

                if len(row[18]) > 0:
                    current_game_counters["blocks"] +=1

                if len(row[19]) > 0:
                    current_game_counters["turnovers"] +=1

                if len(row[20]) > 0:
                    current_game_counters["steals"] +=1                           
                
                # Checks for individual player stats within the current game

                # Check if this team is included in the list of teams we want to collect SEASON stats for
                if tm_str in team_list:
                    # This player plays for the team we care about. Grab the stats.
                    # stat,rteam,player,ramsefr01,Frank,Ramsey,,3,,5,6,,,11,,,,5,,,,
        # stat,rteam|hteam,player,ID,FIRSTNAME,LASTNAME,MIN,FGM,FGA,FTM,FTA,3FGM,3FGA,PTS,OREB,REB,AST,PF,BLOCKS,TURNOVERS,STEALS,TECHNICALFOUL
        # 0    1           2      3  4         5        6   7   8   9   10  11   12   13  14   15  16  17 18     19        20     21        
        
                    if player_id in season_player_games_played:
                       
                        season_player_games_played[player_id] += 1
                        season_player_fgm[player_id] += safeint(row[7])
                        season_player_ftm[player_id] += safeint(row[9])
                        season_player_fta[player_id] += safeint(row[10])
                        season_player_fgm3[player_id] += safeint(row[11])
                        season_player_fga3[player_id] += safeint(row[12])
                        season_player_pts[player_id] += safeint(row[13])
                        season_player_pf[player_id] += safeint(row[17])
                        
                        season_player_min[player_id] += safeint(row[6])
                        season_player_fga[player_id] += safeint(row[8])
                        season_player_oreb[player_id] += safeint(row[14])
                        season_player_reb[player_id] += safeint(row[15])
                        season_player_ast[player_id] += safeint(row[16])
                        season_player_blocks[player_id] += safeint(row[18])
                        season_player_turnovers[player_id] += safeint(row[19])
                        season_player_steals[player_id] += safeint(row[20])

                    else: # create new entries for this player
                        # Only grab name one time
                        season_player_first_names[player_id] = row[4]
                        season_player_last_names[player_id] = row[5]
                    
                        season_player_games_played[player_id] = 1
                        season_player_fgm[player_id] = safeint(row[7])
                        season_player_ftm[player_id] = safeint(row[9])
                        season_player_fta[player_id] = safeint(row[10])
                        season_player_fgm3[player_id] = safeint(row[11])
                        season_player_fga3[player_id] = safeint(row[12])
                        season_player_pts[player_id] = safeint(row[13])
                        season_player_pf[player_id] = safeint(row[17])
                        
                        season_player_min[player_id] = safeint(row[6])
                        season_player_fga[player_id] = safeint(row[8])
                        season_player_oreb[player_id] = safeint(row[14])
                        season_player_reb[player_id] = safeint(row[15])
                        season_player_ast[player_id] = safeint(row[16])
                        season_player_blocks[player_id] = safeint(row[18])
                        season_player_turnovers[player_id] = safeint(row[19])
                        season_player_steals[player_id] = safeint(row[20])                    
                        

            elif row[0] == "tstat":

                if row[1] == "rteam":
                    tm_str = road_team_name
                else:
                    tm_str = home_team_name
                
                team_fgm[tm_str] = safeint(row[3])
                team_ftm[tm_str] = safeint(row[5])
                team_fta[tm_str] = safeint(row[6])
                team_fgm3[tm_str] = safeint(row[7])
                team_fga3[tm_str] = safeint(row[8])
                team_pf[tm_str] = safeint(row[13])
                team_pts[tm_str] = safeint(row[9])
                team_min[tm_str] = safeint(row[2])
                team_fga[tm_str] = safeint(row[4])
                team_oreb[tm_str] = safeint(row[10])
                team_reb[tm_str] = safeint(row[11])
                team_ast[tm_str] = safeint(row[12])
                team_blocks[tm_str] = safeint(row[14])
                team_turnovers[tm_str] = safeint(row[15])
                team_steals[tm_str] = safeint(row[16])
                team_team_reb[tm_str] = safeint(row[17])    

                if len(row[17]) > 0:
                    current_game_counters["team_reb"] += 1                
                
                # Checks for team stats
                if current_game_counters["fga"] > 0 and (team_fgm[tm_str] > team_fga[tm_str]):
                    log_it("ERROR: (%s at %s %s) %s More FGM than FGA %s > %s" % (road_team_name,home_team_name,game_date,tm_str,team_fgm[tm_str],team_fga[tm_str]))
                if current_game_counters["fta"] > 0 and (team_ftm[tm_str] > team_fta[tm_str]):
                    log_it("ERROR: (%s at %s %s) %s More FTM than FTA %s > %s" % (road_team_name,home_team_name,game_date,tm_str,team_ftm[tm_str],team_fta[tm_str]))
                if current_game_counters["fga3"] > 0 and (team_fgm3[tm_str] > team_fga3[tm_str]):
                    log_it("ERROR: (%s at %s %s) %s More FGM3 than FGA3 %s > %s" % (road_team_name,home_team_name,game_date,tm_str,team_fgm3[tm_str],team_fga3[tm_str]))
                
                if len(row[3]) > 0:
                    points_from_shots = (2 * team_fgm[tm_str]) + team_ftm[tm_str] + team_fgm3[tm_str]
                    if points_from_shots != team_pts[tm_str]:
                        log_it("ERROR: (%s at %s %s) %s Points do not match FG + FT math %s != %s" % (road_team_name,home_team_name,game_date,tm_str,team_pts[tm_str],points_from_shots))           
                # Cross-check team stats versus the total stats of all of the players in this game.
                if team_fgm[tm_str] != player_totals_for_current_game_fgm[tm_str] and (current_game_counters["fgm"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s FGM Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_fgm[tm_str],player_totals_for_current_game_fgm[tm_str]))
                if team_fga[tm_str] != player_totals_for_current_game_fga[tm_str] and (current_game_counters["fga"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s FGA Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_fga[tm_str],player_totals_for_current_game_fga[tm_str]))
                if team_ftm[tm_str] != player_totals_for_current_game_ftm[tm_str] and (current_game_counters["ftm"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s FTM Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_ftm[tm_str],player_totals_for_current_game_ftm[tm_str]))
                if team_fta[tm_str] != player_totals_for_current_game_fta[tm_str] and (current_game_counters["fta"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s FTA Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_fta[tm_str],player_totals_for_current_game_fta[tm_str]))
                    
                if team_fgm3[tm_str] != player_totals_for_current_game_fgm3[tm_str] and (current_game_counters["fgm3"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s 3FGM Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_fgm3[tm_str],player_totals_for_current_game_fgm3[tm_str]))
                if team_fga3[tm_str] != player_totals_for_current_game_fga3[tm_str] and (current_game_counters["fga3"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s 3FGA Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_fga3[tm_str],player_totals_for_current_game_fga3[tm_str]))

                if team_pf[tm_str] != player_totals_for_current_game_pf[tm_str] and (current_game_counters["pf"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s PF Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_pf[tm_str],player_totals_for_current_game_pf[tm_str]))

                if team_pts[tm_str] != player_totals_for_current_game_pts[tm_str] and (current_game_counters["pts"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s PTS Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_pts[tm_str],player_totals_for_current_game_pts[tm_str]))

                if team_min[tm_str] != player_totals_for_current_game_min[tm_str] and (current_game_counters["min"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s MIN Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_min[tm_str],player_totals_for_current_game_min[tm_str]))

                # Special case - could have "team rebounds" - 7/21/2024 I added team_team_reb[] to this block because LAT includes "team rebounds" in the team totals.
                if team_reb[tm_str] != (player_totals_for_current_game_reb[tm_str] + team_team_reb[tm_str]) and (current_game_counters["reb"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s POSSIBLE REB Mismatch (Team=%s PlayerTotals=%s TeamRebounds=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_reb[tm_str],player_totals_for_current_game_reb[tm_str],team_team_reb[tm_str]))

                if team_oreb[tm_str] != player_totals_for_current_game_oreb[tm_str] and (current_game_counters["oreb"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s OREB Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_oreb[tm_str],player_totals_for_current_game_oreb[tm_str]))
                    
                if team_ast[tm_str] != player_totals_for_current_game_ast[tm_str] and (current_game_counters["ast"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s AST Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_ast[tm_str],player_totals_for_current_game_ast[tm_str]))

                if team_blocks[tm_str] != player_totals_for_current_game_blocks[tm_str] and (current_game_counters["blocks"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s BLOCKS Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_blocks[tm_str],player_totals_for_current_game_blocks[tm_str]))

                if team_turnovers[tm_str] != player_totals_for_current_game_turnovers[tm_str] and (current_game_counters["turnovers"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s TURNOVERS Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_turnovers[tm_str],player_totals_for_current_game_turnovers[tm_str]))
                    
                if team_steals[tm_str] != player_totals_for_current_game_steals[tm_str] and (current_game_counters["steals"] == current_game_counters["games"]):
                    log_it("ERROR: (%s at %s %s) %s STEALS Mismatch (Team=%s PlayerTotals=%s)" % (road_team_name,home_team_name,game_date,tm_str,team_steals[tm_str],player_totals_for_current_game_steals[tm_str]))

                if tm_str in team_list:
                    # This is a team we care about. Grab the stats for the season-long stats checking
                    # tstat,rteam,,44,,27,38,,,115,,,,34,,,,,
        # tstat,rteam|hteam,MIN,FGM,FGA,FTM,FTA,FG3M,FG3A,PTS,OREB,REB,AST,PF,BLOCKS,TURNOVERS,STEALS,TEAMREBOUNDS,TECHNICALFOUL
        # 0     1           2   3   4   5   6   7    8    9   10   11  12  13 14     15        16     17           18
                    season_team_games_played[tm_str] += 1
                    
                    season_team_fgm[tm_str] += safeint(row[3])
                    season_team_ftm[tm_str] += safeint(row[5])
                    season_team_fta[tm_str] += safeint(row[6])
                    season_team_fgm3[tm_str] += safeint(row[7])
                    season_team_fga3[tm_str] += safeint(row[8])
                    season_team_pf[tm_str] += safeint(row[13])
                    season_team_pts[tm_str] += safeint(row[9])
                    season_team_min[tm_str] += safeint(row[2])
                    season_team_fga[tm_str] += safeint(row[4])
                    season_team_oreb[tm_str] += safeint(row[10])
                    season_team_reb[tm_str] += safeint(row[11])
                    season_team_ast[tm_str] += safeint(row[12])
                    season_team_blocks[tm_str] += safeint(row[14])
                    season_team_turnovers[tm_str] += safeint(row[15])
                    season_team_steals[tm_str] += safeint(row[16])
                    season_team_team_reb[tm_str] += safeint(row[17])
#                    if len(row[17]) > 0:
                        # Special case where we can increment a season stat counter right here
#                        season_stat_counters_team_reb[tm_str] += 1


            elif row[0] == "linescore":
                # This appears after the team stats, which means that we can
                # check it for consistency with itself and with the team's total
                # points.
                if row[1] == "rteam":
                    tm_str = road_team_name
                else:
                    tm_str = home_team_name
                    
                colon_found = False
                period_column = int(2)
                linescore_sum_by_periods = int(0)
                linescore_total = int(0)
                while not colon_found and (period_column < len(row)):
                    if row[period_column] == ":":
                        colon_found = True
                        linescore_total = int(row[period_column+1]) # TBD this will fail if there is not an int in the next column - needs error checking
                        if linescore_total != linescore_sum_by_periods:
                            log_it("ERROR: (%s at %s %s) %s Linescore inconsistent %s" % (road_team_name,home_team_name,game_date,tm_str,row))

                    elif len(row[period_column]) > 0:
                        linescore_sum_by_periods += int(row[period_column])
                        
                    period_column +=1
                
                if colon_found:
                    if linescore_total != team_pts[tm_str]:
                        log_it("ERROR: (%s at %s %s) %s Linescore points (%s) do not match team total points (%s)" % (road_team_name,home_team_name,game_date,tm_str,linescore_total,team_pts[tm_str]))
                else: # might have only the final score
                    if linescore_sum_by_periods != team_pts[tm_str]:
                        log_it("ERROR: (%s at %s %s) %s Linescore points (%s) do not match team total points (%s)" % (road_team_name,home_team_name,game_date,tm_str,linescore_sum_by_periods,team_pts[tm_str]))
                    

# Dump the player and team stats for the SEASON into the output_file.
#print(season_player_games_played)
for t in team_list:
    output_file.write("%s\n" % t)
    output_file.write("       First         Last  GP  MIN  FGM  FGA  FTM  FTA 3FGM 3FGA  PTS  REB  AST OREB  BLK   PF   TO   ST\n")
    for player in sorted(season_player_games_played):
        # We appended the team name at the end of the CBB player id, so check it here.
        if player.split("-")[3] == t:
            output_file.write("%12s %12s %3s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s %4s\n" % (season_player_first_names[player], season_player_last_names[player], season_player_games_played[player], season_player_min[player], season_player_fgm[player], season_player_fga[player], season_player_ftm[player], season_player_fta[player],season_player_fgm3[player], season_player_fga3[player], season_player_pts[player], season_player_reb[player], season_player_ast[player], season_player_oreb[player], season_player_blocks[player], season_player_pf[player], season_player_turnovers[player],season_player_steals[player]))

    output_file.write("                     TEAM %3d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d\n" % (season_team_games_played[t], season_team_min[t], season_team_fgm[t], season_team_fga[t], season_team_ftm[t], season_team_fta[t], season_team_fgm3[t], season_team_fga3[t], season_team_pts[t], season_team_reb[t], season_team_ast[t], season_team_oreb[t],season_team_blocks[t], season_team_pf[t], season_team_turnovers[t], season_team_steals[t]))
            
    output_file.write("            GAME COUNTERS %3d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d %4d\n" % (season_stat_counters_games_played[t], season_stat_counters_min[t], season_stat_counters_fgm[t], season_stat_counters_fga[t], season_stat_counters_ftm[t], season_stat_counters_fta[t], season_stat_counters_fgm3[t], season_stat_counters_fga3[t], season_stat_counters_pts[t], season_stat_counters_reb[t], season_stat_counters_ast[t], season_stat_counters_oreb[t],season_stat_counters_blocks[t], season_stat_counters_pf[t], season_stat_counters_turnovers[t], season_stat_counters_steals[t]))

    output_file.write("Team Rebounds = %d (game counter = %d)\n" % (season_team_team_reb[t],season_stat_counters_team_reb[t]))

    output_file.write("NOTE: Game counters reflect the number of box scores that include a statistic for all players for both teams.\n")
    

    output_file.write("\n\n")
    
    output_file.write(log_dump)
    
    output_file.write("\n\n")

    output_file.write("\nGames with incomplete FGM\n")
    for gm in incomplete_stat_list_fgm:
        output_file.write(" %s\n" % (gm))
        
    output_file.write("\nGames with incomplete FTM\n")
    for gm in incomplete_stat_list_ftm:
        output_file.write(" %s\n" % (gm))        
        
    output_file.write("\nGames with incomplete PTS\n")
    for gm in incomplete_stat_list_pts:
        output_file.write(" %s\n" % (gm))        
        
    output_file.write("\nGames with incomplete FGA\n")
    for gm in incomplete_stat_list_fga:
        output_file.write(" %s\n" % (gm))
        
    output_file.write("\nGames with incomplete FTA\n")
    for gm in incomplete_stat_list_fta:
        output_file.write(" %s\n" % (gm))

    # skipping 3-pt FG for now
    # incomplete_stat_list_fgm3 = []
    # incomplete_stat_list_fga3 = []

    output_file.write("\nGames with incomplete PF\n")
    for gm in incomplete_stat_list_pf:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete MIN\n")
    for gm in incomplete_stat_list_min:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete REB\n")
    for gm in incomplete_stat_list_reb:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete TEAM REB\n")
    for gm in incomplete_stat_list_team_reb:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete AST\n")
    for gm in incomplete_stat_list_ast:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete BLOCKS\n")
    for gm in incomplete_stat_list_blocks:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete TURNOVERS\n")
    for gm in incomplete_stat_list_turnovers:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with incomplete STEALS\n")
    for gm in incomplete_stat_list_steals:
        output_file.write(" %s\n" % (gm))
    
    
    output_file.write("\n\n")

    output_file.write("\nGames with missing FGM\n")
    for gm in missing_stat_list_fgm:
        output_file.write(" %s\n" % (gm))
        
    output_file.write("\nGames with missing FTM\n")
    for gm in missing_stat_list_ftm:
        output_file.write(" %s\n" % (gm))        
        
    output_file.write("\nGames with missing PTS\n")
    for gm in missing_stat_list_pts:
        output_file.write(" %s\n" % (gm))        
        
    output_file.write("\nGames with missing FGA\n")
    for gm in missing_stat_list_fga:
        output_file.write(" %s\n" % (gm))
        
    output_file.write("\nGames with missing FTA\n")
    for gm in missing_stat_list_fta:
        output_file.write(" %s\n" % (gm))

    # skipping 3-pt FG for now
    # missing_stat_list_fgm3 = []
    # missing_stat_list_fga3 = []

    output_file.write("\nGames with missing PF\n")
    for gm in missing_stat_list_pf:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing MIN\n")
    for gm in missing_stat_list_min:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing REB\n")
    for gm in missing_stat_list_reb:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing TEAM REB\n")
    for gm in missing_stat_list_team_reb:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing AST\n")
    for gm in missing_stat_list_ast:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing BLOCKS\n")
    for gm in missing_stat_list_blocks:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing TURNOVERS\n")
    for gm in missing_stat_list_turnovers:
        output_file.write(" %s\n" % (gm))

    output_file.write("\nGames with missing STEALS\n")
    for gm in missing_stat_list_steals:
        output_file.write(" %s\n" % (gm))

output_file.close()

print("File %s created." % (args.output_filename))
