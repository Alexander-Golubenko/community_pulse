from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.response import *
from app.models.questions import *


# flask db init	Создание папки migrations/ и настроек
# flask db migrate -m "..."	Создание миграции на основе diff моделей и текущей базы
# flask db upgrade	Применение всех неприменённых миграций
# flask db downgrade	Откат на одну миграцию назад
# flask db history	Показ всех миграций (id и метки)
# flask db current	Показ текущего состояния (активная ревизия)
# flask db stamp head	Проставить текущую ревизию вручную, без применения
# flask db heads	Показ всех активных "голов" (в случае конфликтов)
# flask db show <revision>	Показ содержимого конкретной миграции
# flask db merge ...	Объединение нескольких веток миграций