from flask import Blueprint

from controllers.artist_controller import artists, search_artists, show_artist, edit_artist, \
    edit_artist_submission, create_artist_form, create_artist_submission

artist_bp = Blueprint('artist_bp', __name__)

artist_bp.route('/artists')(artists)
artist_bp.route('/artists/search', methods=['POST'])(search_artists)
artist_bp.route('/artists/<int:artist_id>')(show_artist)
artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])(edit_artist)
artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])(edit_artist_submission)
artist_bp.route('/artists/create', methods=['GET'])(create_artist_form)
artist_bp.route('/artists/create', methods=['POST'])(create_artist_submission)