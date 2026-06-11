
import sys  # ucitavanje podataka
from collections import OrderedDict  # deterministicka varijanta rijecnika

#region -----TESTING
#python Lab2project.py < primjer.in > izlaz.out
#FC izlaz.out primjer.out
#endregion


#region -----POMOCNE KLASE
class Cestica:
    """Leksicka jedinka"""

    #[sifra uniformnog znaka, broj linije, tekst cestice]
    def __init__(self, sif, red, tekst, razina = 0):
        #ovo instancira ulazna funkcija ulazToList
        self.sif = str(sif)
        self.red = int(red)
        self.tekst = str(tekst)
        self.razina = razina

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

    def isVarijabla(self):
        return True if self.getSif == "IDN" else False

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

#instanca = Cvor("S", 2)
#razina = instacna.getRazina

class Varijabla:
    """ulazna cestica"""

    #[sifra uniformnog znaka, broj linije, tekst cestice]
    def __init__(self, redKor, Ime, kontekst, redDef = 0):
        #ovo instancira ulazna funkcija ulazToList
        self.redKor = str(redKor)
        self.redDef = int(redDef)
        self.Ime = str(Ime)
        self.kontekst = kontekst #radi sakrivanja var, kod provjere pripadnosti listi VARIJABLE moramo provjeriti postoji li var "ime" na razini "razina"

    def getRedKor(self):
        return self.redKor

    def getRedDef(self):
        return self.redDef

    def getIme(self):
        return self.Ime

    def getKontekst(self):
        return self.kontekst

    def isInVarijable(self, trazena):
        #prima trazenu varijablu
        #vraca true ako je pozvana nad cesticom iz predanog skupa, inace false (ako je varijabla "ziva")

        #ime = self.getIme()
        #lokKontekst = self.getKontekst()

        #inicijalno dok je lista prazna odmah vratimo 0
        if len(varijable) == 0:
            return 0

        for var in varijable:
            var.__class__ = Varijabla
            trazena.__class__ = Varijabla

            #vracamo red definicije pronadjene ako medju "zivima" postoji var istog imena definirana na nasoj ili visljoj razini
            if (var.getIme() == trazena.getIme() and var.getKontekst() <= trazena.getKontekst()):
                return var.getRedDef()

        return 0


    def ispis(self):
        redakKoristenja = str(self.getRedKor())
        redakDefinicije = str(self.getRedDef())
        imeVarijable = str(self.getIme())
        print(redakKoristenja + " " + redakDefinicije + " " + imeVarijable,  end='\n')
#endregion


#region -----FUNKCIJE
def nijeKrajLinije(a):
    # vraca istinu ako ulazni znak a != '\n', '\\' and ';'
    if a[0] != '\n' and a[0] != '\\' and a[0] != ';':
        return True
    return False

def jeCvor(linija):
    # vraca istinu ako predani string sadrzi < ili $
    return True if linija.find("<") != -1 or linija.find("$") != -1 else False

def jeCestica(linija):
    # vraca istinu ako predani string sadrzi < ili $
    return False if linija.find("<") != -1 or linija.find("$") != -1 else True


def klasificirajStablo(ulazRaw):
    #prima cisti ulaz i vraca list Cestica i Cvorova
    
    stablo = list()
    remove = ['<', '>', '\n']

    for linija in ulazRaw:
        
        if len(linija) > 0 :
            razina = len(linija) - len(linija.lstrip(' ')) #razinu dobijemo brojanjem razmaka na pocektu linije

            #cvor
            if (jeCvor(linija)):
                #micanje < i >
                for i in remove :
                    linija = linija.replace(i, '')

                ime = linija.strip()

                cestica = Cvor(ime, razina)

                stablo.append(cestica)

            #cestica (leksicka jedinka)
            elif (jeCestica(linija)):
                linija = linija.lstrip()
                podaci = linija.split(" ")
                sif = podaci[0].strip()
                red = podaci[1].strip()
                tekst = podaci[2].strip()

                cestica = Cestica(sif, red, tekst, razina)

                stablo.append(cestica)

    return stablo


def obilazakStabla():
    # ispisuje stablo u zadanom formatu

    for list in stablo:
        if isinstance(list, Cestica):
            list.__class__ = Cestica
            sifra = list.getSif()
            if sifra == "KR_ZA":
                global kontekst
                kontekst = kontekst + 1 #dozvoljavamo istoimene var ako je trenutni kontekst > konteksta postojece var
                global trenutna
                trenutna = "naredba_pridruzivanja"
            elif sifra == "KR_AZ":
                kontekst = kontekst - 1
                pocistiMrtve() #mice sve varijable iz VARIJABLE ako je var.kontekst > trenutni kontekst
            elif sifra == "IDN":
                if trenutna == "naredba_pridruzivanja":
                    dodajVar(list)
                    trenutna = "lista_naredbi"
                else:
                    provjeriVar(list)
            else:
                None

        elif isinstance(list, Cvor):
            list.__class__ = Cvor
            tip = list.getIme()
            if tip == "naredba_pridruzivanja" or tip == "lista_naredbi":
                trenutna = tip

        else:
            raise Exception("type error")

def pocistiMrtve():
    for var in varijable:
        var.__class__ = Varijabla
        if var.getKontekst() > kontekst:
            varijable.remove(var)
        else:
            None
            
def dodajVar(cestica):
    #stvorimo var; red koristenja =0 jer je ovo definicija var
    var = Varijabla(0, cestica.getTekst(), kontekst, cestica.getRed())

    redDef = var.isInVarijable(var)
    if redDef == 0:
        #dodavanje varijable u listu
        varijable.append(var)
        
    else:
        #var vec postoji u listi u trenutnom kontekstu pa ispisujemo gresku
        #raise Exception("err: varijabla (" + var.getIme() + ") je vec definirana u ovom kontekstu")

        #ne dizemo gresku samo nastavljamo dalje
        None

def provjeriVar(cestica):
    cestica.__class__ = Cestica
    var = Varijabla(cestica.getRed(), cestica.getTekst(), kontekst)

    redDef = var.isInVarijable(var)

    if redDef == 0:
        #var nije definirana u trenutnom kontekstu pa ispisujemo gresku
        raise Exception("err " + var.getRedKor() + " " + var.getIme())
    else:
        var.redDef = redDef
        var.ispis()

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
    fileRaw = open(r"<file>.in","r")
    ulazRaw = fileRaw.readlines() #lista linija
elif INPUT == 3:
    #testing
    fileRaw = open(r"<file>.in","r")
    ulazRaw = fileRaw.readlines() #lista linija
#endregion


#region -----GLOBALS
global stablo #ulazni artefakt
stablo = klasificirajStablo(ulazRaw)

global kontekst #sluzi za ciscenje mrtvih var i dozvoljava skrivanje unutar unutarnjeg ZA bloka
kontekst = 0

global trenutna
trenutna = "naredba_pridruzivanja"

global varijable #lista "zivih" varijabli
varijable = list()


#fyi
#file = fileRaw.read() # citav file kao string
#endregion


#region -----POZIVI FUNKCIJA
try:
    obilazakStabla()
except Exception as e:
    print(str(e))
else:
    None
    #ispisVarijabli() #to se radi prolaskom pa mi ne treba zasebna funkcija i struktura u memoriji?
#endregion


#region -----KRAJ
if INPUT == 2 or INPUT == 3:
    fileRaw.close()

# print('\n', end='') # prazna linija potrebna za neke operative sisteme
catchBreak = 1
sys.exit()
#endregion

