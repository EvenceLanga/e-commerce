from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .models import AuxRelayInventory
from .forms import AuxRelayInventoryForm
from supabase import create_client, Client
import os, uuid

# Connect to Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Authentication views ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inventory_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# --- Add inventory item ---
@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        form = AuxRelayInventoryForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            image_file = request.FILES.get('image')

            if image_file:
                file_name = f"{uuid.uuid4()}_{image_file.name}"
                file_bytes = image_file.read()

                # Upload image to Supabase Storage
                supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, file_bytes)
                image_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)
                obj.image_url = image_url

            obj.save()
            return redirect('inventory_list')
    else:
        form = AuxRelayInventoryForm()

    return render(request, 'add_inventory.html', {'form': form})

# --- Paginated list view ---
@login_required
def inventory_list(request):
    items = AuxRelayInventory.objects.all().order_by('material')
    paginator = Paginator(items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory_list.html', {'page_obj': page_obj})
