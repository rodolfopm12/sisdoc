# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()