import statistics


def _extract_field_values(records, field):
    """
    Извлекает значения одного поля из списка записей.

    Args:
        records: список словарей с данными.
        field: имя поля, значения которого нужно извлечь.

    Returns:
        Список значений для указанного поля.
    """
    vals = []
    for r in records:
        if field in r and r[field] is not None:
            vals.append(r[field])
    return vals


def agg_count(records):
    """
    Считает количество записей.

    Args:
        records: список словарей.

    Returns:
        Целое число — длина списка.
    """
    return len(records)


def agg_sum(records, field):
    """
    Считает сумму по числовому полю.

    Args:
        records: список словарей.
        field: имя числового поля.

    Returns:
        Сумма значений поля . Если значений нет — вернет 0.0.
    """
    vals = _extract_field_values(records, field)
    return float(sum(vals))


def agg_mean(records, field):
    """
    Считает среднее значение по числовому полю.

    Args:
        records: список словарей.
        field: имя числового поля.

    Returns:
        Среднее значение (float) или None, если значений нет.
    """
    vals = _extract_field_values(records, field)
    if not vals:
        return None
    return statistics.mean(vals)


def agg_median(records, field):
    """
    Считает медиану по числовому полю.

    Args:
        records: список словарей.
        field: имя числового поля.

    Returns:
        Медиана (float) или None, если значений нет.
    """
    vals = _extract_field_values(records, field)
    if not vals:
        return None
    return statistics.median(vals)


def agg_max(records, field):
    """
    Находит максимальное значение по полю.

    Args:
        records: список словарей.
        field: имя поля.

    Returns:
        Максимальное значение или None, если значений нет.
    """
    vals = _extract_field_values(records, field)
    if not vals:
        return None
    return max(vals)


def agg_min(records, field):
    """
    Находит минимальное значение по полю.

    Args:
        records: список словарей.
        field: имя поля.

    Returns:
        Минимальное значение или None, если значений нет.
    """
    vals = _extract_field_values(records, field)
    if not vals:
        return None
    return min(vals)


def top_n(records, field, n=5, reverse=True):
    """
    Возвращает top-N записей по значению поля.

    Args:
        records: список словарей.
        field: имя поля, по которому сортируем.
        n: сколько записей вернуть.
        reverse: True — по убыванию, False — по возрастанию.

    Returns:
        Список максимум из n словарей, отсортированных по полю.
    """
    recs = [r for r in records if field in r and r[field] is not None]
    recs.sort(key=lambda r: r[field], reverse=reverse)
    return recs[:n]
