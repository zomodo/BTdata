from django import forms

class CompanyForm(forms.Form):
    date=forms.CharField(
        widget=forms.DateInput(
            attrs={'id':'showrangedate'},
        )
    )

    area=forms.ChoiceField(
        initial='all',
        choices=(
            ('all','全省'),
            ('武汉','武汉'),
            ('宜昌','宜昌'),
            ('襄阳','襄阳'),
            ('黄石','黄石'),
            ('十堰','十堰'),
            ('孝感','孝感'),
            ('黄冈','黄冈'),
            ('荆州','荆州'),
            ('恩施','恩施'),
            ('随州','随州'),
            ('荆门','荆门'),
            ('鄂州','鄂州'),
            ('仙桃','仙桃'),
            ('潜江','潜江'),
            ('天门','天门'),
            ('咸宁','咸宁'),
            ('神农架','神农架'),
            ('None','未标注'),
        ),
        widget=forms.Select(
            attrs={'class':'selectpicker','data-live-search':'true','data-size':'5','data-style':'btn btn-default'},
        )
    )

    searchword=forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class':'cus-input','id':'searchword','placeholder':'搜公司/业务'},
        )
    )