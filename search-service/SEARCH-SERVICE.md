### Search-Service

This directory contains the search service application. 
After starting the application, the API can be found at http://localhost:8080

Relevant file and directory information:

| file/dir    | Description |
| ----------- | ----------- | 
| `app/`     | Contains the Flask application  |  
| `tests/`     | Contains tests for the Flask application  |  
| `config.py`     | Contains configurations for the application  |  
| `entrypoint.sh`     | The shell script that container uses to start the application  |  
| `requirements.txt`     | The packages and versions the application uses  |  


### API specs:

Request:

| Method      | Route | Description |
| ----------- | ----------- | ----------- |
| GET     |  `/videogames/search?term=<something>`      | Searches for the given term in the Giantbomb "Game" database. |  

Response:

| Field    | Data Type | Description |
| ----------- | ----------- | ----------- |
| aliases     | List of strings | All "aliases" for the game.  |  
| name     | List of strings | Every videogame title for the game.  |  
| number_of_platforms |  Integer   | Total number of platforms the game can be found or played on. |  
