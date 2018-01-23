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

    name = fields.Many2one('hr.employee', string="Empleado")
    production_lines = fields.One2many('mrp.report.production.line', 'production_id', string='Table lines')
    date_start = fields.Date('Fecha Inicio')
    date_finish = fields.Date('Fecha Fin')
    subtotal = fields.Float('Subtotal', compute="_compute_suma")




class MrpReportProductionLine(models.Model):
    _name = 'mrp.report.production.line'
    production_id = fields.Many2one('mrp.report.production', string='reporte de Produccion Reference', required=True, ondelete='cascade',
                                   index=True, copy=False)
    mrp_production_id = fields.Many2one('mrp.production', string="Orden de Produccion")
    operation_id = fields.Many2one('mrp.workorder', string="Operacion")
    qty= fields.Integer('Piezas')
    precio_unit = fields.Float('Precio')
    total = fields.Float('Total')
