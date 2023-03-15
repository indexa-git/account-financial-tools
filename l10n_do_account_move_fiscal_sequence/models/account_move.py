from odoo import models, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_do_internal_signing(self):
        """
        Whether or not invoice ECF is going to be signed internally
        """
        self.ensure_one()
        return self.journal_id.l10n_do_sequence_ids.filtered(
            lambda seq: seq.l10n_latam_document_type_id
            == self.l10n_latam_document_type_id
        ).l10n_do_internal_sign_xml

    @api.depends(
        "journal_id.l10n_latam_use_documents",
        "l10n_latam_manual_document_number",
        "l10n_latam_document_type_id",
        "company_id",
    )
    def _compute_l10n_do_enable_first_sequence(self):
        # by default disable first fiscal sequence input from invoices
        self.l10n_do_enable_first_sequence = False

    def _post(self, soft=True):
        posted = super(AccountMove, self)._post(soft=soft)

        if posted:
            l10n_do_invoices = self.filtered(
                lambda inv: inv.country_code == "DO" and inv.l10n_latam_use_documents
            )
            for invoice in l10n_do_invoices:
                if invoice.state == "posted":

                    # Only set a new fiscal number if invoice first time post.
                    # I can't use posted_before in this IF because
                    # posted_before is set to True in _post() at the same
                    # time as state is set to "posted".
                    if not invoice.l10n_do_fiscal_number and invoice.journal_id:
                        sequence = invoice.journal_id.l10n_do_sequence_ids.filtered(
                            lambda seq: seq.l10n_latam_document_type_id
                            == invoice.l10n_latam_document_type_id
                        )
                        if not sequence:
                            raise ValidationError(
                                _("No fiscal sequence was found for document type %s")
                                % invoice.l10n_latam_document_type_id.name,
                            )
                        invoice.l10n_do_fiscal_number = sequence.next_by_id()

                    else:
                        invoice.l10n_do_fiscal_number = invoice.l10n_do_fiscal_number

                else:
                    invoice.l10n_do_fiscal_number = invoice.l10n_do_fiscal_number

        return posted
