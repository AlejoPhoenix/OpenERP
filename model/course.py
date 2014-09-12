# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields

class Course(osv.Model):

    _name = "openacademy.course"

    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for course in self.browse(cr, uid, ids, context=context):
            res[course.id] = 0
            for session in course.session_ids:
                res[course.id] += len(session.attendee_ids)
        return res

    def _get_courses_from_sessions(self, cr, uid, ids, context=None):
        sessions = self.browse(cr, uid, ids, context=context)
        return list(set(sess.course_id.id for sess in sessions))

    _columns = {
                'name': fields.char("Title", 256, required=True),
                'description': fields.text("Description"),
                'responsible_id' : fields.many2one('res.users',
                        ondelete='set null', string='Responsible', select=True),
                'session_ids': fields.one2many('openacademy.session', 'course_id',
                        'Sessions', help="Sessions related to this course: A session is guarever"),
                'attendee_count': fields.function(_get_attendee_count,
                    type='integer', string='Attendee Count',
                    store={
                        'openacademy.session' :
                        (_get_courses_from_sessions,['attendee_ids'],0)
                    }),
               }

    def copy(self, cr, uid, id, default, context=None):
        course = self.browse(cr, uid, id, context=context)
        new_name =  "Copy of %s" % course.name
        others_count = self.search(cr,  uid, [('name', '=like', new_name+'%')],
                                   count=True, context=context)
        if others_count > 0:
            new_name = "%s (%s)" % (new_name, others_count+1)
        default.update({'name': new_name})
        return super(Course, self).copy(cr, uid, id, default, context=context)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name <> description)',
         'Title and description should be different'),
        ('name_unique',
         'UNIQUE(name)',
         'The course title should be unique'),
    ]
