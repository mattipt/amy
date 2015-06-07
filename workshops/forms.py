from django import forms
from django.forms import HiddenInput
from django.forms.models import modelform_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from selectable import forms as selectable

from workshops.models import Skill, Airport, Event, Task, Award, Person
from workshops import lookups

INSTRUCTOR_SEARCH_LEN = 10   # how many instrutors to return from a search by default

AUTOCOMPLETE_HELP_TEXT = (
    "Autocomplete field; type characters to view available options, "
    "then select desired item from list."
)

DATE_HELP_TEXT = "Select date using widget, or enter in YYYY-MM-DD format."


class BootstrapHelper(FormHelper):
    form_class = 'form-horizontal'
    label_class = 'col-lg-2'
    field_class = 'col-lg-8'

    def __init__(self, form=None):
        super().__init__(form)

        self.attrs['role'] = 'form'
        self.inputs.append(Submit('submit', 'Submit'))


class BootstrapHelperWithoutForm(BootstrapHelper):
    form_tag = False

bootstrap_helper = BootstrapHelper()
bootstrap_helper_without_form = BootstrapHelperWithoutForm()


class InstructorsForm(forms.Form):
    '''Represent instructor matching form.'''

    wanted = forms.IntegerField(label='Number Wanted',
                                initial=INSTRUCTOR_SEARCH_LEN,
                                min_value=1)
    latitude = forms.FloatField(label='Latitude',
                                min_value=-90.0,
                                max_value=90.0,
                                required=False)
    longitude = forms.FloatField(label='Longitude',
                                 min_value=-180.0,
                                 max_value=180.0,
                                 required=False)
    airport = selectable.AutoCompleteSelectField(
        lookup_class=lookups.AirportLookup,
        label='Airport',
        required=False,
        help_text=AUTOCOMPLETE_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        '''Build checkboxes for skills dynamically.'''
        super(InstructorsForm, self).__init__(*args, **kwargs)
        skills = Skill.objects.all()
        for s in skills:
            self.fields[s.name] = forms.BooleanField(label=s.name, required=False)

    def clean(self):
        cleaned_data = super(InstructorsForm, self).clean()
        airport = cleaned_data.get('airport')
        lat = cleaned_data.get('latitude')
        long = cleaned_data.get('longitude')

        if airport is None:
            if lat is None or long is None:
                raise forms.ValidationError(
                    'Must specify either an airport code or latitude/longitude')
        else:
            if lat is not None or long is not None:
                raise forms.ValidationError(
                    'Cannot specify both an airport code and a '
                    'latitude/longitude. Pick one or the other')
            cleaned_data['latitude'] = airport.latitude
            cleaned_data['longitude'] = airport.longitude
        return cleaned_data


class PersonBulkAddForm(forms.Form):
    '''Represent CSV upload form for bulk adding people.'''

    file = forms.FileField()


class SearchForm(forms.Form):
    '''Represent general searching form.'''

    term = forms.CharField(label='term',
                           max_length=100)
    in_sites = forms.BooleanField(label='in sites',
                                  required=False,
                                  initial=True)
    in_events = forms.BooleanField(label='in events',
                                   required=False,
                                   initial=True)
    in_persons = forms.BooleanField(label='in persons',
                                    required=False,
                                    initial=True)


class DebriefForm(forms.Form):
    '''Represent general debrief form.'''
    begin_date = forms.DateField(
        label='Begin date as YYYY-MM-DD',
        input_formats=['%Y-%m-%d', ]
    )
    end_date = forms.DateField(
        label='End date as YYYY-MD-DD',
        input_formats=['%Y-%m-%d', ]
    )


class EventForm(forms.ModelForm):

    site = selectable.AutoCompleteSelectField(
        lookup_class=lookups.SiteLookup,
        label='Site',
        required=True,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    organizer = selectable.AutoCompleteSelectField(
        lookup_class=lookups.SiteLookup,
        label='Organizer',
        required=False,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start'].help_text = DATE_HELP_TEXT
        self.fields['end'].help_text = DATE_HELP_TEXT

    def clean_slug(self):
        # Ensure slug is not an integer value for Event.get_by_ident
        data = self.cleaned_data['slug']

        try:
            int(data)
        except ValueError:
            pass
        else:
            raise forms.ValidationError("Slug must not be an integer-value.")

        return data

    class Meta:
        model = Event
        exclude = ('deleted', )


class TaskForm(forms.ModelForm):

    person = selectable.AutoCompleteSelectField(
        lookup_class=lookups.PersonLookup,
        label='Person',
        required=True,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        if event:
            self.instance.event = event

    class Meta:
        model = Task
        exclude = ('event', 'deleted')


class TaskFullForm(TaskForm):

    event = selectable.AutoCompleteSelectField(
        lookup_class=lookups.EventLookup,
        label='Event',
        required=True,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    class Meta:
        model = Task
        exclude = ('deleted', )


class PersonForm(forms.ModelForm):

    airport = selectable.AutoCompleteSelectField(
        lookup_class=lookups.AirportLookup,
        label='Airport',
        required=False,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    class Meta:
        model = Person
        # don't display the 'password', 'user_permissions',
        # 'groups' or 'is_superuser' fields
        # + reorder fields
        fields = ['personal', 'middle', 'family', 'username', 'may_contact',
                  'email', 'gender', 'airport', 'github', 'twitter', 'url',
                  'notes', ]


class PersonPermissionsForm(forms.ModelForm):
    class Meta:
        model = Person
        # only display 'user_permissions', 'groups' and `is_superuser` fields
        fields = [
            'is_superuser',
            'user_permissions',
            'groups',
        ]


class BadgeAwardForm(forms.ModelForm):

    person = selectable.AutoCompleteSelectField(
        lookup_class=lookups.PersonLookup,
        label='Person',
        required=True,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    event = selectable.AutoCompleteSelectField(
        lookup_class=lookups.EventLookup,
        label='Event',
        required=False,
        help_text=AUTOCOMPLETE_HELP_TEXT,
        widget=selectable.AutoComboboxSelectWidget,
    )

    class Meta:
        model = Award
        fields = '__all__'
        widgets = {'badge': HiddenInput}

