from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from your_project.app.models.patent import Patent
from your_project.test import scrape_patent_data, store_patent_in_db, get_pat_data
import logging
from your_project.app.extensions import db
from your_project.app import create_app


app = create_app()

scheduler = BackgroundScheduler()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('flask_app.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_patent_details():
    with app.app_context():
        try:
            patents = Patent.query.all()

            for patent in patents:
                patnum = patent.patnum
                patent_data = get_pat_data(patnum)

                if (patent_data.get('title') != patent.title or
                    patent_data.get('inventor_name') != patent.inventor_name or
                    patent_data.get('application_number') != patent.application_number or
                    patent_data.get('grant_date') != patent.grant_date):

                    patent.title = patent_data.get('title')
                    patent.application_number = patent_data.get('application_number')
                    

                    db.session.commit()
                    logger.info(f"Updated patent {patnum} in the database")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating patents: {str(e)}")

if not scheduler.running:
    scheduler.add_job(
        update_patent_details,
        'interval',
        minutes=1,
        id='update_patent_details_job',
        replace_existing=True
    )
    logger.info("Scheduler started successfully")
else:
    logger.warning("Scheduler is already running")















# def start_scheduler():
#     global scheduler
#     if not scheduler.running:
#         scheduler.add_job(
#             update_patent_details,
#             'interval',
#             weeks=1,
#             id='update_patent_details_job',
#             replace_existing=True
#         )
#         scheduler.start()
#         logger.info("Scheduler started successfully")
#     else:
#         logger.warning("Scheduler is already running")

# def stop_scheduler():
#     global scheduler
#     if scheduler.running:
#         scheduler.shutdown()
#         logger.info("Scheduler stopped successfully")
#     else:
#         logger.warning("Scheduler is not running")




# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def update_patent_details():
#     with current_app.app_context():
#         try:
#             patents = Patent.query.all()

#             for patent in patents:
#                 patnum = patent.patnum
#                 patent_data = get_pat_data(patnum)

#                 if (patent_data.get('title') != patent.title or
#                     patent_data.get('inventor_name') != patent.inventor_name or
#                     patent_data.get('application_number') != patent.application_number or
#                     patent_data.get('grant_date') != patent.grant_date):

#                     patent.title = patent_data.get('title')
#                     patent.application_number = patent_data.get('application_number')

#                     db.session.commit()
#                     logger.info(f"Updated patent {patnum} in the database")

#         except Exception as e:
#             db.session.rollback()
#             logger.error(f"Error updating patents: {str(e)}")

# # Add job to scheduler only if it's not already added
