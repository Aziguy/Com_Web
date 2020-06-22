from tqdm.auto import tqdm

from PythonCode.utils import Utilities as utils

tqdm.pandas()

# aff = utils.wordExtratorFromUrl("campingshyeres.com")

monFichier = "C:/Users/INGEMEDIA/PycharmProjects/Com_Web/PythonCode/datasets/WordsExtract.xlsx"
dictionnaire = utils.wordExtractorFromFile(monFichier)
dico_Ok = utils.cleanDictionnaire(dictionnaire)

print("Avant : ")
print([len(dictionnaire[d]) for d in dictionnaire])
print("Après : ")
print([len(dico_Ok[d]) for d in dico_Ok])
