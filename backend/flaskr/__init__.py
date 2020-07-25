import os, sys, traceback
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, json


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#TBD: Change it to None later and see
currentCategory = 5

def paginate_questions(request, selection):
  page = request.args.get('page',1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
      categories = Category.query.order_by(Category.type).all()
      print("get_categories:\n\nGot categories", categories)
      # categories_json_ready = [category.format() for category in categories]
      categories_json_ready = {category.id: category.type for category in categories}
      my_json = {
            'success': True,
            'categories': categories_json_ready,
      }
      print("get_categories:Returning JSON", my_json)
      return jsonify({
            'success': True,
            'categories': categories_json_ready,
        })


# This is a great way This is a great way This is a great way This is a great
# way This is a great way This is a great way This is a great way This is a
# great way This is a great way This is a great way This is a great way This is
# a great way This is a great way This is a great way 
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
# questions: result.questions,
#           totalQuestions: result.total_questions,
#           categories: result.categories,
#           currentCategory: result.current_category 

  @app.route('/questions')
  def get_all_questions():
      
      questions = Question.query.order_by(Question.id).all()
      # if len(books) == 0:
      #     abort(400)
      formatted_ques = paginate_questions(request, questions)

      if len(formatted_ques) == 0:
        abort(404)
      print("Got questions", formatted_ques)

      categories = Category.query.order_by(Category.type).all()
      print("\n\nGot categories", categories)
      # categories_json_ready = [category.format() for category in categories]
      categories_json_ready = {category.id: category.type for category in categories}
      my_json = {
            'success': True,
            'questions': formatted_ques,
            'totalQuestions': len(formatted_ques),
            'categories': categories_json_ready,
            'currentCategory': currentCategory
      }
      print("Returning JSON", my_json)
      return jsonify({
            'success': True,
            'questions': formatted_ques,
            'totalQuestions': len(formatted_ques),
            'categories': categories_json_ready,
            'currentCategory': currentCategory
        })

  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:que_id>', methods=['DELETE'])
  def delete_question(que_id):
    errno = 0
    print("delete_question: Entered with id ", que_id)
    try:
      print("delete_question: Querying for que_id", que_id)
      que = Question.query.get(que_id)
      
      if que == None:
        print("delete_question: Got no question ", que_id)
        errno = 404
        abort(errno)

      que.delete()
      print("delete_question: Got question for id", que_id)
      return jsonify({
        'success': True
      })
    except:
      if errno == 0:
        abort(422)
      else:
        abort(errno)





  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
# {
#         question: this.state.question,
#         answer: this.state.answer,
#         difficulty: this.state.difficulty,
#         category: this.state.category
#       }

  @app.route('/questions', methods=['POST'])
  def add_question_or_search():
    req_data_dict = json.loads(request.data)
    print("add_question_or_search:Got req data dict json",req_data_dict, type(req_data_dict))
    got_create_request,got_search_request = False, False
    # Two possibilities - if it's a search request JSON data contains key search
    # if a create request we get key - title author rating
    #     
    if "searchTerm" in req_data_dict:
      print("add_question_or_search:Got search in request data keys")
      got_search_request = True
    elif "question" in req_data_dict:
      print("add_question_or_search: Got question, add request")
      got_create_request = True
    else:
      print("add_question_or_search:Got neither")
      abort(400)

    if got_create_request:
      try:
        question = req_data_dict["question"]
        answer = req_data_dict["answer"]
        category = req_data_dict["category"]
        difficulty = req_data_dict["difficulty"]
        print("add_question_or_search:Got keys", question, answer, category, difficulty)
        
        if len(question) == 0 or len(answer) == 0:
          print("add_question_or_search: Error got zero length question or answer, not allowed. Enter a valid question & answer")
          abort(400)


        que = Question(question=question, answer=answer, category=category, difficulty=difficulty)
        print("add_question_or_search:Attempting to insert question", que)

        if que == None:
          print ("add_question_or_search:que is None")
        else:
          print("add_question_or_search:Attempting to insert question", que)
        que.insert()
        que_id = que.id
        print("add_question_or_search:Inserted question:", que.format())
        return jsonify({
            'success': True
        })
      except:
        # print(sys.exc_info()[2])
        print(traceback.format_exc())
        abort(422)


    if got_search_request:
      try:
        search_que = req_data_dict["searchTerm"]
        que_query = Question.query.filter(Question.question.ilike('%' + search_que + '%'))
        formatted_questions = paginate_questions(request, que_query)
        # all_books = Book.query.all()
        print("add_question_or_search:Got data for search request ", formatted_questions, len(formatted_questions))
        return jsonify({
          'success': True,        
          'questions': formatted_questions,
          'totalQuestions': len(formatted_questions),
          'currentCategory': currentCategory

        })
      except:
        abort(404)
      
    abort(400)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
#See add_question_or_search

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
#   '''
# http://localhost:3000/categories/4/questions
# Request Method: GET
  @app.route('/categories/<cat_id>/questions')
  def get_cat_questions(cat_id):
      
      questions = Question.query.order_by(Question.id).filter(Question.category == cat_id).all()
      # if len(books) == 0:
      #     abort(400)
      formatted_ques = paginate_questions(request, questions)

      if len(formatted_ques) == 0:
        abort(404)
      print("get_cat_questions:Got questions", formatted_ques)

      categories = Category.query.order_by(Category.type).all()
      print("\n\nget_cat_questions:Got categories", categories)
      # categories_json_ready = [category.format() for category in categories]
      categories_json_ready = {category.id: category.type for category in categories}
      my_json = {
            'success': True,
            'questions': formatted_ques,
            'totalQuestions': len(formatted_ques),
            'categories': categories_json_ready,
            'currentCategory': currentCategory
      }
      print("get_cat_questions: Returning JSON", my_json)
      return jsonify({
            'success': True,
            'questions': formatted_ques,
            'totalQuestions': len(formatted_ques),
            'categories': categories_json_ready,
            'currentCategory': currentCategory
        })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # {"previous_questions":[],"quiz_category":{"type":"Sports","id":"6"}}
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    req_data_dict = json.loads(request.data)
    print("quiz:Got req data dict json",req_data_dict, type(req_data_dict))
    got_create_request,got_search_request = False, False
    # Two possibilities - if it's a search request JSON data contains key search
    # if a create request we get key - title author rating
    #     
    if "previous_questions" in req_data_dict:
      print("quiz:Valid quiz request data previous_questions found")
    else:
      print("quiz:Invalid. previous_questions key not in JSON data")
      abort(400)

    try:
      previous_questions = req_data_dict["previous_questions"]
      quiz_category_id_str = req_data_dict["quiz_category"]["id"]
      quiz_category_id = int(quiz_category_id_str)
      print("quiz:Got keys previous_questions (id):{} quiz_category (id):{}".format(previous_questions, quiz_category_id))
      print("Type of quiz cat", type(quiz_category_id))


      if quiz_category_id > 0:
        questions = Question.query.filter(Question.category == quiz_category_id).all()
      else:
        questions = Question.query.all()
      print("Got following questions for category {}:\n{}".format(quiz_category_id, questions))
      
      # TBD: Optimize later to use only one copy of the list
      # sending_que = {}
      sending_que = None
      for que in list(questions):
        if que.id in previous_questions:
          print("Removing id:{} from questions".format(que.id))
          questions.remove(que)
      
      random.seed() #Random seed based on current system time
      if len(questions) > 0:
        sending_que = random.choice(questions).format()
        # sending_que = questions[0].format()
            
      return jsonify({
            'success': True,
            'question': sending_que
        })      

    except:
      # print(sys.exc_info()[2])
      print(traceback.format_exc())
      abort(422)




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":"resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
    "success": False,
    "error": 422,
    "message":"unprocessable"
  }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
    "success": False,
    "error": 400,
    "message":"bad request"
  }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
    "success": False,
    "error": 405,
    "message":"method not allowed"
  }), 405

  return app

    