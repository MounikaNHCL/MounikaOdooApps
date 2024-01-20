# Copyright 2019 ForgeFlow S.L.
# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from geopy.geocoders import Photon

from datetime import datetime


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _attendance_action_change(self):
        res = super()._attendance_action_change()
        latitude = self.env.context.get("latitude", False)
        longitude = self.env.context.get("longitude", False)
        if latitude and longitude:
            if self.attendance_state == "checked_in":
                geolocator = Photon(user_agent="geoapiExercises")
                # location = geolocator.geocode(Latitude + "," + Longitude)
                location = geolocator.reverse(str(latitude) + "," + str(longitude))
                # address = location.raw['address']
                # traverse the data
                # city = address.get('city', '')
                # state = address.get('state', '')
                # country = address.get('country', '')
                # zipcode = address.get('postcode')
                self.env['checkin.out.history'].create({
                    'checkin': datetime.now(),
                    'checkout_hisoty_id': self.last_attendance_id.id,
                    'check_in_city': location,
                    # 'check_in_state': state,
                    # 'check_in_zipcode': zipcode,
                    'employee_id': self.id,

                })
                res.checkin=datetime.now()
                res.check_in_city=location
                res.write(
                    {
                        "check_in_latitude": latitude,
                        "check_in_longitude": longitude,
                    }
                )
            else:
                geolocator = Photon(user_agent="geoapiExercises")
                # Latitude = str(latitude)
                # Longitude = str(longitude)
                # # location = geolocator.geocode(Latitude + "," + Longitude)
                location = geolocator.reverse(str(latitude) + "," + str(longitude))
                # address = location.raw['address']
                # traverse the data
                # city = address.get('city', '')
                # state = address.get('state', '')
                # country = address.get('country', '')
                # zipcode = address.get('postcode')
                self.env['checkin.out.history'].create({
                    'check_out': datetime.now(),
                    'checkout_hisoty_id': self.last_attendance_id.id,
                    'check_out_city': location,
                    # 'check_out_state': state,
                    # 'check_out_zipcode': zipcode,
                    'employee_id': self.id,

                })
                res.check_out = datetime.now()
                res.check_out_city = location
                res.write(
                    {
                        "check_out_latitude": latitude,
                        "check_out_longitude": longitude,
                    }
                )
        return res
