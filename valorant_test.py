import pandas as pd
from cse163_utils import assert_equals
import valorant as val


def test_total_map_picked(banned_maps, map_picked):
    """
    this method implements test functions for total_map_picked
    """
    assert_equals(['18'], val.total_map_picked(banned_maps, map_picked))


def test_predict_top_ten_kda(masters, players1, players2, agents):
    """
    this method implements test functions for predict_top_ten_kda
    """
    assert_equals(['L1NK', 'Soulcas', 'Derke', 'Doma', 'Boaster',
                   'TenZ', 'Peri', 'Gaabxx', 'ScreaM', 'Foxz'],
                  val.predict_top_ten_kda(masters, players1))
    assert_equals(['L1NK', 'Soulcas', 'Gaabxx', 'ScreaM', 'Mistic',
                  'Patiphan', 'TenZ', 'Boaster', 'Magnum', 'Jamppi'],
                  val.predict_top_ten_kda(masters, players2))


def test_predict_top_ten_agents(masters, players1, players2, agents):
    """
    this method implements test functions for predict_top_ten_agents
    """
    assert_equals(['L1NK', 'Soulcas', 'Peri', 'Doma', 'ScreaM',
                   'TenZ', 'Gaabxx', 'Derke', 'Boaster', 'Foxz'],
                  val.predict_top_ten_agents(masters, players1, agents))
    assert_equals(['L1NK', 'Soulcas', 'Gaabxx', 'ScreaM', 'Patiphan',
                   'Mistic', 'TenZ', 'Magnum', 'Jamppi', 'Boaster'],
                  val.predict_top_ten_agents(masters, players2, agents))


def test_accuracy():
    """
    this method implements test functions for accuracy
    """
    assert_equals((0.0, 0.0),
                  val.accuracy([0, 1, 2], [3, 0, 4], [2, 0, 1]))
    assert_equals((0.25, 0),
                  val.accuracy([0, 0, 1, 2], [5, 1, 1, 4], [4, 2, 0, 1]))


def test_order_change():
    """
    this method implements test functions for order_change
    """
    assert_equals([[0, 1, 2], [0, 3, 4], [0, 1, 2]],
                  val.order_change([0, 1, 2], [3, 0, 4], [2, 0, 1]))
    assert_equals([[0, 0, 1, 2], [5, 1, 1, 4], [4, 0, 1, 2]],
                  val.order_change([0, 0, 1, 2], [5, 1, 1, 4], [4, 2, 0, 1]))


def main():
    masters = pd.read_csv('/data/test_masters.csv')
    players1 = pd.read_csv('/data/test_players1.csv')
    players2 = pd.read_csv('/data/test_players2.csv')
    agents = pd.read_csv('/data/agent_stats.csv')
    banned_maps = pd.read_csv('/data/test_picked.csv')
    map_picked = pd.read_csv('/data/test_banned.csv')
    test_predict_top_ten_kda(masters, players1, players2, agents)
    test_predict_top_ten_agents(masters, players1, players2, agents)
    test_total_map_picked(banned_maps, map_picked)
    test_accuracy()
    test_order_change()
    print('All methods work!')


if __name__ == '__main__':
    main()
