from typing import List, Dict, Any, Callable, Tuple, Optional


def filter_records(records: List[Dict[str, Any]], predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """
    Фильтрует записи по произвольной функции.

    Args:
        records: список словарей.
        predicate: функция, принимающая запись и возвращающая True/False.

    Returns:
        Список записей, для которых predicate вернул True.
    """
    return [r for r in records if predicate(r)]


def filter_by_conditions(records: List[Dict[str, Any]], conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Фильтрует записи по равенству нескольким полям.

    Args:
        records: список словарей.
        conditions: словарь вида {имя_поля: нужное_значение}.

    Returns:
        Список записей, у которых ВСЕ указанные поля равны заданным значениям.
    """
    out = []
    for r in records:
        ok = True
        for field, expected in conditions.items():
            if r.get(field) != expected:
                ok = False
                break
        if ok:
            out.append(r)
    return out


def group_by_attributes(records: List[Dict[str, Any]], attrs: List[str]) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
    """
    Группирует записи по набору полей.

    Args:
        records: список словарей.
        attrs: список имён полей, по которым нужно сгруппировать.

    Returns:
        Словарь: ключ — кортеж значений полей, значение — список записей в группе.
    """
    groups = {}
    for r in records:
        key = tuple(r.get(a) for a in attrs)
        groups.setdefault(key, []).append(r)
    return groups


def apply_aggregation_to_groups(
    groups: Dict[Any, List[Dict[str, Any]]], 
    agg_func: Callable[[List[Dict[str, Any]]], Any]
) -> Dict[Any, Any]:
    """
    Применяет агрегирующую функцию к каждой группе.

    Args:
        groups: словарь {ключ_группы: список_записей}.
        agg_func: функция, которая принимает список записей группы и возвращает одно значение.

    Returns:
        Словарь {ключ_группы: результат_агрегации}.
    """
    out = {}
    for key, recs in groups.items():
        out[key] = agg_func(recs)
    return out


def extract_all_prizes(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Извлекает все призы из списка лауреатов в один плоский список.

    Ожидается, что у лауреатов призы лежат в поле 'prizes_relevant'.

    Args:
        records: список лауреатов (словарей).

    Returns:
        Список словарей-призов.
    """
    prizes = []
    for r in records:
        prs = r.get("prizes_relevant") or []
        for p in prs:
            if isinstance(p, dict):
                prizes.append(p)
    return prizes


def filter_prizes(prizes: List[Dict[str, Any]], predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """
    Фильтрует список призов по условию.

    Args:
        prizes: список словарей-призов.
        predicate: функция, принимающая приз и возвращающая True/False.

    Returns:
        Список призов, удовлетворяющих условию.
    """
    return [p for p in prizes if predicate(p)]
