{
    'name': 'QR Payment on Invoices - SPAYD',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Invoicing',
    'summary': 'SPAYD QR codes on invoices — scan and pay instantly',
    'description': 'Add scannable QR payment codes to customer invoices and vendor bills. '
                   'Follows the SPAYD (Short Payment Descriptor) standard. '
                   'Customers scan the QR code with their banking app and all payment details — IBAN, amount, '
                   'currency, variable symbol — are filled in automatically. '
                   'Supports any currency. '
                   'QR code appears on the invoice PDF report and in the form view (Other Info tab). '
                   'Full IBAN validation with ISO 13616 checksum. '
                   'Zero configuration — just install and set a valid IBAN on your invoices.',
    'author': 'Michal Varyš',
    'website': 'https://michalvarys.eu',
    'support': 'info@michalvarys.eu',
    'license': 'LGPL-3',
    'price': 22.00,
    'currency': 'EUR',
    'depends': [
        'account',
    ],
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        'views/account_move_views.xml',
        'report/invoice_qr_report.xml',
    ],
    'images': ['static/description/cover.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
