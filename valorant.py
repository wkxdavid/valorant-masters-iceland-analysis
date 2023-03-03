import pandas as pd
import plotly.express as px
from sklearn.metrics import accuracy_score


def highest_KDA_players(masters_path):
    """
    takes in the dataset, and plots out a graph that shows
    the highest kda players using plotly
    """
    masters = pd.read_csv(masters_path)
    highest_KDA = px.bar(data_frame=masters.nlargest(10, 'KDA')[['Player',
                         'KDA']], x='Player', y='KDA', color='KDA', text='KDA',
                         title="Highest Players KDA")
    highest_KDA.write_image("/data/KDA.png")
    highest_KDA.show()


def total_map_picked(banned_maps, map_picked):
    """
    takes in two datasets banned_maps and map_picked and merges
    them together. than combines the total maps played for row
    and prints it
    """
    banned = pd.read_csv.(banned_maps)
    picked = pd.read_csv(map_picked)
    maps = pd.merge(banned, picked, on="Map")
    total_map = maps['total'] = maps['Total_x'] + maps['Total_y']
    print("Total amount of times a map was either banned or picked")
    print(total_map)


def predict_top_ten_kda(masters, players):
    """
    This function is meant to be implemented in prediction_model().

    Short:
    This function returns its prediction of the top ten players in the
    masters tournament using the dataframes masters (players in the tournament)
    and players (all professional valorant players)

    Long:
    This function takes 2 pandas dataframes: masters, containing data during
    the tournament of all players present, and players, containing general
    data on all professional Valorant players from the last few months. Using
    the 'K' (#kills), 'A' (#assists), and 'D' (#deaths) columns in players, the
    function calculates the overall kda of each master and tries to predict the
    top ten masters of the tournament based on kda alone. The prediction is
    returned as a list of 10 strings, each value containing the name of one
    player.
    """
    masters_list = masters['Player'].tolist()
    filtered_data = players[players['PLAYER'].isin(masters_list)]
    master_data = filtered_data.copy()
    master_data['KDA'] = (master_data['K']+master_data['A']/2)/master_data['D']
    players_list = master_data['PLAYER'].tolist()
    kda_list = master_data['KDA'].tolist()
    overall_kda = {}
    for i in range(len(players_list)):
        overall_kda[players_list[i]] = kda_list[i]
    top_ten = {}
    for i in range(0, 10):
        temp_max = 0
        temp_name = ""
        for pair in overall_kda.items():
            if pair[1] > temp_max:
                temp_name = pair[0]
                temp_max = pair[1]
        top_ten[temp_name] = temp_max
        overall_kda.pop(temp_name)
    return list(top_ten.keys())


def predict_top_ten_agents(masters, players, agents):
    """
    This function is meant to be implemented in prediction_model().

    Short:
    This function returns its prediction of the top ten players in the
    masters tournament using the dataframes masters (players in the
    tournament), players (all professional valorant players), and agents
    (overall agent data).

    Long:
    This function takes 3 pandas dataframes: masters, containing data during
    the tournament of all players present; players, containing general
    data on all professional Valorant players from the last few months; and
    agents, containing overall data on each agent, such as KDA, win rate, etc.
    Using the 'K' (#kills), 'A' (#assists), and 'D' (#deaths) columns in
    players, the function calculates the overall kda of each master. Then, the
    function finds which agents each master used and adds the average win-rate
    of each agent to each master's kda (average win-rate means that if a player
    used multiple agents, their collective average is what gets added to the
    player's kda). Based off this new quantity, the function tries to predict
    the top ten masters of the tournament. The prediction is returned as a list
    of 10 strings, each value containing the name of one player.
    """
    masters_list = masters['Player'].tolist()
    filtered_data = players[players['PLAYER'].isin(masters_list)]
    master_data = filtered_data.copy()
    master_data['KDA'] = (master_data['K']+master_data['A']/2)/master_data['D']
    players_list = master_data['PLAYER'].tolist()
    kda_list = master_data['KDA'].tolist()
    overall_score = {}
    for i in range(0, len(players_list)):
        overall_score[players_list[i]] = kda_list[i]
    for pair in overall_score.items():
        val = 0
        row = masters[masters['Player'] == pair[0]]['Agents']
        count = 0
        for player_agents in row:
            player_agents = player_agents[1:len(player_agents)-1]
            player_agents = player_agents.split(', ')
            for agent in player_agents:
                agent = agent[1:len(agent)-1]
                agent_percent = agents[agents['Agent'] == agent]['Win %']
                for percent in agent_percent:
                    percent = percent.replace('%', '')
                    score = float(percent)/100
            val += score
            count += 1
        val /= count
        overall_score[pair[0]] += val
    top_ten = {}
    for i in range(0, 10):
        temp_max = 0
        temp_name = ""
        for pair in overall_score.items():
            if pair[1] > temp_max:
                temp_name = pair[0]
                temp_max = pair[1]
        top_ten[temp_name] = temp_max
        overall_score.pop(temp_name)
    return list(top_ten.keys())


def accuracy(true_list, kda_list, agent_list):
    """
    This function is meant to be implemented in prediction_model().

    This function takes 3 lists, one is the correct one (true_list), and the
    others are predictions. The function measures the accuracy of the
    prediction lists using accuracy_score imported from sklearn.metrics and
    returns their respective accuracy scores as a tuple with the first element
    being the score of kda_list and the second being the score of agent_list.
    """
    kda_accuracy = accuracy_score(true_list, kda_list)
    agent_accuracy = accuracy_score(true_list, agent_list)
    return (kda_accuracy, agent_accuracy)


def order_change(true_list, kda_list, agent_list):
    """
    This function is meant to be implemented in prediction_model().

    Short:
    This function takes 3 lists and reorders kda_list and agent_list with
    respect to true_list to arrange them in the best order for the accuracy
    function.

    Long:
    This function takes a target list true_list, and two prediction lists,
    kda_list and agent_list. It is assumed that no list has multiple
    values containing the same name and thatall lists are of the same length.
    The function reorders kda_list and agent_list such that any value in the
    prediction lists that is also in true_list is put into that index. The
    function returns a list of lists, the first being true_list, and the
    second and third being the reordered kda_list and agent_list respectively.
    This is done so that the accuracy score can be calculated based on how many
    correct names were in the list, not the order of names on the list.
    For example,
    order_change([0,1,2], [3,0,4], [2,0,1]) returns
    [[0,1,2], [0,3,4], [0,1,2]]
    """
    for i in range(len(true_list)):
        if true_list[i] in kda_list:
            temp = kda_list[i]
            kda_list[kda_list.index(true_list[i])] = temp
            kda_list[i] = true_list[i]
        if true_list[i] in agent_list:
            temp = agent_list[i]
            agent_list[agent_list.index(true_list[i])] = temp
            agent_list[i] = true_list[i]
    return [true_list, kda_list, agent_list]


def conclusion(true_list, kda_list, agent_list, scores):
    """
    This function is meant to be implemented in prediction_model().

    This function takes 3 lists of strings, true_list being the correct one
    and kda_list and agent_list being the predictions, and a tuple scores
    containing the accuracy scores of kda_list and agent_list (it is assumed
    it is in that order). The function reports both the correct and prediction
    lists, and then interprets the data and prints the conclusion of how
    effective each algorithm was, and how they compare against each other. An
    algorithm is effective if its accuracy score is greater than 0.5.
    """
    print('Actual Top Ten:')
    print(true_list)
    print('\nPrediction:')
    print(kda_list)
    print('\nPrediction Factoring in Agent Selection:')
    print(agent_list)
    if scores[0] > 0.5:
        print('\nWith an accuracy score of ' + str(scores[0]) +
              ', the first prediction model did decently well.')
        if scores[1] > scores[0]:
            print('And with an accuracy score of ' + str(scores[1]) +
                  ', the second model did even better.')
            print('So, we can conclude agent selection was important ' +
                  'during this tournament.')
        else:
            print('Wth an accuracy score of ' + str(scores[1]) +
                  ', the second model did not do better.')
            print('So, we can conclude that agent selection was ' +
                  'not significant during this tournament.')
    else:
        print('\nWith an accuracy score of ' + str(scores[0]) +
              ', the first prediction model was rather inaccurate.')
        if scores[1] > scores[0]:
            if scores[1] > 0.5:
                print('However, the second model did much better with '
                      'an accuracy score of '+str(scores[1])+'.')
                print('So, we can conclude agent selection played a '
                      'crucial role during this tournament.')
            else:
                print('The second model did not do much better: ' +
                      str(scores[1])+'.')
                print('So, we cannot conclude anything about agent selection '
                      'as our model is not accurate.')


def prediction_model(masters_file, players_file, agents_file):
    """
    Short:
    This function is exactly as the name suggests, a prediction model.
    The function takes 3 csv file paths and calls all functions to predict
    the top ten masters of the tournament and test that prediction. The
    results are printed.

    Long:
    This function takes 3 file paths (strings) to 3 different csv files,
    one containing data on all masters in the tournament (masters_file),
    one containing public data on all professional valorant players,
    and one containing overall agent data in valorant. The function
    reads these csvs as pandas dataframes and uses them in calling all
    necessary methods to create and test 2 predictive algorithms, both
    using kda data and one using agent data, that attempt to predict the
    top ten masters of the tournament. The results are printed.
    """
    masters = pd.read_csv(masters_file)
    players = pd.read_csv(players_file)
    agents = pd.read_csv(agents_file)
    kda_list = predict_top_ten_kda(masters, players)
    agent_list = predict_top_ten_agents(masters, players, agents)
    top_ten_masters = masters.head(10)
    true_list = top_ten_masters['Player'].tolist()
    lists = order_change(true_list, kda_list, agent_list)
    results = accuracy(lists[0], lists[1], lists[2])
    conclusion(lists[0], lists[1], lists[2], results)


def main():
    masters_path = 'player_stats.csv'
    players_path = 'public_player_stats.csv'
    agents_path = 'agent_stats.csv'
    banned_maps = 'banned_maps_stats.csv'
    map_picked = 'map_pick_stats.csv'
    highest_KDA_players(masters_path)
    total_map_picked(banned_maps, map_picked)
    prediction_model(masters_path, players_path, agents_path)


if __name__ == '__main__':
    main()
