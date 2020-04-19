from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category
from sqlalchemy import func

from backend.models import db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    QUESTIONS_PER_SITE = 10

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_SITE
        end = start + QUESTIONS_PER_SITE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_category = {category.id: category.type for category in categories}
            return jsonify({'success': True,
                            'categories': formatted_category})
        except:
            abort(400)

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

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            categories = Category.query.all()
            formatted_category = {category.id: category.type for category in categories}

            # formatted_questions = [question.format() for question in current_questions]
            return jsonify({'success': True,
                            'questions': current_questions,
                            'total_questions': len(current_questions),
                            'categories': formatted_category})
        except:
            abort(422)
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(current_questions)
            })
        except:
            abort(422)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.filter(
                    db.func.lower(Question.question).contains(db.func.lower(search))).all()
                current_question = paginate_questions(request, selection)

                return jsonify({
                    'search': True,
                    'success': True,
                    'questions': current_question,
                    'total_questions': len(current_question)
                })
            else:
                if new_question is None or new_answer is None or new_category is None or new_difficulty is None:
                    abort(422)

                question = Question(question=new_question, answer=new_answer, category=new_category,
                                    difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'search': search,
                    'success': True,
                    'id': question.id,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        try:
            question = Question.query.filter(Question.category == str(category_id)).all()
            current_questions = paginate_questions(request, question)
            category = Category.query.filter(Category.id == category_id).first()

            if len(current_questions) == 0:
                abort(404)

            return jsonify({'success': True,
                            'questions': current_questions,
                            'total_questions': len(current_questions),
                            'currentCategory': Category.format(category)})
        except:
            abort(422)

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

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        category_id = quiz_category.get('id', None)

        if previous_questions is None or quiz_category is None:
            abort(404)

        try:
            if len(previous_questions) > 0:
                if int(category_id) > 0:
                    question = Question.query.filter(Question.id.notin_(previous_questions),
                                                     Question.category == category_id).order_by(func.random()).first()
                else:
                    question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(
                        func.random()).first()
            else:
                if int(category_id) > 0:
                    question = Question.query.filter(Question.category == str(category_id)).order_by(
                        func.random()).first()
                else:
                    question = Question.query.order_by(func.random()).first()
            if question is None:
                abort(422)
            previous_questions.append(question.id)
            return jsonify({'success': True,
                            'question': Question.format(question),
                            'previous_questions': previous_questions})
        except:
            abort(422)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    return app
