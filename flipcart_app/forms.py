from django import forms

# -------------------     1.shop forms    -------------------

class shopregform(forms.Form):
    uname = forms.CharField(max_length=30)
    email = forms.EmailField()
    oname = forms.CharField(max_length=30)
    sname = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    cpassword = forms.CharField(max_length=30)
    pic = forms.FileField()
class shoplogform(forms.Form):
    uname = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
class shopaddform(forms.Form):
    iname = forms.CharField(max_length=30)
    iprice = forms.IntegerField()
    idisc=forms.CharField(max_length=500)
    category = forms.CharField(max_length=50)
    iimage = forms.FileField()
    sid=forms.IntegerField()
    
    
# -------------------     2.user forms    -------------------
class userregform(forms.Form):
    pic = forms.FileField()
    phone = forms.IntegerField()
    
    