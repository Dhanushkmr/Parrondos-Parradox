import numpy as np
import random as rd
import math
import colorednoise as cn


def win_or_lose(capital, outcome):
    if outcome:
        capital = capital + 1
        state = 'W'
    else:
        capital = capital - 1
        state = 'L'
    return capital, state


def get_game_mat(p, games, scale):
    p_mat = np.ones((1, games))*p
    noise_mat = cn.powerlaw_psd_gaussian(2, games)*scale
    p_mat_noise = p_mat + noise_mat
    u = np.random.uniform(0, 1, games)
    res = u <= p_mat_noise
    return res


def sim_game_a_single(scale, p1 = 0.5, num_players = 10, games = 2000):
    game_a_outcomes = get_game_mat(p1, games, scale)
    curr_trial_list = [0] 
    player_cap = [0]*num_players
    for i in range(games):
        # for each game, select one random player to play
        random_player = rd.randint(0,num_players-1)
        player_cap[random_player] = win_or_lose(player_cap[random_player], game_a_outcomes[0][i])[0]
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_game_b_single(scale, p2 = 1.0, p3 = 0.16, p4 = 0.7, num_players = 10, games = 2000):
    p_2_outcomes = get_game_mat(p2, games, scale)
    p_3_outcomes = get_game_mat(p3, games, scale)
    p_4_outcomes = get_game_mat(p4, games, scale)

    curr_trial_list = [0]
    player_state = [ rd.choice(["W", "L"]) for _ in range(num_players) ]
    player_cap = [0]*num_players
    for i in range(games):
        random_player = rd.randint(0,num_players-1)
        selected_player_cap = player_cap[random_player]
        left_guy = random_player-1
        right_guy = random_player + 1
        if right_guy == num_players:
            right_guy = 0
        left_state = player_state[left_guy]
        right_state = player_state[right_guy]
        if left_state == right_state == 'L':
            selected_player_cap, selected_player_state = win_or_lose(selected_player_cap, p_2_outcomes[0][i])
        elif left_state != right_state:
            selected_player_cap, selected_player_state = win_or_lose(selected_player_cap, p_3_outcomes[0][i])
        else:
            selected_player_cap, selected_player_state = win_or_lose(selected_player_cap, p_4_outcomes[0][i])
        player_state[random_player] = selected_player_state
        player_cap[random_player] = selected_player_cap
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_rand_a_b_single(scale, p1 = 0.5, p2 = 1.0, p3 = 0.16, p4 = 0.7,num_players = 10, games = 2000):
    p_1_outcomes = get_game_mat(p1, games, scale)
    p_2_outcomes = get_game_mat(p2, games, scale)
    p_3_outcomes = get_game_mat(p3, games, scale)
    p_4_outcomes = get_game_mat(p4, games, scale)
    curr_trial_list = [0]
    player_state = [rd.choice(["W", "L"]) for _ in range(num_players)]
    player_cap = [0]*num_players
    for i in range(games):
        random_player = rd.randint(0,num_players-1)
        if rd.choice(['A', 'B']) == 'A':
            player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_1_outcomes[0][i])
        else:
            left_guy = random_player - 1
            right_guy = random_player + 1
            if right_guy == num_players:
                right_guy = 0
            left_state = player_state[left_guy]
            right_state = player_state[right_guy]
            if left_state == right_state == 'L':
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_2_outcomes[0][i])
            elif left_state != right_state:
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_3_outcomes[0][i])
            else:
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_4_outcomes[0][i])
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list


def sim_aabb_single(scale, p1 = 0.5, p2 = 1.0, p3 = 0.16, p4 = 0.7,num_players = 10, games = 2000):
    p_1_outcomes = get_game_mat(p1, games, scale)
    p_2_outcomes = get_game_mat(p2, games, scale)
    p_3_outcomes = get_game_mat(p3, games, scale)
    p_4_outcomes = get_game_mat(p4, games, scale)
    sequence = 'AABB'*int((games/4))
    curr_trial_list = [0]
    player_state = [rd.choice(["W", "L"]) for _ in range(num_players)]
    player_cap = [0]*num_players
    for i in range(games):
        random_player = rd.randint(0,num_players-1)
        if sequence[i] == 'A':
            player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_1_outcomes[0][i])
        else:
            left_guy = random_player - 1
            right_guy = random_player + 1
            if right_guy == num_players:
                right_guy = 0
            left_state = player_state[left_guy]
            right_state = player_state[right_guy]
            if left_state == right_state == 'L':
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_2_outcomes[0][i])
            elif left_state != right_state:
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_3_outcomes[0][i])
            else:
                player_cap[random_player], player_state[random_player] = win_or_lose(player_cap[random_player], p_4_outcomes[0][i])
        curr_trial_list.append(sum(player_cap))
    return curr_trial_list