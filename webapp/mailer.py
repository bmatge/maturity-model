"""Envoi de mails — stdlib uniquement (smtplib).

Câblé sur le catcher Mailpit du lab (`mailer:1025`) via les variables
d'environnement injectées par spawn (`--mail`), ou sur le relais réel
(`--mail real`). Sans MAIL_HOST, l'envoi est désactivé et l'UI retombe
sur les mailto.
"""

import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

MAIL_HOST = os.environ.get("MAIL_HOST", "")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "1025") or "1025")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME", "Maturité numérique")
MAIL_FROM_ADDR = os.environ.get("MAIL_FROM_ADDR", "maturite@miweb.run")


class MailerError(RuntimeError):
    pass


def enabled():
    return bool(MAIL_HOST)


def _html(titre, corps_html, lien=None, lien_label=None):
    """Gabarit sobre aux couleurs de l'État (table-based, compatible clients mail)."""
    bouton = ""
    if lien:
        bouton = f"""
        <tr><td style="padding:24px 0 8px;">
          <a href="{lien}" style="background:#000091;color:#ffffff;text-decoration:none;
             padding:12px 24px;font-weight:700;display:inline-block;">{lien_label or lien}</a>
        </td></tr>
        <tr><td style="font-size:12px;color:#666666;padding-bottom:8px;">
          Ou copiez ce lien : <a href="{lien}" style="color:#000091;">{lien}</a>
        </td></tr>"""
    return f"""<!DOCTYPE html>
<html lang="fr"><body style="margin:0;background:#f6f6f6;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f6f6;padding:24px 0;">
<tr><td align="center">
<table role="presentation" width="560" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border:1px solid #dddddd;font-family:Marianne,system-ui,Arial,sans-serif;color:#161616;">
  <tr><td style="border-top:4px solid #000091;padding:24px 32px 0;">
    <p style="margin:0;font-size:12px;color:#666666;text-transform:uppercase;letter-spacing:.05em;">
      République française · Maturité numérique</p>
    <h1 style="margin:8px 0 0;font-size:20px;line-height:28px;">{titre}</h1>
  </td></tr>
  <tr><td style="padding:16px 32px 24px;font-size:15px;line-height:24px;">
    {corps_html}
    <table role="presentation" cellpadding="0" cellspacing="0">{bouton}</table>
    <p style="margin:16px 0 0;font-size:12px;color:#666666;">
      Message automatique envoyé par l'outil d'auto-évaluation de la maturité numérique (SIRCOM / MIWEB).</p>
  </td></tr>
</table>
</td></tr></table>
</body></html>"""


def send(to, subject, text, titre=None, corps_html=None, lien=None, lien_label=None):
    """Envoie un mail texte + HTML. Lève MailerError en cas d'échec."""
    if not enabled():
        raise MailerError("aucun serveur mail configuré (MAIL_HOST vide)")
    msg = EmailMessage()
    msg["From"] = formataddr((MAIL_FROM_NAME, MAIL_FROM_ADDR))
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(text)
    msg.add_alternative(_html(titre or subject, corps_html or text.replace("\n", "<br>"),
                              lien=lien, lien_label=lien_label), subtype="html")
    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT, timeout=10) as smtp:
            smtp.send_message(msg)
    except OSError as e:
        raise MailerError(f"mailer injoignable ({MAIL_HOST}:{MAIL_PORT}) : {e}") from e
