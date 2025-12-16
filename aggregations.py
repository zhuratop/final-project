import statistics
from typing import List, Dict, Any, Union, Optional


def _extract_field_values(records: List[Dict[str, Any]], field: str) -> List[Any]:
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


def agg_count(records: List[Dict[str, Any]]) -> int:
    """
    Считает количество записей.

    Args:
        records: список словарей.

    Returns:
        Целое число — длина списка.
    """
    return len(records)


def agg_sum(records: List[Dict[str, Any]], field: str) -> float:
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


def agg_mean(records: List[Dict[str, Any]], field: str) -> Optional[float]:
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


def agg_median(records: List[Dict[str, Any]], field: str) -> Optional[float]:
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


def agg_max(records: List[Dict[str, Any]], field: str) -> Optional[Any]:
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


def agg_min(records: List[Dict[str, Any]], field: str) -> Optional[Any]:
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


def top_n(records: List[Dict[str, Any]], field: str, n: int = 5, reverse: bool = True) -> List[Dict[str, Any]]:
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
