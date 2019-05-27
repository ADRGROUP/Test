# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from datetime import datetime
import dateutil


_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_no = fields.Char('Employee ID', size=32)
    category = fields.Selection([('permanent', 'Permanent'), ('contract', 'Contract')], "Category")
    reporting_1 = fields.Many2one('hr.employee', 'Reporting 1')
    reporting_2 = fields.Many2one('hr.employee', 'Reporting 2')
    date_of_joining = fields.Date('Date of Joining')
    date_of_confirmation = fields.Date('Date of Confirmation')
    date_of_next_revision = fields.Date('Date of Next Revision')
    promotion = fields.Selection([('y', 'Y'), ('n', 'N')], "Promotion")
    resigned_on = fields.Date('Resigned On')
    reason_resigned = fields.Text('Reason for Resignation')
    date_of_relieving = fields.Date('Date of Relieving')
    date_of_retirement = fields.Date('Date of Retirement')
    f_f_amount = fields.Float('F&F amount')
    f_f_settlement = fields.Selection([('cash', 'Cash'), ('cheque', 'Cheque'), ('online_transfer', 'Online Transfer')], 'F&F Settlement Mode')
    pan_no = fields.Char('Pan No', size=32)
    aadhar_no = fields.Char('Aadhar No', size=32)
    pf_no = fields.Char('PF No', size=32)
    esi_no = fields.Char('ESI No', size=32)
    uan_no = fields.Char('UAN No', size=32)
    gratuity_policy_no = fields.Char('Gratuity Policy No', size=32)
    religion_id = fields.Many2one('hr.religion', 'Religion')
    blood_group_id = fields.Many2one('blood.group', 'Blood Group')
    street = fields.Char("Street", size=128)
    street2 = fields.Char("Street2", size=128)
    city = fields.Char("City", size=24)
    state_id = fields.Many2one('res.country.state', "State")
    address_country_id = fields.Many2one('res.country', "Country")
    zip = fields.Char("PIN", size=24)
    permanent_address_street = fields.Char("Street", size=128)
    permanent_address_street2 = fields.Char("Street2", size=128)
    permanent_address_city = fields.Char("City", size=24)
    permanent_address_state_id = fields.Many2one('res.country.state', "State")
    permanent_address_country_id = fields.Many2one('res.country', "Country")
    permanent_address_zip = fields.Char("PIN", size=24)
    home_phone = fields.Char('Phone', size=32)
    home_mobile_phone = fields.Char('Mobile', size=32)
    home_email = fields.Char('Personal Email', size=240)
    mother_language = fields.Many2one('hr.employee.language', 'Mother Tongue')
    emergency_contact_relationship_id = fields.Many2one('hr.relationship','Emergency Contact Person Relationship')
    relation_ids = fields.One2many('hr.relation', 'employee_id', 'Relation')
    education_details_ids = fields.One2many('education.details', 'employee_id', 'Education Details')
    work_experience_ids = fields.One2many('hr.past.work.experience', 'employee_id', 'Past Work Experience')
    language_ids = fields.One2many('mother.tongue', 'employee_id', 'Language Known')
    age = fields.Char(compute='_get_age', string='Age')
    experience = fields.Char(compute='_get_experience', string='Total Experience(years,months)')

    @api.multi
    @api.depends('birthday')
    def _get_age(self):
        today = datetime.today()

        if self.birthday:

            bday = self.birthday.strftime('%Y-%m-%d').split('-')
            year = int(bday[0])
            month = int(bday[1])
            date = int(bday[2])
            age = dateutil.relativedelta.relativedelta(today, datetime(year, month, date))
            self.age = str(age.years) + 'years' + str(age.months) + 'months'
        else:
            self.age = False

    @api.multi
    @api.depends('date_of_joining')
    def _get_experience(self):

        if self.date_of_joining:
            till_day = datetime.today()

            join_date = self.date_of_joining.strftime('%Y-%m-%d').split('-')
            year = int(join_date[0])
            month = int(join_date[1])
            date = int(join_date[2])
            experience = dateutil.relativedelta.relativedelta(till_day, datetime(year, month, date))
            experience_year = experience.years
            experience_month = experience.months

            self.experience = str(experience_year) + ' year(s)\t' + str(experience_month) + ' month(s)'
        else:
            self.experience = False


class Religion(models.Model):
    _name = 'hr.religion'

    name = fields.Char('Religion')

class BloodGroup(models.Model):
    _name = 'blood.group'

    name = fields.Char('Blood Group')

class Relation(models.Model):
    _name = 'hr.relation'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    name = fields.Char('Name')
    relationship_id = fields.Many2one('hr.relationship', 'Relation')
    date_of_birth = fields.Date('Date Of Birth')
    age = fields.Char(compute='_get_age', string='Age')
    occupation_id = fields.Many2one('hr.occupation', 'Occupation')

    @api.multi
    @api.depends('date_of_birth')
    def _get_age(self):
        today = datetime.today()

        if self.date_of_birth:

            bday = self.date_of_birth.strftime('%Y-%m-%d').split('-')
            year = int(bday[0])
            month = int(bday[1])
            date = int(bday[2])
            age = dateutil.relativedelta.relativedelta(today, datetime(year, month, date))
            self.age = str(age.years) + 'years' + str(age.months) + 'months'
        else:
            self.age = False

class Relationship(models.Model):
    _name = 'hr.relationship'

    name = fields.Char('Relationship')

class Occupation(models.Model):
    _name = 'hr.occupation'

    name = fields.Char('Occupation')

class EducationDetails(models.Model):
    _name = 'education.details'

    employee_id = fields.Many2one('hr.employee', 'Employee ID')
    degree = fields.Many2one('hr.recruitment.degree', 'Degree')
    stream = fields.Char('Stream', size=64)
    board_or_university = fields.Char('Board / University', size=64)
    name_of_institution = fields.Char('Institution', size=64)
    year_of_passing = fields.Integer('Year of Passing', size=4)
    percentage = fields.Float('% marks')
    pass_class = fields.Selection([('first_class', 'FIRST CLASS'), ('second_class', 'SECOND CLASS'), ('distinction', 'DISTINCTION')], 'Class')
    certificate_copy = fields.Binary('Certificate Copy')


class PastWorkExperience(models.Model):
    _name = 'hr.past.work.experience'

    employee_id = fields.Many2one('hr.employee', 'Employee ID')
    job_id = fields.Many2one('hr.job', 'Prev Designation')
    employer = fields.Char('Prev Company Name', size=128)
    period_from = fields.Date('Period From')
    period_to = fields.Date('Period To')
    experience = fields.Char(compute='_get_experience', string='Total Experience(years,months)')

    @api.multi
    @api.depends('period_from', 'period_to')
    def _get_experience(self):

        if self.period_from:
            if not self.period_to:
                till_day = datetime.today()
            else:
                till_day = self.period_to
            join_date = self.period_from.strftime('%Y-%m-%d').split('-')
            year = int(join_date[0])
            month = int(join_date[1])
            date = int(join_date[2])
            experience = dateutil.relativedelta.relativedelta(till_day, datetime(year, month, date))
            experience_year = experience.years
            experience_month = experience.months

            self.experience = str(experience_year) + ' year(s)\t' + str(experience_month) + ' month(s)'
        else:
            self.experience = False

class Mothertongue(models.Model):
    _name = 'mother.tongue'

    employee_id = fields.Many2one('hr.employee', 'Employee ID')
    language_id = fields.Many2one('hr.employee.language', 'Language')
    speak = fields.Boolean('Speak', default=False)
    read = fields.Boolean('Read', default=False)
    write = fields.Boolean('write', default=False)

class EmployeeLanguage(models.Model):
    _name = 'hr.employee.language'

    name = fields.Char('Language Name', size=64, required=True)