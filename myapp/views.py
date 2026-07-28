from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


@login_required
def item_list(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, 'read.html', {'items': items})


@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item created successfully!')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'create_update.html', {'form': form, 'action': 'Create'})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'create_update.html', {'form': form, 'action': 'Update'})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('item_list')
    return redirect('item_list')