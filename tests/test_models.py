from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from pauses.models import Pause, Feeling, Need, default_pause_title
from unittest.mock import patch
from datetime import datetime

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@example.com", firstname="Camille", gender="F"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.firstname, "Camille")
        self.assertEqual(user.gender, "F")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_email_unique_constraint(self):
        User.objects.create_user(
            email="test@example.com", firstname="User1", gender="F"
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test@example.com", firstname="User2", gender="M"
            )


class FeelingModelTest(TestCase):
    def test_feeling_family_required(self):
        feeling = Feeling(feminine_name="Heureuse", masculine_name="Heureux")
        with self.assertRaises(ValidationError):
            feeling.full_clean()

    def test_feeling_family_cannot_be_empty(self):
        feeling = Feeling(
            feeling_family="", feminine_name="Heureuse", masculine_name="Heureux"
        )
        with self.assertRaises(ValidationError):
            feeling.full_clean()

    def test_feeling_family_must_be_valid_choice(self):
        feeling = Feeling(
            feeling_family="XX", feminine_name="Heureuse", masculine_name="Heureux"
        )
        with self.assertRaises(ValidationError):
            feeling.full_clean()

    def test_feeling_creation_with_valid_family(self):
        feeling = Feeling.objects.create(
            feeling_family="JO", feminine_name="Heureuse", masculine_name="Heureux"
        )
        self.assertEqual(feeling.feeling_family, "JO")
        self.assertEqual(feeling.feminine_name, "Heureuse")
        self.assertEqual(feeling.masculine_name, "Heureux")

    def test_get_label_feminine(self):
        feeling = Feeling.objects.create(
            feeling_family="JO", feminine_name="Heureuse", masculine_name="Heureux"
        )
        user = User(gender="F")
        self.assertEqual(feeling.get_label(user), "Heureuse")

    def test_get_label_masculine(self):
        feeling = Feeling.objects.create(
            feeling_family="JO", feminine_name="Heureuse", masculine_name="Heureux"
        )
        user = User(gender="M")
        self.assertEqual(feeling.get_label(user), "Heureux")


class NeedModelTest(TestCase):
    def test_need_family_required(self):
        need = Need(name="Sécurité")
        with self.assertRaises(ValidationError):
            need.full_clean()

    def test_need_family_cannot_be_empty(self):
        need = Need(need_family="", name="Sécurité")
        with self.assertRaises(ValidationError):
            need.full_clean()

    def test_need_family_must_be_valid_choice(self):
        need = Need(need_family="XX", name="Sécurité")
        with self.assertRaises(ValidationError):
            need.full_clean()

    def test_need_creation_with_valid_family(self):
        need = Need.objects.create(need_family="SU", name="Sécurité")
        self.assertEqual(need.need_family, "SU")
        self.assertEqual(need.name, "Sécurité")

    def test_need_str_method(self):
        need = Need.objects.create(need_family="SU", name="Sécurité")
        self.assertEqual(str(need), "Sécurité")


class PauseModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", firstname="Test", gender="F"
        )
        self.feeling = Feeling.objects.create(
            feeling_family="JO", feminine_name="Heureuse", masculine_name="Heureux"
        )
        self.need = Need.objects.create(need_family="SU", name="Sécurité")

    def test_pause_creation(self):
        pause = Pause.objects.create(
            user=self.user, title="Ma pause test", observation="Observation test"
        )
        self.assertEqual(pause.user, self.user)
        self.assertEqual(pause.title, "Ma pause test")
        self.assertIsNotNone(pause.created_at)

    def test_pause_feelings_relationship(self):
        pause = Pause.objects.create(
            user=self.user, title="Ma pause test", observation="Observation test"
        )
        pause.feelings.add(self.feeling)
        self.assertEqual(pause.feelings.count(), 1)
        self.assertIn(self.feeling, pause.feelings.all())

    def test_pause_needs_relationship(self):
        pause = Pause.objects.create(
            user=self.user, title="Ma pause test", observation="Observation test"
        )
        pause.needs.add(self.need)
        self.assertEqual(pause.needs.count(), 1)
        self.assertIn(self.need, pause.needs.all())


class DefaultPauseTitleTest(TestCase):

    @patch("pauses.models.timezone.now")
    def test_default_pause_title(self, mock_now):
        mock_now.return_value = datetime(2025, 9, 9)
        result = default_pause_title()
        self.assertEqual(result, "Pause du 9 Septembre 2025")
