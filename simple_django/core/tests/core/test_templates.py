from django import forms
from django.contrib.messages.storage.base import Message
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.translation import activate


def test_403_html():
    tmpl = SimpleTemplateResponse("403.html")
    tmpl.render()
    assert tmpl.is_rendered


def test_404_html():
    tmpl = SimpleTemplateResponse("404.html")
    tmpl.render()
    assert tmpl.is_rendered


def test_500_html():
    tmpl = SimpleTemplateResponse("500.html")
    tmpl.render()
    assert tmpl.is_rendered


def test_full_bleed_html():
    tmpl = SimpleTemplateResponse("fullbleed.html")
    tmpl.render()
    assert tmpl.is_rendered


def test_bootstrap_svg_html(fake):
    ctx = {"class_name": fake.word(), "icon_name": fake.word()}
    tmpl = SimpleTemplateResponse("helpers/_bootstrap-svg.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered

    assert ctx["class_name"] in tmpl.rendered_content
    assert ctx["icon_name"] in tmpl.rendered_content


def test_flash_messages_html(fake):

    ctx = {"messages": [Message(message=fake.sentence(), level=25)]}
    tmpl = SimpleTemplateResponse("partials/_flash-messages.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered

    assert str(ctx["messages"][0]) in tmpl.rendered_content


def test_paginator_html(rf):
    request = rf.get("/")
    ctx = {}
    pages = range(9)
    paginate_by = 10
    paginator = Paginator(pages, paginate_by)
    page_obj = paginator.get_page(1)
    ctx.update(
        {"page_obj": page_obj, "elided_page_range": paginator.get_elided_page_range(1)}
    )
    tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered

    pages = range(1000)
    paginator = Paginator(pages, paginate_by)
    page_obj = paginator.get_page(1)
    ctx.update(
        {"page_obj": page_obj, "elided_page_range": paginator.get_elided_page_range(1)}
    )
    tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered

    page_obj = paginator.get_page(2)
    ctx.update(
        {"page_obj": page_obj, "elided_page_range": paginator.get_elided_page_range(1)}
    )
    tmpl = TemplateResponse(request, "partials/_paginator.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered


def test_form_errors_html(fake):
    activate("en-us")

    class MyForm(forms.Form):
        val = forms.CharField(max_length=5)

        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get("val") == "nein":
                raise ValidationError("Nein!Nein!Nein!")
            return cleaned_data

    form = MyForm({"val": "aye"})
    form.is_valid()
    ctx = {"form": form}
    tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered
    assert "alert" not in tmpl.rendered_content

    form = MyForm({"val": "helloworld"})
    form.is_valid()
    ctx["form"] = form
    tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered
    assert "We found some errors" in tmpl.rendered_content

    form = MyForm({"val": "nein"})
    form.is_valid()
    ctx["form"] = form
    tmpl = SimpleTemplateResponse("partials/_form-errors.html", ctx)
    tmpl.render()
    assert tmpl.is_rendered
    assert "Nein!Nein!Nein!" in tmpl.rendered_content
