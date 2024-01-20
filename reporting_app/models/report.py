from odoo import models, fields, _, api
import base64

class ReportAppClick(models.Model):
    _name = "report.app.click"
    _inherit = ['mail.thread']


    title = fields.Char(string='Title')
    department_ids = fields.Many2many('hr.department','hr_department_new_rel',string="Department")
    manager_ids = fields.Many2many('hr.employee','hr_employee_new_rel',string="Manager")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, required=True)
    project_ids = fields.Many2many('project.project','project_project_new_rel',string="Project")
    time_sheet_lines = fields.One2many('timesheet.report.lines','report_app_id')
    category_id = fields.Many2one('report.config',string="Category")
    create_date = fields.Date('Date', default=fields.Date.today)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company,
                                      readonly=True,
                                      copy=False)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    description = fields.Html(string='Body')
    attachment_ids = fields.Many2many('ir.attachment',string="Attachment")
    state = fields.Selection(
        [('draft', 'Draft'), ('sent', 'Sent')], string="State", default="draft")

    def action_end_email(self):
        message = _("Reporting from '%s'  To '%s'<br> Title : %s <br> Category: %s <br> Projects: %s <br> Body: %s ") % (
            self.from_date, self.to_date, self.title,self.category_id,self.project_ids.mapped('name'),self.description)
        attachments = []
        for i in self.attachment_ids:
            attachments.append(i.id)
        mail_invite = self.env['mail.wizard.invite'].with_context({
            'default_res_model': 'report.app.click',
            'default_res_id': self.id
        }).sudo().with_user(self.env.user).create({
            'partner_ids': self.manager_ids.work_contact_id.ids,
            'send_mail': True})
        mail_invite.sudo().add_followers()
        report_template_id = self.env['ir.actions.report']._render_qweb_pdf('reporting_app.report_app_click_record', res_ids=self.ids)
        data_record = base64.b64encode(report_template_id[0])
        name = "My Attachment"
        data_id = self.env['ir.attachment'].create({
            'name': self.category_id,
            'type': 'binary',
            'datas': data_record,
            # 'datas_fname': name + '.pdf',
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        attachments.append(data_id.id)
        return self.message_post(body=message, attachment_ids=attachments,message_type='comment', subtype_xmlid='mail.mt_comment')



    def name_get(self):
        data = []
        for rec in self:
            data.append((rec.id, '%s' % (rec.title)))
        return data

    @api.onchange('project_ids')
    def do_action_project_ids(self):
        list = []
        for each in self.env['project.project'].search([('id','in',self.project_ids.ids)]):
            for task in each.task_ids:
                for timesheet in task.timesheet_ids:
                    dict = (0,0,{
                        'time_sheet_id':timesheet.id,
                        'project_id':each.id,
                        'task_id':task.id,
                        'date':timesheet.date,
                        'hours':timesheet.unit_amount,
                    })
                    list.append(dict)
        self.time_sheet_lines =False
        self.time_sheet_lines = list

class TimesheetReportLines(models.Model):
    _name = "timesheet.report.lines"

    report_app_id = fields.Many2one('report.app.click')
    time_sheet_id = fields.Many2one('account.analytic.line',string="Timesheet")
    project_id = fields.Many2one('project.project',string="Project")
    task_id = fields.Many2one('project.task',string="Task")
    date = fields.Date(string="Date")
    hours = fields.Float(string="Hours")