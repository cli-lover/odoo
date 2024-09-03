from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import Command

class Estate_property(models.Model):
    _inherit = 'estate.property'

    # ACTION

    def action_sold(self):
        for property in self:
            # Ensure that the property is not canceled before selling
            if property.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            
            # Change the state of the property to 'sold'
            property.state = 'sold'
            
            # Check if the property has a buyer linked
            if not property.buyer_id:
                raise UserError("Cannot create invoice: No buyer is linked to the property.")

             
            # Calculate values for the invoice lines
            commission_fee = property.selling_price * 0.06  # 6% of the selling price
            admin_fee = 100.00  # Flat administrative fee

            # Create an empty invoice using account.move model
            invoice_values = {
                'partner_id': property.buyer_id.id,  # Link the invoice to the property buyer (res.partner)
                'move_type': 'out_invoice',          # This is a Customer Invoice
                'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,  # Journal ID for sale invoices
                'invoice_line_ids': [
                    Command.create({
                        'name': property.name,                # The name of the property
                        'quantity': 1,                        # Quantity of 1 property
                        'price_unit': property.selling_price, # Selling Price
                    }),
                    # Command to create the first invoice line (commission fee)
                    Command.create({
                        'name': 'Commission Fee (6% of Selling Price)',  # Line description
                        'quantity': 1,                                   # Quantity of 1 property
                        'price_unit': commission_fee,                    # Calculated commission fee
                    }),
                    # Command to create the second invoice line (administrative fee)
                    Command.create({
                        'name': 'Administrative Fee',                     # Line description
                        'quantity': 1,                                    # Fixed quantity
                        'price_unit': admin_fee,                          # Fixed price for the administrative fee
                    })
                ],
            }

            # Create the invoice with the specified values and lines
            self.env['account.move'].create(invoice_values)

        return True

    