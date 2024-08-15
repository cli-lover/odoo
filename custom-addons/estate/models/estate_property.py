from odoo import models, fields
from datetime import timedelta

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Real estate properties"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
            [
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Canceled')
            ],
            default='new',
            required=True,
            copy=False
        ) 

    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
            string="Availability Date", 
            copy=False, 
            default=lambda self: fields.Datetime.today() + timedelta(days=90)
        )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
            [('north', 'North'),
             ('south', 'South'),
             ('east', 'East'),
             ('west', 'West')],
            string="Garden Orientation"
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
