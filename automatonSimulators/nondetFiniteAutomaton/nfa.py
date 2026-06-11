import sys


def setPocetno(pocetnoStanje, pravila):
    # vraca i ispisuje set sa s0 i njegovim e-prijelazima

    trenutnaStanja = {pocetnoStanje, }
    pocetnoStanjeSE = eOkolina(trenutnaStanja, pravila)
    ispis(pocetnoStanjeSE)

    return pocetnoStanjeSE


def dodajSusjede(trenutnaStanja, pravila, ulaz='$'):
    # dobiva set stanja i dodaje im:
    # 1 e-okolinu, ako ne proslijedimo ulaz
    # 2 susjede preko ulaza, ako proslijedmo ulaz

    # red je implementiran preko liste:
    # queue = []
    # queue.append('a')
    # queue.pop(0)

    if ulaz == '$':  # ako trazimo e okolinu tada ostavljamo trenutna stanja u rjesenju
        nadopunjena = trenutnaStanja.copy()
    else:  # inace samo susjede stavljamo u rj
        nadopunjena = set()

    nadopunjenaQ = trenutnaStanja.copy()  # trenutna stanja stavimo u red
    nadopunjenaQ = list(nadopunjenaQ)  # red simuliramo listom
    stanje = str()
    while 1:
        try:
            # skidamo jedno po jedno 'trenutno' stanje
            stanje = nadopunjenaQ.pop(0)
        except IndexError:  # kad ih vise nema izlazimo
            break

        # pomocu pravila pronalazimo e-susjede
        stanjeUlaz = (stanje, ulaz)
        # ako za trenutni kljuc (stanje, ulaz) ima prijelaza stavi ih u listu, inace ju ostavi praznu
        eSusjedi = [pravila.get(stanjeUlaz, '')]
        # # .setdefault() ne radi to sto trebam
        # # On je kao get s drugim arg, aka stavlja key/value pair u dict ako ne postoje
        """Ovo je potrebno ako je setdefault = None
        try:
            # micemo None iz skupa susjeda
            eSusjedi.remove(None)
        except ValueError:
            pass
        """
        # nove susjede stavljamo u nadopunjenu listu
        for susjed in eSusjedi:
            for stanje in susjed:
                nadopunjena.add(stanje)

    return nadopunjena


def eOkolina(trenutnaStanja, pravila):
    # vraca e-okolinu trenutnih stanja koristeci dodajSusjede()
    # zove dodajSusjede() sve dok ona pronalazi nove susjede

    trenutnaStanjaESet = set()
    trenutnaStanjaSet = set()
    difNum = int(1)
    while difNum != 0:  # dok pronalazimo nova stanja
        for clan in trenutnaStanjaESet:
            trenutnaStanjaSet.add(clan)
        trenutnaStanjaE = dodajSusjede(
            trenutnaStanja, pravila)  # zovi dodajSusjede()
        for clan in trenutnaStanjaE:
            trenutnaStanjaESet.add(clan)
        # usporedi stanja prije i poslije zvanja dodajSusjede()
        dif = trenutnaStanjaESet.difference(trenutnaStanjaSet)
        trenutnaStanja = trenutnaStanjaE
        difNum = len(dif)

    return trenutnaStanjaE


def ispis(novaStanjaKorakE, ulazi=",", j=0):
    # ispisuje sva stanja u poslanoj listi/setu u trazenom formatu
    # takodjer namjesta brojac c na sljedeci ulazni znak
    # podrazumjevani parametri se koriste kod ispisa pocetnog stanja

    if len(novaStanjaKorakE) == 0:
        print("#", end='')
    else:
        flag2 = False  # need to print ','?
        novaStanjaKorakE = sorted(novaStanjaKorakE)
        for x in novaStanjaKorakE:
            if flag2 is not False:
                print(',', end='')
            if flag2 is False:
                flag2 = True
            if 1:
                print(x, end='')

    if ulazi[j] == ',':
        j += 1
        print('|', end='')
    elif ulazi[j] == '|':
        j += 1
        print('\n', end='')
    return j


"""ucitavamo podatake"""
file = list()
file = sys.stdin.readlines()

ulazi = file[0]
# stanja = file[1]
# abeceda = file[2]
# prihvatljiva = file[3]
i = int()

pocetnoStanje = str()
while file[4][i] != '\n' and file[4][i] != '\\' and file[4][i] != ';':
    pocetnoStanje += file[4][i]
    i += 1


"""gradimo dict pravila"""
pravila = dict()
for i in range(5, len(file)):
    praviloRaw = file[i]  # izvorni string zapis pravila

    j = 0
    pocetno = str()
    while praviloRaw[j] != ',':  # gradimo pocetno stanje
        pocetno += praviloRaw[j]
        j += 1
    j += 1  # preskoci ,
    ulaz = str()
    while praviloRaw[j] != '-':  # gradimo ulaz
        ulaz += praviloRaw[j]
        j += 1
    j += 2  # preskoci ->

    novaStanja = set()  # gradimo set novih stanja
    while praviloRaw[j] != '\n' and praviloRaw[j] != '\\' and praviloRaw[j] != ';':
        tmpString = str()
        while praviloRaw[j] != ',' and praviloRaw[j] != '\n'and praviloRaw[j] != '\\' and praviloRaw[j] != ';':
            tmpString += praviloRaw[j]
            j += 1
        if praviloRaw[j] == ',':
            j += 1
        if tmpString != "#":
            novaStanja.add(tmpString)

    # stanjeUlazPar = {pocetno, ulaz} doesn't work because sets aren't hashable
    stanjeUlazPar = (pocetno, ulaz)

    pravila[stanjeUlazPar] = novaStanja  # gradimo dict pravila


trenutnaStanja = setPocetno(pocetnoStanje, pravila)


"""trazimo i ispisujemo stanja za svaki ulazni niz"""
j = 0
while ulazi[j] != '\n' and ulazi[j] != '\\' and ulazi[j] != ';':
    trenutniUlaz = str()
    while ulazi[j] != ',' and ulazi[j] != '\n' and ulazi[j] != '\\' and ulazi[j] != ';' and ulazi[j] != '|':
        trenutniUlaz += ulazi[j]
        j += 1

    # trenutna stanja s e okolinom
    trenutnaStanjaSE = eOkolina(trenutnaStanja, pravila)

    # nova stanja s preko ulaza
    novaStanjaKorak = dodajSusjede(trenutnaStanjaSE, pravila, trenutniUlaz)

    # nova stanja s preko ulaza s e okolinom
    novaStanjaKorakSE = eOkolina(novaStanjaKorak, pravila)

    # kada krece novi ulazni niz resetiramo automat
    if ulazi[j] == '|':
        j = ispis(novaStanjaKorakSE, ulazi, j)
        trenutnaStanja = setPocetno(pocetnoStanje, pravila)
    # a inace nastavljamo obradjivati trenutni niz
    else:
        j = ispis(novaStanjaKorakSE, ulazi, j)
        trenutnaStanja = novaStanjaKorakSE


print('\n', end='')

sys.exit()
