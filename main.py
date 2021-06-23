# Diese Methode rendert das Hauptmenü
def main_menu():
    # Spiel-Logo
    print(" ______   __     ______        ______   ______     ______        ______   ______     ______    \n" +
          "/\\__  _\\ /\\ \\   /\\  ___\\      /\\__  _\\ /\\  __ \\   /\\  ___\\      /\\__  _\\ /\\  __ \\   /\\  ___\\   \n" +
          "\\/_/\\ \\/ \\ \\ \\  \\ \\ \\____     \\/_/\\ \\/ \\ \\  __ \\  \\ \\ \\____     \\/_/\\ \\/ \\ \\ \\/\\ \\  \\ \\  __\\   \n" +
          "   \\ \\_\\  \\ \\_\\  \\ \\_____\\       \\ \\_\\  \\ \\_\\ \\_\\  \\ \\_____\\       \\ \\_\\  \\ \\_____\\  \\ \\_____\\ \n" +
          "    \\/_/   \\/_/   \\/_____/        \\/_/   \\/_/\\/_/   \\/_____/        \\/_/   \\/_____/   \\/_____/ ")
    print("     v1.1")
    print("\n   Geben Sie \"start\" ein, um das Spiel zu starten, oder \"help\", um alle Befehle zu sehen.\n")

    # User Eingabe
    is_menu = True
    while is_menu:
        x = input("> ")
        if x.lower() == "start":
            is_menu = False
        elif x.lower() == "help":
            print("\nFolgende Commands sind verfügbar:\n" +
                  "     help, start, info\n")
        elif x.lower() == "info":
            print(
                "\nDieses Spiel wurde von proffessionellen Profis im Programmierprofisein programmiert.\n" +
                "Es ist ein simples Tic Tac Toe. Der Programmcode ist aber faszinierend!\n")


# Rendert das Spielfeld in einem 3x3 Grid (Raster)
def render(originalField):
    # Eine leere Kopie der Karte anfertigen, damit man
    # nicht die Originale überschreibt
    field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Ersetzt alle Zahlen gegen Spielcharaktere
    for y in range(0, len(originalField)):
        for x in range(0, len(originalField[y])):
            field[y][x] = translate_to_char(originalField[y][x])

    # Bildschirm frei machen
    print("\n" * 50)
    
    # Gibt das Spielfeld aus
    print("\n       A         B         C     \n\n" +
          "            ║         ║         \n" +
          "1      " + str(field[0][0]) + "    ║    " + str(field[0][1]) + "    ║    " + str(field[0][2]) + "    \n" +
          "            ║         ║         \n" +
          "   ═════════╬═════════╬═════════\n" +
          "            ║         ║         \n" +
          "2      " + str(field[1][0]) + "    ║    " + str(field[1][1]) + "    ║    " + str(field[1][2]) + "    \n" +
          "            ║         ║         \n" +
          "   ═════════╬═════════╬═════════\n" +
          "            ║         ║         \n" +
          "3      " + str(field[2][0]) + "    ║    " + str(field[2][1]) + "    ║    " + str(field[2][2]) + "    \n" +
          "            ║         ║         \n")


# Diese Methode übersetzt die PlayerId in einen Spielcharakter (x oder o)
def translate_to_char(playerId):
    if playerId == 0:
        return " "
    elif playerId == 1:
        return "X"
    elif playerId == 2:
        return "O"
    else:
        raise Exception("PlayerId was " + playerId)


# Diese Methode übersetzt einen Buchstaben in eine Zahl
def translate_to_digit(char):
    alpha = char.lower()

    # Buchstaben zu Zahlen übersetzen
    if alpha == "a":
        return 1
    elif alpha == "b":
        return 2
    elif alpha == "c":
        return 3
    return -1


# Diese Methode verarbeitet die Nutzereingabe (User Input)
def await_user_input(playerId, field):
    # Eingabe vom Spieler erwarten
    command = input("Spieler " + str(playerId) + " ist am Zug > ")  # z. B. 1A

    # Überprüfen, ob der Spieler wirklich 2 Zeichen eingegeben hat
    if len(command) != 2:
        print("Diese Eingabe war nicht richtig! Du musst eine Zahl und einen Buchstaben eingeben.")
        await_user_input(playerId, field)
        return

    # Smart Input System = SIS
    if command[0].isdigit() and command[1].isalpha():
        y = int(command[0])
        x = translate_to_digit(command[1])
    elif command[1].isdigit() and command[0].isalpha():
        y = int(command[1])
        x = translate_to_digit(command[0])
    else:
        print("Du blöde bist! Du eins Zahl und eins Buchstabe eingeben musst.")
        await_user_input(playerId, field)
        return

    # Überprüfen, ob Eingabe richtig war
    if not 0 < x or not 0 < y < 4:
        print("Diese Stelle existiert nicht auf dem Spielfeld!")
        await_user_input(playerId, field)
        return

    # Dieser Block schützt vor Overrides
    state = field[y - 1][x - 1]
    if state == 0:
        # Das Feld wird gesetzt
        field[y - 1][x - 1] = playerId
    else:  # Wenn bereits eine SpielerId an dieser Stelle vorliegt, muss der Spieler eine andere Koordinate wählen
        print("An dieser Stelle hat bereits ein Spieler einen Stein gesetzt! Versuche eine andere Stelle...")
        await_user_input(playerId, field)


# Prüft, ob ein Spieler playerId das Spiel gewonnen hat
def has_won(playerId, field):
    # Liste aller Gewinnmöglichkeiten
    win = [[[0, 0], [1, 0], [2, 0]],
           [[0, 1], [1, 1], [2, 1]],
           [[0, 2], [1, 2], [2, 2]],
           [[0, 0], [0, 1], [0, 2]],
           [[1, 0], [1, 1], [1, 2]],
           [[2, 0], [2, 1], [2, 2]],
           [[0, 0], [1, 1], [2, 2]],
           [[0, 2], [1, 1], [2, 0]]]

    won = False

    # Wir gehen nun alle 8 Möglichkeiten durch
    for situation in win:
        for i in range(len(situation)):  # Vom Szenario testen wir alle Felder
            y = situation[i][0]
            x = situation[i][1]

            # Prüfen, ob das Feld die PlayerId hat
            if field[y][x] == playerId:
                if i == (len(situation) - 1):
                    won = True
                    break
                else:
                    continue
            else:
                break  # Wenn nicht, dann ist dieses Szenario fehlgeschlagen

        if won:
            break

    return won


# Prüft, ob noch Züge gemacht werden können
def turns_avaible(field):
    for y in field:
        for x in y:
            if x == 0:
                return True

    return False


# Main Methode
# Dies ist die Logik des gesamten Spiels
def main():
    running = True
    main_menu()
    field = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    render(field)
    while running:
        await_user_input(1, field)
        render(field)
        if has_won(1, field):
            print("Spieler 1 hat gewonnen!")
            break
        elif not turns_avaible(field):  # Kann nur bei Spieler 1 auftreten, weil er immer der 9. Zug ist
            print("Unentschieden! Entweder habt ihr beide gleich gut oder gleich schlecht gespielt. :)")
            break
        await_user_input(2, field)
        render(field)
        if has_won(2, field):
            print("Spieler 2 hat gewonnen!")
            break

        # Dieser Block ist auskommentiert, weil er nie ausgeführt werden könnte
        # elif not turns_avaible(field):
        #    print("Unentschieden! Entweder habt ihr beide gleich gut oder gleich schlecht gespielt. :)")
        #    break


# Definiert die main Methode als Startpunkt
if __name__ == '__main__':
    main()
