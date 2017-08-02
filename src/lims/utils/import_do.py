from lims import db
from lims.models import DiseaseOntology, DoRelationship, Synonym, SymptomOntology, PhenotypeOntology, Omim
import csv
from pprint import pprint
import pronto
import re


MORBID_MAP = 'morbidmap.txt'

DISEASE_URL = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.owl"
SYMPTOM_URL = 'http://purl.obolibrary.org/obo/symp.owl'
DSO_URL = "http://flash.lakeheadu.ca/~omohamme/DSO.owl"


HPO_URL = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.owl"
HPO_OBO_URL = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"


mondo = "https://raw.githubusercontent.com/monarch-initiative/monarch-disease-ontology/master/src/mondo/mondo.owl"




#
# morbid = []
#
# with open(MORBID_MAP) as f :
#     print f.next()
#     print f.next()
#     print f.next()
#     header = f.next().strip("#").strip().split("\t")
#
#
#     for line in f:
#         s = line.strip().split("\t")
#         if len(s) == 4:
#             mim = int(s[2])
#             d = {header[0]: s[0], header[1]: s[1], header[2]: s[2], header[3]: s[3]}
#             morbid.append(d)
#
#
#
# om = Omim.query.all()
# #
# for o in om:
#     for m in morbid:
#         if o.id == m.get("MIM Number"):
#             print o.id
#             print m.get("Phenotype")
#             print o.name
#             print o.morbid_name
#             print "-"*50
#             # print m.get("Gene Symbols")
#             # print m.get("Cyto Location")
#
#
#             # if o.morbid_name == :
#             #     print "not morbid name"
#             #     o.update({"morbid_name":m.get("Phenotype")})
#             #     db.session.commit()
                











def get_phenotype_annotation():
    with open("phenotype_annotation.tab") as f:
        r = csv.reader(f, delimiter="\t")
        pa = []
        for i in r:
            pa.append({"DB": i[0],
                       "DB_Object_ID": i[1],
                       "DB_Name": i[2],
                       "Qualifier": i[3],
                       "HPO ID": int(i[4].split(":")[1]),
                       "DB:Reference": i[5],
                       "Evidence code": i[6],
                       "Onset modifier": i[7],
                       "Frequency modifier": i[8],
                       "With": i[9],
                       "Aspect": i[10],
                       "Synonym": i[11],
                       "Date": i[12],
                       "Assigned by": i[13],
                       })
    return pa



# ont = pronto.Ontology(DISEASE_URL, import_depth=3)
#
# for term in ont:
#     # m = re.match(r'has_symptom', term.desc)
#     m = re.findall(r'has_symptom\s(\w*\s?\w*)', term.desc)
#
#     print term.id
#     print m
#






hpo_ont =  pronto.Ontology(HPO_URL)

# mondo = pronto.Ontology(mondo)

# symptom_ont = pronto.Ontology(SYMPTOM_URL)
# dso_ont = pronto.Ontology(DSO_URL)

for term in hpo_ont:
    if term.other:
        print term.id
        print term.other







# for term in ont:
#     id = int(term.id.split(":")[1])
#     name = term.name
#     desc = term.desc
#     relations = term.relations
#     other = term.other
#     synonyms = term.synonyms
#
#     comment = other.get("comment")[0] if other.get("comment") else None
#     namespace = other.get("namespace")[0] if other.get("namespace") else None
#     deprecated = True if term.other.get("deprecated") else False
#     xref = other.get("xref")
#     hasAlternativeId = other.get("hasAlternativeId")



# def insert_all_do(ont):
#     do_dict = []
#     for term in ont:
#         if term.id.startswith("DOID"):
#             id = int(term.id.split(":")[1])
#             name = term.name
#             desc = term.desc
#             relations = term.relations
#             other = term.other
#             synonyms = term.synonyms
#
#             comment = other.get("comment")[0] if other.get("comment") else None
#             namespace = other.get("namespace")[0] if other.get("namespace") else None
#             deprecated = True if term.other.get("deprecated") else False
#             xref = other.get("xref")
#             hasAlternativeId = other.get("hasAlternativeId")
#
#             do = DiseaseOntology.query.get(id)
#             do.deprecated





def insert_all_do(ont):
    do_dict = []

    for k in ont:
        if k.id.startswith("DOID"):
            id = int(k.id.split(":")[1])
            deprecated = True if k.other.get('deprecated') else False

            do_dict.append({"name": k.name, "desc": k.desc, "id": id,
                            "deprecated": deprecated})

    db.engine.execute(DiseaseOntology.__table__.insert(), do_dict)




def insert_do_relationship(ont):
    for k in ont:
        if k.id.startswith("DOID"):
            id = k.id.split(":")[1]
            parents = k.relations.get(pronto.Relationship('is_a'))
            children = k.relations.get(pronto.Relationship('can_be'))

            if children:
                for child in children:
                    child_id = int(child.id.split(":")[1])
                    if k in child.relations.get(pronto.Relationship('is_a')):
                        current_do = DiseaseOntology.query.get(id)
                        child_do = DiseaseOntology.query.get(child_id)

                        current_do.add_child(child_do)

    db.session.commit()


def insert_synonyms(ont):
    syn = []
    for k in ont:
        if k.synonyms:
            for s in list(k.synonyms):
                if k.id.startswith("DOID"):
                    id = int(k.id.split(":")[1])
                    # print s.scope
                    # print s.desc
                    # print s.xref
                    # print s.syn_type

                    if s.xref:
                        raise Exception('xref is not empty!!')
                    else:
                        es = Synonym.query.filter(Synonym.description == s.desc).first()
                        do = DiseaseOntology.query.get(id)
                        if not es:
                            syn = Synonym(description=s.desc, scope=s.scope, syn_type=s.syn_type)
                            db.session.add(syn)
                            do.synonyms.append(syn)
                        else:
                            do.synonyms.append(es)

    db.session.commit()


def insert_do_omim(ont):
    for i in ont:
        if i.id.startswith("DOID"):
            xref = i.other.get("xref")
            id = int(i.id.split(":")[1])
            if xref:
                for x in xref:
                    if x.startswith("OMIM:"):
                        omim_id = x.split(":")[1]
                        m = re.match(r'^[A-z]{1,}(\d*)', omim_id)
                        if m:
                            o_id = m.group(1)
                        else:
                            o_id = int(omim_id)
                        omim_name = x.split(":")[0]
                        omim = Omim.query.filter(Omim.id == o_id).first()
                        do = DiseaseOntology.query.get(id)
                        if not omim:
                            o = Omim(id=o_id, db_name=omim_name, name=None, qualifier=None, evidence_code=None,
                                     aspect=None, morbid_name=None)
                            db.session.add(o)
                            do.omims.append(o)
                        else:
                            do.omims.append(omim)
    db.session.commit()


def insert_phenotype_omim(hpo_ont):
    pa = get_phenotype_annotation()
    for i in pa:
        pa_id = i.get("HPO ID")
        database = i.get("DB")
        db_id = i.get("DB_Object_ID")
        name = i.get("DB_Name") # this is NOT the Database name
        qualifier = i.get("Qualifier") if i.get("Qualifier") else None
        evidence_code = i.get("Evidence code")
        aspect = i.get("Aspect")

        # print pa_id, database, db_id
        
        if database == 'OMIM':
            p = PhenotypeOntology.query.get(int(pa_id))
            o = Omim.query.get(int(db_id))

            if not o:
                omim = Omim(id=int(db_id), name=name, db_name="OMIM", qualifier=qualifier, evidence_code=evidence_code,
                            aspect=aspect, morbid_name=None)

                p.omims.append(omim)
            else:
                p.omims.append(o)

    db.session.commit()


def get_clean_columns(term):
    if term.id.startswith("HP"):
        id = int(term.id.split(":")[1])
        name = term.name
        desc = term.desc
        relations = term.relations
        other = term.other
        synonyms = term.synonyms

        comment = other.get("comment")[0] if other.get("comment") else None
        namespace = other.get("namespace")[0] if other.get("namespace") else None
        deprecated = True if term.other.get("deprecated") else False
        xref = other.get("xref")
        hasAlternativeId = other.get("hasAlternativeId")

        return {"id": id, "name":name, "description": desc, "comment": comment, "namespace":namespace, "deprecated":deprecated}



def insert_phenotype_ontology(hpo_ont):
    for term in hpo_ont:
        if term.id.startswith("HP"):
            id = int(term.id.split(":")[1])
            name = term.name
            desc = term.desc
            relations = term.relations
            other = term.other
            synonyms = term.synonyms

            comment = other.get("comment")[0] if other.get("comment") else None
            namespace = other.get("namespace")[0] if other.get("namespace") else None
            deprecated = True if term.other.get("deprecated") else False
            xref = other.get("xref")
            hasAlternativeId = other.get("hasAlternativeId")

            # parents = relations.get(pronto.Relationship('is_a'))
            # children = relations.get(pronto.Relationship('can_be'))

            new_p = PhenotypeOntology(id=id, name=name, namespace=namespace, deprecated=deprecated,
                              xref=xref, hasalternativeid=hasAlternativeId, description=desc)
            db.session.add(new_p)

    db.session.commit()


def insert_po_relationship(hpo_ont):
    for term in hpo_ont:
        if term.id.startswith("HP"):
            term_id = term.id.split(":")[1]
            p = PhenotypeOntology.query.get(term_id)
            if term.children:
                for child in term.children:
                    if term in child.parents:
                        child_id = child.id.split(":")[1]
                        c = PhenotypeOntology.query.get(child_id)
                        p.add_child(c)

    db.session.commit()


def insert_synonyms_po(hpo_ont):
    for term in hpo_ont:
        if term.id.startswith("HP"):
            term_id = term.id.split(":")[1]
            p = PhenotypeOntology.query.get(term_id)

            if term.synonyms:
                for s in list(term.synonyms):
                    es = Synonym.query.filter(Synonym.description == s.desc).first()
                    if not es:
                        syn = Synonym(description=s.desc, scope=s.scope, syn_type=s.syn_type)
                        p.synonyms.append(syn)
                    else:
                        p.synonyms.append(es)

    db.session.commit()





# insert_phenotype_ontology(hpo_ont)
# insert_po_relationship(hpo_ont)
# insert_synonyms_po(hpo_ont)





# insert_phenotype_omim(hpo_ont)


# do_omim = get_do_omim(ont)
# insert_do_omim(ont)






# with open('morbidmap.txt') as f:
#     f.next()
#     f.next()
#     f.next()
#     header = str(f.next())[2:-1].split("\t")
#     genemap = {}
#
#     for line in f:
#         if not line.startswith('#'):
#             l = line[:-1].split('\t')
#             line_dict = {}
#             for c, h in zip(l, header):
#                 line_dict.update({h: c})
#
#             if line_dict.get('MIM Number'):
#                 genemap.update({line_dict.get('MIM Number'): line_dict})




# insert_all_do(ont)
# insert_do_relationship(ont)



#
# for i in ont:
#
#     print i.synonyms
#
#

# insert_all_do(ont)
# insert_do_relationship(ont)
# insert_synonyms(ont)


# pprint.pprint(genemap)




# for i in ont:
#     if i.other.get('xref'):
#         print i.id
#
#         for l in i.other.get('xref'):
#             if l.startswith('OMIM'):
#                 omim = l.split(":")[1]
#                 pprint.pprint(genemap.get(omim))

# def insert_all_so(symptom_ont):
#     so_dict = []
#     for i in symptom_ont:
#         if i.id.startswith("SYMP"):
#             id = int(i.id.split(":")[1])
#             name = i.name
#             desc = i.desc
#             relations = i.relations
#             other = i.other
#             synonyms = i.synonyms
#
#             comment = other.get("comment")
#             namespace = other.get("namespace")
#             deprecated = True if i.other.get("deprecated") else False
#             xref = other.get("xref")
#             hasAlternativeId = other.get("hasAlternativeId")
#
#             parents = relations.get(pronto.Relationship('is_a'))
#             children = relations.get(pronto.Relationship('can_be'))
#
#             print id, name, desc, comment, namespace, deprecated, xref, hasAlternativeId, parents, children
#             so_dict.append({"id": id, "name": name, "comment": comment, "namespace": namespace,
#                             "deprecated": deprecated})
#
#     db.engine.execute(SymptomOntology.__table__.insert(), so_dict)
#
#
# insert_all_so(symptom_ont)



# import json
#
# from sqlalchemy import exc


# with open('do_json.txt') as json_data:
#     d = json.load(json_data)
#
#     do_dict = []
#     for k, v in d.iteritems():
#
#         # print k, v
#         if k.startswith("DOID"):
#             if len(k.split(":")) == 2:
#                 id = int(k.split(":")[1])
#
#
#
#             name = v.get("name") if v.get("name") else "unknown"
#             desc = v.get("desc")
#
#             deprecated = v.get('other').get('deprecated') if not v.get('other').get('deprecated') else True
#             parents = v.get('relations').get('is_a')[0].split(":")[1] if v.get('relations').get('is_a') else None
#
#             children = v.get('relations').get('can_be')
#
#             subset = v.get('other').get('subset')
#             hasAlternativeId = v.get('other').get('hasAlternativeId')
#             # alternative ID is either not existing in the original record or exists but deprecated = True
#
#             xref = v.get('other').get('xref')
#
#             namespace = v.get('other').get('namespace')[0] if v.get('other').get('namespace') else None
#             created_by = v.get('other').get('created_by')
#             creation_date = v.get('other').get('creation_date')
#             onProperty = v.get('other').get('onProperty')

            # print id
            # print namespace
            # print created_by
            # print creation_date
            # print onProperty
            #

            # print xref
            # print hasAlternativeId
            # print namespace
            # print created_by
            # print creation_date
            # print onProperty






            # do_dict.append({"name":name, "desc":desc, "id":id, "deprecated":deprecated})
#
#     db.engine.execute(DiseaseOntology.__table__.insert(), do_dict)






# with open('do_json.txt') as json_data:
#     d = json.load(json_data)
#
#     for k, v in d.iteritems():
#
#         if k.startswith("DOID"):
#             if len(k.split(":")) == 2:
#                 id = int(k.split(":")[1])
#                 parents = v.get('relations').get('is_a')
#                 children = v.get('relations').get('can_be')
#
#                 print "id: {0}".format(id)
#                 print "parents: {0}".format(parents)
#                 print "children: {0}".format(children)
#                 if children:
#                     current = DiseaseOntology.query.get(id)
#                     print "current: {0}".format(current)
#                     # print current.relationship
#                     for child in children:
#                         c_id = child.split(":")[1]
#                         c_json = d.get(child)
#
#                         c_parents = c_json.get('relations').get('is_a')
#                         if not k in c_parents:
#                             raise Exception
#                         else:
#                             c = DiseaseOntology.query.get(c_id)
#                             current.add_child(c)
#     db.session.commit()






