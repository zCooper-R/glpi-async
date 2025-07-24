import datetime

from .criteria import CriteriaBuilder


class QueryBuilder:
    """
    Строитель запросов к объектам GLPI через REST API.

    Позволяет добавлять фильтры, настраивать отображаемые поля,
    указывать диапазон (range) и выполнять запрос к API.

    Пример использования:
        tickets = await glpi.tickets.query() \
            .created_after(dt) \
            .close() \
            .show("22", "15") \
            .range(0, 50) \
            .get()
    """
    def __init__(self, manager):
        self.manager = manager
        self.criteria = CriteriaBuilder()
        self.display = []
        self.uid_cols = True
        self._range = None

    def where(self, field, value, searchtype="equals", link="AND"):
        """
        Добавляет произвольное условие в критерии поиска.

        :param field: поле для фильтрации (по API-коду или имени)
        :param value: значение для сравнения
        :param searchtype: тип сравнения (по умолчанию 'equals')
        :param link: логическая связь (по умолчанию 'AND')
        :return: self
        """
        self.criteria.where(field, value, searchtype, link)
        return self

    def show(self, *fields):
        """
        Указывает поля, которые нужно вернуть (forcedisplay).

        :param fields: имена или ID полей, которые отобразить
        :return: self
        """
        self.display.extend(fields)
        return self

    # Сахар:
    def open(self):
        """
        Добавляет фильтр: статус заявки = Открыта (статус 2).
        :return: self
        """
        return self.where(12, 2)

    def close(self):
        """
        Добавляет фильтр: статус заявки = Закрыта (статус 6).
        :return: self
        """
        return self.where(12, 6)

    def for_user(self, user_id):
        """
        Фильтрация заявок по исполнителю.

        :param user_id: ID пользователя (GLPI)
        :return: self
        """
        return self.where(22, user_id)

    def created_after(self, dt: datetime):
        """
        Фильтрация заявок, созданных после указанной даты.

        :param dt: объект datetime
        :return: self
        """
        return self.where(15, dt.strftime("%Y-%m-%d"), "morethan")

    def created_before(self, dt: datetime):
        """
        Фильтрация заявок, созданных до указанной даты.

        :param dt: объект datetime
        :return: self
        """
        return self.where(15, dt.strftime("%Y-%m-%d"), "lessthan")

    def range(self, start: int, end: int):
        """
        Устанавливает диапазон (пагинация) результатов.

        :param start: начальный индекс (включительно)
        :param end: конечный индекс (включительно)
        :return: self
        """
        self._range = f"{start}-{end}"
        return self

    async def get(self):
        """
        Выполняет асинхронный запрос к GLPI API и возвращает результат.

        :return: список найденных объектов (JSON)
        """
        params = self.criteria.build()
        if self.uid_cols:
            params["uid_cols"] = True
        for i, val in enumerate(self.display):
            params[f"forcedisplay[{i}]"] = val
        if self._range:
            params["range"] = self._range
        return await self.manager.api.get(f"search/{self.manager.item_name}", params=params)
