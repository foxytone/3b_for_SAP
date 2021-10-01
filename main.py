import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Tuple

url = 'http://www.cbr.ru/scripts/XML_daily.asp'

KRONE_VALUTE_ID = "R01535"
FORINT_VALUTE_ID = "R01135"


def ratio_of_first_to_second(id_first: str, id_second: str) -> float:
    first_coin_value, first_coin_nominal, second_coin_value, second_coin_nominal = extract_data(id_first,
                                                                                                id_second)
    return calculate_ratio(first_coin_value, first_coin_nominal, second_coin_value, second_coin_nominal)


def extract_data(id_first: str, id_second: str) -> Tuple[float, float, float, float]:
    for element in get_root(url):
        if element.attrib['ID'] == id_first:
            first_coin_value = float(element[4].text.replace(',', '.'))
            first_coin_nominal = float(element[2].text.replace(',', '.'))
        if element.attrib['ID'] == id_second:
            second_coin_value = float(element[4].text.replace(',', '.'))
            second_coin_nominal = float(element[2].text.replace(',', '.'))
            # coins['forint'] = {'nominal': element[2].text, 'value': element[4].text}
    return first_coin_value, first_coin_nominal, second_coin_value, second_coin_nominal


def get_root(url: str) -> Element:
    return ET.fromstring(requests.get(url).text)


def calculate_ratio(first_coin_value: float, first_coin_nominal: float, second_coin_value: float,
                    second_coin_nominal: float):
    return (first_coin_value * second_coin_nominal) / (second_coin_value * first_coin_nominal)


if __name__ == '__main__':
    ratio = ratio_of_first_to_second(KRONE_VALUTE_ID, FORINT_VALUTE_ID)
    print(f'the cost of one Norwegian krone in Hungarian forints is {ratio}')
