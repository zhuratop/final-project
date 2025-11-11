def add_field(records, field_name, compute_func):
    """
    Добавляет (или переопределяет) поле у каждой записи.

    Args:
        records: список словарей, которые нужно дополнить.
        field_name: имя нового/перезаписываемого поля.
        compute_func: функция, получающая запись и возвращающая значение для этого поля.

    Returns:
        Ничего. Модифицирует список.
    """
    for r in records:
        r[field_name] = compute_func(r)


def remove_field(records, field_name):
    """
    Удаляет поле у всех записей, если оно есть.

    Args:
        records: список словарей.
        field_name: имя поля для удаления.

    Returns:
        Ничего. Модифицирует список на месте.
    """
    for r in records:
        if field_name in r:
            del r[field_name]


def ensure_field(records, field_name, default=None):
    """
    Гарантирует наличие поля у всех записей. Если поля не было — добавляет со значением default.

    Args:
        records: список словарей.
        field_name: имя поля.
        default: значение по умолчанию.

    Returns:
        Ничего. Модифицирует список.
    """
    for r in records:
        if field_name not in r:
            r[field_name] = default
