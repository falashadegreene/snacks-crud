from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="falashadegreene", email="falashadegreene@gmail.com", password=""
        )

        self.snack = Snack.objects.create(
            name="cookies", definition="the best", reviewer=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "cookies")

    def test_snack_content(self):
        self.assertEqual(str(self.snack.name), "cookies")
        self.assertEqual(str(self.snack.reviewer), "falashadegreene")
        self.assertEqual(str(self.snack.definition), "the best")

    def test_snack_list(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cookies")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "cookies")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "name": "cookies",
                "definition": "the best",
                "reviewer": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "the best")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"name": "Updated name", "definition": "low on calories", "reviewer": self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)