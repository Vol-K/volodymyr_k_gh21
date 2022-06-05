from app.celery import app
from .admin_side_support import print_time
from datetime import datetime


# Main logic of processing data ('category' from user).
@app.task()  # queue="get_matches_scores")
def processing_logic():
    print_time()
    # pass


@app.task()
def every_minute_printing():
    print_time()
    # xxx = datetime.now().replace(microsecond=0)
    # print("CELERY func 'print_every_minute' results", xxx)
