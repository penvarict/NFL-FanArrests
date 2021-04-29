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

#-extract games in the upper 15.9%
score_games_morethan_1std_home = team_cut[team_cut['arrests'] > 15.67]
score_games_morethan_1std_home = score_games_morethan_1std_home['home_score']

#-extract games in the lower 15.9%
score_games_lessthan_1std_home = team_cut[team_cut['arrests'] < 15.67]
score_games_lessthan_1std_home = score_games_lessthan_1std_home['home_score']

#-extract total points scored
#team_cut['total_points'] = team_cut['home_score'] + team_cut['away_score']

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
home_team_wins = home_team_wins['arrests']

#--extract losing home teams and arrests
home_team_losses = team_cut[team_cut['home_score']<team_cut['away_score']]
home_team_losses = home_team_losses['arrests']


#--boilerplate display whole frame
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(point_differential)

#-extract total arrests by team
total_arrests_by_teams = team_cut.groupby('home_team')['arrests'].sum().reset_index(name='total_arr')

#-average arrest per game by home team
avg_arrests_per_game = team_cut.groupby('home_team')['arrests'].mean().reset_index(name='mean_arr')

#-arrests by point differential
lose_lt_12 = team_cut[team_cut['away_score']-team_cut['home_score'] < 12]
lose_lt_12 = lose_lt_12['arrests']

lose_mt_12 = team_cut[team_cut['away_score']-team_cut['home_score'] > 12]
lose_mt_12 = lose_mt_12['arrests']

win_mt_12 = team_cut[team_cut['home_score']-team_cut['away_score'] > 12]
win_mt_12 = win_mt_12['arrests']

win_lt_12 = team_cut[team_cut['home_score']-team_cut['away_score'] < 12]
win_lt_12 = win_lt_12['arrests']

######################################################################################
#**** Extract statistics ****
######################################################################################

#-**** selected statistics ****
avg_points_scored_above_mean_home = stats.tmean(score_games_morethan_6_home)
var_points_scored_above_mean_home = stats.tvar(score_games_morethan_6_home)
ci_above_mean_home = stats.t.interval(0.95, len(score_games_morethan_6_home)-1, loc=avg_points_scored_above_mean_home)

print(f"The average points scored by home teams with more than the mean arrests {avg_points_scored_above_mean_home}\n"
      f"n = {len(score_games_morethan_6_home)}, ci = {ci_above_mean_home}")
print(f"The sample variance of the distribution of home teams with more than the mean arrests is {var_points_scored_above_mean_home}")

avg_points_scored_below_mean_arrests_home = stats.tmean(score_games_lessthan_6_home)
var_points_scored_below_mean_home = stats.tvar(score_games_lessthan_6_home)
print(f"The average points scored by home teams with less than the mean arrests {avg_points_scored_below_mean_arrests_home}")
print(f"The sample variance of the distribution of home team points with less than the mean arrests is {var_points_scored_below_mean_home}")

avg_point_diff = stats.tmean(point_differential)
print(f"Average point differential {avg_point_diff}")


score_games_morethan_1std_arr_home_mean = stats.tmean(score_games_morethan_1std_home)
score_games_morethan_1std_arr_home_var = stats.tvar(score_games_morethan_1std_home)
print(f"The average points scored by games that are in the upper 15.9% of fan arrests {score_games_morethan_1std_arr_home_mean}\n"
      f"n = {len(score_games_morethan_1std_home)}")
print(f"The variance of the distribution of games in the 15.9 % of fan arrests {score_games_morethan_1std_arr_home_var}")

score_games_lessthan_1std_home_mean = stats.tmean(score_games_lessthan_1std_home)
score_games_lessthan_1std_home_var = stats.tvar(score_games_lessthan_1std_home)
print(f"The average points scored by home teams who are in the lower 15.9% of fan arrests {score_games_lessthan_1std_home_mean}\n"
      f"n = {len(score_games_lessthan_1std_home)}")
print(f"The variance of the distribution of home teams fan arrests who are in the lower 15.9 % of fan arrests {score_games_lessthan_1std_home_var}")


t_tup_below_above = stats.ttest_ind(score_games_morethan_6_home, score_games_lessthan_6_home)
print(f"T-test, equal variance,upper 50% fan arrests, Lower 50% fan arrests {t_tup_below_above}")

t_tup_below_above_1std = stats.ttest_ind(score_games_lessthan_1std_home,score_games_morethan_1std_home)
print(f"T-test, equal variance,upper 15.9% fan arrests, Lower 15.9% fan arrests {t_tup_below_above}")

#-**** population stats****
mean_arrests = stats.tmean(arrests_cut)
print(f'The mean arrests per game is {mean_arrests}')

#--central limit thm for the sample means of arrests
clt_arrests = method.random_sample(arrests_cut) #extract the population of sample means
#--extract the variance of the sample means
clt_arrests_var = stats.tvar(clt_arrests)
print(f'The var of sample mean arrests per game is {clt_arrests_var}, standard deviation is {sqrt(clt_arrests_var)}')

#--central limit thm for the sample variances of arrests.
clt_var_arrests = method.random_sample(arrests_cut, var=True) #extract the dist of sample vars
#---by clt, the mean of the distribution of clt is the population variance
clt_var_arrests_val = stats.tmean(clt_var_arrests)
print(f'The variance in the number of arrests per game is {clt_var_arrests_val}, std is {sqrt(clt_var_arrests_val)}')
ci_v = stats.t.interval(0.95, len(clt_var_arrests) - 1, loc=clt_var_arrests_val)
print(f"The confidence interval of the variance by chi squared dist is {ci_v}")

# print("The total arrests by team: ")
# print(total_arrests_by_teams)
# print("The average arrests by team per game:")
# print(avg_arrests_per_game)
# print(f"Data outlook: {team_cut.count()}")



#-plots
pyplot.hist(arrests_cut,bins = 30,density= True)
pyplot.gca().set(title='Distribution of The Arrests of Fans at NFL Stadiums\n 2011-2015',xlabel='Arrests' ,ylabel='Probability Density')
pyplot.figure()

# pyplot.hist(winning_home_team_scores, bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Scores of Winning Home Teams\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()
#
# pyplot.hist(score_games_morethan_6_home, bins=30, density= True)
# pyplot.gca().set(title='Distribution of Home Team Scores, at Stadiums With Greater Than The Mean Arrests at The Stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()

# pyplot.hist(score_games_lessthan_6_home, bins=30, density= True)
# pyplot.gca().set(title='Distribution of Home Team Scores, at Stadiums With Less Than The Mean Arrests at The Stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()

# pyplot.hist(home_team_wins,bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Arrests, at Stadiums Where Home Team Won\n 2011-2015',xlabel='Arrests' ,ylabel='Probability')
# pyplot.figure()
# pyplot.hist(home_team_losses,bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Arrests, at Stadiums Where Home Team Lost\n 2011-2015',xlabel='Arrests' ,ylabel='Probability')
# pyplot.figure()
# pyplot.hist(home_team_losses,bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Arrests, at Stadiums Where Home Team Lost\n 2011-2015',xlabel='Arrests' ,ylabel='Probability')
# pyplot.figure()
#
pyplot.hist(clt_arrests,bins = 30, density=True)
pyplot.gca().set(title='Distribution of the Sample Means of Arrests, 300 samples, size n = 30 each\n 2011-2015',xlabel='Sample Mean Arrests' ,ylabel='Probability Density')
pyplot.figure()

pyplot.hist(clt_var_arrests, bins=100, density=True)
pyplot.gca().set(title='Distribution of the Sample Variances of Arrests, 300 samples, each sample of n = 30 each \n 2011-2015',xlabel='Sample Variances of Arrests' ,ylabel='Probability Density')
pyplot.figure()

#
#
# pyplot.hist(point_differential,bins =  30, density=True)
# pyplot.gca().set(title='Point differentials',xlabel='Points', ylabel='Probability')
# pyplot.text(40.0, .06, "Text")
# pyplot.figure()

# pyplot.hist(lose_lt_12,bins = 30, density=True)
# pyplot.gca().set(title='Distribution of Arrests from games where the home team \nlost by less than the mean point diff',
#                  xlabel='Arrests', ylabel='Probability')
# pyplot.figure()
# pyplot.hist(score_games_morethan_6_arr_away, bins=30, density= True)
# pyplot.gca().set(title='Distribution of Away Team Scores, with greater than the mean arrests at the stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()

sub = pyplot.barh(total_arrests_by_teams['home_team'],total_arrests_by_teams['total_arr'])
pyplot.bar_label(sub)
pyplot.xlabel("Arrests")
pyplot.ylabel("Home Team")
pyplot.title("Arrests of Fans by Home Team Stadium, 2011-2015")
pyplot.figure()

# pyplot.barh(avg_arrests_per_game['home_team'],avg_arrests_per_game['mean_arr'])
# pyplot.xlabel("Avg Arrests (per game)")
# pyplot.ylabel("Home Team")
# pyplot.title("Average Arrests by team, 2011-2015")


pyplot.show()