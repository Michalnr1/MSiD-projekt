import requests
import re
from bs4 import BeautifulSoup

#url = "http://db.worldbridge.org/Repository/tourn/Shanghai.07/Asp/BoardAcross.asp?qboard=002.01..607"

def scrap(url):
    """
    :param url: Link to the WBF site with board open
    :return: hands - List of lists of spades (list), hearts (list), diamonds (list), clubs (list), points (int), shape (string)
        can_play - List of lists of contracts done (int), contracts played (int), is it good contract (bool)
    """
    def extract_cards(cell) -> tuple[list, list, list, list]:
        """
        :param cell: text with one hand
        :return: List of spades, list of hearts, list of diamonds, list of clubs
        """
        texts = cell.find_all(string=True)

        spades = re.findall(r'[♠] \t\t(.+) \r\n', texts[0])
        if not spades:
            spades = re.findall(r'[♠] \r\n\t\t(.+) \r\n', texts[0])
        hearts = re.findall(r'\t\t(.+) \r\n', texts[3])
        diamonds = re.findall(r'\t\t(.+) \r\n', texts[6])
        clubs = re.findall(r'[♣] \t\t(.+) \r\n', texts[7])

        if not spades: spades.append('-')
        if not hearts: hearts.append('-')
        if not diamonds: diamonds.append('-')
        if not clubs: clubs.append('-')

        return spades, hearts, diamonds, clubs

    def calculate_points(spades, hearts, diamonds, clubs) -> int:
        """
        :param spades: List of spades
        :param hearts: List os hearts
        :param diamonds: List of diamonds
        :param clubs: List o clubs
        :return: Points in the hand
        """
        hand = spades + hearts + diamonds + clubs
        points = 0
        for card in hand:
            match card:
                case "A":
                    points += 4
                case "K":
                    points += 3
                case "Q":
                    points += 2
                case "J":
                    points += 1
        return points

    def shape(spades, hearts, diamonds, clubs) -> str:
        """
        :param spades: List of spades
        :param hearts: List os hearts
        :param diamonds: List of diamonds
        :param clubs: List o clubs
        :return: shape of the hand (example: 4324)
        """
        shape = f"{len(spades)}{len(hearts)}{len(diamonds)}{len(clubs)}"
        return shape

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    results_table = soup.find("table", {"border": "1", "class": "Text"})
    if not results_table: results_table = soup.find("table", {"border": "2", "class": "Text"})
    results_table_rows = results_table.find_all("tr")[1:]
    results_data = []

    for row in results_table_rows:
        cells = row.find_all("td")
        data_row = {
            "Table": cells[0].text.strip() if len(cells) > 7 else '',
            "Home Team": cells[1].text.strip() if len(cells) > 7 else '',
            "Visiting Team": cells[2].text.strip() if len(cells) > 7 else '',
            "Room": cells[3].text.strip() if len(cells) > 7 else cells[0].text.strip(),
            "Cont.": cells[4].text.strip() if len(cells) > 7 else cells[1].text.strip(),
            "Decl.": cells[5].text.strip() if len(cells) > 7 else cells[2].text.strip(),
            "Lead": cells[6].text.strip() if len(cells) > 7 else cells[3].text.strip(),
            "Tricks": cells[7].text.strip() if len(cells) > 7 else cells[4].text.strip(),
            "NS": cells[8].text.strip() if len(cells) > 7 else cells[5].text.strip(),
            "EW": cells[9].text.strip() if len(cells) > 7 else cells[6].text.strip(),
            "Home Res.": cells[10].text.strip() if len(cells) > 7 else '',
            "Vis Res.": cells[11].text.strip() if len(cells) > 7 else ''
        }
        results_data.append(data_row)

    can_play = [[0, 0, False], [0, 0, False], [0, 0, False], [0, 0, False], [0, 0, False]]

    for row in results_data:
        color = row.get("Cont.")[1:].rstrip('x')
        tricks = row.get("Tricks")
        if not tricks: tricks = 0
        tricks = int(tricks)
        match color:
            case "NT":
                if tricks >= 9:
                    can_play[0][0] += 1
                can_play[0][1] += 1
            case "♠":
                if tricks >= 10:
                    can_play[1][0] += 1
                can_play[1][1] += 1
            case "♥":
                if tricks >= 10:
                    can_play[2][0] += 1
                can_play[2][1] += 1
            case "♦":
                if tricks >= 11:
                    can_play[3][0] += 1
                can_play[3][1] += 1
            case "♣":
                if tricks >= 11:
                    can_play[4][0] += 1
                can_play[4][1] += 1

    for done in can_play:
        if done[0] >= done[1] / 2 and done[0] > 0:
            done[2] = True
    # print("Wyniki: ", can_play)

#================================================================================

    board = soup.find("table", {"border": "0", "class": "textTable"})
    board_hands = board.find_all("td", {"class": "BrdDispl", "align": "left"})


    hands = []

    for i, cell in enumerate(board_hands):
        spades, hearts, diamonds, clubs = extract_cards(cell)
        # print(f"Ręka {i+1}:")
        # print("Piki (♠):", ' '.join(spades))
        # print("Kiery (♥):", ' '.join(hearts))
        # print("Karo (♦):", ' '.join(diamonds))
        # print("Trefle (♣):", ' '.join(clubs))
        # print()
        spades = spades[0].split()
        hearts = hearts[0].split()
        diamonds = diamonds[0].split()
        clubs = clubs[0].split()
        # print("Punkty: ", calculate_points(spades, hearts, diamonds, clubs))
        # print("Układ: ", shape(spades, hearts, diamonds, clubs))
        # print()
        hand = []
        hand.append(spades)
        hand.append(hearts)
        hand.append(diamonds)
        hand.append(clubs)
        hand.append(calculate_points(spades, hearts, diamonds, clubs))
        hand.append(shape(spades, hearts, diamonds, clubs))
        hands.append(hand)

    return hands, can_play

#scrap(url)