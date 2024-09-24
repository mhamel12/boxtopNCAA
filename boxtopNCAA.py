#########################################################################
#
# Creates/updates a BOXTOP file for NCAA basketball box scores.
#
# CC License: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
# https://creativecommons.org/licenses/by-nc/4.0/
#
#
# If specified, the roster files must be named <school>_<anything>.<anything> and 
# follow the format of those used by https://www.sports-reference.com/cbb :
#
# Rk,Player,G,GS,MP,FG,FGA,FG%,FT,FTA,FT%,TRB,AST,STL,BLK,TOV,PF,PTS,Player-additional
# 1,Bill Walton,30,,,277,426,.650,58,102,.569,506,,,,,70,612,bill-walton-1
# 
#  1.0  MH  06/17/2024  Initial version
#
import argparse, csv, datetime, glob, os, re, sys
from collections import defaultdict
from shutil import copyfile


def boxtop_load_roster_files(the_files):
    player_dict = defaultdict(dict)
    list_of_teams = []
        
    for filename in the_files:
        the_path, just_the_filename = os.path.split(filename)
        team_abbrev = just_the_filename.split("_")[0].lower()
        with open(filename,'r') as csvfile: # file is automatically closed when this block completes
            items = csv.reader(csvfile)
            for row in items:    
                if len(row) > 0 and row[0] != "Rk" and len(row[0]) > 0:        
                    player_name = row[1]
                    
                    # games = row[2]
                    # rebounds = row[11]
                    # assists = row[12]
                    additional_player_info = row[18] # first-last-<number>
                    
                    # To faciliate searching by last name, create a player id that starts with
                    # last name. I believe the "additional_player_info" values will be unique.
                    # However, we will want to write the ORIGINAL version of this into the BOXTOP
                    # output as the player id, since the CBB pages are created like this:
                    # https://www.sports-reference.com/cbb/players/bill-walton-1.html
                    player_id = additional_player_info.split("-")[1] + "-" + additional_player_info.split("-")[0] + "-" + additional_player_info.split("-")[2]
                    
                    player_dict[team_abbrev][player_id] = player_name
                        
                    if team_abbrev not in list_of_teams:
                        list_of_teams.append(team_abbrev)

    return(player_dict,list_of_teams)
    
def clean_name_for_id(raw_name):
    n = re.sub("\.","",raw_name) # remove "." to handle K.C. Jones but escape it or else the entire string will get removed
    n = re.sub(" ","",n) # remove spaces to handle cases like 'Van Arsdale'
    n = re.sub("'","",n) # remove "'" and "`" to handle O'Brien and O`Brien
    n = re.sub("`","",n)
   
    return n.lower() # change name to all lower-case to match how CBB Reference does it.

def translate_dictionary_id(id):
    # The id came from boxtop_load_roster_files() so they should be sane. 
    # We use last-first-# in our dictionary for easier sorting.
    # But the id that we write to the BOXTOP file needs to match the original roster file: first-last-#
    p = id.split("-")[1] + "-" + id.split("-")[0] + "-" + id.split("-")[2]
    
    # return id, first, last but capitalize start of first and lastnames
    
    first_name = id.split("-")[1].title()
    last_name = id.split("-")[0].title()
    if last_name == "Mccarter": # This is the only UCLA player whose last name has more than one capital
       last_name = "McCarter"
    
    return p,first_name,last_name

#########################################################################
#
# Misc. input functions
#
#
def get_string():
    s = sys.stdin.readline() # read in one line through the \n
    s = s.rstrip() # remove line endings
    return s  
    
def get_name_string():
    # This works for making sure the first letter is a capital, but it changes
    # McGarry into Mcgarry, so it is not ideal.
    # s = get_string().capitalize()
    s = get_string()
    if len(s) >= 2:
        return s[0].capitalize() + s[1:]
    return s    
    

def get_string_require_nonzero_length():
    spin_until_ok = True
    while spin_until_ok:
        s = sys.stdin.readline() # read in one line through the \n
        s = s.rstrip() # remove line endings
        if len(s) > 0:
            return s
            
    return ""
    
def get_number():
    valid_number = False
    while not valid_number:
        s = sys.stdin.readline() # read in one line through the \n
        s = s.rstrip() # remove line endings
        s = re.sub('[^0-9]','', s)
        if len(s) > 0: # make sure they typed at least ONE numeric character, or python will exit with an error
            number = int(s)
            valid_number = "yes"    
    return number

def get_number_max_allowed(max_allowed):
    valid_number = False
    while not valid_number:
        s = sys.stdin.readline() # read in one line through the \n
        s = s.rstrip() # remove line endings
        s = re.sub('[^0-9]','', s)
        if len(s) > 0: # make sure they typed at least ONE numeric character, or python will exit with an error
            number = int(s)
            if number <= max_allowed:
                valid_number = "yes"    
    return number
    
def get_time_string():
    valid_time = False
    while not valid_time:
        print("Enter start time (00:00AM or PM or blank if unknown): ")
        the_time = get_string()
        the_time = the_time.upper() # to make am or pm into AM/PM
        if len(the_time) == 0:
            return "00:00PM"
        elif re.match("[0-9]{2}:[0-9]{2}[AP]M",the_time):
            return the_time

def day_of_the_week(dt):
    return dt.strftime('%A')
    
def get_date_string():
    valid_date = False
    while not valid_date:
        print("Enter date (mm/dd/yyyy): ")
        the_date = get_string()
        if re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}",the_date):
            month = int(the_date.split("/")[0])
            day = int(the_date.split("/")[1])
            year = int(the_date.split("/")[2])
            day_of_week = datetime.datetime(year, month, day, 0 , 0 , 0).strftime('%A')
            return (the_date,day_of_week)
            
def get_time_of_game_in_minutes():            
    valid_time = False
    # Accept input in Hours:Minutes, then convert to minutes
    while not valid_time:
        print("Enter time of game (HH:MM): ")
        the_time = get_string()
        if re.match("[0-9]{1,2}:[0-9]{2}",the_time):
            hours = the_time.split(":")[0]
            minutes = the_time.split(":")[1]
            time_in_minutes = (int(hours) * 60) + int(minutes)
            return time_in_minutes

def time_to_quit():
    response = display_menu_get_selection(["Continue","Quit"],"")
    if response == "Quit":
        return True
    return False
    
#########################################################################
#
# Menu functions
#
#    
def display_menu(menu):
    for count,item in enumerate(menu):
        line = "%2d. %s " % (count+1, item)
        print("%s" % line)
    
def get_menu_selection(menu,prompt):
    number_of_items = len(menu)
    if len(prompt) > 0:
        print("%s" % (prompt))    
        
    valid = False
    while not valid:
        menu_item_string = sys.stdin.readline()
        
        # remove \n and any non-numeric characters
        menu_item_string = menu_item_string.rstrip()
        menu_item_string = re.sub('[^0-9]','', menu_item_string)
        
        if len(menu_item_string) > 0:
            menu_item = int(menu_item_string)
            if ((menu_item >= 1) and (menu_item <= number_of_items)):
                valid = True
                
    return menu[menu_item-1]
    
def display_menu_get_selection(menu,prompt):
    display_menu(menu)
    return get_menu_selection(menu,prompt)    
    
    
# Allow player selection by typing first three letters of last name.
# If a player had a two-letter last name, use a hyphen for the third digit.
# If user inputs only a "+" character, return "stop" as the id as a signal
# to the calling function to stop asking for names.
def get_player_name_and_id(players,team):
    print("%s:%s" % (players,team))
    valid_name = False
    while not valid_name:
        print("[%s] Name (first three characters or 'Q/q' to stop): " % (team))
        n = get_string()
        if n.lower() == "q":
            return("nobody","stop")        
        n = n.lower()
        n = re.sub('[^a-z]','',n)
        if len(n) >= 3:
            first_three = n[:3]
            possible_name_list = ["TryAgain"]
            for pid in sorted(players[team.lower()]):
                if re.match(first_three,pid):
                    # Yes, this is a hack. By putting both the name and id in this array,
                    # display_menu_get_selection() will return them both, which we will 
                    # then split into their separate parts before returning them back to
                    # the caller.
                    possible_name_list.append(players[team.lower()][pid] + ":" + pid)
            name = display_menu_get_selection(possible_name_list,"")
            if name != "TryAgain":
                return (name.split(':')[0],name.split(':')[1])    

#########################################################################
#
# Main program starts here
#    

# No command-line arguments are needed, but argparse will automatically print this
# help message and then exit.
parser = argparse.ArgumentParser(description='Create or add box scores to a BOXTOP file.')
parser.add_argument('boxtop_file', help="Boxtop file (script will append new box scores to this file)") 
parser.add_argument('-roster_file', '-r', help="Optional roster file or comma-separated list of files whose names start with teamname (no spaces)")
args = parser.parse_args()

output_filename = args.boxtop_file

roster_data = defaultdict(dict)
if args.roster_file:
    if args.roster_file.count(",") > 0:
        list_of_roster_files = args.roster_file.split(",")
    else:
        list_of_roster_files = [args.roster_file]
else:
    list_of_roster_files = []
        
(player_info,list_of_teams) = boxtop_load_roster_files(list_of_roster_files)

print(player_info)
print(list_of_teams)

# Back up the event file before appending to it
current_datetime = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
backup_filename = output_filename.split(".")[0] + "_" + current_datetime + ".txt"

if os.path.exists(output_filename):
    # back up the output file first
    copyfile(output_filename,backup_filename)
    print("Created backup file %s" % (backup_filename))
    
quit_script = False

# A few variables to control which stats to prompt the user to enter.
prompt_for_assists = False
prompt_for_minutes = False
prompt_for_full_box = False # Ast, Min, Turnovers, Steals, Blocks


while not quit_script:
    # This will create the file if it does not exist already, but normally will
    # append a new box score to an existing file.
    output_file = open(output_filename,'a') 

    (b_date,b_dayofweek) = get_date_string()
    print("DATE: %s %s" % (b_dayofweek,b_date))

    print("Source: ")
    b_sources = get_string()
    if b_sources.lower() == "lat":
        b_sources = "Los Angeles Times"
        
    print("Road Team: ")
    b_rteam = get_string_require_nonzero_length()
    print("Home Team: ")
    b_hteam = get_string_require_nonzero_length()
    print("Neutral Site? (Y or blank) ")
    b_neutral_site = get_string()
    if len(b_neutral_site) > 0 and b_neutral_site[0].upper() == "Y":
        b_neutral_site = "YES"
    else:
        b_neutral_site = ""

    print("Game description (playoffs): ")
    b_title = get_string()

    print("Arena: ")
    b_arena = get_string()
    if b_arena == "pp":
        b_arena = "Pauley Pavilion"
        b_city = "Los Angeles"
        b_state = "California"
    else:
        print("City: ")
        b_city = get_string()
        print("State: ")
        b_state = get_string()
    b_country = "United States"
    
    print("Attendance: ")
    b_attendance = get_string()
    
    print("Referee1 (full name): ")
    b_ref1 = get_string()
    print("Referee2 (full name): ")
    b_ref2 = get_string()
    print("Referee3 (full name): ")
    b_ref3 = get_string()
    
    b_gametime = "00:00PM"
    b_timezone = "PT"
    b_radio = ""
    b_tv = ""
    b_prelim = ""
    b_event = ""
    
    print("Technical fouls NOT including coaches/players: ")
    b_other_techs = get_string()
    
    print("Any notes on this game? ")
    b_note = get_string()

    # Start writing this game to the file, starting with the preamble.
    output_file.write("\ngamebxt\nversion,1\n")
    
    # Information fields
    output_file.write("info,date,%s\n" % b_date)
    output_file.write("info,dayofweek,%s\n" % b_dayofweek)
    output_file.write("info,rteam,%s\n" % b_rteam)
    output_file.write("info,hteam,%s\n" % b_hteam)
    output_file.write("info,neutralsite,%s\n" % b_neutral_site)
    output_file.write("info,title,%s\n" % b_title)
    output_file.write("info,arena,%s\n" % b_arena)
    output_file.write("info,city,%s\n" % b_city)
    output_file.write("info,state,%s\n" % b_state)
    output_file.write("info,country,%s\n" % b_country)
    output_file.write("info,attendance,%s\n" % b_attendance)
    output_file.write("info,ref,%s\n" % b_ref1)
    output_file.write("info,ref,%s\n" % b_ref2)
    if len(b_ref3) > 0:
        output_file.write("info,ref,%s\n" % b_ref3)
    output_file.write("info,starttime,%s\n" % b_gametime)
    output_file.write("info,timezone,%s\n" % b_timezone)
    output_file.write("info,radio,%s\n" % b_radio)
    output_file.write("info,tv,%s\n" % b_tv)
    output_file.write("info,note,%s\n" % b_note)
    output_file.write("info,prelim,%s\n" % b_prelim)
    output_file.write("info,event,%s\n" % b_event)
    if len(b_other_techs) > 0:
        output_file.write("info,techs,%s\n" % b_other_techs)

    # team_stats_dict = defaultdict(dict)
    
    # Ask for data from both teams, using menu-driven names for any team we have in our roster files. 
    # Prompt for coach name too (first and last) but make the id first-last-1 in all cases.
    
    for tm in [b_rteam, b_hteam]:
        
        # User should input "UCLA Bruins"... we want to convert to "uclabruins" to match the input files.
        converted_team_name = re.sub(" ","",tm)
        converted_team_name = converted_team_name.lower()
        
        print("%s coach first name: " % (tm))
        coach_first_name = get_name_string()
        print("%s coach last name: " % (tm))
        coach_last_name = get_name_string()
        if len(coach_first_name) > 0 and len(coach_last_name) > 0:
            coach_id = clean_name_for_id(coach_first_name) + "-" + clean_name_for_id(coach_last_name) + "-1" # always use -1 for now
        else:
            coach_id = ""
        print("%s:%s:%s" % (coach_first_name,coach_last_name,coach_id))
        print("%s coach technical fouls: " % (tm))
        coach_technical_fouls = get_string()
        
        if tm == b_rteam:
            tm_string = "rteam"
        if tm == b_hteam:
            tm_string = "hteam"
            
        output_file.write("coach,%s,%s,%s,%s,%s\n" % (tm_string,coach_id,coach_first_name,coach_last_name,coach_technical_fouls))
        
        # player loop
        more_players = True
        while more_players:
            # Moved this to outer loop on 7/22
            # User should input "UCLA Bruins"... we want to convert to "uclabruins" to match the input files.
            #converted_team_name = re.sub(" ","",tm)
            #converted_team_name = converted_team_name.lower()
            if converted_team_name in list_of_teams:
                (full_name,dictionary_id) = get_player_name_and_id(player_info,converted_team_name)
                if dictionary_id == "stop":
                    break
                p_id, p_first_name, p_last_name = translate_dictionary_id(dictionary_id) # we built the dictionary id's with last-first-# when the real CBB pages use first-last-#
                print("%s:%s:%s" % (p_first_name,p_last_name,p_id))
            else:
                print("%s player first name or Q/q to quit: " % (tm))
                p_first_name = get_name_string()
                if p_first_name.lower() == "q":
                    more_players = False
                    break
                
                print("%s player last name: " % (tm))
                p_last_name = get_name_string()
                if len(p_first_name) > 0 and len(p_last_name) > 0:
                     # always use -99 since we really do not know what number to use, and I do not want these to conflict with the ids read from the roster files.
                    p_id = clean_name_for_id(p_first_name) + "-" + clean_name_for_id(p_last_name) + "-99"
                else:
                    p_id = ""                
                print("%s:%s:%s" % (p_first_name,p_last_name,p_id))
            
            if prompt_for_full_box or prompt_for_minutes:
                print("MIN: ")
                p_minutes = get_string()
            else:
                p_minutes = ""
            
            print("FGM: ")
            p_fgm = get_string()
            print("FGA: ")
            p_fga = get_string()
            print("FTM: ")
            p_ftm = get_string()
            print("FTA: ")
            p_fta = get_string()
            
            p_fg3m = ""
            p_fg3a = ""

            p_oreb = ""

            print("REB: ")
            p_reb = get_string()
            
            if prompt_for_assists or prompt_for_full_box:
                print("AST: ")
                p_ast = get_string()
            else:
                p_ast = ""

            if prompt_for_full_box:
                print("STEALS: ")
                p_steals = get_string()
            else:
                p_steals = ""

            if prompt_for_full_box:
                print("BLOCKS: ")
                p_blocks = get_string()
            else:
                p_blocks = ""

            if prompt_for_full_box:
                print("TURNOVERS: ")
                p_turnovers = get_string()
            else:
                p_turnovers = ""
            
            print("FOULS: ")
            p_pf = get_string()
            
            print("PTS: ")
            p_pts = get_string()

            print("TECHNICAL FOULS: ")
            p_technical_fouls = get_string()

            output_file.write("stat,%s,player,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (tm_string,p_id,p_first_name,p_last_name,p_minutes,p_fgm,p_fga,p_ftm,p_fta,p_fg3m,p_fg3a,p_pts,p_oreb,p_reb,p_ast,p_pf,p_blocks,p_turnovers,p_steals,p_technical_fouls))
            
            #print("More players for %s? (Q/q to stop)" % (tm))
            #response = get_string()
            #if response.lower() == "q":
            #    more_players = False
                
        # team stats
        print("%s TEAM STATS" % (tm))
        
        if prompt_for_full_box or prompt_for_minutes:
            print("MIN: ")
            t_minutes = get_string()
        else:
            t_minutes = ""
        
        print("FGM: ")
        t_fgm = get_string()
        print("FGA: ")
        t_fga = get_string()
        print("FTM: ")
        t_ftm = get_string()
        print("FTA: ")
        t_fta = get_string()
        
        t_fg3m = ""
        t_fg3a = ""

        t_oreb = ""

        print("REB: ")
        t_reb = get_string()
        
        print("TEAM REBOUNDS: ")
        t_team_rebounds = get_string()

        if prompt_for_assists or prompt_for_full_box:
            print("AST: ")
            t_ast = get_string()
        else:
            t_ast = ""

        if prompt_for_full_box:
            print("STEALS: ")
            t_steals = get_string()
        else:
            t_steals = ""
            
        if prompt_for_full_box:
            print("BLOCKS: ")
            t_blocks = get_string()
        else:
            t_blocks = ""

        if prompt_for_full_box:
            print("TURNOVERS: ")
            t_turnovers = get_string()
        else:
            t_turnovers = ""

        print("FOULS: ")
        t_pf = get_string()
        
        print("PTS: ")
        t_pts = get_string()
        
        print("TECHNICAL FOULS: ")
        t_technical_fouls = get_string()        

        output_file.write("tstat,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (tm_string,t_minutes,t_fgm,t_fga,t_ftm,t_fta,t_fg3m,t_fg3a,t_pts,t_oreb,t_reb,t_ast,t_pf,t_blocks,t_turnovers,t_steals,t_team_rebounds,t_technical_fouls))
        
        print("LINESCORE (comma delimited, use colon before final score): ")
        t_linescore = get_string()
        output_file.write("linescore,%s,%s\n" % (tm_string,t_linescore))
        
    output_file.write("sources,%s\n" % b_sources)

    output_file.close()
    
    print("Game saved.\n")
    
    if time_to_quit():
        quit_script = True

print("Exiting script.")  
