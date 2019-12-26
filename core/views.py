from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView
from .models import Person, Schedule, AdminSetting
from .forms import CreateScheduleForm, CreatePersonForm, DeletePersonForm, MaxOutForm


@login_required
def admin_view(request):
    admin_setting = AdminSetting.objects.get(pk=1)
    form3 = MaxOutForm(instance=admin_setting)
    if request.method == 'POST':
        if 'Create' in request.POST:
            form1 = CreatePersonForm(request.POST)
            if form1.is_valid():
                form1.save()
                messages.success(request, 'User created.')
            else:
                return render(request, "core/admin.html", context={'max_out': admin_setting.max_out, 'form1': form1, 'form2': DeletePersonForm(), 'form3': form3})
        elif 'Delete' in request.POST:
            form2 = DeletePersonForm(request.POST)
            if form2.is_valid():
                form2.cleaned_data.get('person').delete()
                messages.success(request, 'User deleted.')
            else:
                return render(request, "core/admin.html", context={'max_out': admin_setting.max_out, 'form1': CreatePersonForm(), 'form2': form2, 'form3': form3})
        elif 'max_out' in request.POST:
            form3 = MaxOutForm(request.POST, instance=admin_setting)
            if form3.is_valid():
                form3.save()
                messages.success(request, 'Max Out updated')
            else:
                return render(request, "core/admin.html", context={'max_out': admin_setting.max_out, 'form1': CreatePersonForm(), 'form2': DeletePersonForm(), 'form3': form3})
        else:
            return HttpResponseBadRequest(content=b'Wrong option')
    form1 = CreatePersonForm()
    form2 = DeletePersonForm()

    return render(request, "core/admin.html", context={'max_out': admin_setting.max_out, 'form1': form1, 'form2': form2, 'form3': form3})


class ScheduleCreate(CreateView):
    form_class = CreateScheduleForm
    template_name = "core/schedule_form.html"
    success_url = reverse_lazy('schedule_list')


class ScheduleDelete(DeleteView):
    model = Schedule
    success_url = reverse_lazy('schedule_list')
    template_name = "core/schedule_delete.html"


class ScheduleList(ListView):
    queryset = Schedule.objects.all()
    template_name = "core/schedule_list.html"
    paginate_by = 10


def export_csv(request):
    schedules = Schedule.objects.all()
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="schedules-{}.csv"'.format(timezone.now())

    writer = csv.writer(response)
    writer.writerow(['Name', 'Reason', 'Start Date', 'End Date'])
    for s in schedules:
        writer.writerow([s.person.name, s.get_reason_display(), s.start_date.strftime(
            '%b. %-d, %Y'), s.end_date.strftime('%b. %-d, %Y')])

    return response
