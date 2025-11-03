# проверки для функций предобработки данных

from core import to_int, process_list_of_dicts_with_config, process_dictionary_with_config, extract_nested_value, create_processor
from laureates_configs import CONFIG_PERSON, CONFIG_ORG, date_to_year
from prizes_configs import CONFIG_PRIZE

# 1. to_int
assert to_int("2001") == 2001
assert to_int("  42 ") == 42
assert to_int(None) is None

# 2. date_to_year
assert date_to_year("1943-00-00") == 1943
assert date_to_year("1943-11-30") == 1943
assert date_to_year(None) is None
assert date_to_year(2001) == 2001

# 3. extract_nested_value — ты уже часть проверил, добавим крайний случай
assert extract_nested_value({"a": [10, 20]}, ["a", 0]) == 10
assert extract_nested_value({"a": [10, 20]}, ["a", 5]) is None


# 5. process_dictionary_with_config — проверим на маленьком вручную собранном человеке
test_person = {
    "id": "745",
    "knownName": {"en": "A. Michael Spence"},
    "gender": "male",
    "birth": {
        "date": "1943-01-01",
        "place": {
            "country": {"en": "USA"},
            "countryNow": {"en": "USA"},
        },
    },
    "nobelPrizes": [
        {
            "prizeAmount": 10000000,
            "prizeAmountAdjusted": 15547541,
            "awardYear": "2001",
            "category": {"en": "Economic Sciences"},
            "prizeStatus": "received",
        }
    ],
}

# создаём процессор для человека
person_proc = create_processor(CONFIG_PERSON, list_processor=False)
person_flat = person_proc(test_person)


assert person_flat["id"] == 745
assert person_flat["name"] == "A. Michael Spence"
assert person_flat["gender"] == "male"
assert person_flat["birth_year"] == 1943
assert person_flat["country_birth"] == "USA"
assert person_flat["country_now"] == "USA"
# проверим, что призы тоже обработались
assert isinstance(person_flat["prizes_relevant"], list)
assert len(person_flat["prizes_relevant"]) == 1
assert person_flat["prizes_relevant"][0]["award_year"] == 2001
assert person_flat["prizes_relevant"][0]["category_en"] == "Economic Sciences"

# 6. process_list_of_dicts_with_config — список из двух людей
two_people = [test_person, test_person]
list_proc = process_list_of_dicts_with_config(two_people, CONFIG_PERSON)
assert isinstance(list_proc, list)
assert len(list_proc) == 2
assert list_proc[0]["id"] == 745
assert list_proc[1]["name"] == "A. Michael Spence"

# 7. create_processor — версия для списков
prize_proc = create_processor(CONFIG_PRIZE, list_processor=True)
prizes_in = [
    {
        "prizeAmount": 630000,
        "prizeAmountAdjusted": 4304697,
        "awardYear": "1975",
        "category": {"en": "Physics"},
        "prizeStatus": "received",
    },
    {
        "prizeAmount": 10000000,
        "prizeAmountAdjusted": 15547541,
        "awardYear": "2001",
        "category": {"en": "Economic Sciences"},
        "prizeStatus": "received",
    },
]
prizes_out = prize_proc(prizes_in)
assert len(prizes_out) == 2
assert prizes_out[0]["award_year"] == 1975
assert prizes_out[1]["category_en"] == "Economic Sciences"


print("Все assert-проверки прошли.")