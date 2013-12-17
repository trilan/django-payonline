import pytz
from django import forms


class UTCDateTimeField(forms.DateTimeField):

    def to_python(self, value):
        datetime = super(UTCDateTimeField, self).to_python(value)
        if datetime is None:
            return datetime
        return datetime.replace(tzinfo=pytz.utc)
