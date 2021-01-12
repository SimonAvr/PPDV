## Setting up backend
								* pip install mysql
								* ./initdb.sh #will ask for root password for mysql root user
								* export FLASK_APP=be_app.py
								* python -m flask run
								* python init_patient.py # Filling patient table in db
								* Now endpoints from be_app.py should be avaible
								* recorder.py will run in background to fetch data from server. I will thing how it would be turn on, and off. (Sockets? Http? From fron somehow?)
