# Import all necessary moduls:
# 1) from Celery package.
from app.celery import app

# 2) Local import.
from .admin_side_support import (
    looking_for_scores_of_matches_in_round,
    func_calculate_points_by_user_forecasts
)
from .celery_tasks_support import (
    logic_to_start_score_checking,
    done_forecasts_check
)


# Manualy activation of points calculation.
@app.task()
def points_calculation_manual():
    func_calculate_points_by_user_forecasts()


# Manualy activation of points calculation.
@app.task()
def looking_for_scores_manual():
    looking_for_scores_of_matches_in_round()


# Period tasks which running on background.
@app.task()
def task_every_day_check_match_score():
    logic_to_start_score_checking()


@app.task()
def task_every_hour_done_forecasts_check():
    done_forecasts_check()
