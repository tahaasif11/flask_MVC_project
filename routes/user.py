from flask import Blueprint
from controllers import user_controller
form_bp = Blueprint("form_bp", __name__)

# routes
form_bp.route('/')(user_controller.home)
form_bp.route('/profile')(user_controller.profile)
form_bp.route('/forgot_password',  methods=['POST'])(user_controller.forgot_password)
form_bp.route('/reset_password/<token>', methods=['GET', 'POST'])(user_controller.reset_password)
form_bp.route('/update_reset_password', methods=['POST'])(user_controller.update_reset_password)
form_bp.route('/logout')(user_controller.logout)
form_bp.route('/login', methods=['POST'])(user_controller.login)
form_bp.route('/get_all_data',  methods=['GET','POST'])(user_controller.get_all_data)
form_bp.route('/register',  methods=['POST'])(user_controller.register)
form_bp.route('/get_one_data',  methods=['POST'])(user_controller.get_one_data)
form_bp.route('/update_user', methods=['POST'])(user_controller.update_user)

form_bp.errorhandler(404)(user_controller.page_not_found)
form_bp.errorhandler(500)(user_controller.server_error)