import requests

from odoo import models, fields, api


class LinkedinPost(models.Model):
    _name = 'linkedin.post'
    _description = 'Linkedin Post '

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    config_id = fields.Many2one('linkedin.config', required=True)
    content = fields.Text(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('failed', 'Failed'),
    ], default='draft')

    def action_post(self):
        self.ensure_one()
        url = 'https://api.linkedin.com/v2/ugcPosts'
        headers = {
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': f'Bearer {self.config_id.auth_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'author': f'urn:li:person:{self.config_id.linkedin_user}',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': self.content
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }

        response  = requests.post(url=url,headers=headers,json=params)
        if response.status_code == 201:
            self.state = 'posted'
        else:
            self.state = 'failed'