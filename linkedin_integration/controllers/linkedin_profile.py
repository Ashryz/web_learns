import logging

from odoo import http
from odoo.http import request
import requests

_logger = logging.getLogger(__name__)

class LinkedInProfileOauth2(http.Controller):

    @http.route('/linkedin/callback', type='http', auth='user', website=True)
    def linkedin_auth_callback(self, code=None, state=None, error=None, error_description=None, **kwargs):
        config = request.env['linkedin.config'].search([('linkedin_state', '=', state)])
        try:
            access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'redirect_uri': 'http://localhost:8018/linkedin/callback',
            }

            response = requests.post(url=access_token_url, headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                     params=params)

            access_token = response.json().get('access_token')
            config.write({
                'auth_token': access_token,
                'state': 'connected'
            })
            return  request.render('linkedin_integration.linkedin_success_template',{})
        except Exception as e:
            _logger.error("Error: %s",str(e))
            if config:
                config.write({
                    'state': 'error'
                })
            return  request.render('linkedin_integration.linkedin_failed_template',{'error':error,'error_description':error_description})
