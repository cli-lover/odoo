from odoo import models, fields
class Estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ('unique_property_tag_name','UNIQUE (name)','The property tag name must be unique.')
        ]