# -*- encoding:utf-8 -*-
from openerp.osv import osv, fields

class Attendee(osv.Model):
	_name = "openacademy.attendee"
	_columns = {
		'name': fields.char(string="Attendee",size=256),
	}