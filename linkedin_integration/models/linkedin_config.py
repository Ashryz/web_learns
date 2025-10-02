import urllib.parse

import requests

from odoo import models, fields, api
import secrets

class LinkedinConfig(models.Model):
    _name = 'linkedin.config'
    _description = 'Linkedin Config'

    name = fields.Char(required=True)
    client_id = fields.Char(required=True)
    client_secret = fields.Char(required=True)
    state = fields.Selection([
        ('not_connected', 'Not Connected'),
        ('connected', 'Connected'),
        ('error', 'Error')
    ],default='not_connected')
    active = fields.Boolean(default=True)
    linkedin_state = fields.Char()
    oauth_scopes = fields.Char(default="openid,profile,email,w_member_social")
    linkedin_user = fields.Char()
    auth_token = fields.Char()

    def action_auth_linkedin(self):
        self.ensure_one()
        state = secrets.token_urlsafe(32)
        self.linkedin_state = state
        url = "https://www.linkedin.com/oauth/v2/authorization"
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri':'http://localhost:8018/linkedin/callback',
            'state': state,
            'scope': self.oauth_scopes
        }

        return {
            'type': 'ir.actions.act_url',
            'url': f'{url}?{urllib.parse.urlencode(params)}',
            'target': 'new'
        }

    def action_get_linkedin_user(self):
        self.ensure_one()
        url = 'https://api.linkedin.com/v2/userinfo'
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url=url,headers=headers)
        self.linkedin_user = response.json().get('sub')
