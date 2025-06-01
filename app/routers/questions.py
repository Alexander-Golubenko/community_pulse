from flask import Blueprint, request, jsonify
from app.models import db, Question
from app.schemas.questions import QuestionCreate, QuestionResponse
from pydantic import ValidationError

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    # Используем Flask-SQLAlchemy для загрузки всех вопросов
    questions = Question.query.all()
    # Преобразуем список объектов вопросов в список словарей
    questions_data = [QuestionResponse.from_orm(q).model_dump() for q in questions]
    return jsonify(questions_data)


@questions_bp.route('/', methods=['POST'])
def create_question():
    """Создание нового вопроса."""
    data = request.get_json() # Получаем данные из запроса в формате JSON
    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
            # Проверяем, что текст вопроса присутствует в данных
        return jsonify(e.errors()), 400
    # Проверка на повтор
    existing = Question.query.filter_by(text=question_data.text).first()
    if existing:
        return jsonify({'message': 'Такой вопрос уже существует.'}), 400
    # Создаем экземпляр вопроса
    question = Question(text=data['text'])
    db.session.add(question) # Добавляем вопрос в сессию для записи
    db.session.commit() # Фиксируем изменения в базе данных

    return jsonify({'message': 'Вопрос создан', 'id': question.id}), 201


@questions_bp.route('/<int:question_id>', methods=['GET'] )
def get_question(question_id):
    """Получение деталей конкретного вопроса по его ID."""
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Вопрос с таким ID не найден.'}), 404
    return jsonify({'id': f'{question.id}', 'message': f'Вопрос: {question.text}'}), 200


@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """Обновление конкретного вопроса по его ID."""
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'message': 'Вопрос не найден.'}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'message': 'Вопрос обновлен.'}), 200
    else:
        return jsonify({'message': f'Текст вопроса {question_id} отсутствует.'}), 400


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Удаление конкретного вопроса по его ID."""
    question = Question.query.get(question_id)

    if question is None:
        return jsonify({'message': f'Текст вопроса {question_id} отсутствует.'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f'Текст вопроса {question_id} удален.'}), 200
