{
    'name': 'QR Payment on Invoices - SPAYD',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Invoicing',
    'summary': 'SPAYD QR codes on invoices for Czech & Slovak banks — scan and pay instantly',
    'description': 'Add scannable QR payment codes to customer invoices and vendor bills. '
                   'Follows the SPAYD (Short Payment Descriptor) standard used by all Czech and Slovak banks. '
                   'Customers scan the QR code with their banking app and all payment details — IBAN, amount, '
                   'currency, variable symbol — are filled in automatically. '
                   'Supports CZ and SK IBANs, CZK and EUR currencies. '
                   'QR code appears on the invoice PDF report and in the form view (Other Info tab). '
                   'Full IBAN validation with ISO 13616 checksum. '
                   'Zero configuration — just install and set a valid IBAN on your invoices.',
    'author': 'VaryShop',
    'website': 'https://www.varyshop.eu',
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
