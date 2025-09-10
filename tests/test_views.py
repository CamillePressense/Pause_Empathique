from django.test import TestCase, Client
from pauses.models import *
from users.models import *
from users.forms import RegisterForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")

        # Données de test valides
        self.valid_user_data = {
            "firstname": "Martin",
            "email": "martin@test.fr",
            "password1": "1234marP",
            "password2": "1234marP",
            "gender": "M",
        }

        # Données de test invalides
        self.invalid_email_data = {
            "firstname": "Baduser",
            "email": "invalid-email",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "gender": "M",
        }

        self.invalid_password_data = {
            "firstname": "Baduser",
            "email": "baduser@test.fr",
            "password1": "testpassword123",
            "password2": "differentpassword",
            "gender": "M",
        }

    def test_register_page_get_request(self):
        # On teste l'affichage de la page d'inscription lors d'un GET
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_page_post_valid_data(self):
        # On teste l'inscription avec des données valides

        initial_user_count = User.objects.count()
        response = self.client.post(self.register_url, self.valid_user_data)

        expected_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_user_count + 1)

        created_user = User.objects.get(firstname="Martin")
        self.assertEqual(created_user.email, "martin@test.fr")
        self.assertTrue(created_user.check_password("1234marP"))

        self.assertTrue("_auth_user_id" in self.client.session)

    def test_register_page_post_invalid_email(self):
        # On teste l'inscription avec un email invalide

        initial_user_count = User.objects.count()
        response = self.client.post(self.register_url, self.invalid_email_data)

        self.assertEqual(response.status_code, 200)  # Reste sur la même page
        self.assertTemplateUsed(response, "users/register.html")

        self.assertEqual(User.objects.count(), initial_user_count)
        self.assertIn("email", response.context["form"].errors)
        self.assertIn(
            "Saisissez une adresse de courriel valide.",
            response.context["form"].errors["email"],
        )
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_register_page_post_invalid_password(self):
        # On teste l'inscription avec un password invalide

        initial_user_count = User.objects.count()
        response = self.client.post(self.register_url, self.invalid_password_data)

        self.assertEqual(response.status_code, 200)  # Reste sur la même page
        self.assertTemplateUsed(response, "users/register.html")

        self.assertEqual(User.objects.count(), initial_user_count)
        self.assertIn("password2", response.context["form"].errors)
        self.assertIn(
            "Les deux mots de passe ne correspondent pas.",
            response.context["form"].errors["password2"],
        )
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_register_page_duplicate_email(self):
        # On teste l'inscription avec un utilisateur existant

        User.objects.create_user(
            firstname="existing_user", email="martin@test.fr", password="password123"
        )
        response = self.client.post(self.register_url, self.valid_user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email="martin@test.fr").count(), 1)

    def test_register_page_post_empty_data(self):
        # On teste l'inscription avec des données vides

        response = self.client.post(self.register_url, {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertTemplateUsed(response, "users/register.html")

        form = response.context["form"]
        self.assertFalse(form.is_valid())

        expected_required_fields = [
            "email",
            "firstname",
            "password1",
            "password2",
        ]

        # Vérifier que chaque champ obligatoire a une erreur
        for field in expected_required_fields:
            self.assertIn(field, form.errors)
