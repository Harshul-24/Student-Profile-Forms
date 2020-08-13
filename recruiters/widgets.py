from django.forms import FileInput, Field, TextInput, FileField
from PIL import Image
from io import BytesIO
	
class JPEGImageField(Field):
	widget = FileInput
	def __init__(self, *args, **kwargs):
		super(JPEGImageField, self).__init__(*args, **kwargs)
	def clean(self, value, initial = None):
		myfile = BytesIO(b'')
		try:
			image = Image.open(value.file)
			image_rgb = image.convert("RGB")
			image_rgb.save(myfile, format = "jpeg")
		except AttributeError:
			return None
		return myfile.getvalue()

class CustomComboWidget(TextInput):
	def to_python(self, value):
		return value.split(",")
	def __init__(self, data_list, name, *args, **kwargs):
		super(CustomComboWidget, self).__init__(*args, **kwargs)
		self._list = data_list
		self._name = name
	def render(self, name, value, *args, **kwargs):
		selectedOptions = ""
		for item in self._list:
			selectedOptions += '<div id = "%s-option-%s" value = "%s" class = "selectOption">%s</div>\n' %(name, item[0], item[0], item[1])
		selectedOptionWrapper = '<div id = "%s-selected-option-wrapper" class = "selectedOptionWrapper">\n %s </div>\n' %(name, selectedOptions)
		optionWrapper = '<div id = "%s-option-wrapper" class = "optionWrapper">\n%s</div>' %(name, selectedOptions)
		inputBox = '<input type = "text" id = "id_%s" class = "selectInputText"/>\n'%(name)
		searchBox = '<div id = "%s-search-box" class = "searchBox" contentEditable = "true"></div>\n' %(name)
		inputWrapper = '<div id = "%s-input-wrapper" class = "selectInputWrapper">%s %s </div>\n' %(name, selectedOptionWrapper, searchBox)
		text_html = '%s <div id = "%s-select" class = "selectToolWrapper"> %s %s </div>\n' %(inputBox, name, inputWrapper, optionWrapper)
		return text_html