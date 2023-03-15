from odoo import models


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"

    def _get_document_sequence_vals(self, journal):
        """ Values to create the sequences """

        values = {
            "name": "%s - %s" % (journal.name, self.name),
            "padding": 10 if str(self.l10n_do_ncf_type).startswith("e-") else 8,
            "implementation": "no_gap",
            "prefix": self.doc_code_prefix,
            "l10n_latam_document_type_id": self.id,
            "l10n_do_journal_id": journal.id,
            # get l10n_do_ncf_expiration_date from l10n_do.account.journal.document_type
            "l10n_do_ncf_expiration_date": journal.l10n_do_document_type_ids.filtered(
                lambda doc_type: doc_type.l10n_latam_document_type_id == self
            ).l10n_do_ncf_expiration_date,
        }

        # Only works if called from post_init. In this use case module is installed
        # after fiscal invoices are issued.
        move_type = "in_invoice" if journal.type == "purchase" else "out_invoice"
        last_sequence = (
            self.env["account.move"]
            .with_context(default_move_type=move_type, is_l10n_do_seq=True)
            .new({"l10n_latam_document_type_id": self.id, "journal_id": journal.id})
            ._get_last_sequence()
        )
        if last_sequence:
            # new sequence gets number next from account.move ;)
            values["number_next_actual"] = int(last_sequence[3:]) + 1

        return values
