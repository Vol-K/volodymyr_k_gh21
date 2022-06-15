from app.celery import app
from .admin_side_support import print_time, looking_for_scores_of_matches_in_round


# Main logic of processing data ('category' from user).
@app.task()  # queue="get_matches_scores")
def processing_logic():
    print_time()


#
@app.task()
def every_minute_printing():
    print_time()
