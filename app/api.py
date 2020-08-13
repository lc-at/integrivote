
from flask import Blueprint, abort, jsonify, request

from .models import Student

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/check_student_id')
def check_student_id():
    id = request.args.get('id')
    if not id:
        abort(403)
    student = Student.query.filter_by(id=id).first()
    return jsonify(ok=student is not None)
