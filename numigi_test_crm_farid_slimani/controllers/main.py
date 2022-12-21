# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_crm.controllers.main import WebsiteForm
import logging
_logger = logging.getLogger(__name__)

class WebsiteForm(WebsiteForm):


    def insert_record(self, request, model, values, custom, meta=None):
        team = request.env.ref("numigi_test_crm_farid_slimani.team_sav",raise_if_not_found=False)
        if team :
            values['team_id'] = team.id
        result = super(WebsiteForm, self).insert_record(request, model, values, custom, meta=meta)
        return result