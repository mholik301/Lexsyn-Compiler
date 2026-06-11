
import sys  # ucitavanje podataka
from collections import OrderedDict  # deterministicka varijanta rijecnika


# ------------FUNKCIJE

def nijeKrajLinije(a):
    # vraca istinu ako ulazni znak a != '\n', '\\' and ';'
    if a[0] != '\n' and a[0] != '\\' and a[0] != ';':
        return True
    return False


def obrisiKomentare(linijeRaw):
    #prima cisti ulaz i vraca dict linija koda bez komentara (broj linije je key, linija je value)

    linijeCisto = OrderedDict()
    brojacLinija = 1

    for line in linijeRaw:
        l = line.split("//") #odvajanje komentara od linije
        l[0] = l[0].replace("\n", "") #micanje \n znakova
        if l[0].rstrip():
            linijeCisto[brojacLinija] = l[0] #dodaj liniju koda bez komentara u dict
        brojacLinija += 1 #uvecaj brojac linija za 1

    return linijeCisto


def odvojiPoSpace(linijeDict):
    #prima dict linija koda bez komentara i odvaja cestice prema Space i specijalnim znakovima te vraca listu tih cestica

    cesticeLista = list()

    #broj linije (linija) je key, cesticeDict[linija] je linija
    for linija in linijeDict.keys():
        listaCesticaLinije = linijeDict[linija].split(" ")
        for cestica in listaCesticaLinije:
            if len(cestica) > 0:
                razdvojeneCestice = razdvojiIzraz(cestica)
                for cestica in razdvojeneCestice:
                    razdvojeneCestice = razdvojiIzrazeBezOp(cestica)
                    for cestica in razdvojeneCestice:
                        if len(cestica) > 0:
                            cesticaExtraInfo = [0, "unifSifraPlaceholder", linija, cestica] #identificirano, broj linije, kod cestice, buduci sifra uniformnog znaka
                            cesticeLista.append(cesticaExtraInfo)

    return cesticeLista


def identificirajKROS(cesticeList, KROSDict):
    #prima dict linija koda bez komentara i odvaja cestice prema Space znaku te vraca listu tih cestica

    for cestica in cesticeList:
        if cestica[0] == 0: #ako cestica vec nije identificirana
            uniformniZnak = KROSDict.get(cestica[3], -1)
            if uniformniZnak == -1:
                continue
            cestica[1] = uniformniZnak
            cestica[0] = 1

    return cesticeList


def razdvojiIzraz(cestica):
    komponente = list()
    privCestica = str()
    if len(cestica) < 2:
        komponente.append(cestica)
    else:
        for znak in cestica:
            if isSpecial(znak):
                if privCestica:
                    komponente.append(privCestica)
                komponente.append(znak)
                privCestica = ""
            else:
                privCestica += znak
        komponente.append(privCestica)

    return komponente


def razdvojiIzrazeBezOp(cestica):
    komponente = list()
    privCestica = str()
    if len(cestica) < 2:
        komponente.append(cestica)
    else:
        for znak in cestica:

            if znak.isnumeric():
                if privCestica.isnumeric() or privCestica == "":
                    privCestica += znak
                else:
                    komponente.append(privCestica)
                    privCestica = ""
                    privCestica += znak

            elif znak.isalpha() or privCestica == "":
                if privCestica.isalpha():
                    privCestica += znak
                else:
                    komponente.append(privCestica)
                    privCestica = ""
                    privCestica += znak
                
            else:
                komponente.append(privCestica)
                privCestica = ""
                privCestica += znak

        komponente.append(privCestica)

    return komponente


def isSpecial(znak):

    specijalni = ['=', '+', '-', '*', '/', '(', ')']
    if any(znak in s for s in specijalni):
        return True
    return False


def identificirajVarConst(cesticeList, KROSDict):
    #prima dict linija koda bez komentara i identificira varijable i konstante te vraca listu tih cestica

    for cestica in cesticeList:
        if cestica[0] == 0: #ako cestica vec nije identificirana
            uniformniZnak = SimEnka(cestica, KROSDict)
            if uniformniZnak == -1: #cestica nije niti var niti const?
                continue
            cestica[1] = uniformniZnak
            cestica[0] = 1

    return cesticeList


# ------------SimEnka.py (Matija Holik 0036516800, utr2020)

def SimEnka(cestica, KROSDict):


    def prilagodiCesticu(cestica):
        ulaz = list()

        for znak in cestica[3]:
            znak = str(znak)
            if znak.isnumeric():
                ulaz.append("num")
            elif znak.isalpha():
                ulaz.append("alfa")
            else:
                ulaz.append("&")

        return ulaz


    def setPocetno(pocetnoStanje, pravila):
        # vraca i ispisuje set sa s0 i njegovim e-prijelazima

        trenutnaStanja = {pocetnoStanje, }
        pocetnoStanjeSE = eOkolina(trenutnaStanja, pravila)
        #ispis(pocetnoStanjeSE)

        return pocetnoStanjeSE


    def dodajSusjede(trenutnoStanje, pravila, ulaz):
        # dobiva set stanja i dodaje im:
        # 1 e-okolinu, ako ne proslijedimo ulaz
        # 2 susjede preko ulaza, ako proslijedmo ulaz

        # red je implementiran preko liste:
        # queue = []
        # queue.append('a')
        # queue.pop(0)

        if 0:
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

        stanjeUlaz = (trenutnoStanje, ulaz)
        #eSusjedi = [pravila.get(stanjeUlaz, '')]
        eSusjed = pravila.get(stanjeUlaz, '')
        novoStanje = eSusjed
        return novoStanje


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


    def ispis(novoStanjeKorak, ulazi=",", j=0, KROSDict=OrderedDict()):
        # ispisuje sva stanja u poslanoj listi/setu u trazenom formatu
        # takodjer namjesta brojac j na sljedeci ulazni znak
        # podrazumjevani parametri se koriste kod ispisa pocetnog stanja

        if 0:
            if len(novaStanjaKorakE) == 0:
                noop() # here because a comment isnt sufficiant as a indented body
                #print("#", end='')
            else:
                flag2 = False  # need to print ','?
                novaStanjaKorakE = sorted(novaStanjaKorakE)
                for x in novaStanjaKorakE:
                    #if flag2 is not False:
                    #    print(',', end='')
                    #if flag2 is False:
                    #    flag2 = True
                    #if 1:
                    #    print(x, end='')


                    if x == "s0":
                        klasa = -1
                        break
                    if x == "s1":
                        klasa = KROSDict["const"]
                        break
                    if x == "s2":
                        klasa = KROSDict["var"]
                        break
                    if x == "s3":
                        klasa = -1
                        break

        if novoStanjeKorak == "s0":
            klasa = -1
        elif novoStanjeKorak == "s1":
            klasa = KROSDict["const"]
        elif novoStanjeKorak == "s2":
            klasa = KROSDict["var"]
        elif novoStanjeKorak == "s3":
            klasa = -1

        if 0:
            if ulazi[j] == ',':
                j += 1
                print('|', end='')
            elif ulazi[j] == '|':
                j += 1
                print('\n', end='')

        return j, klasa


    #pravila automata koji identificira varijable i konstante:
    """
        alfa = A-z
        num = 0-9
        & = bilo sto osim alfa i num
    """
    file = list()
    file = [
        #cestica=ulazni niz
        ("s0", "s1", "s2", "s3"), #stanja
        ("alfa", "num"), #ulazni znakovi
        ("s1", "s2"), #prihvatljiva stanja
        ("s0", ), #pocetno stanje
        #pravila:
        "s0,num->s1;",
        "s0,alfa->s2;",
        "s0,$->s3;",
        "s1,num->s1;",
        "s1,alfa->s3;",
        "s1,$->s3;",
        "s2,num->s2;",
        "s2,alfa->s2;",
        "s2,$->s3;",
        "s3,num->s3;",
        "s3,alfa->s3;",
        "s3,$->s3;"
        ]

    # konstante
    # ULAZ = 0
    STANJA = 0
    ABCUL = 1
    PRIH = 2
    POCSTANJE = 3
    FUNK = 4


    ulaz = prilagodiCesticu(cestica)
    i = int()

    """gradimo pocetno stanje"""
    i = int()
    pocetnoStanje = str()
    pocetnoStanje = file[POCSTANJE][0]
    if 0:
        while nijeKrajLinije(file[POCSTANJE][i]):
            pocetnoStanje += file[POCSTANJE][i]
            i += 1


    """gradimo dict pravila"""
    pravila = dict()
    for i in range(FUNK, len(file)):
        praviloRaw = file[i]  # izvorni string zapis pravila

        # gradimo pocetno stanje pravila
        j = 0
        tmpPocetno = str()
        while praviloRaw[j] != ',':
            tmpPocetno += praviloRaw[j]
            j += 1

        j += 1  # preskoci ,

        # gradimo ulazni znak tog prijelaza
        tmpUlaz = str()
        while praviloRaw[j] != '-':
            tmpUlaz += praviloRaw[j]
            j += 1

        j += 2  # preskoci ->

        """ako radimo eNKA tada izlaznih stanja moze biti vise"""
        #novaStanja = set()  # gradimo set novih stanja
        #while nijeKrajLinije(praviloRaw[j]):
        #    tmpString = str()
        #    while praviloRaw[j] != ',' and nijeKrajLinije(praviloRaw[j]):
        #        tmpString += praviloRaw[j]
        #        j += 1
        #    if praviloRaw[j] == ',':
        #        j += 1
        #    if tmpString != "#": # cemu ovo sluzi?
        #        novaStanja.add(tmpString)
        
        tmpNovoStanja = str()
        while nijeKrajLinije(praviloRaw[j]):
            tmpNovoStanja += praviloRaw[j]
            j += 1

        # stanjeUlazPar = {pocetno, ulaz} doesn't work because sets aren't hashable
        stanjeUlazPar = (tmpPocetno, tmpUlaz)

        pravila[stanjeUlazPar] = tmpNovoStanja  # gradimo dict pravila


    #trenutnoStanja = setPocetno(pocetnoStanje, pravila)
    trenutnoStanje = pocetnoStanje


    """trazimo i ispisujemo stanja za svaki ulazni niz"""
    for trenutniUlaz in ulaz:

        # nova stanja s preko ulaza
        novoStanje = dodajSusjede(trenutnoStanje, pravila, trenutniUlaz)

        j, klasa = ispis(novoStanje, trenutniUlaz, j, KROSDict)
        trenutnoStanje = novoStanje

    return klasa





def ispisListeUniformnihZnakova(cesticeList):
    # ispisuje podatke o cestici u formatu: identifikator linija tekst

    for cestica in cesticeList:
        identifikatorCestice = str(cestica[1])
        linijaCestice = str(cestica[2])
        tekstCestice = str(cestica[3])
        print(identifikatorCestice + " " + linijaCestice + " " + tekstCestice,  end='\n')



# ------------UCITAVANJE







for i in range(1, 100):
    if i%3 == 0 and i%5==0:
        print("fizzbuzz")
    elif i%5==0:
        print("buzz")
    elif i%3==0:
        print("fizz")
    else:
       print(i)




c = 3






"""ucitavamo podatake"""
#file = list()

brojalo = 0

#fileRaw = open(r"<file>.in","r")
#linijeRaw = fileRaw.readlines() #lista linija

fileRaw = open(r"<file>.in","r")
linijeRaw = fileRaw.readlines() #lista linija

#file = fileRaw.read() # citav file kao string



#linijeRaw = sys.stdin.readlines()


linijeDict = OrderedDict() #[broj linije] = kod linija
linijeDict = obrisiKomentare(linijeRaw);

cesticeList = list() #[indikator je li znak identificiran, buduca sifra uniformnog znaka, broj linije, tekst cestice]
cesticeList = odvojiPoSpace(linijeDict)



# ------------Tablica (rijecnik) kljucnih rijeci, operatora i specijalnih znakova
KROSDict = OrderedDict([
    ('za', 'KR_ZA'), 
    ('od', 'KR_OD'), 
    ('do', 'KR_DO'), 
    ('az', 'KR_AZ'),
    ('=', 'OP_PRIDRUZI'), 
    ('+', 'OP_PLUS'), 
    ('-', 'OP_MINUS'), 
    ('*', 'OP_PUTA'),
    ('/', 'OP_DIJELI'), 
    ('(', 'L_ZAGRADA'),
    (')', 'D_ZAGRADA'),
    ('var', 'IDN'),
    ('const', 'BROJ')
    ])



# ------------POZIVI FUNKCIJA
cesticeList = identificirajKROS(cesticeList, KROSDict)

cesticeList = identificirajVarConst(cesticeList, KROSDict)

ispisListeUniformnihZnakova(cesticeList)


#file.close() 
# print('\n', end='') # prazna linija potrebna za neke operative sisteme

sys.exit()

