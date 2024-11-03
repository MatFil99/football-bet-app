from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse

from .models import FootballTeam

# Create your tests here.

class FootballTeamModelTests(TestCase):
    def test_create_no_name_team(self):
        ft = None
        try:
            ft = FootballTeam()
            empty_str = ""
            self.assertNotEquals(ft.name, empty_str, msg="You cannot create FootballTeam with no name.")
        except Exception:
            self.assertIsNone(ft)


# views' tests
class TeamsViewTests(TestCase):
    def test_no_teams(self):
        response = self.client.get(reverse("teams"))
        self.assertEqual(response.status_code, 200)