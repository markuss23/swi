from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm


def home(request):
    items = Item.objects.all().order_by("-created_at")
    return render(request, "main/home.html", {"items": items})


class ItemCreateView(View):
    def get(self, request):
        form = ItemForm()
        return render(
            request, 
            "main/item_form.html", 
            {"form": form})

    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "main/item_form.html", {"form": form})


class ItemUpdateView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(instance=item)
        return render(
            request, 
            "main/item_form.html", 
            {"form": form, "item": item})

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(
            request, 
            "main/item_form.html",
            {"form": form, "item": item}
            )


class ItemDeleteView(View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(
            request, 
            "main/item_confirm_delete.html", 
            {"item": item})

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return redirect("home")


class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello, World!")


class RandomView(View):
    def get(self, request):
        return HttpResponse("Random View")


class AddNumbersView(View):
    def get(self, request, num1, num2):
        try:
            result = int(num1) + int(num2)
            return HttpResponse(f"The sum of {num1} and {num2} is {result}")
        except ValueError:
            return HttpResponse(
                "Please provide valid numbers in the URL path", status=400
            )
