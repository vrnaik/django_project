from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
# from .models import Snippet
# from .models import UserReq
from django.core.validators import  RegexValidator


class NameWidget(forms.MultiWidget):

    def __init__(self, attrs=None):
        super().__init__([
            forms.TextInput(),
            forms.TextInput()
        ], attrs)

    def decompress(self, value):
        # 'firstvalue secondvalue'
        if value:
            return value.split(' ')
        return ['name', 'surname']
        # ['firstvalue','secondvalue']



class NameField(forms.MultiValueField):

    widget = NameWidget

    def  __init__(self, *args, **kwargs):

        fields = (
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+', 'Enter a valid first name (only letters)')
            ]),  #name
            forms.CharField(validators=[
                RegexValidator(r'[a-zA-Z]+', 'Enter a valid second name (only letters)')
            ]),  #surname

        )

        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        # data_list = ['firstvalue', 'secondvalue']
        return f'{data_list[0]} {data_list[1]}'
        # 'firstvalue secondvalue'



class HomeForm(forms.Form):
    # name = NameField()
    # # email = forms.EmailField(label='E-Mail')
    # password = forms.CharField(widget=forms.PasswordInput())
    # email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # category = forms.ChoiceField(choices = [('question', 'Question'),('other','Other')])
    # subject = forms.CharField(required=False)
    # body = forms.CharField(widget=forms.Textarea)


# parameters

    # fan = forms.CharField(widget=forms.Textarea)
    # pump = forms.CharField(widget=forms.Textarea)
    # sprinkeler = forms.CharField(widget=forms.Textarea)
    # light = forms.CharField(widget=forms.Textarea)
    # id = forms.CharField(widget=forms.Textarea)





    status = forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'Status'}), required=True)

    # action = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Action'}))
    action = forms.ChoiceField(choices = [('start', 'Start'),('stop','Stop')])
    duration = forms.CharField(validators=[
                RegexValidator(r'[0-9]+', 'Enter a valid duration in minutes (only digit)')
            ],widget=forms.TextInput(attrs={'placeholder': 'Duration'}))
    # startTime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'StartTime'}))
    startTime = forms.TimeField(widget=forms.TimeInput)
    # stopTime = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'StopTime'}))
    stopTime = forms.TimeField(widget=forms.TimeInput)

    status1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Status'}))
    status1.label = 'Status'

    action1 = forms.ChoiceField(choices = [('start', 'Start'),('stop','Stop')])
    action1.label = 'Action'

    duration1 = forms.CharField(validators=[
                RegexValidator(r'[0-9]+', 'Enter a valid duration in minutes (only digit)')
            ],widget=forms.TextInput(attrs={'placeholder': 'Duration'}))
    duration1.label = 'Duration'

    startTime1 = forms.TimeField(widget=forms.TimeInput)
    startTime1.label = 'StartTime'

    stopTime1 = forms.TimeField(widget=forms.TimeInput)
    stopTime1.label = 'StopTime'

    status2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Status'}))
    status2.label = 'Status'

    action2 = forms.ChoiceField(choices = [('start', 'Start'),('stop','Stop')])
    action2.label = 'Action'

    duration2 = forms.CharField(validators=[
                RegexValidator(r'[0-9]+', 'Enter a valid duration in minutes (only digit)')
            ],widget=forms.TextInput(attrs={'placeholder': 'Duration'}))
    duration2.label = 'Duration'

    startTime2 = forms.TimeField(widget=forms.TimeInput)
    startTime2.label = 'StartTime'

    stopTime2 = forms.TimeField(widget=forms.TimeInput)
    stopTime2.label = 'StopTime'

    status3 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Status'}))
    status3.label = 'Status'

    action3 = forms.ChoiceField(choices = [('start', 'Start'),('stop','Stop')])
    action3.label = 'Action'

    duration3 = forms.CharField(validators=[
                RegexValidator(r'[0-9]+', 'Enter a valid duration in minutes (only digit)')
            ],widget=forms.TextInput(attrs={'placeholder': 'Duration'}))
    duration3.label = 'Duration'

    startTime3 = forms.TimeField(widget=forms.TimeInput)
    startTime3.label = 'StartTime'

    stopTime3 = forms.TimeField(widget=forms.TimeInput)
    stopTime3.label = 'StopTime'


    # check_me_out = forms.BooleanField(required=False)

    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper
    #     self.helper.form_method = 'post'
    #     self.helper.layout = Layout(
    #
    #         'name',
    #         # 'email',
    #         # 'category',
    #         # 'subject',
    #         # 'body',
    #         # 'pump',
    #         # 'light',
    #         # 'fan',
    #         # 'sprinkler',
    #
    #         # 'status',
    #         # 'duration',
    #
    #
    #         Submit('submit', 'Submit', css_class='btn-success')
    #     )


#
# class SnippetForm(forms.ModelForm):
#
#     class Meta:
#         model = Snippet
#         fields = ('name', 'body')
#
# # class UserReqForm(forms.ModelForm):
# #
# #     class Meta:
# #         model = UserReq
# #         fields = ('status', 'action', 'duration', 'startTime', 'stopTime','status1', 'action1', 'duration1', 'startTime1', 'stopTime1')
