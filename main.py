import pdfplumber
import os

def extraction(path):
    """Extraction des données contenue dans une fiche de salaire education nationale au format PDF"""
    with pdfplumber.open(path) as pdf:
        data = pdf.pages[0].extract_table()
    print("Accès au chemin :",path)
    print("Données brutes :")
    print(data)
    donnee = []
    """for elem in data:
        try:
            if elem[0].isnumeric and len(elem[0]) == 6:
                donnee.append({elem[0]:elem[2],payer(elem)[0]:payer(elem)[1]})
        except:
            None
    return donnee"""

def main():
    paths = os.listdir('.\PDFs')
    for path in paths:
        extraction(os.getcwd()+'\\PDFs\\'+str(path))
        #'.\PDFs\\'+str(path)
        

if __name__ == '__main__':
    main()