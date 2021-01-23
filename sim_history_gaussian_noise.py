import numpy as np
import random as rd
import math


def win_or_lose(capital, outcome, outcome_seq):        
	if outcome:
		capital += 1
		outcome_seq += 'W'
	else:
		capital -= 1
		outcome_seq += 'L'
	return capital, outcome_seq


def get_game_mat(p, games, mu, sigma, scale):
	p -= 0.003
	p_mat = np.ones((1, games))*p
	noise_mat = np.random.normal(mu, sigma, games)*scale
	p_mat_noise = p_mat + noise_mat
	u = np.random.uniform(0, 1, games)
	res = u <= p_mat_noise
	return res


def game_a_single(mu, sigma, scale, games = 100, p_1 = 0.5):
	p_1_outcomes = get_game_mat(p_1, games, mu, sigma, scale)
	capital_list = [0] * (games + 1)
	for i in range(1, games+1):
		capital_list[i] = win_or_lose(capital_list[i-1], p_1_outcomes[0][i-1], '')[0]
	return capital_list


def game_b_single(mu, sigma, scale, games = 100, p_2 = 0.9, p_3 = 0.25, p_4 = 0.7):
	p_2_outcomes = get_game_mat(p_2, games-2, mu, sigma, scale)
	p_3_outcomes = get_game_mat(p_3, games-2, mu, sigma, scale)
	p_4_outcomes = get_game_mat(p_4, games-2, mu, sigma, scale)
	#seed 2 games
	outcome_seq = rd.choice(['W','L']) + rd.choice(['W','L'])
	if outcome_seq == 'WW':
		capital_list = [0, 1, 2]
	elif outcome_seq == 'LL':
		capital_list = [0, -1, -2]
	elif outcome_seq == 'LW':
		capital_list = [0, -1, 0]
	else:
		capital_list = [0, 1, 0]
	games -= 2
	capital_list = capital_list + [0] * games
	for i in range(games):
		most_recent_2_games = outcome_seq[-2:]
		if most_recent_2_games == 'LL':
			#coin B1
			capital_list[i+3], outcome_seq = win_or_lose(capital_list[i+2], p_2_outcomes[0][i], outcome_seq)
		elif most_recent_2_games in ['LW','WL']:
			#coin B2
			capital_list[i+3], outcome_seq = win_or_lose(capital_list[i+2], p_3_outcomes[0][i], outcome_seq)
		else:
			#coin B4
			capital_list[i+3], outcome_seq = win_or_lose(capital_list[i+2], p_4_outcomes[0][i], outcome_seq)
	return capital_list


def sim_rand_a_b_single(mu, sigma, scale, games = 100, p_1 = 0.5, p_2 = 0.9, p_3 = 0.25, p_4 = 0.7):
	p_1_outcomes = get_game_mat(p_1, games, mu, sigma, scale)
	p_2_outcomes = get_game_mat(p_2, games, mu, sigma, scale)
	p_3_outcomes = get_game_mat(p_3, games, mu, sigma, scale)
	p_4_outcomes = get_game_mat(p_4, games, mu, sigma, scale)
	capital_list = [0]* (games+1)
	outcome_seq = ''
	for i in range(1,games+1):
		prev_capital = capital_list[i-1]
		choice = rd.choice(['a', 'b'])
		if choice == 'a':
			#play game a
			capital_list[i], outcome_seq = win_or_lose(prev_capital, p_1_outcomes[0][i-1], outcome_seq)
		else:
			#play game b
			if len(outcome_seq) < 2:
				outcome_seq += rd.choice(['W','L'])
				if outcome_seq[-1] == 'W':
					capital_list[i] = prev_capital + 1
				else:
					capital_list[i] = prev_capital - 1
			else:
				most_recent_2_games = outcome_seq[-2:]
				if most_recent_2_games == 'LL':
					#coin B1
					capital_list[i], outcome_seq = win_or_lose(prev_capital, p_2_outcomes[0][i-1], outcome_seq)
				elif most_recent_2_games in ['LW','WL']:
					#coin B2
					capital_list[i], outcome_seq = win_or_lose(prev_capital, p_3_outcomes[0][i-1], outcome_seq)
				else:
					#coin B4
					capital_list[i], outcome_seq = win_or_lose(prev_capital, p_4_outcomes[0][i-1], outcome_seq)        
	return capital_list


def sim_AABB_single(mu, sigma, scale, games = 100, p_1 = 0.5, p_2 = 0.9, p_3 = 0.25, p_4 = 0.7):
	p_1_outcomes = get_game_mat(p_1, games, mu, sigma, scale)
	p_2_outcomes = get_game_mat(p_2, games, mu, sigma, scale)
	p_3_outcomes = get_game_mat(p_3, games, mu, sigma, scale)
	p_4_outcomes = get_game_mat(p_4, games, mu, sigma, scale)
	sequence = 'AABB'*(games//4)
	capital_list = [0]* (games+1)
	outcome_seq = ''
	for i in range(1, games+1):
		prev_capital = capital_list[i-1]
		if sequence[i-1] == 'A':
			capital_list[i], outcome_seq = win_or_lose(prev_capital, p_1_outcomes[0][i-1], outcome_seq)
		else:
			most_recent_2_games = outcome_seq[-2:]
			if most_recent_2_games == 'LL':
				#coin B1
				capital_list[i], outcome_seq = win_or_lose(prev_capital, p_2_outcomes[0][i-1], outcome_seq)
			elif most_recent_2_games in ['LW','WL']:
				#coin B2
				capital_list[i], outcome_seq = win_or_lose(prev_capital, p_3_outcomes[0][i-1], outcome_seq)
			else:
				#coin B4
				capital_list[i], outcome_seq = win_or_lose(prev_capital, p_4_outcomes[0][i-1], outcome_seq)
	return capital_list