# Full Stack Trivia API  Frontend

Project Title

Description of project and motivation
Screenshots (if applicable), with captions
Code Style if you are following particular style guides

## Introduction

This project is a virtual bookshelf for Udacity students. Students are able to add their books to the bookshelf, give them a rating, update the rating and search through their book lists. As a part of the Fullstack Nanodegree, it serves as a practice module for lessons from Course 2: API Development and Documentation. By completing this project, students learn and apply their skills structuring and implementing well formatted API endpoints that leverage knowledge of HTTP and API development best practices.

All backend code follows PEP8 style guidelines.

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Required Tasks

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the ```components``` folder in order to edit the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. 

After you complete your endpoints, ensure you return to and update the frontend to make request and handle responses appropriately: 
- Correct endpoints
- Update response body handling 

## Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the ```stylesheets``` folder. 

## Optional: Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category. 

You can optionally update this game play to increase the number of questions or whatever other game mechanics you decide. Make sure to specify the new mechanics of the game in the README of the repo you submit so the reviewers are aware that the behavior is correct. 

### Error
Errors are returned as JSON objects in the following format:

```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable


#### Endpoints

##### GET /books
* General:
Returns a list of book objects, success value, and total number of books
Results are paginated in groups of 8. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/books

```json
  "books": [
    {
      "author": "Stephen King",
      "id": 1,
      "rating": 5,
      "title": "The Outsider: A Novel"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 5,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 5,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    }
  ],
"success": true,
"total_books": 18
}
```

#### POST /books

* General:
Creates a new question using the submitted title, author and rating. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend.
curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'

```json
{
"questions": [
  {
    "author": "Neil Gaiman",
    "id": 24,
    "rating": 5,
    "title": "Neverwhere"
  }
],
"created": 24,
"success": true,
"total_questions": 17
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
    "author": "Gina Apostol",
    "id": 9,
    "rating": 5,
    "title": "Insurrecto: A Novel"
  },
  {
    "author": "Tayari Jones",
    "id": 10,
    "rating": 5,
    "title": "An American Marriage"
  },
  {
    "author": "Jordan B. Peterson",
    "id": 11,
    "rating": 5,
    "title": "12 Rules for Life: An Antidote to Chaos"
  },
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

#### PATCH /questions/{question_id}
* General:
If provided, updates the rating of the specified question. Returns the success value and id of the modified question.
```commandline
curl http://127.0.0.1:5000/questions/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}
```
```json
 { "id": 15, "success": true }
```
