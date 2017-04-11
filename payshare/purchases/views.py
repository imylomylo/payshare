# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# from django.http import HttpResponseRedirect

from payshare.purchases.models import Collective
from payshare.purchases.forms import PurchaseForm


def index(request):
    # # if this is a POST request we need to process the form data
    # if request.method == "POST":
    #     # create a form instance and populate it with data from the request:
    #     form = PurchaseForm(request.POST)
    #     # check whether it"s valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponseRedirect("/thanks/")
    # # if a GET (or any other method) we"ll create a blank form
    # else:
    #    form = PurchaseForm()
    collective = Collective.objects.first()
    purchase_form = PurchaseForm(initial={"collective": collective})
    return render(request, "index.html", {
        "purchase_form": purchase_form,
    })
