# Setting things up

Clone the sources:
```
git clone git@github.com:bratan05/loadimpact.git
```

Create a new virtual environment (I suggest using the pipenv tool and assume you have python 3 by default):
```
cd loadimpact
pipenv shell
```
This will create and activate a new virtual environment for you. You can activate it later using the same command.

Install the requirements:
```
pipenv install

# Running the server

cd devops_server
python manage.py runserver
```
This will start a server for you

# Doing API calls
In order to test the program, do a POST request to the server:
```
POST localhost:8000/api/devops
```
with the following sample body:
```
{
"DM_capacity": 12,
"DE_capacity": 7,
"data_centers": [
	{"name": "Paris", "servers": 11 },
	{"name": "Stockholm", "servers": 21 }
	]
}
```
In return you will recieve a JSON of the following form:
```
{
    "DE": 3,
    "DM_data_center": "Paris"
}
```

# Building service using docker-compose
To spin up a docker container with running server issue the following command:
```
docker-compose up -d
```
Looking at 
```
docker ps
```
should show that container is running and accepting connections on port 8000.

