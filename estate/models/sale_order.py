from odoo import models, fields, api, exceptions
from datetime import timedelta

"""class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('waiting_approval', 'En attente d\'approbation'),
        ('approved', 'Approuvé'),
        ('sent', 'Devis envoyé'),
        ('sale', 'Vente'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    def action_waiting_approval(self):
        # Mettez la commande de vente en attente d'approbation
        self.state = 'waiting_approval'

    def action_approve(self):
        # Approuvez la commande de vente
        self.state = 'approved'"""


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('waiting_approval', 'En attente d\'approbation'),
        ('approved', 'Approuvé'),
        ('sent', 'Devis envoyé'),
        ('sale', 'Vente'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    

    def _check_required_manager_level(self):
        # Vérifiez le montant de la commande et définissez le niveau de gestionnaire requis
        if self.amount_total < 500:
            self.required_manager_level = 0
        elif self.amount_total > 500 and self.amount_total < 2000:
            self.required_manager_level = 1
        elif self.amount_total > 2000:
            self.required_manager_level = 2

    def action_waiting_approval(self):
        # Mettez la commande de vente en attente d'approbation
        self.state = 'waiting_approval'

    def action_approve(self):
        # Approuvez la commande de vente
        self.state = 'approved'

    def action_confirm(self):
        for line in self.order_line:
            if line.employee:
                start_datetime = fields.Datetime.to_string(line.training_date)
                end_datetime = fields.Datetime.from_string(start_datetime) + timedelta(hours=10)
                event = self.env['calendar.event'].create({
                    'name': 'Formation - %s' % line.name,
                    'start': start_datetime,
                    'stop': end_datetime,
                    'partner_ids': [(4, line.employee.id)],
                })

        if self.amount_total > 500:
            self.state = 'waiting_approval'

        if self.env.user.manager_level > 1:
            self.state = 'sent'

    # L'utilisateur actuel est un gestionnaire de niveau 2 ou plus
    # Faites quelque chose ici


