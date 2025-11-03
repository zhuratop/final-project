from core import create_processor, to_int

CONFIG_PRIZE = {
    "prize_amount": ["prizeAmount"],
    "prize_amount_adjusted": ["prizeAmountAdjusted"],
    "award_year": (["awardYear"], to_int),
    "category_en": ["category", "en"],
    "prize_status": ["prizeStatus"],
}


def prize_processor():
    """
    Возвращает готовый процессор для спискак призов.

    Returns:
        функцию-обработчик с предзагруженным конфигом,
        для обработки списка призов
    """
    return create_processor(CONFIG_PRIZE, list_processor=True)