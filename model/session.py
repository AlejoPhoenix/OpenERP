# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv

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

    _columns = {
        'name': fields.char('Name of Session', 256,
                help="Please describe correctly what is the session identifier"),        
        'start_date': fields.date('Start Date',
                help="Please indicate when the session will start"),
        'duration': fields.float('Duration', digits=(6,2), help="It represent duration in Days"),
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
        print """Se dispara el constraint cuando se salve el registro"""
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
