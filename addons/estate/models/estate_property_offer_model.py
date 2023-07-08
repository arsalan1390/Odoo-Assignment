from datetime import timedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    price = fields.Float(string='Price')
    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status',
        copy=False
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline',
                                store=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    create_date = fields.Date.from_string(record.create_date)
                    validity = record.date_deadline - create_date
                    record.validity = validity.days
                else:
                    record.validity = False

    def action_accept(self):
        self.ensure_one()
        self.status = 'accepted'
        property = self.property_id
        property.buyer_id = self.partner_id
        property.selling_price = self.price

    def action_refuse(self):
        self.status = 'refused'


