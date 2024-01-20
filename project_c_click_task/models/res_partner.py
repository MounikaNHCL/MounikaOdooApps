from odoo import models, fields, api, _
import xlwt
import base64
from io import BytesIO
from datetime import datetime

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
class Tasks(models.Model):
    _inherit = 'project.task'

    user_group_id = fields.Boolean(string="User Only",compute="_compute_user_group_id")
    def _compute_user_group_id(self):
        self.user_group_id = self.env['res.users'].has_group('project.group_project_manager')

class ProjectTaskExport(models.Model):
    _name = 'project.task.export'

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    project_export_lines = fields.One2many('project.export.lines','project_export_id')

    def export_project_data(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        heading = xlwt.easyxf("align: vert centre, horiz centre;font: bold on,height 200")
        xlwt.add_palette_colour("warning", 0x21)
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        sheet = workbook.add_sheet('Report', cell_overwrite_ok=True)
        sheet.write(0, 0, 'Project', heading)
        sheet.write(0, 1, 'DATE', heading)
        sheet.write(0, 2, 'Project Manager', heading)
        sheet.write(0, 3, 'status', heading)
        sheet.write(0, 4, 'Task', heading)
        sheet.write(0, 5, 'Task Users', heading)
        row = 0

        all_projects = self.env['project.project'].search([('date_start','>=',self.from_date),('date_start','<=',self.to_date)])
        for obj in all_projects:
            row = row + 1

            sheet.write(row, 0, obj.name)
            sheet.write(row, 1, obj.date_start, date_format)
            sheet.write(row, 2, obj.user_id.name)
            sheet.write(row, 3, obj.sudo().stage_id.name)
            for task_obj in obj.task_ids:
                row = row + 1
                sheet.write(row, 4, task_obj.sudo().name)
                sheet.write(row, 5, task_obj.user_ids.mapped('name'))

            stream = BytesIO()
            workbook.save(stream)
            out = base64.encodebytes(stream.getvalue())
            attachment = self.env['ir.attachment'].sudo()
            filename = "Project Excell Report" +".xls"
            print(filename)
            attachment_id = attachment.create(
                {'name': filename,
                 'type': 'binary',
                 'public': False,
                 'datas': out})
        if attachment_id:
            report = {
                'type': 'ir.actions.act_url',
                'url': '/web/content/%s?download=true' % (attachment_id.id),
                'target': 'self',
            }
            return report


class ProjectExportLines(models.Model):
    _name = 'project.export.lines'

    project_export_id = fields.Many2one('project.task.export')
    project_id = fields.Many2one('project.project',string="Project")
    date = fields.Date(string="Date")
    stage_id = fields.Many2one('project.task',string="State")



class Tasks(models.Model):
    _inherit = 'project.task'

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False)])

    # @api.multi
    def _inverse_state(self):
        """
        For sure you can change body or subject, and generate those based on a template
        """
        for obj in self:
            # message = _("State is changed to '%s'") % (self.stage_id.name)
            message = _("State is changed to '%s'<br> Changed By: %s <br> Date&Time: %s") % (
            self.stage_id.name, self.env.user.name, datetime.now())
            # email_to = 'mounika@nhclindia.com',
            email_to = obj.project_id.user_id.email

            obj.message_post(body=_('Task Information'),
                         message_type="notification", subtype_xmlid="mail.mt_comment")
            obj.message_post(body=message, subject="State is changed", subtype_xmlid="mail.mt_comment",email_from=self.env.user.email,email_to=email_to,author_id=False)

    stage_id = fields.Many2one('project.task.type', string='Stage', compute='_compute_stage_id',
                               store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
                               default=_get_default_stage_id, group_expand='_read_group_stage_ids',
                               domain="[('project_ids', '=', project_id)]", copy=False, task_dependency_tracking=True,inverse=_inverse_state)
    add_followers_multi = fields.Many2many('res.partner','add_followers_partrel',string="accept task",tracking=True)
    accept_task = fields.Boolean(string="Accept Task")
    accept_task_lines = fields.One2many('accept.task.lines','accept_task_ids')

    @api.onchange('user_ids')
    def _onchange_user_ids_new(self):
        if self.user_ids:
            list = []
            for user in self.user_ids:
               dict = (0, 0, {
                    'Follwer': user.partner_id._origin.id,
                })
               list.append(dict)
            self.accept_task_lines = False
            self.accept_task_lines = list
    def action_add_followers(self):
        mail_invite = self.env['mail.wizard.invite'].with_context({
            'default_res_model': 'project.task',
            'default_res_id': self.id
        }).sudo().with_user(self.env.user).create({
            # 'partner_ids': mainl_send_list,
            'partner_ids': self.add_followers_multi.ids,
            'send_mail': True})
        # with rec.mock_mail_gateway():
        mail_invite.add_followers()
        message = _("Followers added '%s'<br> Date&Time: %s") % (
            self.add_followers_multi.mapped('name'),datetime.now())
        # email_to = 'mounika@nhclindia.com',
        self.message_post(body=message,message_type='comment', subtype_xmlid='mail.mt_comment')


    # reg = {
    #     'res_id': record.id,
    #     'res_model': 'crm.lead',
    #     'partner_id': partner_id,
    # }
    # if not env['mail.followers'].search(
    #         [('res_id', '=', record.id), ('res_model', '=', 'crm.lead'), ('partner_id', '=', partner_id)]):
    #     follower_id = env['mail.followers'].create(reg)

class AcceptTaskLines(models.Model):
    _name = 'accept.task.lines'
    _inherit = ['mail.thread']


    accept_task_ids = fields.Many2one('project.task')
    accept = fields.Boolean(string="Accept",store=True)
    Follwer = fields.Many2one('res.partner',string="Follower")
    @api.onchange('accept')
    def _onchange_accept(self):
        if self.accept:
            self.accept = True
            mail_invite = self.env['mail.wizard.invite'].with_context({
                'default_res_model': 'project.task',
                'default_res_id': self.accept_task_ids.id
            }).sudo().with_user(self.env.user).create({
                'partner_ids': self.Follwer.ids,
                'send_mail': True})
            mail_invite.sudo().add_followers()
            message = _("Accepted User '%s'<br> On Date&Time: %s") % (
                self.Follwer.name, datetime.now())
            # self.accept_task_ids.user_ids +=
            self.accept_task_ids.sudo().message_post(body=message, message_type='comment', subtype_xmlid='mail.mt_note')
        return

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    set_default = fields.Boolean('Default?')


class ProjectDefault(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        rtn = super(ProjectDefault, self).create(vals)
        stage_obj = self.env['project.task.type']
        stage_ids = stage_obj.search([('set_default', '=', True)])
        project_ids = [x.id for x in rtn]
        for stage in stage_ids:
            stage.sudo().write({'project_ids': [(4, tuple(project_ids), 0)]})
        return rtn
