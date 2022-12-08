from django.core.exceptions import ValidationError

class LengthValidator:
    def validate(self, password, user=None):
        if password.length < 8:
            raise ValidationError('le mot de passe doit contenir au moins 8 charactères', code='password length')
    
    def get_help_text(self):
         return 'Votre mot de passe doit contenir au 8 charactères alphanumériques.'

class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')
                
    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'
