from typing import Dict, Any, Callable, List

from core import to_int, date_to_year, create_processor, load_data
from prizes_configs import prize_processor

CONFIG_PERSON = {
    "id": (["id"], to_int),
    "name": ["knownName", "en"],
    "gender": ["gender"],
    "birth_year": (["birth", "date"], date_to_year),
    "country_birth": ["birth", "place", "country", "en"],
    "country_now": ["birth", "place", "countryNow", "en"],
    # ВАЖНО: сюда кладём уже ГОТОВЫЙ процессор списков призов
    "prizes_relevant": (["nobelPrizes"], prize_processor()),
}


CONFIG_ORG = {
    "id": (["id"], to_int),
    "name": ["orgName", "en"],
    "founded_year": (["founded", "date"], date_to_year),
    "country_founded": ["founded", "place", "country", "en"],
    "country_now": ["founded", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor()),
}


def person_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Возвращает готовый процессор для одного человека.

    Returns:
        функцию-обработчик с предзагруженным конфигом,
        для обработки одного человека
    """
    return create_processor(CONFIG_PERSON, list_processor=False)


def org_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Возвращает готовый процессор для одной организации.

    Returns:
        функцию-обработчик с предзагруженным конфигом,
        для обработки одной организации.
    """
    return create_processor(CONFIG_ORG, list_processor=False)
