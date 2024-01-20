# -*- coding: utf-8 -*-
from odoo import http, models, fields, api, tools,SUPERUSER_ID,_
from odoo.http import request
from odoo.addons.web.controllers.home import Home as WebHome
from odoo.service import security
from odoo.exceptions import AccessError
import json
from urllib.parse import unquote

class Home(WebHome):

    def _login_redirect(self, uid, redirect=None):
        print('MOUNIKAAAAAA LOGIN')
        #
        # super()._login_redirect(uid, redirect=
        # self.env['res.config.settings'].search([])
        # / web  # menu_id=77&action=116
        redirect = '/web#action=116&cids=6&menu_id=77'
        # redirect=request.env['res.config.settings'].sudo().search([],limit=1).login_default_url
        default_login_company = request.env['res.company'].search([('click_login_page','!=',False)])
        if default_login_company:
            redirect = default_login_company.click_login_page


        return super()._login_redirect(uid, redirect=redirect)

