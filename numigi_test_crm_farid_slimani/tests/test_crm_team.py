from psycopg2 import IntegrityError

from odoo.tests.common import SavepointCase,tagged
from odoo.exceptions import ValidationError
import pytest
@tagged('post_install', '-at_install')
class TestCrmTeamBase(SavepointCase):
   
    @classmethod
    def setUpClass(cls):
        super(TestCrmTeamBase, cls).setUpClass()
        cls.user_1 = cls.env["res.users"].create({"name": "User1",
                                                  "login": "user1@ts.fr",
                                                  "email":"user1@ts.fr"})
        cls.user_2 = cls.env["res.users"].create({"name": "User2",
                                                  "login": "user2@ts.fr",
                                                  "email":"user2@ts.fr",
                                                  })

        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.team = cls.env["crm.team"].create({"name": "SAV",
                                                "member_ids": [(6, 0, [cls.user_1.id,cls.user_2.id])]
                                                })
        cls.lead = cls.env["crm.lead"].create({"name": "Test lead",
                                               "team_id": cls.team.id, 
                                               "create_date" : "2020-02-03 00:00:00",
                                                })
        # print('self.lead=>',cls.lead.team_id)    

class TestCrmTeam(TestCrmTeamBase):

    def test_notify_members(self):
        with pytest.raises(ValidationError):
         
            self.team.notify_members()  
            raise ValidationError("Notification non envoyée") 



    def test_compute_emails_field(self):
        assert  self.team.emails == self.user_1.email+','+self.user_2.email   


      