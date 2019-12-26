from datetime import timedelta
from django import forms
from django.utils.translation import gettext as _
from django.db.models import Q

from .models import Person, Schedule, AdminSetting


class CreateScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['person', 'reason', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={"type": "date"}),
            'end_date': forms.widgets.DateInput(attrs={"type": "date"})
        }
        labels = {
            "person": _('The Scheduler')
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('start_date') > cleaned_data.get('end_date'):
            self.add_error(
                'start_date', 'start date must be less than end date')
            return cleaned_data

        delta = cleaned_data.get('start_date') - cleaned_data.get('end_date')

        schedules = Schedule.objects.filter(Q(start_date__lte=cleaned_data.get(
            'start_date')) | Q(end_date__gte=cleaned_data.get('start_date')))
        # count=0
        # one_day = timedelta(days=1)
        # for s in schedules:
        #     start = cleaned_data.get('start_date')
        #     end = cleaned_data.get('end_date')
        #     while start <=end:
        count = 0
        day = []
        cur = []
        cur_s = cleaned_data.get('start_date')
        cur_e = cleaned_data.get('end_date')
        max_out = AdminSetting.objects.get(pk=1).max_out
        for s in schedules:
            # for column_number, data in enumerate(row_data):
            #     datta.append(data)
            sdate = s.start_date
            edate = s.end_date
            print(sdate, edate)

            delta = edate - sdate  # as timedelta

            for i in range(delta.days + 1):
                d = sdate + timedelta(days=i)
                day.append(d)
            print(day)
            delta = cur_e - cur_s
            for i in range(delta.days + 1):
                c = cur_s + timedelta(days=i)
                cur.append(c)
            print(cur)

            def intersection(lst1, lst2):
                lst3 = [value for value in lst1 if value in lst2]
                return lst3

            lst1 = cur
            lst2 = day
            # print(intersection(lst1, lst2))
            print(len(intersection(lst1, lst2)))

            count = count + len(intersection(lst1, lst2))

            lst1 = []
            lst2 = []
            cur = []
            day = []
            # datta = []
        print(count, max_out)
        if count >= max_out:
            raise forms.ValidationError('Exceeded Max Out Value')


class CreatePersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = "__all__"


class DeletePersonForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.all())


class MaxOutForm(forms.ModelForm):

    class Meta:
        model = AdminSetting
        fields = ['max_out']
