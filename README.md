# bball_league

This program simulates a fake basketball league's season.  It creates a league with N teams, fills out each roster with five unique players, and simulates each possession of the games between the teams.  I wrote this as a way to generate my own data with which to learn SQL and Tableau.  Check out the portfolio project <a href="https://reedhodges.github.io/sql-project/">webpage</a> for a walkthrough, or go straight to the <a href="https://reedhodges.github.io/html_files/bball_league_story.html">visualization</a>.

## File descriptions

- `rosters.py`: contains the classes for the creation of rosters with players of unique attributes
- `game.py`: contains the functions that simulate a possession in a game, as well as a full game itself
- `season.py`: contains the class the simulates a full season and stores the game statistics
- `lists.py`: contains lists of team nicknames/mascots
- `expl_data_analysis.py`: plots real NBA stats using plotly (for use in the portfolio project), and obtains means and/or standard deviations for the distributions used in the simulation