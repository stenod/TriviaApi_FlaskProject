import os
import unittest
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.testing import db

from backend.flaskr import create_app
from backend.models import Question, Category, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass

        # clean up logic for the test suite declared in the test module

    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'category': '1',
            'question': 'Neil Gaiman',
            'answer': 'aaaaaaa',
            'difficulty': 5
        }
        self.new_category = {
            'id': '1',
            'type': 'test_type',
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            self.db.init_app(self.app)
            self.db.create_all()


            # # create all tables

            # create all tables
            self.question = Question(difficulty=self.new_question['difficulty'],
                                     question=self.new_question['question'],
                                     answer=self.new_question['answer'], category=self.new_question['category'])
            self.question.insert()

            if Category.query.first() is None:
                category = Category(type=self.new_category['type'])
                category.insert()

    def tearDown(self):
        """Executed after reach test"""
        if self.question is not None:
            self.question.delete()
        self.db.drop_all()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """Test _____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 1)

    def test_get_categories_wrong_method(self):
        """Test _____________ """
        res = self.client().post('/categories')
        self.assertEqual(res.status_code, 405)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_question(self):
        question = self.db.session.query(Question).order_by('answer').first()
        question_id = question.id
        res = self.client().delete('/questions/' + str(question.id))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)


    def test_search_question_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'Neil'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 1)
        self.assertTrue(data['questions'])

    def test_search_question_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'hey'})
        data = json.loads(res.data)

        question = Question.query.filter(
            self.db.func.lower(Question.question).contains(self.db.func.lower('hey'))).first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(question, None)

    def test_get_question_by_category_with_results(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        category = Category.query.first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['currentCategory'], Category.format(category))

    def test_get_question_by_category_without_results(self):
        res = self.client().get('/categories/2/questions')
        self.assertEqual(res.status_code, 404)

    def test_get_quizzes_with_results(self):
        category = Category.query.first()
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [], 'quiz_category': Category.format(category)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['previous_questions']), 1)

    def test_get_quizzes_with_wrong_category(self):
        category = Category.query.first()
        category.id = 5
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [], 'quiz_category': Category.format(category)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
