import os
import sys
from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )

        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route("/categories")
    def show_categories():

        category_data = Category.query.order_by(Category.id).all()

        if category_data is None:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {cat.format()['id']: cat.format()['type'] for cat in category_data}
            }
        ), 200

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

    category_data = Category.query.order_by(Category.id).all()
    categories = {cat.format()['id']: cat.format()['type']
                  for cat in category_data}

    QUESTION_PER_PAGE = 10

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTION_PER_PAGE
        end = start + QUESTION_PER_PAGE

        questions = [q.format() for q in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                'currentCategory': categories[current_questions[-1]['category']]
            }
        ), 200

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        error = False
        try:

            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
        except:
            error = True
            print(sys.exc_info())

        if error:
            abort(422)

        else:
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            ), 200

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()

            question = body.get("question", None)
            answer_text = body.get("answer", None)
            category = body.get("category", None)
            difficulty_score = body.get("difficulty", None)
            print(question, answer_text, category, difficulty_score)
            question = Question(question=question, answer=answer_text,
                                category=category, difficulty=difficulty_score)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except Exception as e:
            #   print(sys.exc_info())
            #   error = True
            # if error:
            # abort(422)
            print(category_data, e)
        # else:

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    # @app.route('/questions/<string:search_term>', methods=['POST'])
    # def search_question(search_term):
    #   selection = Question.query.filter(Question.question.ilike(f"%{search_term}%")).order_by(Question.id).all()
    #   current_questions = paginate_questions(request, selection)

    #   if len(current_questions) == 0:
    #     abort(404)

    #   return jsonify(
    #     {
    #       "success": True,
    #       "questions": current_questions,
    #       "total_match": len(selection),
    #     }
    #   )

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()

            if "searchTerm" in body:
                # request.json['search']
                search_term = body.get("searchTerm", None)
            else:
                abort(404)

            if search_term:
                selection = Question.query.filter(Question.question.ilike(
                    f"%{search_term}%")).order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "search_term": search_term,
                    "success": True,
                    "questions": current_questions,
                    "total_match": len(selection),
                    'currentCategory': categories[current_questions[-1]['category']]
                }
            ), 200
        except:
            print(sys.exc_info())
            abort(401)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category>/questions', methods=['GET'])
    def retrieve_questions_by_category(category):
        selection = Question.query.filter(
            Question.category == category).order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_match": len(selection),
                'current_category': categories[category]
            }
        ), 200

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
    def post_quiz():
        error = False
        body = request.get_json()
        quiz_category = body.get('quiz_category', None)
        get_previous_question = body.get('previous_question', [])
        try:
            if quiz_category.get('id', None) == 0:
                questionsQuery = Question.query.all()
            else:
                questionsQuery = Question.query.filter(
                    Question.category == quiz_category.get('id', None)).all()
            nextQuestion = random.choice(questionsQuery)

            for _ in range(len(questionsQuery)):
                if nextQuestion.id not in get_previous_question:
                    get_previous_question.append(nextQuestion.id)
            # while nextQuestion.id not in get_previous_question:
            #     get_previous_question.append(nextQuestion.id)

        except:
            error = True
            print(sys.exc_info())
        if error:
            abort(401)
        else:
            return jsonify(
                {
                    'success': True,
                    'question': {
                        "answer": nextQuestion.answer,
                        "category": nextQuestion.category,
                        "difficulty": nextQuestion.difficulty,
                        "id": nextQuestion.id,
                        "question": nextQuestion.question
                    },
                    'previousQuestion': get_previous_question
                }
            ), 200

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    return app
