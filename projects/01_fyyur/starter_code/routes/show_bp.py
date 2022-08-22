from flask import Blueprint

from controllers.show_controller import shows, create_shows, create_show_submission

show_bp = Blueprint('show_bp', __name__)

show_bp.route('/shows')(shows)
show_bp.route('/shows/create')(create_shows)
show_bp.route('/shows/create', methods=['POST'])(create_show_submission)
