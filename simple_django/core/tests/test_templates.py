from django import forms
from django.contrib.messages.storage.base import Message
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.test import RequestFactory, SimpleTestCase
from django.utils.translation import activate
from faker import Faker


class TemplatesTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(TemplatesTests, cls).setUpClass()
        fake = Faker()
        cls.fake = fake
        cls.rf = RequestFactory()

    def test_403_html(self):
        tmpl = SimpleTemplateResponse("403.html")
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_404_html(self):
        tmpl = SimpleTemplateResponse("404.html")
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_500_html(self):
        tmpl = SimpleTemplateResponse("500.html")
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_full_bleed_html(self):
        tmpl = SimpleTemplateResponse("fullbleed.html")
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_bootstrap_svg_html(self):
        ctx = {"class_name": self.fake.word(), "icon_name": self.fake.word()}
        tmpl = SimpleTemplateResponse("helpers/_bootstrap-svg.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

        self.assertIn(ctx["class_name"], tmpl.rendered_content)
        self.assertIn(ctx["icon_name"], tmpl.rendered_content)

    def test_flash_messages_html(self):

        ctx = {"messages": [Message(message=self.fake.sentence(), level=25)]}
        tmpl = SimpleTemplateResponse("partials/_flash-messages.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)
        self.assertIn(str(ctx["messages"][0]), tmpl.rendered_content)

    def test_paginator_html(self):
        request = self.rf.get("/")
        ctx = {}
        pages = range(9)
        paginate_by = 10
        paginator = Paginator(pages, paginate_by)
        page_obj = paginator.get_page(1)
        ctx.update(
            {
                "page_obj": page_obj,
                "elided_page_range": paginator.get_elided_page_range(1),
            }
        )
        tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

        pages = range(1000)
        paginator = Paginator(pages, paginate_by)
        page_obj = paginator.get_page(1)
        ctx.update(
            {
                "page_obj": page_obj,
                "elided_page_range": paginator.get_elided_page_range(1),
            }
        )
        tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

        page_obj = paginator.get_page(2)
        ctx.update(
            {
                "page_obj": page_obj,
                "elided_page_range": paginator.get_elided_page_range(1),
            }
        )
        tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_form_errors_html(self):
        activate("en-us")

        error_msg = "Nein!Nein!Nein!"

        class MyForm(forms.Form):
            val = forms.CharField(max_length=5)

            def clean(self):
                cleaned_data = super().clean()
                if cleaned_data.get("val") == "nein":
                    raise ValidationError(error_msg)
                return cleaned_data

        form = MyForm({"val": "aye"})
        form.is_valid()
        ctx = {"form": form}
        tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)
        self.assertNotIn("alert", tmpl.rendered_content)

        form = MyForm({"val": "helloworld"})
        form.is_valid()
        ctx["form"] = form
        tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)
        self.assertIn("We found some errors", tmpl.rendered_content)

        form = MyForm({"val": "nein"})
        form.is_valid()
        ctx["form"] = form
        tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
        tmpl.render()
        assert tmpl.is_rendered
        self.assertTrue(tmpl.is_rendered)
        self.assertIn(error_msg, tmpl.rendered_content)
