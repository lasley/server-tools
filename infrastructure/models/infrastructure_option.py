# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class InfrastructureOption(models.Model):

    _name = 'infrastructure.option'
    _description = 'Infrastructure Options'

    name = fields.Char(
        required=True,
    )
    value = fields.Char(
        required=True,
    )

    _sql_constraints = [
        ('name_value_unique', 'UNIQUE(name, value)',
         'This name/value combination already exists.'),
    ]

    @api.multi
    def name_get(self):
        return [
            (n.id, '%s: "%s"' % (n.name, n.value)) for n in self
        ]

    @api.multi
    def get_or_create(self, name, value, **others):
        """Return an existing or new option matching ``name`` and ``value``.
        """
        domain = [
            ('name', '=', name),
            ('value', '=', value),
        ]
        domain += [(k, '=', v) for k, v in others.items()]
        option = self.search(domain)
        if option:
            return option[:1]
        values = {
            'name': name,
            'value': value,
        }
        values.update(others)
        return self.create(values)
