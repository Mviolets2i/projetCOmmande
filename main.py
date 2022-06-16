import pdfplumber
from termcolor import colored
from regle_calcul_educ import *

def payer(liste):
    """Extraction du code "A PAYER", "A DEDUIRE" et "POUR INFO" d'une fiche de paye de l'education nationale"""
    if liste[-1] != '':
        return "INFO",liste[-1]
    elif liste[-2] != '':
        return "A DEDUIRE",liste[-2]
    elif liste[-3] != '':
        return "A PAYER",liste[-3]

def extraction(path):
    """Extraction des données contenue dans une fiche de salaire education nationale au format PDF"""
    with pdfplumber.open(path) as pdf:
        data = pdf.pages[0].extract_table()
    donnee = []
    donnee.append({"Echelon":data[0][-11][-8:-6],"Indice":data[0][-11][-4:], "Corps":data[0][-11][-21:-15], "Grade":data[0][-11][-14:-12]})
    for elem in data:
        try:
            if elem[0].isnumeric and len(elem[0]) == 6:
                donnee.append({elem[0]:elem[2],payer(elem)[0]:payer(elem)[1]})
        except:
            None
    return donnee

def affichage_extraction(donnee, calcul):
    """Affiche les données d'une fiche de paye après extraction"""
    print("--------------------------------------------------------------------")
    print("----- Vous êtes", colored(donnee[0]["Corps"],'blue',attrs=['bold']), colored(donnee[0]["Grade"],'blue',attrs=['bold']),\
         "à l'échelon", colored(donnee[0]["Echelon"],'blue',attrs=['bold']), "avec donc",colored(donnee[0]["Indice"],'blue',attrs=['bold']), "points -----")
    print("--------------------------------------------------------------------")
    print("{:<8} {:<43} {:<11} {:>8} {:>12}".format("Code", "Dénomination", "Type", "Extrait", "Calculé"))
    prime_donnee = 0
    prime_calcul = 0
    for elem in donnee:
        if "A PAYER" in elem.keys():
            affichage_tableau(elem, calcul, "green")
            prime_donnee += int(float(elem["A PAYER"].replace(',', '.')))
            prime_calcul += calcul[list(elem.keys())[0]]
    print ("{:>60} {:>25} {:>25}".format("TOTAL Primes, indemnités et heures sup.",\
        colored(prime_donnee-int(float(donnee[1]['A PAYER'].replace(',','.'))),'green', attrs=['underline']),\
        colored(prime_calcul-int(float(donnee[1]['A PAYER'].replace(',','.'))),'green', attrs=['underline'])))
    for elem in donnee:
        if "A DEDUIRE" in elem.keys():
            affichage_tableau(elem, calcul, "red")
    for elem in donnee:
        if "INFO" in elem.keys():
            affichage_tableau(elem, calcul, "grey")

def affichage_tableau(donnee, calcul, couleur):
    """Mise de forme des données alignées à gauche en table"""
    valeurs = []
    for val in donnee.items():
        calculee = 0
        for elems in val:
            if elems in calcul:
                calculee = calcul[elems]
            valeurs.append(elems)
        valeurs.append(calculee)
    print ("{:<8} {:<43} {:<20} {:>8} {:>12}".format(valeurs[0], valeurs[1], colored(valeurs[3], couleur), valeurs[4], valeurs[2]), end="")
    print("")

def calcul_compare(donnee):
    """Calcul d'une fiche de paye d'après des données extraites d'un PDF"""
    indice = int(donnee[0]["Indice"])
    echelon = int(donnee[0]["Echelon"])
    corps = donnee[0]["Corps"]
    grade = donnee[0]["Grade"]
    HSA = 3.55
    HSE = 11.25
    pp = "T"
    salaire = {}
    code10(salaire, indice)
    code20(salaire, HSA, HSE, corps, pp, echelon)
    retenue_absences(0, salaire)
    code50(salaire)
    code40(salaire)
    #[print (key,"-",value) for key,value in salaire.items()]
    return salaire

def main():
    path = "D:\\Documents\\07 - Documents administratifs et Professionnels\\02 - Payes\\2022\\05 - Mai.pdf"
    donnee = extraction(path)
    calcul = calcul_compare(donnee)
    affichage_extraction(donnee, calcul)
    

if __name__ == '__main__':
    main()