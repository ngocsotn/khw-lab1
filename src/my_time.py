# import time
from datetime import datetime

def get_current_time():
    current_time = datetime.now()
    return str(current_time.strftime("%d-%m-%Y_%H.%M.%S"))