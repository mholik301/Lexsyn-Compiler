import sys  # ucitavanje podataka
from collections import OrderedDict  # deterministicka varijanta rijecnika


# ------------FUNKCIJE
def korak(konfig, ulazL, pravila):
    # dobiva konfiguraciju, ulaz i pravila
    # napravi "korak" i modificira konfiguraciju
    # ako uspije (postoji valjani prijelaz) vrati True
    # ako ne uspije (ne postoji valjani prijelaz) vrati False

    # red je implementiran preko liste:
    # queue = []
    # queue.append('a')
    # queue.pop(0)

    stanje = konfig[0]
    # stog = konfig[1]
    try:
        vrhStog = konfig[1].pop(0)
        # ako je stog prazan vracamo False
    except IndexError:
        return False
    ulaz = ulazL[0]

    # kljuc rijecnika pravila
    PocStanjeUlazStog = (stanje, ulaz, vrhStog)
    # ako za trenutni kljuc (stanje, ulaz, stog) ima prijelaz stavi novi konfig u NovoStanjeStog
    # inace novi konfig NovoStanjeStog ostavi prazan
    NovoStanjeStog = pravila.get(PocStanjeUlazStog, '')

    # ako nema prijelaza za trenutnu konfiguraciju vrati False
    if not NovoStanjeStog:
        konfig[1].insert(0, vrhStog)
        return False
    # inace promjeni konfiguraciju i vrati True
    else:
        konfig[0] = NovoStanjeStog[0]
        for stanje in reversed(NovoStanjeStog[1]):
            if (stanje != '$'):
                konfig[1].insert(0, stanje)
        return True


def epsilonKorak(konfig, pravila):
    # dobiva konfiguraciju, ulaz i pravila
    # napravi "korak" i modificira konfiguraciju
    # ako uspije (postoji valjani prijelaz) vrati True
    # ako ne uspije (ne postoji valjani prijelaz) vrati False

    # red je implementiran preko liste:
    # queue = []
    # queue.append('a')
    # queue.pop(0)

    stanje = konfig[0]
    # stog = konfig[1]
    try:
        vrhStog = konfig[1].pop(0)
        # ako je stog prazan vracamo False
    except IndexError:
        return False
    ulaz = '$'

    # kljuc rijecnika pravila
    PocStanjeUlazStog = (stanje, ulaz, vrhStog)
    # ako za trenutni kljuc (stanje, ulaz, stog) ima prijelaz stavi novi konfig u NovoStanjeStog
    # inace novi konfig NovoStanjeStog ostavi prazan
    NovoStanjeStog = pravila.get(PocStanjeUlazStog, '')

    # ako nema prijelaza za trenutnu konfiguraciju vrati False
    if not NovoStanjeStog:
        return False
    # inace promjeni konfiguraciju i vrati True
    else:
        konfig[0] = NovoStanjeStog[0]
        for stanje in reversed(NovoStanjeStog[1]):
            if (stanje != '$'):
                konfig[1].insert(0, stanje)
        return True


def korakIspis(konfig, znak, pravila):
    uspjelo = korak(konfig, znak, pravila)
    if (uspjelo):
        konfiguracijaIspis(konfig)
        return 1

    uspjelo = epsilonKorak(konfig, pravila)
    if (uspjelo):
        konfiguracijaIspis(konfig)
        return 2
    else:
        print('fail|0')
    return 0


def prihvatljiva(konfig):
    # ako je konacna konfiguracija prihvatljivaSt vrati True
    if konfig[0] in prihvatljivaSt:
        return True
    # inace vrati False
    else:
        return False


def prihvatljivaIspis(konfig):
    # ako je konacna konfiguracija prihvatljivaSt ispisi 1
    if konfig[0] in prihvatljivaSt:
        print('1', end='\n')
    # inace ispisi 0
    else:
        print('0', end='\n')


def konfiguracijaIspis(konfig):
    # ispisuje konfiguraciju

    stanje = konfig[0]
    stog = konfig[1]

    print(stanje + '#', end='')

    # ako je stog prazan ispisi $
    if not stog:
        print('$', end='')
    # ako stog nije prazan ispisi ga
    else:
        for stanje in stog:
            print(stanje, end='')

    # korak terminiramo sa |
    print('|', end='')


def nijeKrajLinije(a):
    # vraca istinu ako ulazni znak a != '\n', '\\' and ';'
    if a[0] != '\n' and a[0] != '\\' and a[0] != ';':
        return True
    return False


def stanje(konfig):
    stanje = konfig[0]
    return stanje


def vrhStoga(konfig):
    vrhStoga = konfig[1]
    if not stog:
        return ''
    else:
        return vrhStoga[0]


# ------------UCITAVANJE
"""ucitavamo podatake"""
file = list()
#file = sys.stdin.readlines()


file = [
    "a,b,a,b,b,b|a,b,b,a|b,b,a|a,a,b,b,b,b|a,b,b,b,a,b;",
    "p0,p1,p2;",
    "a,b;",
    "K,A;",
    "p2;",
    "p0;",
    "K;",
    "p0,a,K->p1,AAK;",
    "p1,a,A->p1,AAA;",
    "p1,b,A->p1,$;",
    "p1,$,K->p2,K;"
]


"""
# inicijalni ispis: "inicijalnoStanje#inicijalniZnakStoga|"
# ispis za svaki ulazni znak (nakon prijelaza): "stanje#stog|"
# ako je stog prazan ispisuje se $

# ako ne postoji prijelaz za trenutni par stanje#stog+ulaz ispisujemo "fail|0"

# ispis nakon cijelog ulaznog niza: 0 ili 1 (konacno stanje prihvatljivo ili nije)
# nakon obrade prihvatljivog niza ispisujemo samo onu konfig u kojoj je ostvaren uvijet prihvatljivosti
# ne ispisujemo epsilon prijelaze nakon obrade cijelog niza

# rezultat za svaki niz ide u novi red
"""

# konstante
ULAZI = 0
STANJA = 1
ABCUL = 2
ABCST = 3
PRIH = 4
POCSTANJE = 5
POCSTOG = 6
FUNK = 7

"""gradimo ulaze"""
ulazi = list()  # 2D polje ulaznih nizova
tmpString = str()
i = 0
while nijeKrajLinije(file[ULAZI][i]):
    niz = list()
    while file[ULAZI][i] != '|' and nijeKrajLinije(file[ULAZI][i]):
        tmpString = str()
        while file[ULAZI][i] != ',' and file[ULAZI][i] != '|' and nijeKrajLinije(file[ULAZI][i]):
            tmpString += file[ULAZI][i]
            i += 1
        niz.append(tmpString)
        if file[ULAZI][i] == ',':
            i += 1
    ulazi.append(niz)
    if file[ULAZI][i] == '|':
        i += 1

'''
"""gradimo stanja"""
stanja = list()
tmpString = str()
i = 0
while nijeKrajLinije(file[STANJA][i]):
    while file[STANJA][i] != ',' and nijeKrajLinije(file[STANJA][i]):
        tmpString += file[STANJA][i]
        i += 1
    stanja.append(tmpString)
    if nijeKrajLinije(file[STANJA][i]):
        i += 1
        tmpString = ""
stanja.sort()

"""gradimo abecedu ulaza"""
abecedaUl = list()
tmpString = str()
i = 0
while nijeKrajLinije(file[ABCUL][i]):
    while file[ABCUL][i] != ',' and nijeKrajLinije(file[ABCUL][i]):
        tmpString += file[ABCUL][i]
        i += 1
    abecedaUl.append(tmpString)
    if nijeKrajLinije(file[ABCUL][i]):
        i += 1
        tmpString = ""
abecedaUl.sort()

"""gradimo abecedu stoga"""
abecedaSt = list()
tmpString = str()
i = 0
while nijeKrajLinije(file[ABCST][i]):
    while file[ABCST][i] != ',' and nijeKrajLinije(file[ABCST][i]):
        tmpString += file[ABCST][i]
        i += 1
    abecedaSt.append(tmpString)
    if nijeKrajLinije(file[ABCST][i]):
        i += 1
        tmpString = ""
abecedaSt.sort()
'''

"""gradimo prihvatljivaSt"""
prihvatljivaSt = list()
tmpString = str()
i = 0
while nijeKrajLinije(file[PRIH][i]):
    while file[PRIH][i] != ',' and nijeKrajLinije(file[PRIH][i]):
        tmpString += file[PRIH][i]
        i += 1
    prihvatljivaSt.append(tmpString)
    if nijeKrajLinije(file[PRIH][i]):
        i += 1
        tmpString = ""
prihvatljivaSt.sort()

"""gradimo pocetno stanje"""
i = int()
pocetnoStanje = str()
while nijeKrajLinije(file[POCSTANJE][i]):
    pocetnoStanje += file[POCSTANJE][i]
    i += 1

"""gradimo pocetno stanje stoga"""
i = int()
pocetnoStanjeSt = str()
while nijeKrajLinije(file[POCSTOG][i]):
    pocetnoStanjeSt += file[POCSTOG][i]
    i += 1

"""gradimo dict pravila"""
pravila = OrderedDict()
for i in range(FUNK, len(file)):
    # ucitavanje izvornog string zapisa pravila
    praviloRaw = file[i]

    # gradimo pocetno stanje pravila
    j = 0
    tmpPocetno = str()
    while praviloRaw[j] != ',':
        tmpPocetno += praviloRaw[j]
        j += 1

    j += 1  # preskoci ,

    # gradimo ulazni znak tog prijelaza
    tmpUlaz = str()
    while praviloRaw[j] != ',':
        tmpUlaz += praviloRaw[j]
        j += 1

    j += 1  # preskoci ,

    # gradimo pocetni znak stoga pravila
    tmpStog = str()
    while praviloRaw[j] != '-':
        tmpStog += praviloRaw[j]
        j += 1

    j += 2  # preskoci ->

    # gradimo novo stanje pravila
    tmpNovoStanje = str()
    while praviloRaw[j] != ',':
        tmpNovoStanje += praviloRaw[j]
        j += 1

    j += 1  # preskoci ,

    # gradimo novi znak stoga
    tmpNovoZnStoga = str()
    while (nijeKrajLinije(praviloRaw[j])):
        tmpNovoZnStoga += praviloRaw[j]
        j += 1

    # pocetno stanje, znak prijelaza i znak stoga cine kljuc rijecnika pravlia
    PocStanjeUlazStog = (tmpPocetno, tmpUlaz, tmpStog)

    # novo stanje i znak stoga cine vrijednost rijecnika pravlia
    NovoStanjeStog = (tmpNovoStanje, tmpNovoZnStoga)

    # dodajemo pravilo u rijecnik
    pravila[PocStanjeUlazStog] = NovoStanjeStog


# ------------POSAO

# za svaki ulazni niz
for ulaz in ulazi:

    # postavi automat i ispisi inicijalnu konfiguraciju
    stog = [pocetnoStanjeSt]
    konfig = [pocetnoStanje, stog]
    konfiguracijaIspis(konfig)
    uspjelo = 1

    # za svaki znak niza
    for znak in ulaz:
        while(uspjelo != 0):
            # napravi korak i ispisi novu konfiguraicju
            uspjelo = korakIspis(konfig, znak, pravila)
            # ako je napravljen epsilon korak ponovno probaj isti ulazni znak
            # inace izadji
            if (uspjelo != 2):
                break

    # nakon prolaza kroz sve clanove ulaznog niza
    if (uspjelo):
        # ako je konacno stanje prihvatljivo ispisi ga
        if (prihvatljiva(konfig)):
            prihvatljivaIspis(konfig)

        # inace jos probaj epsilon tranzicije
        else:
            while(1):
                if (stanje(konfig), '$', vrhStoga(konfig)) in pravila.keys():
                    uspjelo = korakIspis(konfig, '$', pravila)
                    if (prihvatljiva(konfig)):
                        break
                else:
                    break
            prihvatljivaIspis(konfig)


# print('\n', end='')

sys.exit()
