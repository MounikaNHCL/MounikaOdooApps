from odoo import models,fields,api,_,tools

class ClickPassword(models.Model):
    _name = 'click.password'

    name = fields.Char(string="Name")
    user_name = fields.Char(string="User Name")
    password = fields.Char(string="Password")
    url_link = fields.Text(string="URL")
    note     = fields.Html(string="Note")
    create_date = fields.Datetime(string="CreateDateTime", default=lambda self: fields.Datetime.now())
    user_id = fields.Many2one('res.users', 'Created User', default=lambda self: self.env.user, readonly=True)
    department_id = fields.Many2one('hr.department', 'Department',readonly=True)
    manager_id = fields.Many2one('hr.employee', 'Manager',readonly=True)
    manager_user_id = fields.Many2one('res.users', 'User Manager')
    manager_true = fields.Boolean(String="Own Manager",compute='_compute_manager_true')
    user_id_true = fields.Boolean(String="Own Manager",compute='_compute_manager_true')


    @api.depends('user_id','create_date')
    def _compute_manager_true(self):
        for each in self:
            each.manager_true = False
            each.user_id_true = False
            if each.manager_id == self.env.user.employee_id:
                each.manager_true =True
            if self.env.user == self.user_id:
                each.user_id_true = True

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            if self.user_id.department_id:
               self.department_id = self.user_id.department_id.id
               self.manager_id = self.user_id.department_id.manager_id.id
               self.manager_user_id = self.user_id.department_id.manager_id.user_id.id
            else:
                self.department_id =self.user_id.employee_id.department_id.id
                self.manager_id =self.user_id.employee_id.parent_id.id
                self.manager_user_id = self.user_id.employee_id.parent_id.user_id.id
    def name_get(self):
        data = []
        for rec in self:
            data.append((rec.id, '%s' % (rec.name)))
            return data


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    click_login_page = fields.Char(string="Click Login Page")


class Company(models.Model):
    _inherit = "res.company"

    click_login_page = fields.Char(string="Click Login Page")
