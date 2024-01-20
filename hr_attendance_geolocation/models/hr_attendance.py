# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from geopy.geocoders import Nominatim
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float(digits="Location", readonly=True)
    check_in_latitude_text = fields.Char(
        "Check-in Latitude", compute="_compute_check_in_latitude_text"
    )
    check_in_longitude = fields.Float(digits="Location", readonly=True)
    check_in_longitude_text = fields.Char(
        "Check-in Longitude", compute="_compute_check_in_longitude_text"
    )
    check_out_latitude = fields.Float(digits="Location", readonly=True)
    check_out_latitude_text = fields.Char(
        "Check-out Latitude", compute="_compute_check_out_latitude_text"
    )
    check_out_longitude = fields.Float(digits="Location", readonly=True)
    check_out_longitude_text = fields.Char(
        "Check-out Longitude", compute="_compute_check_out_longitude_text"
    )
    checkout_history = fields.One2many('checkin.out.history','checkout_hisoty_id')
    check_in_city = fields.Char(string="Checkin City")
    check_in_state = fields.Char(string="Checkin State")
    check_in_zipcode = fields.Char(string="Checkin ZIP")
    check_out_city = fields.Char(string="Checkout City")
    check_out_state = fields.Char(string="Checkout State")
    check_out_zipcode = fields.Char(string="Checkout ZIP")
    checkin = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")

    def _get_raw_value_from_geolocation(self, dd):
        d = int(dd)
        m = int((dd - d) * 60)
        s = (dd - d - m / 60) * 3600.00
        z = round(s, 2)
        return "%sº %s' %s'" % (abs(d), abs(m), abs(z))

    def _get_latitude_raw_value(self, dd):
        return "%s %s" % (
            "N" if int(dd) >= 0 else "S",
            self._get_raw_value_from_geolocation(dd),
        )

    def _get_longitude_raw_value(self, dd):
        return "%s %s" % (
            "E" if int(dd) >= 0 else "W",
            self._get_raw_value_from_geolocation(dd),
        )

    @api.depends("check_in_latitude")
    def _compute_check_in_latitude_text(self):
        for item in self:
            # geolocator = Nominatim(user_agent="geoapiExercises")
            # Latitude = str(item.check_in_latitude)
            # Longitude = str(item.check_in_longitude)
            # # location = geolocator.geocode(Latitude + "," + Longitude)
            # location = geolocator.reverse(Latitude + "," + Longitude)
            # address = location.raw['address']
            # # traverse the data
            # city = address.get('city', '')
            # state = address.get('state', '')
            # country = address.get('country', '')
            # zipcode = address.get('postcode')
            # # print('City : ', city)
            # # print('State : ', state)
            # # print('Country : ', country)
            # # print('Zip Code : ', zipcode)
            # item.check_in_city = city
            # item.check_in_state = state
            # item.check_in_zipcode = zipcode
            # self.env['checkin.out.history'].create({
            #     'checkin': datetime.now(),
            #     'checkout_hisoty_id':item.id,
            #     'check_in_city':city,
            #     'check_in_state':state,
            #     'check_in_zipcode':zipcode,
            #     'employee_id': item.employee_id.id,
            #
            # })
            # address = location.raw['address']

            item.check_in_latitude_text = (
                self._get_latitude_raw_value(item.check_in_latitude)
                if item.check_in_latitude
                else False
            )

    @api.depends("check_in_longitude")
    def _compute_check_in_longitude_text(self):
        for item in self:
            item.check_in_longitude_text = (
                self._get_longitude_raw_value(item.check_in_longitude)
                if item.check_in_longitude
                else False
            )

    @api.depends("check_out_latitude")
    def _compute_check_out_latitude_text(self):
        for item in self:
            # geolocator = Nominatim(user_agent="geoapiExercises")
            # Latitude = str(item.check_out_latitude)
            # Longitude = str(item.check_out_longitude)
            # location = geolocator.reverse(Latitude + "," + Longitude)
            # address = location.raw['address']
            # # traverse the data
            # city = address.get('city', '')
            # state = address.get('state', '')
            # zipcode = address.get('postcode')
            # # pytz.utc.localize(datetime.now())
            #
            # self.env['checkin.out.history'].create({
            #     'check_out':datetime.now(),
            #     'checkout_hisoty_id': item.id,
            #     'check_out_city': city,
            #     'check_out_state': state,
            #     'check_out_zipcode': zipcode,
            #     'employee_id': item.employee_id.id,
            #
            # })
            #
            # item.check_out_city = city
            # item.check_out_state = state
            # item.check_out_zipcode = zipcode
            item.check_out_latitude_text = (
                self._get_latitude_raw_value(item.check_out_latitude)
                if item.check_out_latitude
                else False
            )

    @api.depends("check_out_longitude")
    def _compute_check_out_longitude_text(self):
        for item in self:
            item.check_out_longitude_text = (
                self._get_longitude_raw_value(item.check_out_longitude)
                if item.check_out_longitude
                else False
            )
    def open_checkin_out_history(self):
            return {
                'name': 'Check In/Out History',
                'domain': [('id', 'in', self.checkout_history.ids)],
                'res_model': 'checkin.out.history',
                'view_mode': 'tree',
                'type': 'ir.actions.act_window',
            }


class CheckinOutHistory(models.Model):
    _name = "checkin.out.history"

    checkout_hisoty_id = fields.Many2one('hr.attendance')

    check_in_city = fields.Char(string="Checkin City")
    check_in_state = fields.Char(string="Checkin State")
    check_in_zipcode = fields.Char(string="Checkin ZIP")
    check_out_city = fields.Char(string="Checkout City")
    check_out_state = fields.Char(string="Checkout State")
    check_out_zipcode = fields.Char(string="Checkout ZIP")
    employee_id = fields.Many2one('hr.employee', string="Employee",ndelete='cascade', index=True)
    checkin = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
