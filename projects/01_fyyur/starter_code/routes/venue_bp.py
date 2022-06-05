# import sys
# sys.path.append('../')

from flask import Blueprint
from controllers.venue_controller import index, venues, search_venues, show_venue, create_venue_form, create_venue_submission, delete_venue, edit_venue, edit_venue_submission

venue_bp = Blueprint('venue_bp', __name__)

venue_bp.route('/')(index)
venue_bp.route('/venues')(venues)
venue_bp.route('/venues/search', methods=['POST'])(search_venues)
venue_bp.route('/venues/<int:venue_id>')(show_venue)
venue_bp.route('/venues/create', methods=['GET'])(create_venue_form)
venue_bp.route('/venues/create', methods=['POST'])(create_venue_submission)
venue_bp.route('/venues/<int:venue_id>', methods=['DELETE'])(delete_venue)
venue_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])(delete_venue)
venue_bp.route('/venues/<int:venue_id>/edit', methods=['POST'])(edit_venue_submission)