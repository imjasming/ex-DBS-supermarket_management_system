from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request,'home.html')
class RegistrationForm(forms.Form):
    username = forms.CharField(required=True,max_length=10)
    email = forms.EmailField(required=True,max_length=100)
    password = forms.CharField(min_length=6)
    confirm = forms.CharField(min_length=6)

    def clean_username(self):
        username=self.cleaned_data.get('username')
       
        if username_check(username):
            filter_result = User.objects.filter(username=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("username already taken.")
            return username
        else:
            raise forms.ValidationError("username has illegal characters.")

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("email already taken.")
        else:
            raise forms.ValidationError("enter a valid email address.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("password too short.")
        elif len(password) > 20:
            raise forms.ValidationError("Your password is too long.")

        return password

    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Password mismatch.")
        return confirm
#用户注册方法
def user_register(request):
    Method = request.method
    if Method == 'POST':
        #如果有post提交的动作，就将post中的数据赋值给uf，供该函数使用
        uf = RegistrationForm(request.POST)
        if uf.is_valid():
            # 读取表单值
            username=uf.cleaned_data['username']
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            user = User.objects.create_user(username=username,email=email, password=password)
            return render(request, 'login.html', {'error': 'create success'})
        else:
            return render(request,'register.html',{'error':uf.errors})
    else:
        return render(request, 'register.html', {})

#登录表单
class UserForm(forms.Form):
    email = forms.EmailField(required=True,max_length=100,widget=forms.TextInput(attrs={'type':'text','placeholder':'请输入您的用户名'}))
    password = forms.CharField(min_length=6,widget=forms.TextInput(attrs={'type':'password','placeholder':'请输入您的密码'}))
    def clean_username(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email=email)
            if not filter_result:
                raise forms.ValidationError("email not found.")
        return email

#用户登录
def user_login(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                #成功登录
                login(req, user)
                return redirect('/profile')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
        
            return render(req, 'login.html', {"error": "password is invalid."})
    else:
        return render(req, 'login.html', {})