# Full Stack Trivia API Backend

It is a Webapplication which let you play answering random trivia questions. You are also able to create new questions, search for questions and delete questions. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

##Endpoints

##### GET /categories
* General:
Returns all categories from the database
Sample: curl http://127.0.0.1:5000/categories

```json
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
```

#### GET /questions

* General:
Returns all questions from the database
curl http://127.0.0.1:5000/questions?page=1 -X

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": "6", 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": "6", 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 10
}

```

#### DELETE /questions/{question_id}
* General:
Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.
```commandline
curl -X DELETE http://127.0.0.1:5000/questions/16?page=2
```

```json
{
"questions": [
  {
    "author": "Kiese Laymon",
    "id": 12,
    "rating": 1,
    "title": "Heavy: An American Memoir"
  },
  {
    "author": "Emily Giffin",
    "id": 13,
    "rating": 4,
    "title": "All We Ever Wanted"
  },
  {
    "author": "Jose Andres",
    "id": 14,
    "rating": 4,
    "title": "We Fed an Island"
  },
  {
    "author": "Rachel Kushner",
    "id": 15,
    "rating": 1,
    "title": "The Mars Room"
  }
],
"deleted": 16,
"success": true,
"total_questions": 15
}
```

#### POST /questions
* General:
Creates a new question in the database

Request:
```commandline
curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":  "What?","answer":  "Yes","difficulty":  5,"category":  "3"}'
```
Response:
```json
{
  "id": 102,
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "ein Schwein",
      "category": "2",
      "difficulty": 3,
      "id": 24,
      "question": "Was bist du"
    },
    {
      "answer": "Yes",
      "category": "3",
      "difficulty": 5,
      "id": 101,
      "question": "What?"
    },
    {
      "answer": "Yes",
      "category": "3",
      "difficulty": 5,
      "id": 102,
      "question": "What?"
    }
  ],
  "search": null,
  "success": true,
  "total_questions": 16
}
```

#### GET /categories/{categie_id}/questions
* General:
Gets all questions for a given category

Request:
```commandline
curl http://127.0.0.1:5000/categories/1/questions
```
Response:
```json
{
"currentCategory": {
"id": 1,
"type": "Science"
},
"questions": [
{
"answer": "The Liver",
"category": "1",
"difficulty": 4,
"id": 20,
"question": "What is the heaviest organ in the human body?"
},
{
"answer": "Alexander Fleming",
"category": "1",
"difficulty": 3,
"id": 21,
"question": "Who discovered penicillin?"
},
{
"answer": "Blood",
"category": "1",
"difficulty": 4,
"id": 22,
"question": "Hematology is a branch of medicine involving the study of what?"
}
],
"success": true,
"total_questions": 3
}
```


#### POST /quizzes
* General:
Gets a random question for one category
Request:
```commandline
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [],"answer":  "Yes","quiz_category": {"id": "1","type": "Science"}}'
```
Response:
```json
{
  "previous_questions": [
    20
  ],
  "question": {
    "answer": "The Liver",
    "category": "1",
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
