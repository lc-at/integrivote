import re
import time

import requests
from flask import (abort, flash, g, redirect, render_template, request,
                   session, url_for)

from . import app
from .models import Preference, Student, Vote, db


@app.before_request
def add_context():
    g.accepts_vote = Preference.get('ACCEPTS_VOTE')


@app.route('/')
def root():
    if not session.get('verified'):
        return redirect(url_for('verify_identity'))
    return redirect(url_for('vote'))


@app.route('/verification', methods=['GET', 'POST'])
def verify_identity():
    if session.get('verified'):
        return redirect(url_for('root'))
    elif request.method == 'POST':
        nisn = request.form.get('nisn')
        name = request.form.get('name')
        mother_name = request.form.get('mother_name')
        class_ = request.form.get('class')
        if not (class_ and nisn and mother_name) or \
                not class_.isdigit() or int(class_) >= len(
                app.config['CLASSES']) or int(class_) < 0 \
                or len(mother_name) < 3:
            abort(403)
        class_ = int(class_)
        student = Student.query.filter(
            Student.id == nisn, Student.mother_name.like(f'%{mother_name}%'),
            Student.class_ == app.config['CLASSES'][class_]).first()
        if student or name:
            if name and (Student.query.filter_by(id=nisn).first() or \
                    len(name) < 4):
                abort(403)
            session['nisn'] = student.id if student else nisn.strip()
            session['name'] = student.name if student else name.strip()
            session['pob'] = student.pob if student else '-'
            session['dob'] = student.dob if student else '-'
            session['gender'] = student.gender if student else '-'
            session[
                'mother_name'] = student.mother_name if student else mother_name.strip(
                )
            session['class'] = class_ if student else class_
            session['verified'] = True
            session['bypassed'] = True if name else False

            return redirect(url_for('root'))

        flash(' '.join([
            'NISN tidak cocok dengan nama ibu kandung dan kelas.',
            'Jika kelas sudah benar, coba masukkan hanya sebagian nama ibu kandung.',
        ]))

    return render_template('identity_verification.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if not session.get('verified'):
        return redirect(url_for('root'))

    vote = Vote.query.filter_by(id=session.get('nisn')).first()

    if request.method == 'POST':
        choice = request.form.get('choice')
        if not g.accepts_vote or vote or not choice.isdigit() \
                or int(choice) >= len(app.config['CANDIDATES']) \
                or int(choice) < 0:
            abort(403)

        vote = Vote()
        vote.id = session.get('nisn')
        vote.ts = time.time()
        vote.dob = session.get('dob')
        vote.pob = session.get('pob')
        vote.name = session.get('name')
        vote.gender = session.get('gender')
        vote.mother_name = session.get('mother_name')
        vote.class_ = session.get('class')
        vote.choice = int(choice)
        vote.verified = False if session.get('bypassed') else True

        if not vote.validate() or Vote.query.filter_by(id=vote.id).first():
            abort(403)

        db.session.add(vote)
        db.session.commit()

    return render_template('vote.html',
                           candidates=app.config['CANDIDATES'],
                           vote=vote)


@app.route('/stats')
def stats():
    if g.accepts_vote and not (
            session.get('verified')
            and Vote.query.filter_by(id=session.get('nisn')).first()):
        return redirect(url_for('root'))

    data = {
        'verified': {
            'total_votes':
            Vote.query.filter_by(verified=True).count(),
            'per_candidate_votes': [
                Vote.query.filter_by(choice=i, verified=True).count()
                for i in range(len(app.config['CANDIDATES']))
            ]
        },
        'unverified': {
            'total_votes':
            Vote.query.filter_by(verified=False).count(),
            'per_candidate_votes': [
                Vote.query.filter_by(choice=i, verified=False).count()
                for i in range(len(app.config['CANDIDATES']))
            ]
        }
    }
    return render_template('stats.html', data=data)


@app.route('/clearsession')
def clear_session():
    if session.get('verified'):
        del session['verified']
    if session.get('bypassed'):
        del session['bypassed']
    return redirect(url_for('root'))
