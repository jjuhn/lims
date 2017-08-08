# from lims import db
# from lims.models import DiseaseOntology, DoRelationship, Synonym, SymptomOntology, PhenotypeOntology, Omim
# import csv
#
#
# # FREEZER STORAGE               :  storage_location - sample ? aliquot?
# # PLATE_ID / CONTAINER BARCODE  :  subject?
# # DATE DNA EXTRACTED            :  sample?
# # IMPORTED INTO PROGENY         :  ?
# # COUNTRY                       :  subject
# # NOTES                         :  ?
# # JURISDICTION                  :  subject
# # DATE DNA RECEIVED             :  Sample?
# # BARCODE / SAMPLE NAME         :  aliquot id
# # CONTAINER TYPE                :  container -- sample
# # CONCENTRATION (ng/ul)         :  aliquot ? or sample ?
# # COLLABORATOR SURNAME          :  collaborator -- subject or sample ?
# # POSITION                      :  container -- position -- aliquot
# # Sample Plate Classification   :  classification -- sample
# # INDIVIDUAL NAME / UNIQUE ID   :  aliquot? or sample?
# # DNA EXTRACTED FROM            :  sample type? or aliquot type?
# # COLLABORATOR ID               :  collaborator id -- subject or sample?
# # CLINIC ID                     :  clinic ? -- sample?
# # DNA VOLUME (ul)               :  sample?
# # EXAUSTED                      :  sample?
#
#
# with open("Sheet1-Table 1.csv") as f:
#     r = csv.DictReader(f)
#
#     for line in r:
#         print line
#
#

# count total set bits in all numbers from 1 to n
def countSetBits(n):
    count = 0

    for i in range(1, n+1):
        count += bin(i)[2:].count("1")
        
    return count




if __name__ == '__main__':
    for i in range(1, 20):

        print i, countSetBits(i), countSetBits(i)-i
