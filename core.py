import requests
from collections import Counter


def load_data(link):
    """
    Загружает данные по указанной ссылке и возвращает распарсенный JSON.

    Args:
        link: строка с URL.

    Returns:
        Python-объект (обычно словарь), полученный из JSON-ответа.

    Raises:
        ValueError: если ссылка не строка или пустая.
        requests.RequestException: если запрос не удался.
    """
    if not link or not isinstance(link, str):
        raise ValueError('wrong value in link in func load_data')
    resp = requests.get(link)
    resp.raise_for_status()
    return resp.json()


def is_suitable_key(obj):
    """
    Проверяет, может ли объект использоваться как ключ словаря.

    Args:
        obj: произвольный объект.

    Returns:
        True, если объект имеет допустимый тип для ключа словаря, иначе False.
    """
    return isinstance(obj, (int, float, str, tuple, frozenset, type(None), bool))


def to_int(value):
    """
    Преобразует значение к целому числу, если это возможно.

    Args:
        value: значение (строка, int или None).

    Returns:
        int, если удалось преобразовать;
        None, если значение пустое или нельзя преобразовать.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        try:
            return int(s)
        except ValueError:
            return None
    return None


def date_to_year(birth_date):
    """
    Извлекает год из строки даты.

    Поддерживаемые форматы:
      - 'YYYY'
      - 'YYYY-MM-DD'
      - 'YYYY-00-00'

    Args:
        birth_date: строка с датой или int с годом.

    Returns:
        int — год, если его удалось извлечь;
        None — если формат не распознан или значение пустое.
    """
    if not birth_date:
        return None
    if isinstance(birth_date, int):
        return birth_date
    if isinstance(birth_date, str):
        year_part = birth_date[:4]
        if year_part.isdigit():
            return int(year_part)
    return None


def extract_nested_value(obj, keys):
    """
    Безопасно извлекает значение по цепочке ключей из вложенных структур.

    Поддерживает словари и списки/кортежи. При любой несостыковке возвращает None.

    Args:
        obj: исходный вложенный объект (обычно словарь).
        keys: список ключей/индексов, которые нужно пройти.

    Returns:
        Значение по указанному пути или None, если пройти путь не удалось.
    """
    cur = obj
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            if not is_suitable_key(k):
                return None
            cur = cur.get(k)
        elif isinstance(cur, (list, tuple)):
            if not isinstance(k, int):
                return None
            if 0 <= k < len(cur):
                cur = cur[k]
            else:
                return None
        else:
            return None
    return cur


def _has(d, path):
    """
    Вспомогательная функция: проверяет, что по указанному пути есть непустое значение.

    Args:
        d: словарь.
        path: список ключей.

    Returns:
        True, если extract_nested_value(...) вернуло не None, иначе False.
    """
    return extract_nested_value(d, path) is not None


def is_org(rec):
    """
    Определяет, что запись относится к организации.

    Использует признаки, характерные для организаций (наличие orgName, founded и т.п.).

    Args:
        rec: словарь с сырыми данными лауреата.

    Returns:
        True, если запись похожа на организацию,
        False — если нет.
    """
    hard = _has(rec, ["orgName"]) or _has(rec, ["founded"])
    soft = any([
        _has(rec, ["orgName", "en"]),
        _has(rec, ["acronym"]),
    ])
    return (hard or soft)


def is_person(rec):
    """
    Определяет, что запись относится к человеку.

    Использует признаки, характерные для людей (knownName, birth, gender и т.п.).

    Args:
        rec: словарь с сырыми данными лауреата.

    Returns:
        True, если запись похожа на человека,
        False — если нет.
    """
    hard = _has(rec, ["knownName"]) or _has(rec, ["birth"]) or _has(rec, ["gender"])
    soft = any([
        _has(rec, ["fullName"]),
        _has(rec, ["givenName"]),
        _has(rec, ["familyName"]),
        _has(rec, ["death"]),
    ])
    return (hard or soft)


def process_dictionary_with_config(dictionary, config):
    """
    Обрабатывает один словарь по конфигу и возвращает плоский словарь.

    Конфиг имеет вид:
        {
          "field1": ["path", "to", "value"],
          "field2": (["path", "to", "value"], функция_обработки),
        }

    Args:
        dictionary: исходный вложенный словарь.
        config: словарь-конфиг.

    Returns:
        Новый словарь {атрибут: значение} согласно конфигу.
    """
    dict_processed = {}
    for attribute, path_rule in config.items():
        if isinstance(path_rule, list):
            dict_processed[attribute] = extract_nested_value(dictionary, path_rule)
        elif isinstance(path_rule, tuple) and len(path_rule) == 2 and callable(path_rule[1]):
            path, process_func = path_rule
            raw_value = extract_nested_value(dictionary, path)
            dict_processed[attribute] = process_func(raw_value)
    return dict_processed


def process_list_of_dicts_with_config(list_of_dicts, config):
    """
    Обрабатывает список словарей по одному и тому же конфигу.

    Args:
        list_of_dicts: список вложенных словарей (например, список призов).
        config: словарь-конфиг.

    Returns:
        Список плоских словарей.
    """
    dicts_processed = []
    if not list_of_dicts:
        return []
    if not isinstance(list_of_dicts, list):
        raise TypeError("функция process_list_of_dicts_with_config ожидает список словарей")

    for dic in list_of_dicts:
        if not isinstance(dic, dict):
            raise TypeError("Все элементы list_of_dicts должны иметь тип словаря")
        dicts_processed.append(process_dictionary_with_config(dic, config=config))
    return dicts_processed


def create_processor(config, list_processor=False):
    """
    Создаёт и возвращает функцию-процессор с уже подставленным конфигом.

    Args:
        config: словарь-конфиг для обработки.
        list_processor: если True — вернётся процессор для СПИСКА словарей;
                        если False — для ОДНОГО словаря.

    Returns:
        Функция, которую потом можно просто вызвать: processor(data).
    """
    if not config:
        raise TypeError('value of config error')
    if not isinstance(config, dict):
        raise TypeError('config должен быть типа dict')
    if list_processor:
        def process_dict_list(list_dicts):
            return process_list_of_dicts_with_config(list_dicts, config)
        return process_dict_list
    else:
        def process_dict(dic):
            return process_dictionary_with_config(dic, config)
        return process_dict