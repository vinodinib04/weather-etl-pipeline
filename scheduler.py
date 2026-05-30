import schedule
import time
from pipeline import run_pipeline

# Run immediately once on start
run_pipeline()

# Then schedule to run every hour
schedule.every(1).hours.do(run_pipeline)

print("Scheduler running — pipeline will execute every hour. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)