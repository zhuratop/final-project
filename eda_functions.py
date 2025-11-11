from collections import Counter


def count_records(records):
    """
    Считает общее число записей.

    Args:
        records: список объектов.

    Returns:
        Целое число — длина списка.
    """
    return len(records)


def extract_fields_from_config(config):
    """
    Возвращает список имён полей (ключей) из конфига.

    Args:
        config: словарь-конфиг.

    Returns:
        Список строк — имён полей.
    """
    return list(config.keys())


def split_by_type(records):
    """
    Делит записи на людей и организации по полю 'type_'.

    Args:
        records: список уже предобработанных словарей.

    Returns:
        Кортеж (persons, orgs), где оба — списки словарей.
    """
    persons = []
    orgs = []
    for r in records:
        if r.get('type_') == 'person':
            persons.append(r)
        elif r.get('type_') == 'org':
            orgs.append(r)
    return persons, orgs


def count_missing(records, fields):
    """
    Считает количество и долю пропусков по указанным полям.

    Args:
        records: список словарей.
        fields: список имён полей.

    Returns:
        Кортеж (counts, ratios):
          counts — словарь {поле: число пропусков}
          ratios — словарь {поле: доля пропусков}
    """
    n = len(records)
    counts = {f: 0 for f in fields}
    for rec in records:
        for f in fields:
            if f not in rec or rec[f] is None:
                counts[f] += 1
    ratios = {f: (counts[f] / n if n > 0 else 0) for f in fields}
    return counts, ratios


def collect_all_prizes(records):
    """
    Собирает все призы из лауреатов в один список.

    Args:
        records: список лауреатов (словарей).

    Returns:
        Список словарей-призов.
    """
    prizes = []
    for rec in records:
        if not rec:
            continue
        for p in rec.get("prizes_relevant", []) or []:
            if isinstance(p, dict):
                prizes.append(p)
    return prizes


def count_missing_prizes(prizes, prize_config):
    """
    Считает пропуски по полям призов.

    Args:
        prizes: список словарей-призов.
        prize_config: конфиг для призов (берём из него список полей).

    Returns:
        Кортеж (counts, ratios), аналогично count_missing.
    """
    fields = list(prize_config.keys())
    n = len(prizes)
    counts = {f: 0 for f in fields}
    for pr in prizes:
        for f in fields:
            if f not in pr or pr[f] is None:
                counts[f] += 1
    ratios = {f: (counts[f] / n if n > 0 else 0) for f in fields}
    return counts, ratios


def get_award_years_from_rec(rec):
    """
    Возвращает список годов награждений из одной записи лауреата.

    Args:
        rec: словарь лауреата.

    Returns:
        Список целых годов (может быть пустым).
    """
    years = []
    for p in rec.get("prizes_relevant", []) or []:
        y = p.get("award_year")
        if y is not None:
            years.append(y)
    return years


def get_min_max_id_info(records):
    """
    Находит минимальный и максимальный id и возвращает их вместе с годами награждения.

    Args:
        records: список лауреатов (уже плоских).

    Returns:
        Словарь вида:
        {
          "min_id": ...,
          "min_id_years": [...],
          "max_id": ...,
          "max_id_years": [...],
        }
        или None, если id нет.
    """
    ids = [r["id"] for r in records if r and r.get("id") is not None]
    if not ids:
        return None
    min_id = min(ids)
    max_id = max(ids)
    rec_min = next(r for r in records if r and r.get("id") == min_id)
    rec_max = next(r for r in records if r and r.get("id") == max_id)
    return {
        "min_id": min_id,
        "min_id_years": get_award_years_from_rec(rec_min),
        "max_id": max_id,
        "max_id_years": get_award_years_from_rec(rec_max),
    }


def find_duplicate_ids(records):
    """
    Находит id, которые встречаются больше одного раза.

    Args:
        records: список словарей.

    Returns:
        Список дублирующихся id (может быть пустым).
    """
    ids = [r["id"] for r in records if r and r.get("id") is not None]
    cnt = Counter(ids)
    return [i for i, c in cnt.items() if c > 1]


def find_id_gaps(records, gap_threshold=1):
    """
    Ищет разрывы в последовательности id.

    Args:
        records: список словарей.
        gap_threshold: порог разрыва (обычно 1).

    Returns:
        Список кортежей (предыдущий_id, следующий_id), между которыми разрыв больше порога.
    """
    ids = sorted(set(r["id"] for r in records if r and r.get("id") is not None))
    gaps = []
    for prev, curr in zip(ids, ids[1:]):
        if curr - prev > gap_threshold:
            gaps.append((prev, curr))
    return gaps


def round_ratios(ratios, ndigits):
    """
    Округляет все значения в словаре с долями.

    Args:
        ratios: словарь {поле: доля}.
        ndigits: сколько знаков после запятой оставить.

    Returns:
        Новый словарь с округлёнными значениями.
    """
    return {k: round(v, ndigits) for k, v in ratios.items()}