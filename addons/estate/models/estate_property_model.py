from datetime import date, timedelta
from odoo import fields, models, api, exceptions, tools
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=date.today() + timedelta(days=90))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', default=0.0, readonly=True, copy=False,
                                 compute='_compute_selling_price', store=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        string='Garden Orientation')
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')],
        string='State', required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area', compute='_compute_total_area', store=True)
    best_price = fields.Float(string='Best Price', compute='_compute_best_price', store=True)
    property_status = fields.Selection([
        ('new', 'New'),
        ('cancelled', 'Cancelled'),
        ('sold', 'Sold')
    ], string='Status', default='new', readonly=True, copy=False)

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price') or [0.0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'North'

    def action_sold(self):
        for record in self:
            if record.property_status != 'new':
                raise UserError('Only properties in "New" status can be marked as sold.')
            record.property_status = 'sold'

    def action_cancel(self):
        for record in self:
            if record.property_status == 'sold':
                raise UserError('Sold properties cannot be cancelled.')
            record.property_status = 'cancelled'

    @api.depends('expected_price', 'offer_ids', 'offer_ids.status', 'offer_ids.price')
    def _compute_selling_price(self):
        for property in self:
            if property.offer_ids.filtered(lambda o: o.status == 'accepted'):
                accepted_offer = property.offer_ids.filtered(lambda o: o.status == 'accepted')[0]
                property.selling_price = accepted_offer.price
            else:
                property.selling_price = 0.0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if not tools.float_is_zero(property.selling_price,
                                       precision_digits=2) and property.selling_price < 0.9 * property.expected_price:
                raise exceptions.ValidationError("Selling price cannot be lower than 90% of the expected price.")
