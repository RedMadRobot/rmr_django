import time

from django import forms


class StartStopTime(forms.Form):

    max_range = None

    start_time = forms.IntegerField(required=False)
    stop_time = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.pre_init()
        super().__init__(*args, **kwargs)

    def pre_init(self):
        self.declared_fields['stop_time'].required = \
            self.declared_fields['start_time'].required = \
            self.max_range is not None

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        stop_time = cleaned_data.get('stop_time')
        if None not in (stop_time, start_time):
            if start_time > stop_time:
                raise forms.ValidationError(
                    'start_time can\'t be greater then stop_time',
                )
            if self.max_range is not None and stop_time - start_time > self.max_range:
                raise forms.ValidationError(
                    'range between start_time and stop_time can\'t be greater '
                    'then {max_range}'.format(max_range=self.max_range),
                )
        return cleaned_data


class StartStopTimeDefaultStop(StartStopTime):

    def pre_init(self):
        super().pre_init()
        self.declared_fields['stop_time'].required = False

    def clean_stop_time(self):
        stop_time = self.cleaned_data['stop_time']
        return int(time.time()) if stop_time is None else stop_time
