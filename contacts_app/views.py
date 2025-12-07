import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from .models import Contact
from .forms import UploadCSVForm, ContactForm

# --- Dashboard / Upload CSV ---
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = file.read().decode('utf-8').splitlines()
            reader = csv.reader(data)
            for row in reader:
                # Expecting: name, phone, state, address
                if len(row) != 4:
                    continue
                name, phone, state, address = [col.strip() for col in row]
                Contact.objects.update_or_create(
                    phone=phone,
                    defaults={
                        'name': name.upper(),
                        'state': state,
                        'address': address
                    }
                )
            return redirect('upload_csv')
    else:
        form = UploadCSVForm()

    # Dashboard statistics
    total_contacts = Contact.objects.count()
    states_count_qs = Contact.objects.values('state').annotate(total=Count('id')).order_by('-total')
    total_states = states_count_qs.count()
    most_common_state = states_count_qs[0]['state'] if states_count_qs else '-'

    # Chart data
    states_labels = [s['state'] for s in states_count_qs]
    states_counts = [s['total'] for s in states_count_qs]

    # Recent contacts
    recent_contacts = Contact.objects.order_by('-id')[:5]

    context = {
        "form": form,
        "total_contacts": total_contacts,
        "total_states": total_states,
        "most_common_state": most_common_state,
        "states_labels": states_labels,
        "states_counts": states_counts,
        "recent_contacts": recent_contacts,
    }
    return render(request, 'contacts_app/upload.html', context)


# --- List All Contacts ---
def list_contacts(request):
    contacts = Contact.objects.all().order_by('name')
    return render(request, 'contacts_app/list.html', {'contacts': contacts})


# --- Export Contacts as CSV ---
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'State', 'Address'])
    for c in Contact.objects.all():
        writer.writerow([c.name, c.phone, c.state, c.address])
    return response


# --- Add Single Contact Manually ---
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_contacts')
    else:
        form = ContactForm()
    return render(request, 'contacts_app/add_contact.html', {'form': form})


# --- Edit Contact ---
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('list_contacts')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts_app/add_contact.html', {'form': form, 'edit': True})


# --- Delete Contact ---
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('list_contacts')
    return render(request, 'contacts_app/confirm_delete.html', {'contact': contact})
