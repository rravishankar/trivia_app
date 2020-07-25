import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)        
        setup_db(self.app, self.database_path)
        self.new_que = {
            'question':'What color is space?',
            'answer': 'Good question',
            'difficulty': 5,
            'category': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_sent_request_beyond_validate_page(self):
        resp = self.client().get('/questions?page=100', json={'rating':1})
        data = json.loads(resp.data)
        print("test_404_sent_request_beyond_validate_page:Got data", data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_que(self):
        que_id = 4
        resp = self.client().delete('/questions/' + str(que_id))
        data = json.loads(resp.data)

        book = Question.query.filter(Question.id == que_id).one_or_none()
        # {
        # 'success': True,        
        # 'deleted': book_id,
        # 'books': current_books,
        # 'total_books': len(selection)
        # }
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_que_does_not_exist(self):
        resp = self.client().delete('/questions/1000')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question(self):
        
        resp = self.client().post('/questions', json=self.new_que)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_que_creation_not_allowed(self):
        resp = self.client().post('/questions/45', json=self.new_que)
        data = json.loads(resp.data)
        # {
        #     "success": False,
        #     "error": 405,
        #     "message":" method not allowed"
        # }
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_question_success(self):
        resp = self.client().post('/questions', json={'searchTerm': 'Hall'})
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_search_book_failure(self):
        resp = self.client().post('/books', json={'searchTerm': 'Bizzaree'})
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_category_question_success(self):
        resp = self.client().get('/categories/2/questions')
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_get_category_question_failure(self):
        resp = self.client().get('/categories/20/questions')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()