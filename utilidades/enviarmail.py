# -*- encoding: utf-8 -*-
import django.core.mail
from django.core.mail.message import EmailMessage

__author__ = 'brian'

import smtplib
import mimetypes
import commands

from configuracion import settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def enviar_email(asunto, mensaje, mensaje_html, destinos):
    msg = EmailMessage(asunto, mensaje_html, settings.EMAIL_HOST_USER, destinos)
    msg.content_subtype = "html"
    msg.send()
