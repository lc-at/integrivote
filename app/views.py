import re
import time

import requests
from flask import (abort, flash, g, redirect, render_template, request,
                   session, url_for)

from . import app
from .models import Preference, Vote, db


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
        data = {
            'token_id': request.form.get('token_id'),
            'nisn': request.form.get('nisn'),
            'nama_ibu_kandung': request.form.get('mother_name'),
            'kode_captcha': request.form.get('captcha')
        }

        class_ = request.form.get('class')
        if not class_ or not class_.isdigit() or int(class_) >= len(
                app.config['CLASSES']) or int(class_) < 0:
            abort(403)
        class_ = int(class_)

        for v in data.values():
            if not v and v != '':
                abort(403)

        req = requests.post('https://referensi.data.kemdikbud.go.id/' +
                            'nisn/index.php/Cindex/caribynisn/',
                            data=data)
        if 'Status Aktif' in req.text:
            nisn = request.form.get('nisn')
            name, pob, dob, gender, status = re.findall(
                r'<td>(.+?)</td>\r\n.+?</tr', req.text, re.M)[1:]
            session['nisn'] = nisn
            session['name'] = name
            session['pob'] = pob
            session['dob'] = dob
            session['gender'] = gender
            session['status'] = status
            session['class'] = class_

            session['verified'] = True

            return redirect(url_for('root'))

        flash(' '.join([
            'Data yang Anda masukkan tidak valid! Silahkan mencoba kembali.',
            'Jika data sudah benar, kemungkinan Anda mengetikkan kode yang tidak',
            'sesuai dengan gambar (captcha).'
        ]))

    req = requests.get('https://referensi.data.kemdikbud.go.id/nisn/')
    data = {
        'token_id':
        re.findall(r'token_id".+?value="(.*?)" d', req.text, re.M).pop(),
        'captcha_url':
        re.findall(r'captImg".+?src="(.+?)" w', req.text, re.M).pop()
    }
    return render_template('identity_verification.html', **data)


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
        vote.status = session.get('status')
        vote.gender = session.get('gender')
        vote.class_ = session.get('class')
        vote.choice = int(choice)

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

    data = {'total_votes': Vote.query.count(), 'per_candidate_votes': []}
    for cand_index in range(len(app.config['CANDIDATES'])):
        data['per_candidate_votes'].append(
            Vote.query.filter_by(choice=cand_index).count())

    return render_template('stats.html', data=data)


@app.route('/clearsession')
def clear_session():
    if session.get('verified'):
        del session['verified']
    return redirect(url_for('root'))
