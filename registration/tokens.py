from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#token generator for the email confirmation and also we are using password reset token generator for this.

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()