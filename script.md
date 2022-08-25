python3 -c "from results import *; get_data('results', 359, 'arsenal')"
python3 -c "from results import *; get_data()"

python3 results.py "$split4" "$split3" "{query}"

{('  ||  ' +get_win_status(club_id, project['team_home_id'], project['team_away_id'], project['score'])) if project['time'] != 'v' else ''}