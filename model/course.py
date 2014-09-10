# -*- coding:utf-8 -*-

from openerp.osv import osv,fields

class Course(osv.Model):
	_name = "openacademy.course"
	_columns = {
		'name' : fields.char(string="Title",size=256,required=True),
		'description' : fields.text(string="Description"),
		'responsable_id' : fields.many2one("res.users",ondelete="set null",string="Responsable",select="True"),
		'session_ids': fields.one2many ("openacademy.session","course_id", string="Sessions", help="Sessions related to this course, a session is whatever."),
	}
	_sql_constraints = [
        ('name_description_check',
         'CHECK(name <> description)',
         'Title and description should be different'),
        ('name_unique',
         'UNIQUE(name)',
         'The course title should be unique'),
    ]