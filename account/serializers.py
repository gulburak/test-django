from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists() > 0:
            raise serializers.ValidationError('polzovatel s takim email uzhe suchestvuet')
        return email

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('paroli dolzhni sovpadat')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        user.send_activation_email()

        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    def validate(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('polzovatel ne naiden')
        return email
    def validation_code(self, code):
        if User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('polzovatel ne naiden')
        return code
    def validate(self, data):
        email = data.get('email')
        code = data.pop('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError()
        return data
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    mew_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_pass):
        request = self.context.get('request')
        user = request.user
        if not request.user.check_password(old_pass):
            raise serializers.ValidationsError('vvedite vernii parol')
        return old_pass
    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError('paroli ne sovpadaut')
        return attrs
    def set_new_password(self):
        new_pass = self.validated_data('new_password')
        user = self.context.get('reequired').user
        user.set_password(new_pass)
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(selfself, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('takoi polzovatel ne zaregistrirovan')
        return email
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.filter(email=email)
        user.create_activation_code()
        send_mail('vostanovlenie parolya',
                  f'vash kod vostanovleniya:{user.activation_code}',
                  'test1@gmail.com',
                  [user.email])
class ForgotPassCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if not User.objects.filter(email = email, activation_code=code).exists():
            raise serializers.ValidationError('pozovatel ne naiden')
        if password1 != password2:
            raise serializers.ValidationError('paroli ne sovpadaut')
        return attrs
    def set_new_password(self):
        email = self.validated_data('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email = email)
        user.set_password()
        user.save()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists() > 0:
            raise serializers.ValidationError('polzovatel s takim email uzhe suchestvuet')
        return email
    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('nevernii email ili parol')
        else:
            raise serializers.ValidationError('email i parol obyazatelni')
        data['user'] = user
        return data
# class ForgotPassSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('takoi polzovatel ne zaregistrirovan')
#         return email
#
#     def send_verification_email(self):
#         email = self.validated_data.get('email')
#         user = User.objects.filter(email=email)
#         random_password = get_random_string(length=10)
#         user.set_password(random_password)
#         user.create_activation_code()
#         send_mail('vostanovlenie parolya',
#                   f'vash novii parol:{random_password}',
#                   'test1@gmail.com',
#                   [user.email])
