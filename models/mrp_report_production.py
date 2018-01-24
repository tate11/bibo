from odoo import models, fields, api

class MrpReportProduction(models.Model):
    _name = 'mrp.report.production'

    @api.depends('production_lines')
    def _compute_suma(self):
        total = 0
        for mrp in self:
            for line in mrp.production_lines:
                total += line.total
            mrp.subtotal = total

    name = fields.Many2one('hr.employee', string="Empleado", readonly=True)
    production_lines = fields.One2many('mrp.report.production.line', 'production_id', string='Table lines')
    date_start = fields.Date('Fecha Inicio',readonly=True)
    date_finish = fields.Date('Fecha Fin', readonly=True)
    subtotal = fields.Float('Subtotal', compute="_compute_suma")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Confirmado'),
        ('pay', 'Pagado'),
    ], string='Estatus', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.multi
    def action_confirm(self):
        for order in self:
            order.state = 'done'

    @api.multi
    def action_pay(self):
        for order in self:
            order.state = 'pay'

    @api.multi
    def action_cancel(self):
        for order in self:
            order.state = 'draft'




class MrpReportProductionLine(models.Model):
    _name = 'mrp.report.production.line'
    production_id = fields.Many2one('mrp.report.production', string='reporte de Produccion Reference', required=True, ondelete='cascade',
                                   index=True, copy=False)
    mrp_production_id = fields.Many2one('mrp.production', string="Orden de Produccion", readonly=False, states={'pay': [('readonly', True)]})
    operation_id = fields.Many2one('mrp.workorder', string="Operacion", readonly=False, states={'pay': [('readonly', True)]})
    qty= fields.Integer('Piezas', readonly=False, states={'pay': [('readonly', True)]})
    precio_unit = fields.Float('Precio', readonly=True, states={'pay': [('readonly', True)]})
    total = fields.Float('Total', readonly=False, states={'pay': [('readonly', True)]})
