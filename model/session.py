# -*- encoding:utf-8 -*-
from openerp.osv import fields, osv

class Session(osv.Model):
	_name = "openacademy.session"

	def _get_taken_seats_percent(self, seats, attendee_list):
		try:
			return(100.0 * len(attendee_list)) / seats
		except ZeroDivisionError:
			return 0.0

	def _taken_seats_percent(self, cr, uid, ids, field, arg, context=None):
		result = {}

		for session in self.browse(cr, uid, ids, context=context):
			result[session.id] = self._get_taken_seats_percent(session.seats,session.attendee_ids)
		return result	

	_columns = {
			'name': fields.char(string="Name of session",size=256,help="Please describe correctly waht is the session identifier"),
			'taken_seats_percent' : fields.function(_taken_seats_percent, type='float', string = "Taken seats"),
			'start_date': fields.date(string="Start Date", help="Please indicate when the session will start"),
			'duration': fields.float(string="Duration",digits=(6,2),help="If represent duration in days"),
			'seats' : fields.integer(string="Seats",help="Total seats availables"),
			'course_id' : fields.many2one("openacademy.course",'Course',help="Select a course related to this session",ondelete="cascade"),
			'instructor_id' :fields.many2one("res.partner",string="Instructor",domain="[('instructor','=',True)]"),
			'attendee_ids' : fields.one2many("openacademy.attendee","session_id",string="Attendees",help="Who will be participated in this ession"),
	}

	def onchange_taken_seats(self, cr, uid, ids, seats, attendee_ids):
		attendee_records = self.resolve_2many_commands(cr, uid, 'attendee_ids', attendee_ids,['id'])
		res = {
			value : {
			 	'taken_seats_percent':
			 		self._get_taken_seats_percent(seats,attendee_records),
			},
		}
		return res