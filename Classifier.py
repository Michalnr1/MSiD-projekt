import re

from Collector import read_boards


def classifier(all_hands, all_results) -> tuple[list[list[list[int | str]]], list[list[list[int | str]]], list[list[list[int | str]]], list[list[list[int | str]]], list[list[list[int | str]]], list[list[list[int | str]]]]:
    """
    Classify hands depends on the length of the longest suits in both partners hands

    :param all_hands: List of all hands
    :param all_results: List of all results
    :return:
    """
    longestSuit4_4 = []
    longestSuit5_4 = []
    longestSuit5_5 = []
    longestSuit6_4 = []
    longestSuit6_5 = []
    longestSuit6_6 = []

    for hands, result in zip(all_hands, all_results):
        hands = remove_opps_hands(hands)
        shape1 = hands[0][5]
        shape2 = hands[1][5]
        hands.append(result)

        longestSuit1 = find_longest_suit(shape1)
        longestSuit2 = find_longest_suit(shape2)
        if longestSuit1 == 4 and longestSuit2 == 4:
            longestSuit4_4.append(hands)
        elif (longestSuit1 == 4 and longestSuit2 == 5) or (longestSuit1 == 5 and longestSuit2 == 4):
            longestSuit5_4.append(hands)
        elif longestSuit1 == 5 and longestSuit2 == 5:
            longestSuit5_5.append(hands)
        elif (longestSuit1 == 4 and longestSuit2 == 6) or (longestSuit1 == 6 and longestSuit2 == 4):
            longestSuit6_4.append(hands)
        elif (longestSuit1 == 5 and longestSuit2 == 6) or (longestSuit1 == 6 and longestSuit2 == 5):
            longestSuit6_5.append(hands)
        elif longestSuit1 == 6 and longestSuit2 == 6:
            longestSuit6_6.append(hands)

    return longestSuit4_4, longestSuit5_4, longestSuit5_5, longestSuit6_4, longestSuit6_5, longestSuit6_6


def find_longest_suit(shape: str) -> int:
    """
    Find the longest suit in the hand

    :param shape: Shape of the hand (example: 4324)
    :return: The length of the longest suit in the hand
    """
    if re.search(r'[7]', shape):
        return 7
    elif re.search(r'[6]', shape):
        return 6
    elif re.search(r'[5]', shape):
        return 5
    else:
        return 4


def remove_opps_hands(hands: list[list[int | str]]) -> list[list[int | str]]:
    """
    Remove opponents hands from the lists

    :param hands: Hands from one board
    :return: Only two hands: declarer and dummy
    """
    if 23 <= hands[0][4] + hands[3][4] <= 28:
        hands.pop(2)
        hands.pop(1)
    elif 23 <= hands[1][4] + hands[2][4] <= 28:
        hands.pop(3)
        hands.pop(0)
    return hands


all_hands, all_results = read_boards('Boards.json')
#print(len(all_hands))
longestSuit4_4, longestSuit5_4, longestSuit5_5, longestSuit6_4, longestSuit6_5, longestColour6_6 = classifier(all_hands, all_results)
#print(longestColour4_4)
#print(len(longestSuit4_4))
#print(longestColour5_4)
#print(len(longestSuit5_4))
#print(longestColour5_5)
#print(len(longestSuit5_5))
#print(longestColour6_4)
#print(len(longestSuit6_4))
#print(longestColour6_5)
#print(len(longestSuit6_5))
#print(longestColour6_6)
#print(len(longestColour6_6))