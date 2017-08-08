from lims import app, db
from flask import render_template, redirect, request, jsonify, url_for
from lims.form import SampleReceptionForm, PhysicianForm, LaboratoryForm, ElectrophoresisForm, SubjectForm, NewAliquotForm, BatchForm
from lims.models import Subject, Sample, Aliquot, Gender, Physician, Institute, Qa, AliquotQa, Batch, BatchAliquot, Storage
from flask import flash
from flask_login import current_user

from datetime import datetime
import json

from flask_admin import BaseView, expose

from flask_security import login_required
from flask_security import roles_required
from sa_jsonapi import serializer as jsonapi


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/api/physicians')
def get_physicians():
    response = jsonapi.get_collection(db.session, request.args, 'physicians')
    return jsonify(response.document), response.status


@app.route('/api/users')
def get_users():
    response = jsonapi.get_collection(db.session, request.args, 'users')
    return jsonify(response.document), response.status


@app.route('/api/subjects')
def get_subjects():
    response = jsonapi.get_collection(db.session, request.args, 'subjects')
    return jsonify(response.document), response.status


@app.route('/api/aliquots')
def get_aliquots():
    response = jsonapi.get_collection(db.session, request.args, 'aliquots')
    return jsonify(response.document), response.status


@app.route('/api/samples')
def get_samples():
    response = jsonapi.get_collection(db.session, request.args, 'samples')
    return jsonify(response.document), response.status


@app.route('/api/batches')
def get_batches():
    response = jsonapi.get_collection(db.session, request.args, 'batches')
    return jsonify(response.document), response.status


#
# @app.route('/api/subjects/<int:subject_id>')
# @login_required
# def get_subject(subject_id):
#     response = jsonapi.get_resource(db.session, request.args, 'subjects', subject_id)
#     return jsonify(response.document), response.status




# @app.route('/register')
# def register():
#     return render_template('auth/register.html')




# @app.route('/login')
# def login():
#     return render_template('auth/login.html')
# @app.route('/api/neurocode_id', methods=['GET'])
# def get_neurocode_id():
#     n_id = request.args.get('term')
#     try:
#         int(n_id)
#         exists = Subject.query.filter(Subject.neurocode==n_id).all()
#         print jsonify(exists)
#
#         if exists:
#             print jsonify(exists)
#
#     except:
#         return""



@app.route('/auto_subject', methods=['GET'])
def auto_subject():
    n_id = request.args.get('term')
    try:
        int(n_id)
        exists = Subject.query.filter(Subject.neurocode_id==n_id).first()
        if exists:
            return jsonify(exists)




            # res = subject_schema.dump(exists)
            # return jsonify(subject=res.data)
            # return ""

        return ""

    except:
        return""
#

@app.route('/auto_physician', methods=['GET'])
def auto_physician():
    msp = request.args.get('term')
    exists = Physician.query.filter(Physician.msp == msp).first()
    if exists:
        return ""
        # res = physician_schema.dump(exists)
        # return jsonify(physician=res.data)

    return ""

# physician_schema.dump(Physician.query.filter(Physician.msp == 111).first())

    # r1 = registration_schema.dump(Registration.query.filter(Physician.msp == 111).all())
    # rm = registrations_schema.dump(Registration.query.filter(Physician.msp == 111).all(), many=True)


# @app.route('/sop')
# def view_sops():
#     return render_template('sop/index.html')
#
# @app.route('/sop/create')
# def create_sops():
#     return render_template('sop/create.html')
#
# @app.route('/sop/<int:id>/edit')
# def edit_sops(id):
#     return render_template('sop/edit.html', id=id)


@app.route('/lab')
@roles_required('admin', 'lab_tech')
def lab():
    return render_template('lab/index.html')


# @app.route('/physician', methods=['GET'])
# def get_physician():
#     result = physicians_schema.dump(Physician.query.all())
#     return jsonify(result.data)
#
# @app.route('/api/aliquots', methods=['GET'])
# def get_aliquots():
#     result = aliquots_schema.dump(Aliquot.query.all())
#     return jsonify(result.data)
#
#
# @app.route('/api/samples', methods=['GET'])
# def get_sample():
#     result = samples_schema.dump(Sample.query.all())
#     return jsonify(result.data)


@app.route('/lab/physician', methods=['GET'])
def show_physicians():
    return render_template("lab/physician/index.html")


@app.route('/lab/physician/create', methods=['GET', 'POST'])
def create_physician():
    physician_form = PhysicianForm()
    return render_template("lab/physician/create_physician.html", physician_form=physician_form)



@app.route('/lab/subject', methods=['GET'])
def show_subjects():
    return render_template("lab/subject/index.html")


@app.route('/lab/subject/<int:subject_id>', methods=['GET'])
def show_subject(subject_id):
    subject = Subject.query.get(subject_id)

    return render_template("lab/subject/subject.html", subject=subject)


@app.route('/lab/create_subject', methods=['GET', 'POST'])
def create_subject():
    subject_form = SubjectForm()
    if subject_form.validate_on_submit():
        neurocode_id = subject_form.neurocode_id.data
        gender = subject_form.gender.data
        age = subject_form.age.data
        label = subject_form.label.data
        if Subject.query.filter(Subject.neurocode==subject_form.neurocode_id.data).first():
            flash("record already exists in our database", "error")
        else:
            s = Subject(age=age, neurocode=neurocode_id, label=label)
            g = Gender.query.get(gender)
            s.gender = g
            db.session.add(s)

            try:
                db.session.commit()
            except Exception as e:
                print "I should catch specific exception here"
                print e
            finally:
                # needs better message
                flash('New Subject Added', 'info')

            return redirect(url_for('show_subjects'))

    return render_template("lab/subject/create_subject.html", subject_form=subject_form)


@app.route('/lab/plate/create', methods=['GET', 'POST'])
def create_plate():
    return render_template("lab/plate/create_plate.html")


@app.route('/lab/aliquot', methods=['GET'])
def show_aliquot():
    return render_template("lab/aliquot/index.html")


@app.route('/lab/aliquot/create_aliquot', methods=['GET', 'POST'])
def create_aliquot():
    aliquot_form = NewAliquotForm()
    subjects = Subject.query.filter(Subject.samples != None).all()
    storage = Storage.query.all()

    if aliquot_form.validate_on_submit():
        print request.form
        sample = request.form.get('sample')
        subject = request.form.get('subject')
        barcode = request.form.get('barcode')
        store = request.form.get('storage')
        storage_db = Storage.query.get(store)
        s = Sample.query.get(sample)

        if s:
            a = Aliquot(barcode=barcode, created=datetime.now())
            a.user = current_user
            a.storage = storage_db if storage_db else None

            db.session.add(a)
            a.sample = s
            # s.append(a)
            db.session.commit()
            return redirect(url_for('show_aliquot'))

        else:
            flash('Please provide Barcode ', 'danger')

    return render_template("lab/aliquot/create_aliquot.html", aliquot_form=aliquot_form, subjects=subjects, storage=storage)



@app.route('/lab/sample', methods=['GET'])
def show_samples():
    return render_template("lab/sample/index.html")


@app.route('/lab/sample/<int:sample_id>', methods=['GET'])
def show_sample(sample_id):
    sample = Sample.query.get(sample_id)
    if sample:
        return render_template("lab/sample/sample.html", sample=sample)


@app.route('/lab/batch', methods=['GET'])
def show_batches():
    return render_template("lab/batch/index.html")


@app.route('/lab/batch/<int:batch_id>', methods=['GET'])
def show_batch(batch_id):
    batch = Batch.query.get(batch_id)
    if batch:
         return render_template("lab/batch/batch.html", batch=batch)


@app.route('/lab/batch/create', methods=['GET', 'POST'])
def create_batch():
    batch_form = BatchForm()

    return render_template("lab/batch/create_batch.html", batch_form=batch_form)




# @app.route('/lab/sop/sample_reception', methods=['GET', 'POST'])
# def sample_reception():
#     sample_form = SampleReceptionForm()
#     physician_form = PhysicianForm()
#     subject_form = SubjectForm()
#
#     return render_template("lab/sop/sample_reception/hide_multiform.html")


@app.route('/lab/sop/sample_reception', methods=['GET', 'POST'])
def sample_reception():
    sample_form = SampleReceptionForm()
    physician_form = PhysicianForm()
    subject_form = SubjectForm()
    lab_form = LaboratoryForm()

    if "step" not in request.form:
        print "physician page"
        return render_template("lab/sop/sample_reception/multipage.html", step="physician_form", physician_form=physician_form)

    elif request.form["step"] == "subject_form":
        print "subject form"

        if physician_form.validate_on_submit():
            print physician_form.msp.data
            print Physician.query.filter(Physician.msp == physician_form.msp.data).all()

        else:
            flash('Please provide post content', 'danger')

        return render_template("lab/sop/sample_reception/multipage.html", step="subject_form", subject_form=subject_form)

    elif request.form["step"] == "sample_form":
        print "sample form"
        if subject_form.validate_on_submit():
            print "subject form works"
            print request.form

        else:
            flash(subject_form.errors, 'danger')

        return render_template("lab/sop/sample_reception/multipage.html", step="sample_form", sample_form=sample_form)

    elif request.form["step"] == "finish":
        print "finish"
        print request.form
        if sample_form.validate_on_submit():
            print "Sample form good"
        else:
            flash('something went wrong', 'danger')

        return render_template("lab/sop/sample_reception/multipage.html", step="finish")

@app.route('/lab/sop/sample_reception2', methods=['GET', 'POST'])
def sample_reception2():


    return render_template("lab/sop/sample_reception/index2.html")

@app.route('/lab/sop/sample_reception2/step1')
def step1():
    physicians = Physician.query.all()
    return render_template("lab/sop/sample_reception/physician.html", physicians=physicians)


@app.route('/lab/sop/sample_reception2/step2')
def step2():
    return render_template("lab/sop/sample_reception/step2.html")


# def sample_reception():
#     sample_form = SampleReceptionForm()
#     physician_form = PhysicianForm()
#     lab_form = LaboratoryForm()
#     # print sample_form.validate_on_submit()
#     # print physician_form.validate_on_submit()
#
#     if sample_form.validate_on_submit() and physician_form.validate_on_submit():
#         print "hihi"
#
#             # and physician_form.validate_on_submit() and lab_form.validate_on_submit():
#
#         # neurocode_id = request.form['neurocode_id']
#         # age = request.form['age']
#         # gender = request.form['gender']
#         # sample_type = request.form['sample_type']
#         # first_name = request.form['physician_first_name']
#         # last_name = request.form['physician_last_name']
#         # msp = request.form['msp']
#         # institute = request.form['physician_institute']
#         # phone = request.form['physician_phone_number']
#         # fax = request.form['physician_fax']
#         # email = request.form['physician_email']
#         #
#         # new_subject = Subject(age, gender)
#         # new_sample = Sample(sample_type, datetime.now(), neurocode_id)
#         # for i in request.form:
#         #     if i.startswith("aliquot_barcode"):
#         #         new_sample.aliquots.append(Aliquot(request.form[i]))
#         #
#         # new_subject.samples.append(new_sample)
#         # new_physician = Physician(first_name, last_name, msp, phone, fax, email)
#         # new_institute = Institute(institute)
#         # new_physician.institutes.append(new_institute)
#         # new_subject.physicians.append(new_physician)
#         #
#         # db.session.add(new_subject)
#         #
#         # db.session.flush()
#         # db.session.commit()
#
#         return redirect('/lab')
#
#
#     return render_template('lab/sop/sample_reception/multipage.html',
#                            sample_form=sample_form, physician_form=physician_form, lab_form=lab_form)






def upsert_qa(aliquot_id, qa_id, tech_id, value):
    a = Aliquot.query.get(aliquot_id)
    qa = Qa.query.get(qa_id)

    exists = AliquotQa.query.filter(AliquotQa.aliquot_id == aliquot_id).filter(AliquotQa.qa_id == qa_id).all()
    if exists:
        exists[0].value = value
        exists[0].date_entered = datetime.now()
        exists[0].tech_id = tech_id
        print "updated"
    else:
        aqa_2 = AliquotQa(a, qa, value, tech_id, datetime.now())
        db.session.add(aqa_2)
        print "added"


@app.route('/lab/sop/electrophoresis', methods=['GET', 'POST'])
def electrophoresis():
    electrophoresis_form = ElectrophoresisForm()
    results = db.session.query(Subject.id, Gender.name, Subject.age, Subject.neurocode, Sample.id, Sample.type, Aliquot.barcode).join(Sample, Sample.subject_id == Subject.id).join(
        Aliquot, Aliquot.sample_id == Sample.id).join(Gender, Gender.id==Subject.gender_id).all()

    if electrophoresis_form.validate_on_submit():
        print request.form

        aliquot_id = request.form.get("aliquot")
        total_volume = request.form['total_volume']
        conc_abs = request.form['DNA_conc_abs']
        conc_flr = request.form['DNA_conc_flr']
        qual = request.form['DNA_qual']
        integrity = request.form['DNA_integrity']
        notes = request.form['notes']

        a = Aliquot.query.get(aliquot_id)

        # qa_id, aliquot_id, value,
        qa_2 = Qa.query.get(2)

        upsert_qa(aliquot_id, 2, 1, total_volume)
        upsert_qa(aliquot_id, 3, 1, conc_abs)
        upsert_qa(aliquot_id, 4, 1, conc_flr)
        upsert_qa(aliquot_id, 5, 1, qual)
        upsert_qa(aliquot_id, 6, 1, integrity)
        upsert_qa(aliquot_id, 7, 1, notes)

        # exists = AliquotQa.query.filter(AliquotQa.aliquot_id == a.id).filter(AliquotQa.qa_id == qa_2.id).all()
        #
        # if exists:
        #     exists[0].value = total_volume
        #     exists[0].date_entered = datetime.now()
        #     exists[0].tech_id = 3
        #     print "updated"
        # else:
        #     aqa_2 = AliquotQa(a, qa_2, total_volume, '', datetime.now())
        #     db.session.add(aqa_2)
        #     print "added"

        db.session.flush()
        db.session.commit()


        print total_volume, conc_abs, conc_flr, qual, integrity, notes
        return redirect('/lab')



    return render_template('lab/sop/dna_electrophoresis/index.html', form=electrophoresis_form, results=results)



@app.route('/lab/sop/batch_aliquots', methods=['GET', 'POST'])
def batch_aliquots():
    aliquots = Aliquot.query.all()

    print request.form

    return render_template('lab/aliquot/batch_aliquots.html', aliquots=aliquots, form=ElectrophoresisForm())



@app.route('/lab/sop/tbd')
def extraction():

    batches = Batch.query.all()


    return render_template('lab/sop/tbd/index.html', batches=batches)




# @app.route('/_get_data')
# def subject_info():
#     results = db.session.query(Subject.id, Subject.age, Sample.neurocode_id, Aliquot.barcode).outerjoin(Sample, Sample.subject_id == Subject.id).outerjoin(Aliquot, Aliquot.sample_id == Sample.id).all()
#     res = []
#     for u in results:
#         dicts = {"id":u.id, "age":u.age, "neurocode_id":u.neurocode_id, "barcode":u.barcode}
#         res.append(dicts)
#
#     return jsonify(results)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    subject = Subject.query.all()
    res = subjects_schema.dump(subject)
    return jsonify({'subject': res.data})


    #
    # if request.args:
    #     term = request.args.get('neurocode_id')
    #     try:
    #         subject = Subject.query.filter(Subject.neurocode_id==term).all()
    #     except IntegrityError:
    #         return jsonify({'message': 'New Subject'})
    #
    #     res = subject_schema.dump(subject)
    #     return jsonify({'subject': res.data})
    #
    # return jsonify({'subject': ''})

#
# def run():
#     app.run()


