from app.celery import app
from .admin_side_support import (
    print_time,
    looking_for_scores_of_matches_in_round,
    every_hour_done_forecasts_check
)


# Main logic of processing data ('category' from user).
@app.task()  # queue="get_matches_scores")
def processing_logic():
    print_time()


#
@app.task()
def task_every_minute_printing():
    print_time()
    # looking_for_scores_of_matches_in_round()


#
@app.task
def task_every_hour_done_forecasts_check():
    every_hour_done_forecasts_check()
    pass
