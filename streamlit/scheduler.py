from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()

@scheduler.scheduled_job('interval', minutes=30)  
def check_for_patent_updates():
    patents = Patent.query.all()
    for patent in patents:
        if patent.details_have_changed():  
            patent.update_details() 