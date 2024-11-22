from flask import Blueprint

recruiter_bp = Blueprint('recruiter', __name__)

from . import routes, auth,post_job,profile
