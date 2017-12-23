# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from .constants import STATES_ACTIVE, STATES_HEALTH


class InfrastructureService(models.Model):

    _name = 'infrastructure.service'
    _description = 'Infrastructure Services'

    name = fields.Char(
        required=True,
    )
    description = fields.Char()
    state = fields.Selection(
        selection=STATES_ACTIVE,
        default='inactive',
    )
    stack_id = fields.Many2one(
        string='Stack',
        comodel_name='infrastructure.stack',
        ondelete='cascade',
    )
    environment_id = fields.Many2one(
        string='Environment',
        comodel_name='infrastructure.environment',
        ondelete='cascade',
    )
    date_create = fields.Datetime(
        string='Creation Date',
        default=fields.Datetime.now,
    )
    scale_current = fields.Integer()
    state_health = fields.Selection(
        selection=STATES_HEALTH,
    )
    instance_ids = fields.One2many(
        string='Instances',
        comodel_name='infrastructure.instance',
        inverse_name='service_id',
    )
    config_id = fields.Many2one(
        string='Current Configuration',
        comodel_name='infrastructure.service.config',
        compute='_compute_config_id',
    )
    previous_config_id = fields.Many2one(
        string='Previous Configuration',
        comodel_name='infrastructure.service.config',
    )

    @api.multi
    def write(self, values):

        if not values.get('config_id'):
            return super(InfrastructureService, self).write(values)

        for record in self:
            values['previous_config_id'] = record.config_id.id
            super(InfrastructureService, record).write(values)
