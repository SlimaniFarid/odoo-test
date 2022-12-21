from odoo import fields, models,api
from datetime import timedelta
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)




class CrmTeam(models.Model):
    _inherit = "crm.team"


    emails      =   fields.Char("Emails des membres", compute="_compute_members_emails_list")

   
    @api.depends('member_ids','member_ids.email')
    def _compute_members_emails_list(self):
        for rec in self:
            rec.emails = ','.join(self._get_mails_members_by_one_team(rec))

    def _get_mails_members_by_one_team(self,team):
        return [member.email for member in team.member_ids if member.email]
   
    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            self.member_ids =[(4,self.user_id.id)]      


            
    

    def notify_members(self):
        leads = self.get_lead_exceeding_ten_days_in_draft_status()
        if len(leads)>0:
            self.send_mail_notofocation_team_members(leads)

    def get_lead_exceeding_ten_days_in_draft_status(self):
        start_stage = self.env['crm.stage'].search([],order='sequence',limit=1)
        if start_stage:
            today = fields.Datetime.now()
            domain = [('stage_id','=',start_stage.id),('team_id','!=',False),('create_date','<', today - timedelta(days = 0))]
            leads = self.env['crm.lead'].search(domain)
            return leads
        else:
            return False      


    def send_mail_notofocation_team_members(self,leads):
        template = self.env.ref('numigi_test_crm_farid_slimani.team_notification',raise_if_not_found=False)
        mail_ids = []
        if not template:
            raise UserError(("Le modèle d'e-mail n'est pas dans la base de données"))
        for lead in leads.filtered(lambda l: l.team_id.emails != ""):

            lead_url = lead._notify_get_action_link('view')
            email_values = {'lead_url': lead_url,
                            'lead_name':lead.name,   
                            }
            template.write({'email_to':lead.team_id.emails})
            mail_ids.append(template.with_context(email_values).send_mail(self.env.user.id))

        self.env['mail.mail'].search([('id','in',mail_ids)]).process_email_queue()
      
                