from django.shortcuts import render, redirect
from django.views import View
from .models import Item
from .forms import ItemForm


def home(request):
    items = Item.objects.all().order_by("-created_at")
    return render(request, "main/home.html", {"items": items})


class ItemCreateView(View):
    def get(self, request):
        form = ItemForm()
        return render(request, "main/item_form.html", {"form": form})

    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "main/item_form.html", {"form": form})