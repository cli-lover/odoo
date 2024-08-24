from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Real estate properties"
    _order = "id DESC"

    # FIELDS
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
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" )
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids =fields.One2many('estate.property.offer','property_id',string="Offers")
    
    best_price = fields.Float(string="Best Price", compute="_best_price", store=True)
    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total")


    _sql_constraints = [
        ('check_positive_expected_price','CHECK (expected_price > 0)','The expected price must be strictly positive.'),
        ('check_positive_selling_price','CHECK (selling_price >= 0)','The selling price must be strictly positive.')
        ]


    # ACTIONS

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")             
    def _best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped('price')
            record.best_price = max(offer_prices) if offer_prices else 0.0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    

    def action_sold(self):
        for property in self:
            if property.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            else:
                property.state = 'sold'
        return True
    
    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            else:
                property.state = 'canceled'
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_validity(self):
        for property in self:
            if not property.selling_price:
                continue
            min_price = property.expected_price * 0.9
            if float_compare(property.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    f"The selling price cannot be lower than 90% of the expected price."
                )
        return True
        
            
     
    @api.ondelete(at_uninstall=False)
    def _check_state_on_delete(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties in the 'New' or 'Canceled' state.")
    
class ResUsers(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        string="Properties",
        domain="[('state','=','new')]"
    )