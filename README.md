# boxtopNCAA
Python scripts for entering NCAA box scores in BOXTOP format

These scripts are loosely based on the boxtopABA scripts (which were written in Perl) and the boxtopBaseball scripts (which were written in Python).
The scripts store basketball box scores in the BOXTOP format that I have developed over the past 10+ years for ABA, NBA, and NCAA box scores.

boxtop2Text.py - Converts a BOXTOP file into a .csv file that is suitable for cutting-and-pasting into a spreadsheet (like Excel) to make it easier to cut-and-paste the same data into a word processor (like Word).
boxtopCheck.py - Checks a BOXTOP file for inconsistencies.
boxtopGameLog.py - Creates a game log for an individual player from a BOXTOP file.
boxtopNCAA.py - Creates a BOXTOP file by prompting the user to enter stats and other information from a box score. Easy to modify to adjust to the format of the box score in the original source.
boxtopTeamGameLog.py - Create a game log for a single team from a BOXTOP file.

BOXTOP format

The BOXTOP format is loosely based on Retrosheet’s “Box Score Event Files” (BSEF) format, which is essentially a comma-separated file (.csv) format.

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit # http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
