# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import datetime, timedelta

class Session(osv.Model):

    _name = "openacademy.session"

    def _get_taken_seats_percent(self, seats, attendee_list):
        try:
            return (100.0 * len(attendee_list)) / seats
        except ZeroDivisionError:
            return 0.0

    def _taken_seats_percent(self, cr, uid, ids, field, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            result[session.id] = self._get_taken_seats_percent(session.seats, session.attendee_ids)
        return result

    def _determin_end_date(self, cr, uid, ids, field, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.start_date and session.duration:
                start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
                duration = timedelta( days=(session.duration - 1) )
                end_date = start_date + duration
                result[session.id] = end_date.strftime("%Y-%m-%d")
            else:
                result[session.id] = session.start_date
        return result

    def _set_end_date(self, cr, uid, id, field, value, arg, context=None):
        session = self.browse(cr, uid, id, context=context)
        if session.start_date and value:
            start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(value[:10], "%Y-%m-%d")
            duration = end_date - start_date
            self.write(cr, uid, id, {'duration' : (duration.days + 1)},
                               context=context)

    def _determin_hours_from_duration(self, cr, uid, ids, field, arg, context=None):
        result = {}
        sessions = self.browse(cr, uid, ids, context=context)
        for session in sessions:
            result[session.id] = (session.duration * 24 if session.duration \
                                                        else 0)
        return result

    def _set_hours(self, cr, uid, id, field, value, arg, context=None):
        if value:
            self.write(cr, uid, id,
                       {'duration' : (value / 24)},
                       context=context)

    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res

    _columns = {
        'name': fields.char('Name of Session', 256,
                help="Please describe correctly what is the session identifier"),        
        'start_date': fields.date('Start Date',
                help="Please indicate when the session will start"),
        'end_date': fields.function(_determin_end_date, fnct_inv=_set_end_date,
                                                type='date', string='End Date'),
        'duration': fields.float('Duration', digits=(6,2), help="It represent duration in Days"),
        'attendee_count': fields.function(_get_attendee_count,
                                type='integer', string='Attendee Count', store=True),
        'hours' : fields.function(_determin_hours_from_duration,
            fnct_inv=_set_hours, type='float', string="Hours"),
        'seats': fields.integer('Seats', help="Total seats availables"),
        'instructor_id' : fields.many2one('res.partner', string="Instructor",
                                          domain=['|',('instructor','=',True),
                                          ('category_id.name','ilike','Teacher')]),
        'course_id': fields.many2one('openacademy.course', 'Course',
            help="Select a course related to this new session", ondelete="cascade"),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', 'Attendees',
            help="Who will be participating in this session"),
        'taken_seats_percent': fields.function(_taken_seats_percent,
                                                type='float', string='Taken Seats'),
        'active' : fields.boolean("Active"),
    }

    _defaults = {
        'start_date' : fields.date.today,
        'active': True,
    }

    def onchange_taken_seats(self, cr, uid, ids, seats, attendee_ids):
        attendee_records = self.resolve_2many_commands(cr, uid, 'attendee_ids', attendee_ids, ['id'])
        res = {
            'value' : {
                'taken_seats_percent' :
                    self._get_taken_seats_percent(seats, attendee_records),
            },
        }
        if seats < 0:
            res['warning'] = {
                'title'   : "Warning: bad value",
                'message' : "You cannot have negative number of seats",
                
            }
        elif seats < len(attendee_ids):
            res['warning'] = {
                'title'   : "Warning: problems",
                'message' : "You need more seats for this session",
                
            }
        return res

    def _check_instructor_not_in_attendees(self, cr, uid, ids):
        for session in self.browse(cr, uid, ids):
            partners = [att.partner_id for att in session.attendee_ids]
            if session.instructor_id and session.instructor_id in partners:
                return False
        return True

    _constraints = [
        (_check_instructor_not_in_attendees,
         "The instructor can not be also an attendee!",
         ['instructor_id','attendee_ids']),
    ]