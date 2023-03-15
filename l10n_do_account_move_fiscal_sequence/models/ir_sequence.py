from odoo import models, fields


class Sequence(models.Model):
    _inherit = "ir.sequence"

    l10n_do_journal_id = fields.Many2one("account.journal", "Fiscal Journal")
    l10n_do_ncf_expiration_date = fields.Date(
        string="Expiration date",
        required=True,
        default=fields.Date.end_of(fields.Date.today(), "year"),
    )
    l10n_do_internal_sign_xml = fields.Boolean(
        "Enable/Disable internal ECF xml signing"
    )
