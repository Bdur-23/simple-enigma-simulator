"""
Wikipedia: https://en.wikipedia.org/wiki/Enigma_machine

This module contains function 'enigma' which emulates
the famous Enigma machine from WWII.
Module includes:
- enigma function
- showcase of function usage
- 9 randomly generated rotors
- reflector (aka static rotor)
- original alphabet
"""
from __future__ import annotations

RotorPositionT = tuple[int, int, int]
RotorSelectionT = tuple[str, str, str]


# used alphabet --------------------------
# from string.ascii_uppercase
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# -------------------------- default selection --------------------------
# rotors --------------------------
rotor1 = "EGZWVONAHDCLFQMSIPJBYUKXTR"
rotor2 = "FOBHMDKEXQNRAULPGSJVTYICZW"
rotor3 = "ZJXESIUQLHAVRMDOYGTNFWPBKC"
# reflector --------------------------
reflector = {
    "A": "N",
    "N": "A",
    "B": "O",
    "O": "B",
    "C": "P",
    "P": "C",
    "D": "Q",
    "Q": "D",
    "E": "R",
    "R": "E",
    "F": "S",
    "S": "F",
    "G": "T",
    "T": "G",
    "H": "U",
    "U": "H",
    "I": "V",
    "V": "I",
    "J": "W",
    "W": "J",
    "K": "X",
    "X": "K",
    "L": "Y",
    "Y": "L",
    "M": "Z",
    "Z": "M",
}

# -------------------------- extra rotors --------------------------
rotor4 = "RMDJXFUWGISLHVTCQNKYPBEZOA"
rotor5 = "SGLCPQWZHKXAREONTFBVIYJUDM"
rotor6 = "HVSICLTYKQUBXDWAJZOMFGPREN"
rotor7 = "RZWQHFMVDBKICJLNTUXAGYPSOE"
rotor8 = "LFKIJODBEGAMQPXVUHYSTCZRWN"
rotor9 = "KOAEGVDHXPQZMLFTYWJNBRCIUS"
rotor_list = [rotor1, rotor2, rotor3, rotor4, rotor5, rotor6, rotor7, rotor8, rotor9]


def _validator(
    rotpos: RotorPositionT, rotsel: RotorSelectionT, pb: str
) -> tuple[RotorPositionT, RotorSelectionT, dict[str, str]]:
    """
    Checks if the values can be used for the 'enigma' function

    >>> _validator((1,1,1), (rotor1, rotor2, rotor3), 'POLAND')
    ((1, 1, 1), ('EGZWVONAHDCLFQMSIPJBYUKXTR', 'FOBHMDKEXQNRAULPGSJVTYICZW', \
'ZJXESIUQLHAVRMDOYGTNFWPBKC'), \
{'P': 'O', 'O': 'P', 'L': 'A', 'A': 'L', 'N': 'D', 'D': 'N'})

    :param rotpos: rotor_positon
    :param rotsel: rotor_selection
    :param pb: plugb -> validated and transformed
    :return: (rotpos, rotsel, pb)
    """
    # Checks if there are 3 unique rotors

    unique_rotsel = len(set(rotsel))
    if unique_rotsel < 3:
        raise Exception(f"Please use 3 unique rotors (not {unique_rotsel})")

    # Checks if rotor positions are valid
    rotorpos1, rotorpos2, rotorpos3 = rotpos
    if not 0 < rotorpos1 <= len(abc):
        raise ValueError(
            "First rotor position is not within range of 1..26 (" f"{rotorpos1}"
        )
    if not 0 < rotorpos2 <= len(abc):
        raise ValueError(
            "Second rotor position is not within range of 1..26 (" f"{rotorpos2})"
        )
    if not 0 < rotorpos3 <= len(abc):
        raise ValueError(
            "Third rotor position is not within range of 1..26 (" f"{rotorpos3})"
        )

    # Validates string and returns dict
    pbdict = _plugboard(pb)

    return rotpos, rotsel, pbdict


def _plugboard(pbstring: str) -> dict[str, str]:
    if not isinstance(pbstring, str):
        raise TypeError(f"Plugboard setting isn't type string ({type(pbstring)})")
    elif len(pbstring) % 2 != 0:
        raise Exception(f"Odd number of symbols ({len(pbstring)})")
    elif pbstring == "":
        return {}

    pbstring.replace(" ", "")

    # Checks if all characters are unique
    tmppbl = set()
    for i in pbstring:
        if i not in abc:
            raise Exception(f"'{i}' not in list of symbols")
        elif i in tmppbl:
            raise Exception(f"Duplicate symbol ({i})")
        else:
            tmppbl.add(i)
    del tmppbl

    # Created the dictionary
    pb = {}
    for j in range(0, len(pbstring) - 1, 2):
        pb[pbstring[j]] = pbstring[j + 1]
        pb[pbstring[j + 1]] = pbstring[j]

    return pb


def enigma(
    text: str,
    rotor_position: RotorPositionT,
    rotor_selection: RotorSelectionT = (rotor1, rotor2, rotor3),
    plugb: str = "",
) -> str:

    text = text.upper()
    rotor_position, rotor_selection, plugboard = _validator(
        rotor_position, rotor_selection, plugb.upper()
    )

    rotorpos1, rotorpos2, rotorpos3 = rotor_position
    rotor1, rotor2, rotor3 = rotor_selection
    rotorpos1 -= 1
    rotorpos2 -= 1
    rotorpos3 -= 1

    result = []

    # encryption/decryption process --------------------------
    for symbol in text:
        if symbol in abc:

            # 1st plugboard --------------------------
            if symbol in plugboard:
                symbol = plugboard[symbol]

            # rotor ra --------------------------
            index = abc.index(symbol) + rotorpos1
            symbol = rotor1[index % len(abc)]

            # rotor rb --------------------------
            index = abc.index(symbol) + rotorpos2
            symbol = rotor2[index % len(abc)]

            # rotor rc --------------------------
            index = abc.index(symbol) + rotorpos3
            symbol = rotor3[index % len(abc)]

            # reflector --------------------------
            # this is the reason you don't need another machine to decipher

            symbol = reflector[symbol]

            # 2nd rotors
            symbol = abc[rotor3.index(symbol) - rotorpos3]
            symbol = abc[rotor2.index(symbol) - rotorpos2]
            symbol = abc[rotor1.index(symbol) - rotorpos1]

            # 2nd plugboard
            if symbol in plugboard:
                symbol = plugboard[symbol]

            # moves/resets rotor positions
            rotorpos1 += 1
            if rotorpos1 >= len(abc):
                rotorpos1 = 0
                rotorpos2 += 1
            if rotorpos2 >= len(abc):
                rotorpos2 = 0
                rotorpos3 += 1
            if rotorpos3 >= len(abc):
                rotorpos3 = 0

        result.append(symbol)

    return "".join(result)


if __name__ == "__main__":
    while True:
        message = input('enter: ')
        #rotor_pos = (1,1,1)
        rotor_pos = tuple([int(i) for i in input('enter 3 with space max 26: ').split(' ')[:3]])
        pb = "pictures"
        #rotor_sel = (rotor1, rotor5, rotor3)
        rotor_sel = tuple([rotor_list[int(i)-1] for i in input('enter 3 with space max 9: ').split(' ')[:3]])
        en = enigma(message, rotor_pos, rotor_sel, pb)

        print("Encrypted message:", en)
        print("Decrypted message:", enigma(en, rotor_pos, rotor_sel, pb))
