from scipy import stats
from matplotlib import pyplot
import pandas as pd
from math import sqrt
import method

frame = pd.read_csv('arrests.csv')
team_names = frame['home_team']
print(frame)
# Cut out team that reported unreliable data, no data collected there. Not in the data file are also Buffalo and St. Louis
team_cut = frame[~frame['home_team'].isin(['st_louis','Detroit', 'Minnesota', 'Miami','Oakland','Atlanta','Cleveland','New Orleans'])]
#**** Extract Relevant Data ****
arrests_cut = team_cut['arrests']
home_score_cut = team_cut['home_score']
away_score_cut = team_cut['away_score']
#-extract home team score of games with more than mean arrests
score_games_morethan_6_home = team_cut[team_cut['arrests'] > 6.56]
score_games_morethan_6_home = score_games_morethan_6_home['home_score']

#-extract away team score of games with more than mean arrests
score_games_morethan_6_away = team_cut[team_cut['arrests'] > 6.56]
score_games_morethan_6_away = score_games_morethan_6_away['away_score']

#-extract home team score of games with less than mean arrests
score_games_lessthan_6_home = team_cut[team_cut['arrests'] < 6.56]
score_games_lessthan_6_home = score_games_lessthan_6_home['home_score']

#-extract away team score of games with more than mean arrests
score_games_lessthan_6_away = team_cut[team_cut['arrests'] > 6.56]
score_games_lessthan_6_away = score_games_lessthan_6_away['away_score']

#-extract total points scored from games with more than a mean number of arrests.
score_games_morethan_6_total = team_cut[team_cut['arrests'] > 6.56]
score_games_morethan_6_total = score_games_morethan_6_total['home_score'] + score_games_morethan_6_total['away_score']

#-extract total points scored from games with elss than the mean arrests
score_games_lessthan_6_total = team_cut[team_cut['arrests'] < 6.56]
score_games_lessthan_6_total = score_games_lessthan_6_total['home_score'] + score_games_lessthan_6_total['away_score']

#-extract games in the upper 15.9%
score_games_morethan_1std_home = team_cut[team_cut['arrests'] > 15.67]
score_games_morethan_1std_home = score_games_morethan_1std_home['home_score']

#-extract games in the lower 15.9%
score_games_lessthan_1std_home = team_cut[team_cut['arrests'] < 15.67]
score_games_lessthan_1std_home = score_games_lessthan_1std_home['home_score']

#-extract total points scored
total_points_cut = team_cut['home_score'] + team_cut['away_score']

#-extract scoring details
winning_home_team_scores = []
losing_home_team_scores = []
point_differential = []
for score_home, score_away in zip(home_score_cut,away_score_cut):
    if score_home -score_away <= 0:
        losing_home_team_scores.append(score_home)
        point_differential.append(score_away-score_home)
    elif score_home - score_away > 0:
        winning_home_team_scores.append(score_home)
        point_differential.append(score_home- score_away)

#-- extract winning home teams and arrests
home_team_wins = team_cut[team_cut['home_score']>team_cut['away_score']]
home_team_wins_arrests = home_team_wins['arrests']
ht_win_arrests_clt = method.random_sample(home_team_wins_arrests, samples_total=150)
ht_win_arrests_clt_var = method.random_sample(home_team_wins_arrests, var=True ,samples_total=150)
#--extract losing home teams and arrests
home_team_losses = team_cut[team_cut['home_score']<team_cut['away_score']]
home_team_losses_arrests = home_team_losses['arrests']
ht_loss_arrests_clt = method.random_sample(home_team_losses_arrests,samples_total=150)
ht_loss_arrests_clt_var = method.random_sample(home_team_losses_arrests, var=True ,samples_total=150)


#--boilerplate display whole frame
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(point_differential)

#-extract total arrests by team
total_arrests_by_teams = team_cut.groupby('home_team')['arrests'].sum().reset_index(name='total_arr')

#-average arrest per game by home team
avg_arrests_per_game = team_cut.groupby('home_team')['arrests'].mean().reset_index(name='mean_arr')

#-arrests by point differential
#-- home lost by less than 12
lose_lt_12_arr = team_cut[team_cut['away_score'] - team_cut['home_score'] < 12]
lose_lt_12_arr = lose_lt_12_arr['arrests']

lose_mt_12_arr = team_cut[team_cut['away_score'] - team_cut['home_score'] > 12]
lose_mt_12_arr = lose_mt_12_arr['arrests']

#--home team won by more than 12
win_mt_12_arr = team_cut[team_cut['home_score'] - team_cut['away_score'] > 12]
win_mt_12_arr = win_mt_12_arr['arrests']

win_lt_12_arr = team_cut[team_cut['home_score']-team_cut['away_score'] <= 12]
win_lt_12_arr = win_lt_12_arr['arrests']

######################################################################################
#**** Extract statistics ****
######################################################################################

#-**** selected statistics ****

#--points rv's
avg_points_scored_above_mean_home = stats.tmean(score_games_morethan_6_home)
var_points_scored_above_mean_home = stats.tvar(score_games_morethan_6_home)

avg_points_scored_below_mean_home = stats.tmean(score_games_lessthan_6_home)
var_points_scored_below_mean_home = stats.tvar(score_games_lessthan_6_home)

ci_above_mean_home = stats.t.interval(0.05, len(score_games_morethan_6_home)-1, loc=avg_points_scored_above_mean_home)

print(f"The average points scored by home teams with more than the mean arrests {avg_points_scored_above_mean_home}\n"
      f"n = {len(score_games_morethan_6_home)}, ci = {ci_above_mean_home}")
print(f"The sample variance of the distribution of home teams with more than the mean arrests is {var_points_scored_above_mean_home}")
print(f"The ci for the var is {method.chi_2(score_games_morethan_6_home)}")

print(f"The average points scored by home teams with less than the mean arrests {avg_points_scored_below_mean_home}\n"
      f"n = {len(score_games_lessthan_6_home)}, ci = {method.t_interval(score_games_lessthan_6_home)}")
print(f"The sample variance of the distribution of home teams with less than the mean arrests is {var_points_scored_below_mean_home}")
print(f"The ci for the var is {method.chi_2(score_games_lessthan_6_home)}")

t_tup_below_above = stats.ttest_ind(score_games_morethan_6_home, score_games_lessthan_6_home)
print(f"T-test, equal variance,upper 50% fan arrests, Lower 50% fan arrests {t_tup_below_above}")

avg_points_scored_above_mean_total = stats.tmean(score_games_morethan_6_total)
var_points_scored_above_mean_total = stats.tvar(score_games_morethan_6_total)
avg_points_scored_below_mean_total = stats.tmean(score_games_lessthan_6_total)
var_points_scored_below_mean_total = stats.tvar(score_games_lessthan_6_total)

print(f"The average points scored at games with more than the mean arrests {avg_points_scored_above_mean_total}\n"
      f"n = {len(score_games_morethan_6_total)}, ci = {method.t_interval(score_games_morethan_6_total)}")
print(f"The sample variance of the distribution of games with more than the mean arrests is {var_points_scored_above_mean_total}")
print(f"The ci for the var is {method.chi_2(score_games_morethan_6_total)}")

print(f"The average points scored at games with less than the mean arrests {avg_points_scored_below_mean_total}\n"
      f"n = {len(score_games_lessthan_6_total)}, ci = {method.t_interval(score_games_lessthan_6_total)}")
print(f"The sample variance of the distribution of games with less than the mean arrests is {var_points_scored_below_mean_total}")
print(f"The ci for the var is {method.chi_2(score_games_lessthan_6_total)}")


#--arrest stats
mean_arrests_ht_win = stats.tmean(ht_win_arrests_clt)
mean_arrests_ht_loss = stats.tmean(ht_loss_arrests_clt)
var_arrests_ht_win = stats.tmean(ht_win_arrests_clt_var)
var_arrests_ht_loss = stats.tmean(ht_loss_arrests_clt_var)

print(f"The average arrests where ht won {mean_arrests_ht_win}, ci {method.t_interval(ht_win_arrests_clt)}")
print(f"var {var_arrests_ht_win}, ci = {method.t_interval(ht_win_arrests_clt_var)}")
print(f"The average arrests where ht lost {mean_arrests_ht_loss}, ci {method.t_interval(ht_loss_arrests_clt)}")
print(f"var {var_arrests_ht_loss}, ci = {method.t_interval(ht_loss_arrests_clt_var)}")


print(f"t-test {stats.ttest_ind(ht_win_arrests_clt,ht_loss_arrests_clt,equal_var=False)}")


#-**** population stats****
print('#'*20)
print("Population Statistics: \n")
avg_total_points_scored = stats.tmean(total_points_cut)
print(f"Average total points scored {avg_total_points_scored}, ci: {method.t_interval(total_points_cut)}, \n "
      f"n = {len(total_points_cut)} var = {stats.tvar(total_points_cut)} ci = {method.chi_2(total_points_cut)}")
avg_point_diff = stats.tmean(point_differential)
print(f"Average point differential {avg_point_diff} ci: {method.t_interval(point_differential)}, n = {len(point_differential)}")

avg_home_team_win_score = stats.tmean(home_team_wins['home_score'])
print(f"Average score of winning teams: {avg_home_team_win_score}, n = {len(home_team_wins['home_score'])}")
avg_home_team_loss_score = stats.tmean(home_team_losses['home_score'])
print(f"Average score of losing teams: {avg_home_team_loss_score}, n = {len(home_team_losses['home_score'])}")

mean_arrests = stats.tmean(arrests_cut)
print(f'The mean arrests per game is {mean_arrests}')

#--central limit thm for the sample means of arrests
clt_arrests = method.random_sample(arrests_cut) #extract the population of sample means
#--extract the variance of the sample means
clt_arrests_var = stats.tvar(clt_arrests)
clt_arrests_mean = stats.tmean(clt_arrests)
print(f'The mean of sample mean arrests per game is {clt_arrests_mean}\n'
      f'Confidence interval {method.t_interval(clt_arrests)}')
print(f'The var of sample mean arrests per game is {clt_arrests_var}, standard deviation is {sqrt(clt_arrests_var)}')

#--central limit thm for the sample variances of arrests.
clt_var_arrests = method.random_sample(arrests_cut, var=True) #extract the dist of sample vars
#---by clt, the mean of the distribution of clt is the population variance
clt_var_arrests_val = stats.tmean(clt_var_arrests)
print(f'The variance in the number of arrests per game is {clt_var_arrests_val}, std is {sqrt(clt_var_arrests_val)}')
ci_v = method.t_interval(clt_var_arrests)
print(f"The confidence interval of the variance by chi squared dist is {ci_v}")

# print("The total arrests by team: ")
# print(total_arrests_by_teams)
# print("The average arrests by team per game:")
# print(avg_arrests_per_game)
# print(f"Data outlook: {team_cut.count()}")



#-plots
axis_size = 17
title_sz = 20
tick_sz = 15
pt_x_size = 10
pt_y_size = 5.6
left_p = .093
bot_p = .126
right_p = .981
top_p = .8
wspace = hspace = .02


pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(arrests_cut,bins = 30,density= True)
pyplot.xlabel('Arrests', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label='Distribution of The Arrests of Fans at NFL Stadiums\n 2011-2015',
             fontsize = title_sz )

pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('ArrestsPerGameDist.png')




# pyplot.hist(winning_home_team_scores, bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Scores of Winning Home Teams\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()
pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(score_games_morethan_6_home, bins=30, density= True)
pyplot.xlabel('Points', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of Home Team Scores:\n Stadiums With More Than The Mean Arrests at The Stadium\n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('mt_avearrest_sc.png')


pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(score_games_lessthan_6_home, bins=30, density= True)
pyplot.xlabel('Points', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of Home Team Scores:\n Stadiums With Less Than The Mean Arrests at The Stadium\n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('lt_avearrest_sc.png')




pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(clt_arrests,bins = 30, density=True)
pyplot.xlabel('Sample Means of Arrests', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of the Sample Means of Arrests, 300 samples, size n = 30 each\n 2011-2015", fontsize= title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('clt_mean_arrests.png')

pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(clt_var_arrests, bins=100, density=True)
pyplot.xlabel('Sample Variances of Arrests', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of the Sample Variances of Arrests \n 300 samples, each sample of n = 30 each \n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p+.039,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('clt_var_arrests.png')


#--Home team wins, dist of arrests

pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(ht_win_arrests_clt, bins=30, density= True)
pyplot.xlabel('Arrests', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of Arrests at Stadiums Where Home Team Won \n CLT of 150 Samples, of n = 30 each\n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('ht_win_arr.png')


pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(ht_loss_arrests_clt, bins=30, density= True)
pyplot.xlabel('Arrests', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of Arrests at Stadiums Where Home Team Lost \n CLT of 150 Samples, of n = 30 each\n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('ht_loss_arr.png')

#
# pyplot.hist(point_differential,bins =  30, density=True)
# pyplot.gca().set(title='Point differentials',xlabel='Points', ylabel='Probability')
# pyplot.text(40.0, .06, "Text")
# pyplot.figure()

# pyplot.hist(lose_lt_12,bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Arrests from games where the home team \nlost by less than the mean point diff',
#                  xlabel='Arrests', ylabel='Probability')

pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
pyplot.hist(score_games_morethan_6_total, bins=30, density= True)
pyplot.xlabel('Total Points', fontsize = axis_size)
pyplot.ylabel('Probability Density' , fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title(label = "Distribution of Total Points Scored, by Games With \n Above Mean Arrests"
                     "\n 2011-2015", fontsize = title_sz)
pyplot.subplots_adjust(    top=top_p,
    bottom=bot_p,
    left=left_p,
    right=right_p,
    hspace=hspace,
    wspace=wspace)
pyplot.savefig('tot_points.png')


pyplot.figure(figsize=(pt_x_size, pt_y_size), dpi=100)
sub = pyplot.barh(total_arrests_by_teams['home_team'],total_arrests_by_teams['total_arr'])
pyplot.bar_label(sub)
pyplot.xlabel("Arrests",fontsize = axis_size)
pyplot.ylabel("Home Team", fontsize = axis_size)
pyplot.tick_params(axis='both', labelsize=tick_sz)
pyplot.title("Arrests of Fans by Home Team Stadium, 2011-2015",fontsize=title_sz)
pyplot.subplots_adjust(
    left= .226,)
pyplot.savefig('ArrestsByHomeTeam.png')


# pyplot.barh(avg_arrests_per_game['home_team'],avg_arrests_per_game['mean_arr'])
# pyplot.xlabel("Avg Arrests (per game)")
# pyplot.ylabel("Home Team")
# pyplot.title("Average Arrests by team, 2011-2015")


#pyplot.show()