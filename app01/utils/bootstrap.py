from django import forms

class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加插件
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }

class BootStrapModelForm(BootStrap,forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环找到所有插件，添加插件
    #     for name, field in self.fields.items():
    #         if field.widget.attrs:
    #             field.widget.attrs['class'] = 'form-control'
    #             field.widget.attrs['placeholder'] = field.label
    #         else:
    #             field.widget.attrs = {
    #                 'class': 'form-control',
    #                 'placeholder': field.label
    #             }
    pass
class BootStrapForm(BootStrap,forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环找到所有插件，添加插件
    #     for name, field in self.fields.items():
    #         if field.widget.attrs:
    #             field.widget.attrs['class'] = 'form-control'
    #             field.widget.attrs['placeholder'] = field.label
    #         else:
    #             field.widget.attrs = {
    #                 'class': 'form-control',
    #                 'placeholder': field.label
    #             }
    pass