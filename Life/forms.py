from django import forms

class Welcome(forms.Form):
    phrase = forms.CharField(label='phrase', max_length=140)



class Descisionbasic(forms.Form):
    name = forms.CharField(label='name',max_length=50)


class Option(forms.Form):
    name = forms.CharField(label='name',max_length=90)

class Argument(forms.Form):
    argument = forms.CharField(label='argument', max_length=500)


class Description(forms.Form):
    description = forms.CharField(label='description', max_length=500)



class Login(forms.Form):
    inputUser = forms.EmailInput()
    inputPassword = forms.PasswordInput()



class Quotes(forms.Form):
    quote = forms.CharField(label='quote', max_length=500)


class Activitybasic(forms.Form):
    name = forms.CharField(label='name',max_length=50)
    CHOICES = [('01', '01'), ('02', '02'), ('03', '03'),('04', '04'),('05', '05'),]
    type = forms.ChoiceField(choices=CHOICES)

class flrp(forms.Form):
    description = forms.CharField(label='description', max_length=500)
    times = forms.IntegerField(label='times')
    CHOICES = [('day', 'day'),
               ('week', 'week')]
    ina = forms.ChoiceField(choices=CHOICES)
    deviation = forms.IntegerField(label='deviation')

class repe(forms.Form):
    description = forms.CharField(label='description', max_length=500)
    CHOICES = [('y', 'y'),
               ('N', 'N')]
    time = forms.TimeField(label ='time')
    rtd = forms.ChoiceField(choices=CHOICES)

class remi(forms.Form):
    text = forms.CharField(label="text", max_length=500)
    CHOICES = [('activity', 'activity'), ('now', 'now')]
    acti = forms.ChoiceField(choices=CHOICES)

class dead(forms.Form):
    description = forms.CharField(label="description", max_length=500)
    day = forms.IntegerField(label="day")
    month = forms.IntegerField(label="month")
    time = forms.TimeField(label="time")
    warning = forms.IntegerField(label="warning")


class video(forms.Form):
    description = forms.CharField(label="description", max_length=500)
    name = forms.CharField(label='name',max_length=50)
    htmlembedder = forms.CharField(label="htmlembedder", max_length=1000)

class article(forms.Form):
    description = forms.CharField(label="description", max_length=500)
    name = forms.CharField(label='name', max_length=50)
    link = forms.CharField(label='link', max_length=500)
    article = forms.CharField(label='article', max_length=6000)




class note(forms.Form):
    title = forms.CharField(label="title", max_length=50)
    subtitle = forms.CharField(label="subtitle", max_length=50)
    note = forms.CharField(label="note", max_length=2000)
