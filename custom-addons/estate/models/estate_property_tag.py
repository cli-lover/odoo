from odoo import models, fields
class Estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char(required=True)