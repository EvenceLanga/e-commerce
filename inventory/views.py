from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import AuxRelayInventoryForm
from supabase import create_client
from dotenv import load_dotenv
import os, uuid
from django.contrib.auth import logout

# Load environment variables
load_dotenv(r"C:\Users\EvenceMohauLanga\OneDrive - Net Nine Nine\Documents\Jacky\.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "images")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- AUTH ----------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inventory_list")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])  # allow both GET and POST
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

@login_required
def profile_view(request):
    """Display user profile information."""
    user = request.user
    context = {
        "user": user,
    }
    return render(request, "profile.html", context)

# ---------------- ADD ITEM ----------------
@login_required
def add_inventory_item(request):
    if request.method == "POST":
        form = AuxRelayInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            image_url = None
            image_file = request.FILES.get("image")

            # Upload image to Supabase
            if image_file:
                file_name = f"{uuid.uuid4()}_{image_file.name}"
                file_bytes = image_file.read()
                supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, file_bytes)
                image_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

            # Prepare data for Supabase
            data = {
                "material": form.cleaned_data["material"],
                "alternative_mat": form.cleaned_data.get("alternative_mat", ""),
                "mat_group": form.cleaned_data.get("mat_group", ""),
                "basic_data_text": form.cleaned_data.get("basic_data_text", ""),
                "material_description": form.cleaned_data.get("material_description", ""),
                "standard_price": form.cleaned_data.get("standard_price") or 0,
                "total_stock": form.cleaned_data.get("total_stock") or 0,
                "per": form.cleaned_data.get("per") or 1,
                "image_url": image_url,
                "created_by": request.user.username,           # ✅ Added
                "last_updated_by": request.user.username,
            }

            supabase.table("aux_relay_inventory").insert(data).execute()
            return redirect("inventory_list")

    else:
        form = AuxRelayInventoryForm()

    return render(request, "add_inventory.html", {"form": form})


# ---------------- LIST ITEMS ----------------
@login_required
def inventory_list(request):
    # Pagination
    page = int(request.GET.get("page", 1))
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size - 1

    # Sorting
    sort_by = request.GET.get("sort", "material")
    sort_order = request.GET.get("order", "asc")  # 'asc' or 'desc'

    # Search
    search_query = request.GET.get("search", "").strip().lower()

    # Fetch all items
    response = supabase.table("aux_relay_inventory").select("*").execute()
    items = response.data or []

    # Filter search manually
    if search_query:
        items = [
            item for item in items
            if search_query in (item.get("material") or "").lower()
            or search_query in (item.get("material_description") or "").lower()
            or search_query in (item.get("mat_group") or "").lower()
        ]

    # Sort manually in Python
    reverse = sort_order == "desc"
    items.sort(key=lambda x: x.get(sort_by) or "", reverse=reverse)

    # Pagination
    total_count = len(items)
    total_pages = (total_count + page_size - 1) // page_size
    items = items[start:end+1]

    table_columns = [
        "material","alternative_mat","mat_group","basic_data_text",
        "material_description","standard_price","per","total_stock","total_value"
    ]

    return render(request, "inventory_list.html", {
        "items": items,
        "table_columns": table_columns,
        "page": page,
        "total_pages": total_pages,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "search_query": request.GET.get("search", "")
    })


# ---------------- EDIT ITEM ----------------
@login_required
def edit_inventory_item(request, material):
    # Get item by material
    response = supabase.table("aux_relay_inventory").select("*").eq("material", material).single().execute()
    item = response.data if hasattr(response, "data") else None

    if not item:
        return redirect("inventory_list")

    if request.method == "POST":
        form = AuxRelayInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            image_url = item.get("image_url")
            image_file = request.FILES.get("image")

            # Re-upload new image if provided
            if image_file:
                file_name = f"{uuid.uuid4()}_{image_file.name}"
                file_bytes = image_file.read()
                supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, file_bytes)
                image_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

            data = {
                "alternative_mat": form.cleaned_data.get("alternative_mat", ""),
                "mat_group": form.cleaned_data.get("mat_group", ""),
                "basic_data_text": form.cleaned_data.get("basic_data_text", ""),
                "material_description": form.cleaned_data.get("material_description", ""),
                "standard_price": form.cleaned_data.get("standard_price") or 0,
                "total_stock": form.cleaned_data.get("total_stock") or 0,
                "per": form.cleaned_data.get("per") or 1,
                "image_url": image_url,
                "last_updated_by": request.user.username,
            }

            supabase.table("aux_relay_inventory").update(data).eq("material", material).execute()
            return redirect("inventory_list")
    else:
        form = AuxRelayInventoryForm(initial=item)

    return render(request, "add_inventory.html", {"form": form, "edit": True})


# ---------------- DELETE ITEM ----------------
@login_required
def delete_inventory_item(request, material):
    supabase.table("aux_relay_inventory").delete().eq("material", material).execute()
    return redirect("inventory_list")


import openpyxl
from django.http import HttpResponse

@login_required
def export_inventory_excel(request):
    # Fetch all data
    response = supabase.table("aux_relay_inventory").select("*").execute()
    items = response.data or []

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory"

    # Headers
    headers = ["Material", "Description", "Price", "Stock", "Per", "Total Value", "Image URL"]
    ws.append(headers)

    # Rows
    for item in items:
        ws.append([
            item.get("material"),
            item.get("material_description"),
            item.get("standard_price"),
            item.get("total_stock"),
            item.get("per"),
            item.get("total_value"),
            item.get("image_url"),
        ])

    # Prepare response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=inventory.xlsx'
    wb.save(response)
    return response


from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")
