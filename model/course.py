# -*- coding:utf-8 -*-

from openerp.osv import osv,fields

class Course(osv.Model):

    _name = "openacademy.course"
    _columns = {
                'name': fields.char("Title", 256, required=True),
                'description': fields.text("Description"),
                'responsable_id' : fields.many2one('res.users',
                        ondelete='set null', string='Responsible', select=True),
                'session_ids': fields.one2many('openacademy.session', 'course_id',
                        'Sessions', help="Sessions related to this course: A session is guarever")
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