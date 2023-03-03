Some additional things may be needed to properly use those codes as it was transfered from personal storage.

Insert the code (valorant.py and valorant_test.py) to the python
software. Than upload all of the csv files (agent_stats.csv, banned_map_stats.csv
map_pick_stats.csv, player_stats.csv, public_player_stats.csv, side_pick_stats.csv,
test_banned.csv, test_masters.csv, test_players1.csv, and test_players2.csv)

The python software will need to be able to
import plotly, pandas, sklearn.metrics. Which means install
if necessary those things if necessary.
For theses below:
    import pandas as pd
    import plotly.express as px
    from sklearn.metrics import accuracy_score


Now the code should be runnable.
To remove or use a specific function, go to the main method in valorant.py and
comment methods out.
Otherwise, all of the programs will default be on.
There is a KDA.PNG that is meant for the highest_KDA_players(masters_path) function

To merge the two datasets, use the function highest_KDA_players()

To plot the KDA's, use the function test_total_map_picked()

The rest of the functions should be for the machine learning aspect.

