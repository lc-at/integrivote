from hashlib import md5
import re

from flask import (Blueprint, Response, abort, current_app, flash, redirect,
                   render_template, request, session, url_for)

from .models import Preference, Vote, db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.before_request
def check_auth():
    if not session.get('admin') and request.endpoint != 'admin.login':
        return redirect(url_for('admin.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin'):
        return redirect(url_for('admin.root'))
    elif request.method == 'POST':
        password = request.form.get('password')
        if not password:
            abort(403)
        elif md5(password.encode()).hexdigest() == Preference.get(
                'MASTER_PASSWORD'):
            session['admin'] = True
            return redirect(url_for('admin.root'))
        else:
            flash('Password yang Anda masukkan salah.')
    return render_template('admin/login.html')


@bp.route('/')
def root():
    data = {
        'total_data': {
            'verified': Vote.query.filter_by(verified=True).count(),
            'unverified': Vote.query.filter_by(verified=False).count(),
        }
    }
    return render_template('admin/index.html', **data)


@bp.route('/manual-verification')
def manual_verification():
    accepted_id = request.args.get('accepted_id')
    rejected_id = request.args.get('rejected_id')
    if rejected_id:
        vote = Vote.query.filter_by(id=rejected_id,
                                    verified=False).first_or_404()
        db.session.delete(vote)
        db.session.commit()
        flash('Sukses menghapus suara dengan NISN: %s' % rejected_id)
        return redirect(url_for(request.endpoint))
    elif accepted_id:
        vote = Vote.query.filter_by(id=accepted_id,
                                    verified=False).first_or_404()
        vote.verified = True
        db.session.commit()
        flash('Sukses mengesahkan suara dengan NISN: %s' % accepted_id)
        return redirect(url_for(request.endpoint))

    votes = Vote.query.filter_by(verified=False).all()
    return render_template('admin/manual_verification.html', votes=votes)


@bp.route('/toggle-voting')
def toggle_voting():
    p = Preference.get('ACCEPTS_VOTE')
    Preference.set('ACCEPTS_VOTE', not bool(p))
    return redirect(url_for('admin.root'))


@bp.route('/export-csv')
def export():
    rows = Vote.query.all()
    classes = current_app.config['CLASSES']

    def generate():
        yield ','.join([
            'waktu', 'nisn', 'nama', 'kelas', 'tempat lahir', 'tanggal lahir',
            'jenis kelamin', 'nama ibu kandung', 'terverifikasi'
        ]) + '\n'
        for row in rows:
            coldata = [
                round(row.ts), row.id, row.name, classes[row.class_], row.pob,
                row.dob, row.gender, row.mother_name,
                int(row.verified)
            ]
            for i, value in enumerate(coldata):
                if not isinstance(value, str):
                    coldata[i] = str(value)
                if ',' in coldata[i]:
                    coldata[i] = coldata[i].replace(',', ' ')

            yield ','.join(coldata) + '\n'

    return Response(generate(), mimetype='text/csv')


@bp.route('/delete-vote')
def delete_vote():
    nisn = request.args.get('nisn')
    vote = Vote.query.filter_by(id=nisn).first()
    if not (nisn and vote):
        flash('Tidak ditemukan suara terkait dengan NISN tersebut.')
    else:
        db.session.delete(vote)
        db.session.commit()
        flash('Sukses menghapus suara dengan NISN: %s' % nisn, 'success')
    return redirect(url_for('admin.root'))


@bp.route('/delete-all')
def delete_all():
    Vote.query.delete()
    db.session.commit()
    flash('Seluruh data suara telah dihapus.', 'success')
    return redirect(url_for('admin.root'))


@bp.route('/change-password', methods=['POST'])
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    new_password2 = request.form.get('new_password2')
    old_password_hash = md5(
        old_password.encode()).hexdigest() if old_password else None
    if not (old_password and new_password and new_password2) \
            or new_password != new_password2 \
            or old_password_hash != Preference.get('MASTER_PASSWORD'):
        flash('Data yang Anda masukkan tidak valid.')
        return redirect(url_for('admin.root'))
    Preference.set('MASTER_PASSWORD', md5(new_password.encode()).hexdigest())
    flash('Password berhasil diubah. Silahkan masuk kembali.', 'success')
    return logout()


@bp.route('/logout')
def logout():
    del session['admin']
    return redirect(url_for('admin.root'))
