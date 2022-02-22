from django import forms
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.test import RequestFactory, TestCase


class AForm(forms.Form):
    val = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.is_clean = kwargs.pop("is_clean", True)
        super(AForm, self).__init__(*args, **kwargs)

    def clean_val(self):
        val = self.cleaned_data["val"]
        if val == "fail":
            raise ValidationError("Failed")

        return val

    def clean(self):
        if not self.is_clean:
            raise ValidationError("Non field")


class CoreTemplatesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        factory = RequestFactory()
        request = factory.get("/")
        cls.request = request

    def test_paginator_html(self):
        pages = list(range(10000))
        paginator = Paginator(pages, 10)
        page = paginator.get_page(1)
        tmpl = TemplateResponse(
            self.request, "partials/_paginator.html", {"page_obj": page}
        )
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

        page = paginator.get_page(3)
        tmpl = TemplateResponse(
            self.request, "partials/_paginator.html", {"page_obj": page}
        )
        tmpl.render()
        self.assertTrue(tmpl.is_rendered)

    def test_form_errors_html(self):
        form = AForm({"val": "ok"})
        tmpl = TemplateResponse(
            self.request, "partials/_form-errors.html", {"form": form}
        )
        self.assertTrue(tmpl.render().is_rendered)

        form = AForm({"val": "fail"})
        tmpl = TemplateResponse(
            self.request, "partials/_form-errors.html", {"form": form}
        )
        self.assertTrue(tmpl.render().is_rendered)

        form = AForm({"val": "ok"}, is_clean=False)
        tmpl = TemplateResponse(
            self.request, "partials/_form-errors.html", {"form": form}
        )
        self.assertTrue(tmpl.render().is_rendered)

        form = AForm({"val": "fail"}, is_clean=False)
        tmpl = TemplateResponse(
            self.request, "partials/_form-errors.html", {"form": form}
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_home_html(self):
        tmpl = TemplateResponse(
            self.request,
            "pages/home.html",
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_404_html(self):
        tmpl = TemplateResponse(
            self.request,
            "404.html",
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_403_html(self):
        tmpl = TemplateResponse(
            self.request,
            "403.html",
        )
        self.assertTrue(tmpl.render().is_rendered)

    def test_500_html(self):
        tmpl = TemplateResponse(
            self.request,
            "500.html",
        )
        self.assertTrue(tmpl.render().is_rendered)
