from app.schemas.response import ResponseCreate
from pydantic import ValidationError
from flask import Blueprint, request, jsonify
from app.models import Statistic, Question, Response, db

response_bp = Blueprint('response', __name__, url_prefix='/response')

@response_bp.route('/', methods=['GET'])
def get_responses():
    """Получение статистики ответов."""
    statistics = Statistic.query.all()
    results = [
        {
            'question_id': stat.question_id,
            'agree_count': stat.agree_count,
            'disagree_count': stat.disagree_count
        }
        for stat in statistics
    ]
    return jsonify(results), 200

@response_bp.route('/<int:question_id>', methods=['GET'])
def get_response_for_question(question_id):
    """Получение статистики по конкретному вопросу."""
    statistic = Statistic.query.get(question_id)
    if not statistic:
        return jsonify({'message': 'Статистика не найдена для этого вопроса.'}), 404

    return jsonify({
        'question_id': statistic.question_id,
        'agree_count': statistic.agree_count,
        'disagree_count': statistic.disagree_count
    }), 200

@response_bp.route('/', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос."""
    data = request.get_json()
    try:
        validated_data = ResponseCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    question = Question.query.get(validated_data.question_id)
    if not question:
        return jsonify({'message': 'Вопрос не найден.'}), 404

    new_response = Response(
        question_id=validated_data.question_id,
        is_agree=validated_data.is_agree,
        response="Согласен" if validated_data.is_agree else "Не согласен"
    )
    db.session.add(new_response)

    statistic = Statistic.query.get(validated_data.question_id)
    if not statistic:
        statistic = Statistic(
            question_id=validated_data.question_id,
            agree_count=0,
            disagree_count=0
        )

    if validated_data.is_agree:
        statistic.agree_count += 1
    else:
        statistic.disagree_count += 1

    db.session.add(statistic)
    db.session.commit()

    return jsonify({'message': 'Ответ сохранён.'}), 201
