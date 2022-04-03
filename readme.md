# FastAPI and NDB Python 3 Protype App

# DEV Setup
- Create a python 3 virtual environment
```
python3 -m venv .venv
```
- Activate you python 3 virtual environment
```
source .venv/bin/active
```
- install python dependencies
```
pip install -r requirements.txt
```
- Create a service account that has access to Google Cloud Datastore
- Download the service account and save in the root folder
- create a .env file in the root folder and set the service_account_path to the name of your json file
```
GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
DATASTORE_EMULATOR_HOST=localhost:8420
```
- Start the Datastore emulator using the following command.
```
gcloud beta emulators datastore start --data-dir=data --host-port=localhost:8420
```
- If you don't want to use the datastore emulator comment out the DATASTORE_EMULATOR_HOST environment variable in the .env file
```
GOOGLE_APPLICATION_CREDENTIALS="service_account.json"
#DATASTORE_EMULATOR_HOST=localhost:8420
```
- Run the Application and go to http://localhost:8000
- GET - http://localhost:8000/movies to get all movies
- POST - http://localhost:8000/movies to save a new movie