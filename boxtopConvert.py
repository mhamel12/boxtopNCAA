# ===============================================================
# 
# boxtopConvert.py
#
# Convert .csv box score data obtained from Sports Reference's websites
# to BOXTOP format.
#
# CC License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
# https://creativecommons.org/licenses/by-nc/4.0/
#
# Version history
# 12/15/2024  1.0  MH  Initial version
#
# ===============================================================
import argparse, csv, re
from collections import defaultdict

boxtop_header = """
gamebxt
version,1
info,date,
info,dayofweek,
info,rteam,
info,hteam,
info,neutralsite,
info,title,
info,arena,
info,city,
info,state,
info,country,United States
info,attendance,
info,ref,
info,ref,
info,starttime,00:00PM
info,timezone,
info,radio,
info,tv,
info,note,
info,prelim,
info,event,
"""

def clean_name_for_id(raw_name):
    n = re.sub("\.","",raw_name) # remove "." to handle K.C. Jones but escape it or else the entire string will get removed
    n = re.sub(" ","",n) # remove spaces to handle cases like 'Van Arsdale'
    n = re.sub("'","",n) # remove "'" and "`" to handle O'Brien and O`Brien
    n = re.sub("`","",n)
   
    return n.lower() # change name to all lower-case to match how CBB Reference does it.

#########################################################################
#
# Main program starts here
#    

# No command-line arguments are needed, but argparse will automatically print this
# help message and then exit.
parser = argparse.ArgumentParser(description='Convert .csv box score data from Sports Reference into BOXTOP format')
parser.add_argument('roadteam_file', help="Data file for road team, must include a header row that identifies each column. Assumes that 'Team Totals' is used to denote the team totals.") 
parser.add_argument('hometeam_file', help="Data file for home team, must include a header row that identifies each column. Assumes that 'Team Totals' is used to denote the team totals.")
args = parser.parse_args()

team_id = "rteam"

print(boxtop_header)

input_filenames = [args.roadteam_file,args.hometeam_file]

for input_file in input_filenames:
    with open(input_file, newline='') as csvfile:
        print("coach,%s,,,," % (team_id))
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Player'] == "Team Totals":
                #
                # Print team totals
                #
                stats_line = "tstat,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,," % (team_id,row['MP'],row['FG'],row['FGA'],row['FT'],row['FTA'],row['3P'],row['3PA'],row['PTS'],row['ORB'],row['DRB'],row['AST'],row['PF'],row['BLK'],row['TOV'],row['STL'])
                
                print(stats_line)
            else:
                #
                # Print player stats
                #

                # Player,MP,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS

                if row['Player'].count(" ") > 0:
                    (first_name,last_name) = row['Player'].rsplit(" ",1)
                else: # no first name?
                    first_name = ""
                    last_name = row['Player']
                
                player_id = "%s-%s-1" % (clean_name_for_id(first_name), clean_name_for_id(last_name))
                
                stats_line = "stat,%s,player,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," % (team_id,player_id,first_name,last_name,row['MP'],row['FG'],row['FGA'],row['FT'],row['FTA'],row['3P'],row['3PA'],row['PTS'],row['ORB'],row['DRB'],row['AST'],row['PF'],row['BLK'],row['TOV'],row['STL'])
                
                print(stats_line)
        print("linescore,%s," % (team_id))
        
        team_id = "hteam"
        
print("sources,")