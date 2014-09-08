 # -*- encoding:utf-8 -*-
from openerp.osv import fields, osv

class Partner(osv.Model):
	_inherit = 'res.partner'
	_columns = {
		'instructor' : fields.boolean("Instructor"),
	}
	_defaults = {
		'instructor' : False,
	}
