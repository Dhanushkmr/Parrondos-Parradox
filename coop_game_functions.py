import numpy as np
import random as rd
import math


def win_or_lose(capital, p):
    u = rd.uniform(0,1)
    if u <= p:
        capital = capital + 1
        state = 'W'
    else:
        capital = capital - 1
        state = 'L'
    return capital, state


def game_a(capital, e = 0):
    #coin 1
    p_1 = 0.5 - e
    return win_or_lose(capital, p_1)


def game_b(capital, left, right, e = 0):
    #coin 2
    if left == right == 'L':
        p_2 = 1.0 - e
        return win_or_lose(capital, p_2)
    #coin 3
    elif left != right:
        p_3 = 0.16 - e
        return win_or_lose(capital, p_3)
    #coin 4
    else:
        p_4 = 0.7 - e
        return win_or_lose(capital, p_4)


def sim_game_a_single(num_players = 50, e = 0, games = 20000):
    curr_trial_list = [0]
    player_cap = [0]*num_players
    for _ in range(games):
        # for each game, select one random player to play
        random_player = rd.randint(0,num_players-1)
        player_cap[random_player] = game_a(player_cap[random_player])[0]
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_game_b_single(num_players = 50, e = 0, games = 20000):
    curr_trial_list = [0]
    player_state = [ rd.choice(["W", "L"]) for _ in range(num_players) ]
    player_cap = [0]*num_players
    for _ in range(games):
        random_player = rd.randint(0,num_players-1)
        selected_player_cap = player_cap[random_player]
        left_guy = random_player-1
        right_guy = random_player + 1
        if right_guy == num_players:
            right_guy = 0
        left_state = player_state[left_guy]
        right_state = player_state[right_guy]
        selected_player_cap, selected_player_state = game_b(selected_player_cap, left_state, right_state)
        player_state[random_player] = selected_player_state
        player_cap[random_player] = selected_player_cap
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_rand_a_b_single(num_players = 50, e = 0, games = 20000):
    curr_trial_list = [0]
    player_state = [rd.choice(["W", "L"]) for _ in range(num_players)]
    player_cap = [0]*num_players
    for _ in range(games):
        random_player = rd.randint(0,num_players-1)
        if rd.choice(['A', 'B']) == 'A':
            player_cap[random_player], player_state[random_player] = game_a(player_cap[random_player])
        else:
            left_guy = random_player - 1
            right_guy = random_player + 1
            if right_guy == num_players:
                right_guy = 0
            left_state = player_state[left_guy]
            right_state = player_state[right_guy]
            player_cap[random_player], player_state[random_player] = game_b(player_cap[random_player], left_state, right_state)
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_aabb_single(num_players = 50, e = 0, games = 20000):
    sequence = 'AABB'*int((games/4))
    curr_trial_list = [0]
    player_state = [rd.choice(["W", "L"]) for _ in range(num_players)]
    player_cap = [0]*num_players
    for _ in range(games):
        random_player = rd.randint(0,num_players-1)
        if sequence[games] == 'A':
            player_cap[random_player], player_state[random_player] = game_a(player_cap[random_player], e)
        else:
            left_guy = random_player - 1
            right_guy = random_player + 1
            if right_guy == num_players:
                right_guy = 0
            left_state = player_state[left_guy]
            right_state = player_state[right_guy]
            player_cap[random_player], player_state[random_player] = game_b(player_cap[random_player], left_state, right_state, e)
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list