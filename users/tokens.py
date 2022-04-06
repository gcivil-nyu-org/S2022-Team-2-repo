from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):  # pragma: no cover
        hash_val = str(user.pk) + str(timestamp)
        print(hash_val)
        return hash_val


account_activation_token = TokenGenerator()
