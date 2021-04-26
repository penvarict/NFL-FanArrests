from scipy import stats
from matplotlib import pyplot
import pandas as pd
import pprint

frame = pd.read_csv('arrests.csv')
team_names = frame['home_team']
print(frame)
# Cut out team that reported unreliable data, no data collected there. Not in the data file are also Buffalo and St. Louis
team_cut = frame[~frame['home_team'].isin(['Detroit', 'Minnesota', 'Miami','Oakland','Atlanta','Cleveland','New Orleans'])]
# cut the arrests column
arrests_cut = team_cut['arrests']
home_score_cut = team_cut['home_score']
away_score_cut = team_cut['away_score']
#-extract home team score of games with more than mean arrests
score_games_morethan_6_arr_home = team_cut[team_cut['arrests'] > 6.56]
score_games_morethan_6_arr_home = score_games_morethan_6_arr_home['home_score']

#-extract away team score of games with more than mean arrests
score_games_morethan_6_arr_away = team_cut[team_cut['arrests'] > 6.56]
score_games_morethan_6_arr_away = score_games_morethan_6_arr_away['away_score']

#-extract home team score of games with less than mean arrests
score_games_lessthan_6_arr_home = team_cut[team_cut['arrests'] < 6.56]
score_games_lessthan_6_arr_home = score_games_lessthan_6_arr_home['home_score']

#-extract away team score of games with more than mean arrests
score_games_lessthan_6_arr_away = team_cut[team_cut['arrests'] > 6.56]
score_games_lessthan_6_arr_away = score_games_lessthan_6_arr_away['away_score']

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

#-extract total arrests by team
total_arrests_by_teams = team_cut.groupby('home_team')['arrests'].sum().reset_index(name='total_arr')

#-average arrest per game by home team
avg_arrests_per_game = team_cut.groupby('home_team')['arrests'].mean().reset_index(name='mean_arr')

#**** Extract statistics ****

avg_points_scored_above_mean_home = stats.tmean(score_games_morethan_6_arr_home)
var_points_scored_above_mean_home = stats.tvar(score_games_morethan_6_arr_home)
print(f"The average points scored by home teams with more than the mean arrests {avg_points_scored_above_mean_home}")
print(f"The sample variance of the distribution of home teams with more than the mean arrests is {var_points_scored_above_mean_home}")

avg_points_scored_below_mean_arrests_home = stats.tmean(score_games_lessthan_6_arr_home)
var_points_scored_below_mean_home = stats.tvar(score_games_lessthan_6_arr_home)
print(f"The average points scored by home teams with less than the mean arrests {avg_points_scored_below_mean_arrests_home}")
print(f"The sample variance of the distribution of home teams with less than the mean arrests is {var_points_scored_below_mean_home}")

t_tup_below_above = stats.ttest_ind(score_games_morethan_6_arr_home,score_games_lessthan_6_arr_home)
print(f"T-test, equal variance {t_tup_below_above}")
#-population stats
mean_arrests = stats.tmean(arrests_cut)
print(f'The mean arrests per game is {mean_arrests}')
print("The total arrests by team: ")
print(total_arrests_by_teams)
print("The average arrests by team per game:")
print(avg_arrests_per_game)
print(f"Data outlook: {team_cut.count()}")





#-plots
pyplot.hist(arrests_cut,bins = 60,density= True)
pyplot.gca().set(title='Distribution of The Arrests of Fans at NFL Stadiums\n 2011-2015',xlabel='Arrests' ,ylabel='Probability')
pyplot.figure()


pyplot.hist(winning_home_team_scores, bins = 30, density=True)
pyplot.gca().set(title='Distribution of Scores of Winning Home Teams\n 2011-2015',xlabel='Points' ,ylabel='Probability')
pyplot.figure()

pyplot.hist(score_games_morethan_6_arr_home, bins=30, density= True)
pyplot.gca().set(title='Distribution of Home Team Scores, at Stadiums With Greater Than The Mean Arrests at The Stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
pyplot.figure()

pyplot.hist(score_games_lessthan_6_arr_home, bins=30, density= True)
pyplot.gca().set(title='Distribution of Home Team Scores, at Stadiums With Less Than The Mean Arrests at The Stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
pyplot.figure()

# pyplot.hist(score_games_morethan_6_arr_away, bins=30, density= True)
# pyplot.gca().set(title='Distribution of Away Team Scores, with greater than the mean arrests at the stadium\n 2011-2015',xlabel='Points' ,ylabel='Probability')
# pyplot.figure()

sub = pyplot.barh(total_arrests_by_teams['home_team'],total_arrests_by_teams['total_arr'])
pyplot.bar_label(sub)
pyplot.xlabel("Arrests")
pyplot.ylabel("Home Team")
pyplot.title("Arrests by Team, 2011-2015")
pyplot.figure()

# pyplot.barh(avg_arrests_per_game['home_team'],avg_arrests_per_game['mean_arr'])
# pyplot.xlabel("Avg Arrests (per game)")
# pyplot.ylabel("Home Team")
# pyplot.title("Average Arrests by team, 2011-2015")


#pyplot.show()