from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase
from faker import Faker


class ManagementCommandsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fake = Faker()
        cls.fake = fake

    def test_init_site(self):
        project_name = self.fake.word()
        domain_name = self.fake.domain_name()

        with self.settings(
            PROJECT_NAME=project_name, DOMAIN_NAME=domain_name, PORT_NUMBER=443
        ):
            site = Site.objects.first()
            self.assertNotEqual(site.name, project_name)
            self.assertNotEqual(site.domain, domain_name)

            call_command("init_site")

            site.refresh_from_db()
            self.assertEqual(site.name, project_name)
            self.assertEqual(site.domain, domain_name)

        with self.settings(
            PROJECT_NAME=project_name, DOMAIN_NAME=domain_name, PORT_NUMBER=3000
        ):
            call_command("init_site")
            site = Site.objects.first()
            self.assertEqual(site.domain, f"{domain_name}:3000")
