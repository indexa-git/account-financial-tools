{
    "name": "Account Move Fiscal Sequence",
    "summary": "Generate invoices fiscal number from sequence... like Odoo 13 .|.",
    "author": "Indexa",
    "website": "https://www.indexa.do",
    "category": "Uncategorized",
    "version": "14.0.1.1.0",
    "depends": ["account_move_name_sequence", "l10n_do_ecf_invoicing"],
    "data": [
        "data/account_journal_data.xml",
        "views/account_journal_views.xml",
        "views/ir_sequence_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
