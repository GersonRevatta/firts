from django import forms
from .models import  usuario
       
  
class FormularioRegistro(forms.ModelForm):
	
	class Meta:
		model = usuario
		fields = ['username','password','email','first_name','last_name','dni','gender']    
		widgets = {
			'password':forms.TextInput(attrs = {'type':'password','placeholder': 'Password','pattern':'[a-zA-Z0-9/ñ]{7,32}','class':'form-control','id':'pass'}),
            'username' : forms.TextInput(attrs = {'placeholder': 'Username','pattern':'[a-zA-Z0-9]{3,32}','class':'form-control','id':'usuario'}),
            'email'    : forms.EmailInput(attrs = {'placeholder': 'E-Mail','pattern':'[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{1,5}','class':'form-control','id':'gmail'}),
            'first_name':forms.TextInput(attrs = {'placeholder': 'Nombre','pattern':'[a-zA-Z0-9]{3,32}','class':'form-control','id':'nombre'}),
            'last_name':forms.TextInput(attrs = {'placeholder': 'Apellidos','pattern':'[a-zA-Z0-9]{3,32}','class':'form-control','id':'apellido'}),
            'dni':forms.TextInput(attrs = {'placeholder': 'DNI','pattern':'[0-9]{8,9}','class':'form-control','id':'dni'}),
            #'max':'99999999','min':'9999999'
		}#,'oninvalid':'this.setCustomValidity("Ingrese solo 8 caracteres ")'
#,'oninvalid':'this.setCustomValidity("Ingrese una contraseña mayor a 7 caracteres")'  (?=.*\d)(?=.*[a-z])(?=.*[A-Z]) 

	def save(self, commit=True):
		user = super(FormularioRegistro, self).save(commit=False)
		if commit:
			user.is_active = False # No está activo hasta que active el vínculo de verificación
			user.save()	
		return user   

'''
YESNO = (
    ('Yes','Yes'),
    ('No', 'No'),


    aria-describedby="sizing-addon1"
)'''
class FormularioContacto(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre','class':'form-control'}))
	correo = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email','class':'form-control'}))
	mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Mensaje a enviar','class':'form-control','rows':'5','id':'MensajeContent'}))
	#this is test																		style="height: 45px;"
	#like = forms.ChoiceField(widget=forms.RadioSelect, choices=YESNO)
'''	
	correo = forms.EmailField()
	mensaje = forms.CharField()
'''

