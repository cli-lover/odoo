from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError

class Estate_property_offer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order = "price DESC"
    
    #FIELD
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted','Accepted'),
         ('refused','Refused')
        ],
          copy=False,
          string="Status"
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity(days)")
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_positive_offer_price','CHECK (price > 0)','The offer price must be strictly positive.')
        ]

    #ACTION

    @api.depends("create_date","validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date and record.validity:
              record.date_deadline = record.create_date.date() + timedelta(days = record.validity)
    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
              record.validity = (record.date_deadline - record.create_date.date()).days    
    
    def action_accept(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError("This offer has already been accepted.")
            
            if len(offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')) > 0:
                raise UserError("Only one offer can be accepted per property.")
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id
            })
            offer.property_id.state = 'sold'
            offer.status = 'accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
    

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        
        existing_offers = self.search([('property_id', '=', property_id.id)])
        if any(offer.price > vals.get('price', 0) for offer in existing_offers):
            raise UserError("You cannot create an offer with a lower price than an existing offer.")
        
        property_id.state = 'offer_received'

        return super().create(vals)
