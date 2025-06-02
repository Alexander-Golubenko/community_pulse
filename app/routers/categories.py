from flask import Blueprint, request, jsonify
from app.models import db, Category
from app.schemas.questions import CategoryCreate, CategoryResponse
from pydantic import ValidationError

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Получение списка всех категорий."""
    # Используем Flask-SQLAlchemy для загрузки всех категорий
    categories = Category.query.all()
    # Преобразуем список объектов категорий в список словарей
    categories_data = [CategoryResponse.from_orm(q).model_dump() for q in categories]
    return jsonify(categories_data)


@categories_bp.route('/', methods=['POST'])
def create_category():
    """Создание новой категории."""
    data = request.get_json() # Получаем данные из запроса в формате JSON
    try:
        category_data = CategoryCreate(**data)
    except ValidationError as e:
            # Проверяем, что текст категории присутствует в данных
        return jsonify(e.errors()), 400
    # Проверка на повтор
    existing = Category.query.filter_by(name=category_data.name).first()
    if existing:
        return jsonify({'message': 'Такая категория уже существует.'}), 400
    # Создаем экземпляр вопроса
    category = Category(
        name=category_data.name
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Категория создана', 'id': category.id, 'category_descr': category.name}), 201


@categories_bp.route('/<int:category_id>', methods=['GET'] )
def get_category(category_id):
    """Получение деталей конкретной категории вопросов по её ID."""
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'message': 'Категории с таким ID не найдено.'}), 404
    return jsonify({CategoryResponse.from_orm(category).model_dump()}), 200


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Обновление конкретной категории по её ID."""
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({'message': 'Категория не найдена.'}), 404

    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Категория обновлена.'}), 200
    else:
        return jsonify(CategoryResponse.from_orm(category).model_dump()), 400


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Удаление конкретной категории по её ID."""
    category = Category.query.get(category_id)

    if category is None:
        return jsonify({'message': f'Категория {category_id} отсутствует.'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Категория удалена.'}), 200