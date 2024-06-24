
from your_project.app.scheduler import scheduler
from your_project.app import create_app

app = create_app()

if __name__ == '__main__':
    
    scheduler.start()  
    app.run(debug=True)



    