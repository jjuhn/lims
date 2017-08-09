from lims import db
from lims.auth.models import  User
from sqlalchemy.ext.associationproxy import association_proxy


# physician_institute = db.Table('physician_institute',
#                                db.Column('physician_id', db.Integer, db.ForeignKey('physician.id'), primary_key=True),
#                                db.Column('institute_id', db.Integer, db.ForeignKey('institute.id'), primary_key=True))


# class DoRelationship(db.Model):
#     __tablename__ = 'do_relationship'
#     p_id = db.Column(db.Integer, db.ForeignKey("DiseaseOntology.id"), primary_key=True)
#     c_id = db.Column(db.Integer, db.ForeignKey("DiseaseOntology.id"), primary_key=True)

DoRelationship = db.Table('do_relationship',
                          db.Column('p_id', db.Integer, db.ForeignKey('disease_ontology.id'), primary_key=True),
                          db.Column('c_id', db.Integer, db.ForeignKey('disease_ontology.id'), primary_key=True))

DoSynonym = db.Table('do_synonym',
                     db.Column('do_id', db.Integer, db.ForeignKey('disease_ontology.id'), primary_key=True),
                     db.Column('syn_id', db.Integer, db.ForeignKey('synonym.id'), primary_key=True))

DoOmim = db.Table('do_omim',
                  db.Column('do_id', db.Integer, db.ForeignKey('disease_ontology.id'), primary_key=True),
                  db.Column('omim_id', db.Text, db.ForeignKey('omim.id'), primary_key=True))

PoRelationship = db.Table('po_relationship',
                          db.Column('p_id', db.Integer, db.ForeignKey('phenotype_ontology.id'), primary_key=True),
                          db.Column('c_id', db.Integer, db.ForeignKey('phenotype_ontology.id'), primary_key=True))

PoSynonym = db.Table('po_synonym',
                     db.Column('po_id', db.Integer, db.ForeignKey('phenotype_ontology.id'), primary_key=True),
                     db.Column('syn_id', db.Integer, db.ForeignKey('synonym.id'), primary_key=True))

PhenoOmim =  db.Table('pheno_omim',
                      db.Column('phenotype_id', db.Integer, db.ForeignKey('phenotype_ontology.id'), primary_key=True),
                      db.Column('omim_id', db.Text, db.ForeignKey('omim.id'), primary_key=True))



class DiseaseOntology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text)
    deprecated = db.Column(db.Boolean, default=False)

    relationship = db.relationship('DiseaseOntology', secondary=DoRelationship, primaryjoin=id==DoRelationship.c.p_id,
                                   secondaryjoin=id==DoRelationship.c.c_id)

    synonyms = db.relationship('Synonym', secondary=DoSynonym)
    omims = db.relationship('Omim', secondary=DoOmim)

    def __init__(self, id, name, desc, deprecated):
        self.id = id
        self.name = name
        self.desc = desc
        self.deprecated = deprecated


    def add_child(self, child):
        if child not in self.relationship:
            self.relationship.append(child)
            # child.relationship.append(self)


class Omim(db.Model):
    id = db.Column(db.Text, primary_key=True)
    db_name = db.Column(db.Text)
    name = db.Column(db.Text)
    qualifier = db.Column(db.Text)
    evidence_code = db.Column(db.Text)
    aspect = db.Column(db.Text)
    morbid_name = db.Column(db.Text)


    def __init__(self, id, name, db_name, qualifier, evidence_code, aspect, morbid_name):
        self.id = id
        self.name = name
        self.db_name = db_name
        self.qualifier = qualifier
        self.evidence_code = evidence_code
        self.aspect = aspect
        self.morbid_name = morbid_name


class PhenotypeOntology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    namespace = db.Column(db.Text)
    deprecated = db.Column(db.Text)
    xref = db.Column(db.Text)
    hasalternativeid = db.Column(db.Text)
    description = db.Column(db.Text)

    omims = db.relationship('Omim', secondary=PhenoOmim)

    synonyms = db.relationship('Synonym', secondary=PoSynonym)

    relationship = db.relationship('PhenotypeOntology', secondary=PoRelationship, primaryjoin=id==PoRelationship.c.p_id,
                                   secondaryjoin=id==PoRelationship.c.c_id)


    def __init__(self, id, name, namespace, deprecated, xref, hasalternativeid, description):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.deprecated = deprecated
        self.xref = xref
        self.hasalternativeid = hasalternativeid
        self.description = description

    def add_child(self, child):
        if child not in self.relationship:
            self.relationship.append(child)


class SymptomOntology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    comment = db.Column(db.Text)
    namespace = db.Column(db.Text)
    deprecated = db.Column(db.Boolean, default=False)

    def __init__(self, id, name, description, comment, namespace, deprecated):
        self.id = id
        self.name = name
        self.description = description
        self.comment = comment
        self.namespace = namespace
        self.deprecated = deprecated



class Synonym(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    scope = db.Column(db.Text)
    syn_type = db.Column(db.Text)

    def __init__(self, description, scope, syn_type):
        self.description = description
        self.scope = scope
        self.syn_type = syn_type




class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Gender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    subjects = db.relationship('Subject', backref='gender')

    # def __init__(self):
    #     print self

    def __str__(self):
        return '%s' % (self.name)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer)
    gender_id = db.Column(db.Integer, db.ForeignKey(Gender.id))
    neurocode = db.Column(db.Integer)
    label = db.Column(db.Text)

    samples = db.relationship('Sample', backref='subject')


    def __init__(self, age, neurocode, label):
        self.age = age
        self.neurocode = neurocode
        self.label = label
        # self.gender_id = gender_id

    def __str__(self):
        return '<neurocode id=%s>' % (self.neurocode)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Text)
    amount = db.Column(db.Text)
    date_received = db.Column(db.TIMESTAMP)
    subject_id = db.Column(db.Integer, db.ForeignKey(Subject.id))
    label = db.Column(db.Text)

    aliquots = db.relationship('Aliquot', backref='sample')

    institutions = db.relationship("Institute", secondary="registration")
    physicians = db.relationship("Physician", secondary="registration")
    # institutions = db.relationship("Registration", back_populates="sample")
    # physicians = db.relationship("Registration", back_populates="sample")

    def __init__(self, type, amount, date_received, label):
        self.type = type
        self.amount = amount
        self.date_received = date_received
        self.label = label

    def __str__(self):
        return '<sample id=%s sample type=%s recieved=%s>' % (self.id, self.type, self.date_received)


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    created = db.Column(db.TIMESTAMP)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    aliquots = db.relationship("Aliquot", backref='storage')
    batches = db.relationship("Batch", backref='storage')


    def __init__(self, name, created):
        self.name = name
        self.created = created


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)

    aliquots = db.relationship("Aliquot", backref='status')

# class Thing(db.Model):
#     __abstract__ = True
#     created_on = db.Column(db.DateTime, default=db.func.now())
#     updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Aliquot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.Text)

    sample_id = db.Column(db.Integer, db.ForeignKey(Sample.id))
    created = db.Column(db.TIMESTAMP)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    storage_id = db.Column(db.Integer, db.ForeignKey(Storage.id))
    status_id = db.Column(db.Integer, db.ForeignKey(Status.id))

    qas = db.relationship("Qa", secondary="aliquot_qa")

    def __init__(self, barcode, created):
        self.barcode = barcode
        self.created = created

    def __str__(self):
        return '<barcode=%s status=%s>' % (self.barcode, self.status)


class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    storage_id = db.Column(db.Integer, db.ForeignKey(Storage.id))
    created = db.Column(db.TIMESTAMP)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __str__(self):
        return '<name=%s>' % (self.name)


class BatchAliquot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aliquot_id = db.Column(db.Integer, db.ForeignKey(Aliquot.id))
    batch_id = db.Column(db.Integer, db.ForeignKey(Batch.id))
    position = db.Column(db.Text)

    aliquot = db.relationship(Aliquot, backref='batches')
    batch = db.relationship(Batch, backref='aliquots')


class Registration(db.Model):
    __tablename__= 'registration'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    physician_id = db.Column('physician_id', db.Integer, db.ForeignKey('physician.id'), primary_key=True)
    institute_id = db.Column('institute_id', db.Integer, db.ForeignKey('institute.id'), primary_key=True)
    sample_id = db.Column('sample_id', db.Integer, db.ForeignKey('sample.id'), primary_key=True)
    received_date = db.Column(db.TIMESTAMP)

    sample = db.relationship("Sample", backref='sample_registrations')
    physician = db.relationship("Physician", backref='physician_registrations')
    institute = db.relationship("Institute", backref='institute_registrations')

    # physician = db.relationship(lambda: Physician, back_populates="institutions")
    # institute = db.relationship(lambda: Institute,  back_populates="physicians")
    # sample = db.relationship(lambda: Sample, backref="sample_registration")



class Physician(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # take this out to physician_name?
    first = db.Column(db.Text)
    last = db.Column(db.Text)

    # take physician address out?
    msp = db.Column(db.Integer, unique=True)
    phone_number = db.Column(db.Text)
    fax = db.Column(db.Text)
    email = db.Column(db.Text)

    institutions = db.relationship("Institute", secondary="registration")
    samples = db.relationship("Sample", secondary="registration")
    # institutions = db.relationship(lambda:Registration, back_populates="physician")
    # samples = db.relationship(lambda:Registration, back_populates="physician")

    def __init__(self, first, last, msp, phone_number, fax, email):
        self.first = first
        self.last = last
        self.msp = msp
        self.phone_number = phone_number
        self.fax = fax
        self.email = email




class Institute(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    # physicians = db.relationship(lambda:Registration, back_populates="institute")
    # samples = db.relationship(lambda:Registration, back_populates="institute")

    def __init__(self, name):
        self.name = name




class Qa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    units = db.Column(db.Text)

    # aliquots = db.relationship("Aliquot", secondary="aliquot_qa")


class AliquotQa(db.Model):
    __tablename__ = 'aliquot_qa'
    aliquot_id = db.Column('aliquot_id', db.Integer, db.ForeignKey('aliquot.id'), primary_key=True)
    qa_id = db.Column('qa_id', db.Integer, db.ForeignKey('qa.id'), primary_key=True)
    value = db.Column(db.Text)
    tech_id = db.Column(db.Integer)
    date_entered = db.Column(db.TIMESTAMP)

    aliquot = db.relationship("Aliquot", backref='aliquot_qa')
    qa = db.relationship("Qa", backref='aliquot_qa')

    def __init__(self, aliquot, qa, value, tech_id, date_entered):
        self.aliquot = aliquot
        self.qa = qa
        self.value = value
        self.tech_id = tech_id
        self.date_entered = date_entered


class Collaborator(db.Model):
    __tablename__ = 'collaborator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    equipments = db.relationship('Equipment', backref='manufacturer')


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    catalog_identifier = db.Column(db.Text)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey(Manufacturer.id))


# class AliquotSchema(ma.ModelSchema):
#     sample = fields.Nested('SampleSchema')
#
#     class Meta:
#         model = Aliquot


# class GenderSchema(ma.ModelSchema):
#     class Meta:
#         model = Gender
#
#
# class SampleSchema(ma.ModelSchema):
#     # aliquots = ma.Nested(AliquotSchema, many=True)
#     # institutions = ma.Nested('InstituteSchema', many=True)
#     # physicians = ma.Nested('PhysicianSchema', many=True)
#
#     class Meta:
#         model = Sample
#
#
# class SubjectSchema(ma.ModelSchema):
#     samples = ma.Nested(SampleSchema, many=True)
#     class Meta:
#         model = Subject
#
#
# class InstituteSchema(ma.ModelSchema):
#     class Meta:
#         model = Institute
#
#
# class PhysicianSchema(ma.ModelSchema):
#     # institutes = ma.Nested(InstituteSchema, many=True)
#     # samples = ma.Nested(SampleSchema, many=True)
#     class Meta:
#         model = Physician
#
#
# class RegistrationSchema(ma.ModelSchema):
#     institute = ma.Nested(InstituteSchema)
#     sample = ma.Nested(SampleSchema)
#     physician = ma.Nested(PhysicianSchema)
#
#     class Meta:
#         model = Registration
#
#
#
# samples_schema = SampleSchema(many=True)
# sample_schema = SampleSchema()
#
# physicians_schema = PhysicianSchema(many=True)
# physician_schema = PhysicianSchema()
#
# subjects_schema = SubjectSchema(many=True)
# subject_schema = SubjectSchema()
#
# registrations_schema = RegistrationSchema(many=True)
# registration_schema = RegistrationSchema()

