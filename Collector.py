import json
import re

from Scraper import scrap

def is_ok(hands, can_play) -> bool:
    """
    Initially check boards if they fulfil the conditions

    :param hands: Hand parameters
    :return: True if declarer and dummy have no shortness and at least game can be played
    """

    if (23 <= hands[0][4] + hands[3][4] <= 28 and not re.search(r'[01]', hands[0][5]) and not re.search(r'[01]', hands[3][5])) or (
            23 <= hands[1][4] + hands[2][4] <= 28 and not re.search(r'[01]', hands[1][5]) and not re.search(r'[01]', hands[2][5])):
        for play in can_play:
            if play[2]:
                return True
        return False
    else:
        return False

def read_links(path) -> list:
    """
    Read URLs from the file

    :param path: Path to the file with URLs
    :return: List of URLs
    """
    links = []
    with open(path) as file:
        for link in file:
            links.append(link.strip())
    return links

def save_boards (path, all_hands, all_results) -> None:
    """
    Saves boards into a JSON file

    :param path: Path to the file to save in
    :param all_hands: List of all hands
    :param all_results: List os all results
    """
    with open(path) as file:
        if file.read():
            hands, results = read_boards(path)
            all_hands += hands
            all_results += results
    with open(path, 'w') as file:
        json.dump({'all_hands': all_hands, 'all_results': all_results}, file)


def read_boards(path) -> tuple[list[list[list[list, list, list, list, int, str], list[list, list, list, list, int, str],
    list[list, list, list, list, int, str], list[list, list, list, list, int, str]]], list[list[list, list, list, list]]]:
    """
    Read boards from JSON file

    :param path: Path to the JSON file with boards
    :return: List of all hands and list of all results
    """
    with open(path, 'r') as file:
       data = json.load(file)
    return data['all_hands'], data['all_results']


def collect_boards(path) -> tuple[list[list[list[list, list, list, list, int, str], list[list, list, list, list, int, str],
    list[list, list, list, list, int, str], list[list, list, list, list, int, str]]], list[list[list, list, list, list]]]:
    """
    Read boards from links and initially check them if they fulfil the conditions

    :param path: Path to the file with URLs
    :return: List of all hands and list of all results
    """
    links = read_links(path)
    all_hands = []
    all_results = []
    for i, link in enumerate(links):
        print(i + 1)
        hands, can_play = scrap(link)
        if is_ok(hands, can_play):
            all_hands.append(hands)
            all_results.append(can_play)

    return all_hands, all_results

#all_hands, all_results = collect_boards('URL_07.txt')
#all_hands, all_results = collect_boards('test.txt')

#save_boards('Boards.json', all_hands, all_results)
#save_boards('Boards_test.json', all_hands, all_results)