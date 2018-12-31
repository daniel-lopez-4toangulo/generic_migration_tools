
import datetime
import io
import itertools
import logging
import psycopg2
import operator
import os
import re

import base64
from odoo.exceptions import UserError
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.misc import ustr
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat

FIELDS_RECURSION_LIMIT = 2
ERROR_PREVIEW_BYTES = 200
_logger = logging.getLogger(__name__)

import xlrd
from xlrd import xlsx

FILE_TYPE_DICT = {
    'text/csv': ('csv', True, None),
    'application/vnd.ms-excel': ('xls', xlrd, 'xlrd'),
    'application/octet-stream': ('xlsx', xlsx, 'xlrd >= 1.0.0'),
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('xlsx', xlsx, 'xlrd >= 1.0.0')
}
EXTENSIONS = {
    '.' + ext: handler
    for mime, (ext, handler, req) in FILE_TYPE_DICT.items()
}

class ImportGenericData(models.Model):
    _name = 'import.generic.data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Import Data Document"

    file = fields.Binary('File', help="File")
    file_name = fields.Char('File Name')
    file_type = fields.Char('File Type', default='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    date = fields.Date('Date', default=fields.Date.context_today)
    ir_model_id = fields.Many2one('ir.model', string='Model')
    generic_data_line_ids = fields.One2many('import.generic.data.line', 'generic_data_id', string='Data Lines')
    obj_identification_field = fields.Many2one('ir.model.fields', string='Identification Field')
    obj_identification_column = fields.Integer('Object Id on Column',default=1)
    imported = fields.Boolean()

    @api.multi
    def _read_file(self):
        """ Dispatch to specific method to read file content, according to its mimetype or file type
            :param options : dict of reading options (quoting, separator, ...)
        """
        self.ensure_one()
        # guess mimetype from file content
        mimetype = guess_mimetype(self.file)

        excep_flag = False
        excep_obj = False
        # mimetype = self.file_type
        (file_extension, handler, req) = FILE_TYPE_DICT.get(mimetype, (None, None, None))
        if handler:
            try:
                excep_obj = False
                excep_flag = False
                return getattr(self, '_read_' + file_extension)()
            except Exception as e:
                _logger.warn("Failed to read file '%s' (transient id %d) using guessed mimetype %s",
                             self.file_name or '<unknown>', self.id, mimetype)
                excep_obj = e
                excep_flag = True

        # try reading with user-provided mimetype
        (file_extension, handler, req) = FILE_TYPE_DICT.get(self.file_type, (None, None, None))
        if handler:
            try:
                excep_obj = False
                excep_flag = False
                return getattr(self, '_read_' + file_extension)()
            except Exception as e:
                _logger.warn("Failed to read file '%s' (transient id %d) using user-provided mimetype %s",
                             self.file_name or '<unknown>', self.id, self.file_type)
                excep_obj = e
                excep_flag = True

        # fallback on file extensions as mime types can be unreliable (e.g.
        # software setting incorrect mime types, or non-installed software
        # leading to browser not sending mime types)
        if self.file_name:
            p, ext = os.path.splitext(self.file_name)
            if ext in EXTENSIONS:
                try:
                    excep_obj = False
                    excep_flag = False
                    return getattr(self, '_read_' + ext[1:])()
                except Exception as e:
                    _logger.warn("Failed to read file '%s' (transient id %s) using file extension", self.file_name,
                                 self.id)
                    excep_obj = e
                    excep_flag = True

        if excep_flag:
            # raise UserError('Error: %s' % str(excep_obj.name))
            raise UserError('Error: %s' % str(excep_obj))

    @api.multi
    def _read_xls(self):
        """ Read file content, using xlrd lib """
        book = xlrd.open_workbook(file_contents=base64.b64decode(self.file))
        return self._read_xls_book(book)

    def update_create_obj(self, row, type='csv'):
        dict_vals = dict()
        for line in self.generic_data_line_ids:
            row_col_value = row[line.column_number]
            if type != 'csv':
                row_col_value = row[line.column_number].value
            row_col_value = row_col_value.strip()
            if line.ir_model_fields_id.relation:
                rel_obj = self.env[line.ir_model_fields_id.relation].search([(line.technical_search_value_field,'=',row_col_value)])
                if rel_obj:
                    row_col_value = rel_obj[0].id
            if row_col_value == 'False' or row_col_value == 'FALSE' or row_col_value == 'Falso' or row_col_value == 'FALSO' \
                or row_col_value == 'No' or row_col_value == 'no' or row_col_value == 'NO' or row_col_value == '0':
                row_col_value = False
            elif row_col_value == 'True' or row_col_value == 'TRUE' or row_col_value == 'Verdadero' or row_col_value == 'VERDADERO' \
                or row_col_value == 'Si' or row_col_value == 'si' or row_col_value == 'SI' or row_col_value == '1':
                row_col_value = True
            dict_vals.update({line.ir_model_fields_id.name: row_col_value})
        try:
            row_id_value = row[self.obj_identification_column]
            if type != 'csv':
                row_id_value = row[self.obj_identification_column].value
            row_id_value = row_id_value.strip()
            if row_id_value:
                search_objs = self.env[self.ir_model_id.model].search([(self.obj_identification_field.name,'=',row_id_value)])
                if search_objs:
                    search_objs.write(dict_vals)
            else:
                self.env[self.ir_model_id.model].create(dict_vals)
        except Exception as e:
            error = e
            raise UserError(_('An error has been detected'))


    def _read_xls_book(self, book):
        sheet = book.sheet_by_index(0)
        row_counter = 0
        for row in pycompat.imap(sheet.row, range(sheet.nrows)):
            if row_counter == 0:
                pass
            else:
                self.update_create_obj(row,'xls')
            row_counter += 1



    # use the same method for xlsx and xls files
    _read_xlsx = _read_xls

    @api.multi
    def _read_csv(self):
        """ Returns a CSV-parsed iterator of all empty lines in the file
            :throws csv.Error: if an error is detected during CSV parsing
            :throws UnicodeDecodeError: if ``options.encoding`` is incorrect
        """
        csv_data = base64.b64decode(self.file)

        # TODO: guess encoding with chardet? Or https://github.com/aadsm/jschardet
        encoding = 'utf-8'
        if encoding != 'utf-8':
            # csv module expect utf-8, see http://docs.python.org/2/library/csv.html
            csv_data = csv_data.decode(encoding).encode('utf-8')

        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data),
            quotechar=str('"'),
            delimiter=str(','))

        row_counter = 0
        for row in csv_iterator:
            if row_counter == 0:
                pass
            else:
                self.update_create_obj(row)
            row_counter += 1

    @api.one
    def import_data(self):
        self._read_file()
        self.date = fields.Date.today()


class ImportGenericDataLine(models.Model):
    _name = 'import.generic.data.line'
    _description = "Import Data Detail"

    ir_model_id = fields.Many2one('ir.model', string='Model')
    ir_model_fields_id = fields.Many2one('ir.model.fields', string='Field')
    generic_data_id = fields.Many2one('import.generic.data', string='Generic Data Import')
    column_number = fields.Integer('Colunm Number')
    technical_search_value_field = fields.Char('Technical Search Value Field')