import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_do_sequence_ids = fields.One2many(
        "ir.sequence",
        "l10n_do_journal_id",
        string="Fiscal Sequences",
    )

    def _l10n_do_create_document_sequences(self):
        self.ensure_one()
        if self.country_code != "DO":
            return True
        if not self.l10n_latam_use_documents:
            return False

        sequences = self.l10n_do_sequence_ids
        sequences.unlink()

        # Create Sequences
        ncf_types = self._get_journal_ncf_types()
        internal_types = ["invoice", "in_invoice", "debit_note", "credit_note"]
        domain = [
            ("country_id.code", "=", "DO"),
            ("internal_type", "in", internal_types),
            ("active", "=", True),
            "|",
            ("l10n_do_ncf_type", "=", False),
            ("l10n_do_ncf_type", "in", ncf_types),
        ]
        documents = self.env["l10n_latam.document.type"].search(domain)
        for document in documents:
            sequences |= (
                self.env["ir.sequence"]
                .sudo()
                .create(document._get_document_sequence_vals(self))
            )
        return sequences

    @api.model
    def create_journal_l10n_do_sequences(self):  # to be called from data file
        """ "
        For each fiscal journal, fetch document types last issued sequence and creates
        journal fiscal sequences.
        """
        fiscal_journals = self.with_context(active_test=False).search(
            [
                ("type", "in", ("sale", "purchase")),
                # ("l10n_latam_use_documents", "=", True),
                ("l10n_do_sequence_ids", "=", False),
            ],
            limit=2,
        )
        for journal in fiscal_journals:
            _logger.warning("Creating fiscal sequences for journal %s" % journal.name)
            journal._l10n_do_create_document_sequences()

        return

    @api.model
    def create(self, values):
        """ Create Document sequences after create the journal """
        res = super().create(values)
        res._l10n_do_create_document_sequences()
        return res

    def write(self, values):
        """ Update Document sequences after update journal """
        to_check = {"type", "l10n_latam_use_documents"}
        res = super().write(values)
        if to_check.intersection(set(values.keys())):
            for rec in self:
                rec._l10n_do_create_document_sequences()
        return res
