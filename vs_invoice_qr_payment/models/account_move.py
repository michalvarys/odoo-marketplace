import base64
import io
import logging
import re

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

try:
    import qrcode
except ImportError:
    qrcode = None
    _logger.warning("qrcode library not installed. Install it with: pip install qrcode[pil]")


class AccountMove(models.Model):
    _inherit = 'account.move'

    vs_qr_payment_data = fields.Char(
        string="QR Payment Data (SPAYD)",
        compute='_compute_vs_qr_payment',
    )
    vs_qr_payment_image = fields.Binary(
        string="QR Payment Code",
        compute='_compute_vs_qr_payment',
    )

    @api.depends(
        'move_type', 'state', 'amount_residual', 'currency_id',
        'partner_bank_id', 'partner_bank_id.acc_number',
        'name', 'ref',
    )
    def _compute_vs_qr_payment(self):
        for move in self:
            if (
                move.move_type not in ('out_invoice', 'in_invoice')
                or move.state != 'posted'
                or move.payment_state == 'paid'
                or not move.partner_bank_id
            ):
                move.vs_qr_payment_data = False
                move.vs_qr_payment_image = False
                continue

            spayd = move._vs_build_spayd()
            if not spayd:
                move.vs_qr_payment_data = False
                move.vs_qr_payment_image = False
                continue

            move.vs_qr_payment_data = spayd
            move.vs_qr_payment_image = move._vs_generate_qr_image(spayd)

    def _vs_build_spayd(self):
        """Build SPAYD (Short Payment Descriptor) string.

        Format: SPD*1.0*ACC:CZ6508000000192000145399*AM:1234.56*CC:CZK*X-VS:1234567890
        See: https://qr-platba.cz/pro-vyvojare/specifikace-formatu/
        """
        self.ensure_one()
        iban = self._vs_get_iban()
        if not iban:
            return False

        amount = self.amount_residual
        if amount <= 0:
            return False

        currency_code = self.currency_id.name

        parts = [
            'SPD*1.0',
            'ACC:%s' % iban,
            'AM:%.2f' % amount,
            'CC:%s' % currency_code,
        ]

        vs = self._vs_extract_variable_symbol()
        if vs:
            parts.append('X-VS:%s' % vs)

        return '*'.join(parts)

    def _vs_get_iban(self):
        """Extract clean IBAN from partner bank account."""
        self.ensure_one()
        if not self.partner_bank_id:
            return False
        acc = self.partner_bank_id.acc_number or ''
        iban = re.sub(r'\s+', '', acc).upper()
        if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$', iban):
            return False
        if not self._vs_validate_iban_checksum(iban):
            return False
        return iban

    @staticmethod
    def _vs_validate_iban_checksum(iban):
        rearranged = iban[4:] + iban[:4]
        numeric = ''
        for ch in rearranged:
            if ch.isdigit():
                numeric += ch
            else:
                numeric += str(ord(ch) - 55)
        return int(numeric) % 97 == 1

    def _vs_extract_variable_symbol(self):
        """Extract variable symbol from invoice number.

        Strips all non-digit characters and returns up to 10 digits.
        CZ/SK variable symbol is max 10 digits.
        """
        self.ensure_one()
        source = self.ref or self.name or ''
        digits = re.sub(r'\D', '', source)
        if not digits:
            return False
        return digits[-10:]

    def _vs_generate_qr_image(self, data):
        """Generate QR code image as base64-encoded PNG."""
        if not qrcode:
            return False
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=2,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue())
        except Exception:
            _logger.exception("Failed to generate QR payment code")
            return False
