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
```
pip install django ortools
pip install pip==18.0
```
