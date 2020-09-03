# Full Stack Trivia API Backend

Gettting Started:

Prequisites:


Our tech stack will include:

    SQLAlchemy ORM to be our ORM library of choice
    PostgreSQL as our database of choice
    Python3 and Flask as our server language and server framework
    Flask-Migrate for creating and running schema migrations
    Node, HTML, CSS, and Javascript with Bootstrap 3 for our website's frontend



Development Setup

Assumption is you have already installed Python (e.g.: version 3.6 and later), NPM, PostgreSQL

Backend :

    Initialize and activate a virtualenv:

$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env
(no-site-packages does not work)

$ source env/bin/activate

    Install the dependencies:

$ pip3 install -r requirements.txt

    Run the development server:

$ export FLASK_APP=flaskr
$ export FLASK_ENV=development # enables debug mode
$ flask run

flask run command should be run in the backend directory where flaskr dir is present. It runs the file __init__.py. Working in the development mode with interactive debugger, restarts server when changes are made.

By default the application runs on http://127.0.0.1:5000/ and is a proxy in the frontend configuration.

The user also needs to export the following environment variables (substituting datanase username and password as apporpriate) to ensure database access.
export TRIVIA_DB_USER="postgres"
export TRIVIA_DB_PASSWORD="postgres"



For front end:
#1 Install npm (better to install nvm)

From the frontend folder, run the following commands to start the client:
1. For the first time run the "npm install" command in the frontend folder (containing the package.json file) - this will install the node_modules directory which will contain the required dependencies.

2. Run npm start (only this step is required to be done for all runs including the first)
By default, the frontend will run on localhost:3000.



Tests
In order to run tests navigate to the backend folder and run the following commands:


```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.



Installation: 
Main Files: Project Structure - backend

Execute "flask run" in backend directory to run after installing dependences

├── README.md
├── flaskr
│   ├── __init__.py ** the main driver of the app. 
├── models.py - Database - setup and models              
├── startup.sh - Sets up environment variables required for access to database and debugging 
├── test_flaskr.py - Tests all application API points for success and failures
├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
├── trivia.psql Schema and data for sample database. Refer above on how to use it.


Overall:

    Models are located in the models.py
    Controllers are also located in flaskr/__init__.py 
    The web frontend is located in frontend folder. For details refer section "For front end"

    

Endpoints:

1. GET /categories
 - Gets all the categories.
 Sample response:
 curl -X GET http://localhost:3000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}


Erros:

None

2. GET /questions
- Gets 10 questions (has an option to specify page)
GET /questions?page=2

JSON Response:
{
            'success': True,
            'questions': 
            'totalQuestions': 
            'categories': 
            'currentCategory': 
})

Sample request:

curl -X GET http://localhost:3000/questions
Sample response:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": 5, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "totalQuestions": 10
}


Errors:

Returned when resource not found. 
e.g. : Trying to find questions which don't exisit
curl -X GET http://localhost:3000/questions?page=3
Returns the following JSON response as no data is available for page 3
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}


3. DELETE /questions/<int:question_id>

JSON Request and Response Sample :

curl http://127.0.0.1:5000/questions/13 -X DELETE
{
  "success": true
}

Error: When the question with specified ID does not exist.

curl http://127.0.0.1:5000/questions/13 -X DELETE
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}


4. POST /questions

Two tasks can be performed:

#1. Adding new qustions

For Add a question, parameters in the JSON request are as below:

{
         question: 
         answer: 
         difficulty: 
         category: 
}
Sample request and response:

curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What color is space?","answer": "Good question","difficulty": 5, "category": 5}'

{
  "success": true
}
Errors:
Like a wrong endpoint:
curl http://127.0.0.1:5000/questions/2000 -X POST -H "Content-Type: application/json" -d '{"question":"What color is space?","answer": "Good question","difficulty": 5, "category": 5}'
{
  "error": 405, 
  "message": "method not allowed", 
  "success": false
}
Attempting to add a question with zero length will return 400 (see Generic Error section in this documentation)
Generic error, due to other reasons 422:
{
    "success": False,
    "error": 422,
    "message":"unprocessable"
  }



#2 Searching a based on text (case insensitve) in the question text attribute (doesn't look in answer or category).
Sample JSON request and response: 

Search Success Sample request and response:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"space"}'
{
  "currentCategory": 5, 
  "questions": [
    {
      "answer": "Good question", 
      "category": 5, 
      "difficulty": 5, 
      "id": 29, 
      "question": "What color is space?"
    }
  ], 
  "success": true, 
  "totalQuestions": 1
}
Search failure Sample request and response:

 curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"colors"}'
{
  "currentCategory": 5, 
  "questions": [], 
  "success": true, 
  "totalQuestions": 0
}

5. GET /categories/6/questions

Gets questions for a specific category only. Sample JSON request and response (format is similar to GET for question):

curl -X GET http://localhost:3000/categories/6/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": 5, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}

Returns 404 if no question in requested category.


6. POST /quizzes

Plays 5 different questions of the selected category as a quiz. Returns only one question at time. Previous questions is a list of ID's of those questions being played in this attempt of the quiz. 
Sample request and response:

curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Sports","id":"6"}}'
{
  "question": {
    "answer": "Brazil", 
    "category": 6, 
    "difficulty": 3, 
    "id": 10, 
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  }, 
  "success": true
}

Returns null if there are no more questions of the selected category:

curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[10,11],"quiz_category":{"type":"Sports","id":"6"}}'
{
  "question": null, 
  "success": true
}

Category ID is specified as 0 in request if questions can be chosen across any of the categories ("ALL" option in GUI)

Returns 400 status if "previous_questions" key not present in JSON data.


--End of endpoints doc--


Generic Error Responses for all requests:
{
      "success": False,
      "error": 404,
      "message":"resource not found"
}

  {
    "success": False,
    "error": 422,
    "message":"unprocessable"
  }

  {
    "success": False,
    "error": 400,
    "message":"bad request"
  }

  {
    "success": False,
    "error": 405,
    "message":"method not allowed"
  }
