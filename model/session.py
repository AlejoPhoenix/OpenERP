# -*- encoding:utf-8 -*-
from openerp.osv import fields, osv

class Session(osv.Model):
	_name = "openacademy.session"
	_columns = {
			'name': fields.char(string="Name of session",size=256,help="Please describe correctly waht is the session identifier"),
			'start_date': fields.date(string="Start Date", help="Please indicate when the session will start"),
			'duration': fields.float(string="Duration",digits=(6,2),help="If represent duration in days"),
			'seats' : fields.integer(string="Seats",help="Total seats availables"),
			'course_id' : fields.many2one("openacademy.course",'Course',help="Select a course related to this session",ondelete="cascade"),
			'instructor_id' :fields.many2one("res.partner",string="Instructor"),
			'attendee_ids' : fields.one2many("openacademy.attendee","session_id",string="Attendees",help="Who will be participated in this ession")
	}