from odoo import models, fields

class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = "sequence, name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence", default=10)
    _sql_constraints = [
        ('unique_property_type_name','UNIQUE (name)','The property type name must be unique.')
        ]