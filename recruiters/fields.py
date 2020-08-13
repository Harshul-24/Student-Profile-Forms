from django.db.models import BinaryField, CharField
import csv
from .widgets import JPEGImageField
from django.forms import Field

def get_choices(path):
	fp = open(path, "rt", newline = "", encoding = "UTF-8-sig")
	reader = csv.reader(fp)
	data = list(reader)
	return data

class MultiChoiceField(CharField):
	def __init__(self, data_list, name, *args, **kwargs):
		kwargs['max_length'] = 127
		super().__init__(*args, **kwargs)
		self._name = name
		self._list = data_list
		self._num_list = [row[0] for row in data_list]

	def deconstruct(self):
		name, path, args, kwargs = super(MultiChoiceField, self).deconstruct()
		del kwargs['max_length']
		args.insert(0, self._list)
		args.insert(1, self._name)
		return name, path, args, kwargs
	
	def to_python(self, value):
		if value is None:
			return value
		try:
			num_list = value.split(",")
			return [self._list[self._num_list.index(num)] for num in num_list]
		except:
			return value
	
	def get_db_prep_value(self, value, connection, prepared = False):
		value = super().get_db_prep_value(value, connection, prepared)
		values = value.split(",")
		ret = ""
		for code in values:
			if code in self._num_list:
				ret += code + ","
		return ret
	
	def from_db_value(self, value, expression, connection):
		if value is None:
			return value
		value_list = value.split(",")
		return '\n'.join([self._list[self._num_list.index(num)][1] for num in value_list if num in self._num_list])

	def value_from_object(obj):
		return '\n'.join(row[1] for row in obj)
	
class ImageBinaryField(BinaryField):
	def __init__(self, *args, **kwargs):
		super(ImageBinaryField, self).__init__(*args, **kwargs)
	def formfield(self, **kwargs):
		kwargs.update({ 'form_class' : JPEGImageField })
		return super().formfield(**kwargs)