import sys  # ucitavanje podataka
from collections import OrderedDict  # deterministicka varijanta rijecnika

#region -----TESTING
#python Lab2project.py < primjer.in > izlaz.out
#FC izlaz.out primjer.out
#endregion


#region -----POMOCNE KLASE
class Cestica:
    """ulazna cestica"""

    #[sifra uniformnog znaka, broj linije, tekst cestice]
    def __init__(self, sif, red, tekst):
        #ovo instancira ulazna funkcija ulazToList
        self.sif = str(sif)
        self.red = int(red)
        self.tekst = str(tekst)
        self.razina = 0

    def getSif(self):
        return self.sif

    def getRed(self):
        return self.red

    def getTekst(self):
        return self.tekst

    def isInPrimijeni(self, primijeni):
        #prima skup PRIMIJENI
        #vraca true ako je pozvana nad cesticom iz predanog skupa, inace false

        sif = self.getSif()

        if any(sif in s for s in primijeni):
            return True
        return False

    def isEndl(self):
        return True if self.getTekst() == "endl" else False

    def isNotEndl(self):
        return False if self.getTekst() == "endl" else True

    def ispis(self):
        identifikatorCestice = self.getSif()
        linijaCestice = str(self.getRed())
        tekstCestice = self.getTekst()
        razina = self.razina
        print(razina * ' ' + identifikatorCestice + " " + linijaCestice + " " + tekstCestice,  end='\n')


class Cvor:
    """cvor stabla, odnosno nezavrsni znak"""

    def __init__(self, ime, razina):
        #ovo instancira potprogram nezavrsnog znaka koji ujedno proslijedi i
        #ime te popuni listu
        self.ime = ime
        self.razina = razina

    def getIme(self):
        return self.ime

    def getRazina(self):
        return self.razina

    def ispis(self):
        print(self.getRazina() * ' ' + self.getIme(), end='\n')

#instanca = neza("S", 2)
#razina = instacna.getRazina
#endregion


#region -----FUNKCIJE
def nijeKrajLinije(a):
    # vraca istinu ako ulazni znak a != '\n', '\\' and ';'
    if a[0] != '\n' and a[0] != '\\' and a[0] != ';':
        return True
    return False

def ulazToList(ulazRaw):
    #prima cisti ulaz i vraca list Cestica
    
    cestice = list()

    for linija in ulazRaw:
        if len(linija) > 0:
            podaci = linija.split(" ")
            sif = podaci[0].strip()
            red = podaci[1].strip()
            tekst = podaci[2].strip()

            cestica = Cestica(sif, red, tekst)

            cestice.append(cestica)

    return cestice


def ispisStabla():
    # ispisuje stablo u zadanom formatu

    for list in stablo:
        if isinstance(list, Cestica):
            list.__class__ = Cestica
            list.ispis()
        elif isinstance(list, Cvor):
            list.__class__ = Cvor
            list.ispis()
        else:
            raise Exception("type error")
            
def getUlaz():
    #dohvaca sljedecu ulaznu cesticu
    if brojilo in range(-len(ulazCestice), len(ulazCestice)):
        return ulazCestice[brojilo]
    else:
        #ako smo procitali sve ulazne cestice vracamo "endl"
        return Cestica("ENDL", 0, "endl")


def provjeriZavrsni(razina, trazeni):
    #provjerava odgovara li prosljedjeni znak cestici na ulazu
    #ako da, dodaje cesticu u stablu i cita sljedecu ulaznu cesticu
    #ako ne, baca iznimku
    ulaz = getUlaz()
    ulazStr = ulaz.getSif()

    strazeni = str(trazeni)

    if ulazStr == trazeni:
        ulaz.razina = razina + 1
        stablo.append(ulaz) #dodavanje zavrsnog znaka u stablo
        global brojilo #prebacujemo se na sljedecu ulaznu leksicku jedinku
        brojilo = brojilo + 1
    else:
        handleException(ulaz)


def handleException(ulaz):
    if ulaz.isEndl():
        raise Exception("err kraj")
    else:
        raise Exception("err " + ulaz.getSif() + " " + str(ulaz.getRed()) + " " + ulaz.getTekst())
#endregion


#region -----POTPROGRAMI NEZAVRSNIH ZNAKOVA
#stvore cesticu (ime, razina++)
def P_program(razina=0):
    imeNezavrsnog = "<program>"
    PRIMIJENI1 = ['IDN', 'KR_ZA', 'ENDL']

    #dodavanje cvora u stablo
    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)




    #odabir prave produkcije na temelju trenutnog ulaza i skupova PRIMIJENI
    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):

        P_lista_naredbi(razina + 1)

    else:
        #ulaz ne odgovara niti jednom PRIMIJENI skup -> error
        handleException(ulaz)
    



    #pocetni nezavrsni provjera jesmo li procitali sve ulazne cestice
    #ako nismo ispisuje se error radi "viska" cestice
    if brojilo < len(ulazCestice):
        handleException(ulaz)
    
    return None

def P_lista_naredbi(razina):
    imeNezavrsnog = "<lista_naredbi>"
    PRIMIJENI1 = ['IDN', 'KR_ZA']
    PRIMIJENI2 = ['KR_AZ', 'ENDL']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        P_naredba(razina + 1)
        P_lista_naredbi(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI2):
        cvor = Cvor("$", razina + 1)
        stablo.append(cvor)

    else:
        handleException(ulaz)

    return None

def P_naredba(razina):
    imeNezavrsnog = "<naredba>"
    PRIMIJENI1 = ['IDN']
    PRIMIJENI2 = ['KR_ZA']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        P_naredba_pridruzivanja(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI2):
        P_za_petlja(razina + 1)

    else:
        handleException(ulaz)

    return None

def P_naredba_pridruzivanja(razina):
    imeNezavrsnog = "<naredba_pridruzivanja>"
    PRIMIJENI1 = ['IDN']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):

        provjeriZavrsni(razina, "IDN")
        provjeriZavrsni(razina, "OP_PRIDRUZI")
        P_E(razina + 1)

    else:
        handleException(ulaz)

    return None

def P_za_petlja(razina):
    imeNezavrsnog = "<za_petlja>"
    PRIMIJENI1 = ['KR_ZA']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):

        provjeriZavrsni(razina, "KR_ZA")
        provjeriZavrsni(razina, "IDN")
        provjeriZavrsni(razina, "KR_OD")
        P_E(razina + 1)
        provjeriZavrsni(razina, "KR_DO")
        P_E(razina + 1)
        P_lista_naredbi(razina + 1)
        provjeriZavrsni(razina, "KR_AZ")

    else:
        handleException(ulaz)

    return None

def P_E(razina):
    imeNezavrsnog = "<E>"
    PRIMIJENI1 = ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        P_T(razina + 1)
        P_E_lista(razina + 1)

    else:
        handleException(ulaz)

    return None

def P_E_lista(razina):
    imeNezavrsnog = "<E_lista>"
    PRIMIJENI1 = ['OP_PLUS']
    PRIMIJENI2 = ['OP_MINUS']
    PRIMIJENI3 = ['IDN', 'KR_ZA', 'KR_DO', 'KR_AZ', 'D_ZAGRADA', 'ENDL']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        provjeriZavrsni(razina, "OP_PLUS")
        P_E(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI2):
        provjeriZavrsni(razina, "OP_MINUS")
        P_E(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI3):
        cvor = Cvor("$", razina + 1)
        stablo.append(cvor)

    else:
        handleException(ulaz)

    return None

def P_T(razina):
    imeNezavrsnog = "<T>"
    PRIMIJENI1 = ['IDN', 'BROJ', 'OP_PLUS', 'OP_MINUS', 'L_ZAGRADA']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        P_P(razina + 1)
        P_T_lista(razina + 1)

    else:
        handleException(ulaz)

    return None

def P_T_lista(razina):
    imeNezavrsnog = "<T_lista>"
    PRIMIJENI1 = ['OP_PUTA']
    PRIMIJENI2 = ['OP_DIJELI']
    PRIMIJENI3 = ['IDN', 'KR_ZA', 'KR_DO', 'KR_AZ', 'OP_PLUS', 'OP_MINUS', 'D_ZAGRADA', 'ENDL']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        provjeriZavrsni(razina, "OP_PUTA")
        P_T(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI2):
        provjeriZavrsni(razina, "OP_DIJELI")
        P_T(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI3):
        cvor = Cvor("$", razina + 1)
        stablo.append(cvor)

    else:
        handleException(ulaz)

    return None

def P_P(razina):
    imeNezavrsnog = "<P>"
    PRIMIJENI1 = ['OP_PLUS']
    PRIMIJENI2 = ['OP_MINUS']
    PRIMIJENI3 = ['L_ZAGRADA']
    PRIMIJENI4 = ['IDN']
    PRIMIJENI5 = ['BROJ']

    cvor = Cvor(imeNezavrsnog, razina)
    stablo.append(cvor)

    ulaz = getUlaz()
    if ulaz.isInPrimijeni(PRIMIJENI1):
        provjeriZavrsni(razina, "OP_PLUS")
        P_P(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI2):
        provjeriZavrsni(razina, "OP_MINUS")
        P_P(razina + 1)

    elif ulaz.isInPrimijeni(PRIMIJENI3):
        provjeriZavrsni(razina, "L_ZAGRADA")
        P_E(razina + 1)
        provjeriZavrsni(razina, "D_ZAGRADA")

    elif ulaz.isInPrimijeni(PRIMIJENI4):
        provjeriZavrsni(razina, "IDN")

    elif ulaz.isInPrimijeni(PRIMIJENI5):
        provjeriZavrsni(razina, "BROJ")

    else:
        handleException(ulaz)

    return None

#endregion


#region -----UCITAVANJE

#1 cin (default/predaja)
#2 hardcode
#3 testing
INPUT = 1

if INPUT == 1:
    #cin
    ulazRaw = sys.stdin.readlines()
elif INPUT == 2:
    #hardcode
    fileRaw = open(r"H:\Media\Misc\Downloads\Lab2project\test16.in","r")
    ulazRaw = fileRaw.readlines() #lista linija
elif INPUT == 3:
    #testing
    fileRaw = open(r"H:\lab1_laksa_unpacked\05_znam_var_test.in","r")
    ulazRaw = fileRaw.readlines() #lista linija
#endregion


#region -----GLOBALS
global ulazCestice #[sifra uniformnog znaka, broj linije, tekst cestice]
ulazCestice = ulazToList(ulazRaw)

global brojilo #prva nepronadjena cestica
brojilo = 0
global stablo #konacni artefakt
stablo = list()


#fyi
#file = fileRaw.read() # citav file kao string
#endregion


#region -----POZIVI FUNKCIJA
try:
    P_program()
except Exception as e:
    print(str(e))
else:
    ispisStabla()
#endregion


#region -----KRAJ
if INPUT == 2 or INPUT == 3:
    fileRaw.close()

# print('\n', end='') # prazna linija potrebna za neke operative sisteme
sys.exit()
#endregion

