import pdfplumber

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

def main():
    path = "D:\\Documents\\07 - Documents administratifs et Professionnels\\02 - Payes\\2022\\05 - Mai.pdf"
    donnee = extraction(path)
    calcul = calcul_compare(donnee)
    affichage_extraction(donnee, calcul)
    

if __name__ == '__main__':
    main()