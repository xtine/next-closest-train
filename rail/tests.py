from django.test import TestCase, Client
from django.urls import reverse

from .models import rail_lines, station, StopTime


class RailLineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.my_instance = rail_lines.objects.create(
            route_code="Metro X Line", line_id=99
        )

    def test_model_creation(self):
        self.assertEqual(self.my_instance.route_code, "Metro X Line")
        self.assertTrue(isinstance(self.my_instance, rail_lines))
        self.assertEqual(rail_lines.objects.count(), 1)

    def test_model_str_method(self):
        self.assertEqual(str(self.my_instance), "Metro X Line")


# Basic test that home page works
class IndexPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")

    # Test if the page loads the header, and has CSRF token
    def test_home_page_content(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Where's my closest Metro Rail Station?")
        self.assertContains(response, "csrfmiddlewaretoken")
