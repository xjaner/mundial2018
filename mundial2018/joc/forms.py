from django.contrib.auth.models import User

from registration.forms import RegistrationForm
from registration.users import UsernameField


class RegistrationFormComplete(RegistrationForm):
    def as_table(self):
        return self._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<a class="helptext">?<span>%s</span></a>',
            errors_on_separate_row=True)

    class Meta:
        model = User
        fields = (UsernameField(), "email", "first_name", "last_name")
