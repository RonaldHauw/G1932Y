from django import forms

class AlarmForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    time = forms.TimeField(label ='time')
    CHOICES = (('Soft', 'Soft'), ('Hard', 'Hard'),('Gently, Gently'))
    type = forms.ChoiceField(choices=CHOICES)


class QuickAlarmForm(forms.Form):
    time = forms.TimeField(label ='time')
    CHOICES = (('Soft', 'Soft'), ('Hard', 'Hard'),('Gently, Gently'))
    type = forms.ChoiceField(choices=CHOICES)


class Login(forms.Form):
    inputUser = forms.EmailInput()
    inputPassword = forms.PasswordInput()

class change_led(forms.Form):
    R = forms.IntegerField(label='R')
    G = forms.IntegerField(label='G')
    B = forms.IntegerField(label='B')
    W = forms.IntegerField(label='W')
    Brig = forms.IntegerField(label='Brig')

class change_led_1(forms.Form):
    R = forms.IntegerField(label='R')
    G = forms.IntegerField(label='G')
    B = forms.IntegerField(label='B')
    W = forms.IntegerField(label='W')
    Brig = forms.IntegerField(label='Brig')
    x = forms.IntegerField(label='x')
    y = forms.IntegerField(label='y')

class dynamic_input(forms.Form):
    timeabrupt = forms.IntegerField(label='timeabrupt')
    fad = forms.CharField(max_length=10, label='fad')
    x = forms.IntegerField(label='x')
    y = forms.IntegerField(label='y')
    a = forms.IntegerField(label='a')
    b = forms.IntegerField(label='b')
    color1c = [('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'),('06', '06 '),('07', '07'),('08', '08'),('09', '09'),('10', '10') ]
    color1 = forms.ChoiceField(choices=color1c, label="color1")
    color2 = forms.ChoiceField(choices=color1c, label="color2")
    color3 = forms.ChoiceField(choices=color1c, label="color3")
    color4 = forms.ChoiceField(choices=color1c, label="color4")

    colorgenc = [('01', '01'), ('02', '02'), ('03', '03')]
    colorgen = forms.ChoiceField(choices=colorgenc, label="colorgen")

    cc = [('01', '01'), ('02', '02'), ('03', '03'), ('04', '04') ]
    c1 = forms.ChoiceField(choices=cc, label="c1")
    c2 = forms.ChoiceField(choices=cc, label="c2")
    c3 = forms.ChoiceField(choices=cc, label="c3")

    actionc = [('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'),('06', '06 '),('07', '07')]
    action = forms.ChoiceField(choices=actionc, label="action")

