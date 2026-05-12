# zmienne globalne

#zmienna typu bool przechowuje informacje czy użytkownik jest zalogowany. (False - nie zalogowany | True - zalogowany)
isLoggedIn = False

# zmienna trzymająca numer id zalogowanego urzytkownika
userID = 0

# zmienna przchowuje czy użytkownik jest adminem
isAdmin = False

# przyszła funkcja do sprawdzania czy to admin
def checkAdmin():
    return False