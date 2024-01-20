from odoo import models, fields, _, api


class ReportConfig(models.Model):
    _name = "report.config"

    name = fields.Char(string="Category")
