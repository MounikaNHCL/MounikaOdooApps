from odoo import fields, models, api,_
from odoo.exceptions import UserError, AccessError

class ClassFacilities(models.Model):
    _name = "class.facilities"
    _description = "Class Facilities"

    name = fields.Char(string="Name")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)


class ClassRoom(models.Model):
    _name = "class.room"
    _description = "Class Room"
    _order = "id desc"

    name = fields.Char('Name')
    course_id = fields.Many2one('student.course', string="Course")
    no_of_persons = fields.Integer(string="No of Persons")
    class_rooms = fields.One2many('class.room.facilities','class_room_id')
    assert_lines = fields.One2many('class.room.asserts','class_assert_id')
    class_code = fields.Char(string="Code",copy=False, readonly=True, default=lambda x: _('New'))
    batch_id = fields.Many2one('student.batch', string="Batch")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)



    @api.model
    def create(self, vals):
        if not vals.get('class_code') or vals['class_code'] == _('New'):
            vals['class_code'] = self.env['ir.sequence'].next_by_code('class.room') or _('New')
        return super(ClassRoom, self).create(vals)




class ClassRoomfacilities(models.Model):
    _name = "class.room.facilities"
    _description = "class room lines"
    _order = "id desc"

    facility_id = fields.Many2one('class.facilities',string='Name')
    class_room_id = fields.Many2one('class.room')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    quantity = fields.Integer(string="Quantity")



class ClassRoomAsserts(models.Model):
    _name = "class.room.asserts"
    class_assert_id = fields.Many2one('class.room')
    product_id = fields.Many2one('product.product',string="Product")
    quantity = fields.Integer(string="Quantity")

