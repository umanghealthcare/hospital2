from django.shortcuts import render,redirect
from .models import User,Contact,Doctor_profile,Appointment,cancelappointment,doctorcancelappointment,Healthprofile
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def initiate_payment(request,pk):
	patient=Appointment.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	print(user)
	try:
		amount = int(request.POST['amount'])
	except:
		return render(request, 'myappointment.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = Transaction.objects.create(made_by=user, amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY

	params = (
		('MID', settings.PAYTM_MERCHANT_ID),
		('ORDER_ID', str(transaction.order_id)),
		('CUST_ID', str('usahu3589@gmail.com')),
		('TXN_AMOUNT', str(transaction.amount)),
		('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
		('WEBSITE', settings.PAYTM_WEBSITE),
		# ('EMAIL', request.user.email),
		# ('MOBILE_N0', '9911223388'),
		('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
		('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
		# ('PAYMENT_MODE_ONLY', 'NO'),
	)

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()
	patient.fees_status="paid"
	patient.save()
	paytm_params['CHECKSUMHASH'] = checksum
	print('SENT: ', checksum)
	if 	patient.fees_status=="paid":
 
		try:
			user=patient.patient.email
			fname=patient.patient.fname
			lname=patient.patient.lname
			time=patient.time
			date=patient.date
			fees=patient.doctor.doctor_fee
			de=patient.doctor.doctor.email
			dfname=patient.doctor.doctor.fname
			dlname=patient.doctor.doctor.lname
			dname=patient.doctor.doctor_speciality
			print(user)
			print(de)
			subject = 'Your appointments book  with  doctor '
			message = 'Appointments with  doctor '+str(dfname)+' '+str(dlname)+'\n Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)+''+'\n You have paid Rs'+ str(fees)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
			pass	
	return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		received_data = dict(request.POST)
		paytm_params = {}
		paytm_checksum = received_data['CHECKSUMHASH'][0]
		for key, value in received_data.items():
			if key == 'CHECKSUMHASH':
				paytm_checksum = value[0]
			else:
				paytm_params[key] = str(value[0])
		# Verify checksum
		is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
		if is_valid_checksum:
			received_data['message'] = "Checksum Matched"
		else:
			received_data['message'] = "Checksum Mismatched"
			return render(request, 'callback.html', context=received_data)
		return render(request, 'callback.html', context=received_data)



def index(request):
	return render(request,'index.html')

def doctor(request):
	doctor=Doctor_profile.objects.all()
	return render(request,'doctor.html',{'doctor':doctor})
def contact(request):
	if  request.method=='POST':
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			phone=request.POST['phone'],
			topic=request.POST['topic'],
			message=request.POST['message']
			)
		msg='contact save successfuly'
		contact=Contact.objects.all().order_by('-id')[:5]
		return  render(request,'contact.html',{'msg':msg,'contact':contact})
	else:
		contact=Contact.objects.all().order_by('-id')[:5]
		return render(request,'contact.html',{'contact':contact})
def appoinment(request):
	return render(request,'appoinment.html')
def confirmation(request):
	return render(request,'confirmation.html')
def service(request):
	return render(request,'service.html')
def doctor_single(request,pk):
	doctor=Doctor_profile.objects.get(pk=pk)
	return render(request,'doctor-single.html',{'doctor':doctor})
def header(request):
	return render(request,'header.html')
def about(request):
	return render(request,'about.html')

def signup(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			msg='email  is already registered'
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					phone=request.POST['phone'],
					address=request.POST['address'],
					profile_pic=request.FILES['profile_pic'],
					password=request.POST['password'],
					)
				msg='Signup successfuly'
				return render(request,'login.html',{'msg':msg})
			else:
				msg='password  and confirm password doesnot match'
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')
def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'],
					password=request.POST['password'])
			if user.usertype=='patient':
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				appointments=Appointment.objects.filter(patient=user,status='pendding')
				request.session['appointment_count']=len(appointments)
				return redirect('index')

			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				return redirect('doctor_index')
		except Exception as e:
			print(e)
			msg='email  id and password does not match'
			return render(request,'login.html',{'msg':msg})

	else:
		return render(request,'login.html')
def logout(request):
	try:		
		del request.session['email']
		del request.session['fname']
		del request.session['profile']
		return redirect('login')
	except Exception as e:
		print(e)
		return redirect('login')

def user_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.address=request.POST['address']
		user.phone=request.POST['phone']
		user.save()
		

		msg='user upadate successfuly'
		return render(request,'user_profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'user_profile.html',{'user':user})
def change_pass(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password== request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect(logout)
			else:
				msg='New password and confirm password does not match'
				return render(request,'change_pass.html',{'msg':msg})
		else:
			msg='old password does not match'
			return  render(request,'change_pass.html',{'msg':msg})
		return render(request,'change_pass.html',{'user':user})
	else:	

		return render(request,'change_pass.html')

def doctor_index(request):
	return render(request,'doctor_index.html')
	
def doctor_header(request):
	return render(request,'doctor_header.html')

def doctor_persional_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		if user.fname:
			user.fname=request.POST['fname']
			user.lname=request.POST['lname']
			user.email=request.POST['email']
			user.address=request.POST['address']
			user.phone=request.POST['phone']
			try:
				user.profile_pic=request.FILES['profile_pic']
			except Exception as e:
				print(e)
				pass
			user.save()
			return redirect('doctor_index')
		else:
			return redirect('doctor_index')
	else:
		return render(request,'doctor_persional_profile.html',{'user':user})


def doctor_office_details(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_profile=Doctor_profile()
	try:
		doctor_profile=Doctor_profile.objects.get(doctor=doctor)
	except Exception as e:
		print(e)
		pass
	if request.method=='POST':
		if doctor_profile.doctor_speciality:
			doctor_profile.doctor=doctor
			doctor_profile.doctor_deegre=request.POST['doctor_deegre']
			doctor_profile.doctor_speciality=request.POST['doctor_speciality']
			doctor_profile.doctor_fee=request.POST['doctor_fee']
			doctor_profile.doctor_start_time=request.POST['doctor_start_time']
			doctor_profile.doctor_end_time=request.POST['doctor_end_time']
			doctor_profile.doctor_address=request.POST['doctor_address']
			doctor_profile.save()
			msg='Doctor upadate successfuly'
			return render(request,'doctor_office_details.html',{'doctor_profile':doctor_profile,"msg":msg})
		else:
			doctor_profile=Doctor_profile.objects.create(
				doctor=doctor,
				doctor_deegre=request.POST['doctor_deegre'],
				doctor_speciality=request.POST['doctor_speciality'],
				doctor_fee=request.POST['doctor_fee'],
				doctor_start_time=request.POST['doctor_start_time'],
				doctor_end_time=request.POST['doctor_end_time'],
				doctor_address=request.POST['doctor_address']

				)
			msg='Doctor upadate '
			return render(request,'doctor_office_details.html',{'doctor_profile':doctor_profile,"msg":msg})
	else:
		return render(request,'doctor_office_details.html',{'doctor_profile':doctor_profile})
def doctor_change_pass(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password== request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect(logout)
			else:
				msg='New password and confirm password does not match'
				return render(request,'doctor_change_pass.html',{'msg':msg})
		else:
			msg='old password does not match'
			return  render(request,'doctor_change_pass.html',{'msg':msg})
	else:	

		return render(request,'doctor_change_pass.html')


def makeappointment(request,pk):
	doctor=Doctor_profile.objects.get(pk=pk)
	patient=User.objects.get(email=request.session['email'])
	if request.method=='POST':
			Appointment.objects.create(
					doctor=doctor,
					patient=patient,
					time=request.POST['time'],
					date=request.POST['date'],
					issue=request.POST['issue'],
				)
			appointments=Appointment.objects.filter(patient=patient)
			appointments1=Appointment.objects.filter(patient=patient,status='pendding')
			request.session['appointment_count']=len(appointments1)
			return redirect('myappointment')
	else:
		return render(request,'makeappointment.html',{'doctor':doctor,'patient':patient})
def myappointment(request):
	patient=User.objects.get(email=request.session['email'])
	appointments=Appointment.objects.filter(patient=patient)
	appointments1=Appointment.objects.filter(patient=patient,status='pendding')
	request.session['appointment_count']=len(appointments1)
	return render(request,'myappointment.html',{'appointments':appointments})


def doctor_appointment(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_id=Doctor_profile.objects.get(doctor=doctor)
	appointments=Appointment.objects.filter(doctor_id=doctor_id)		
	return render(request,'doctor_appointment.html',{'appointments':appointments})

def patient_appointments_cancel(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		cancelappointment.objects.create(
			appointments=appointments,
			cancel_issue=request.POST['cancel_issue'],
			)
		appointments.status='cancel by patient'
		appointments.save()
		return redirect('myappointment')
	else:
		return render(request,'patient_appointments_cancel.html',{'appointments':appointments})


def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)
def appcept_request(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		appointments.status='accepted'
		appointments.save()
		return redirect('doctor_appointment')
	else:
		return render(request,'doctor_appointment_cancel.html')

def doctor_appointment_cancel(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		doctorcancelappointment.objects.create(
			appointments=appointments,
			issue=request.POST['issue'],
			)
		appointments.status="canceled by doctor"
		appointments.save()
		return redirect('doctor_appointment')
	else:
		return render(request,'doctor_appointment_cancel.html',{'appointments':appointments})

def health_profile(request):
	patient_report=Healthprofile()
	patient=User.objects.get(email=request.session['email'])
	try:
		patient_report=Healthprofile.objects.get(patient=patient)
	except Exception as e:
		print(e)
		pass
	if request.method=='POST':
		if patient_report.blood_pressuer:
			patient_report.patient=patient
			if request.POST['diabetes']=='yes':
				flags1=True
			else:
				flags1=False
			if request.POST['blood_pressuer']=='yes':
				flags2=True
			else:
				flags2=False
			patient_report.blood_group=request.POST['blood_group']
			patient_report.weights=request.POST['weights']
			patient_report.allergy=request.POST['allergy']
			patient_report.blood_pressuer=flags2
			patient_report.diabetes=flags1

			patient_report.save()
			msg='update successfuly'
			return render(request,'health_profile.html',{'msg':msg,'patient_report':patient_report})

		else:
			diabetes=request.POST['diabetes']
			if diabetes =='yes':
				flags1=True
			else:
				flags1=False
			blood_pressuer=request.POST['blood_pressuer']	
			if blood_pressuer =='yes':
				flags2=True
			else:
				flags2=False
			patient_report=Healthprofile.objects.create(
				patient=patient,
				blood_group=request.POST['blood_group'],
				blood_pressuer=flags2,
				diabetes=flags1,
				weights=request.POST['weights'],
				allergy=request.POST['allergy'],

				)
			msg='health profile update successfuly'
			return render(request,'health_profile.html',{'patient_report':patient_report})
	else:	
		return render(request,'health_profile.html',{'patient_report':patient_report})

def doctor_patient_report(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	patient=appointments.patient
	patient_report=Healthprofile.objects.get(patient=patient)
	return render(request,'doctor_patient_report.html',{'patient_report':patient_report})

def prescription_by_doctor(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	if request.method=='POST':
		appointments.prescription=request.POST['prescription']
		appointments.status='complated'
		appointments.save()
		try:
			user=appointments.patient.email
			fname=appointments.patient.fname
			lname=appointments.patient.lname
			de=appointments.doctor.doctor.email
			dfname=appointments.doctor.doctor.fname
			dlname=appointments.doctor.doctor.lname
			dname=appointments.doctor.doctor_speciality
			prescription=appointments.prescription
			print(user)
			print(de)
			subject = 'Your appointments book  with  doctor '
			message = 'Appointments with  doctor '+str(dfname)+' '+str(dlname)+'complated'+'\n Speciality In '+str(dname)+'\n At time '+str(time)+'\n '+"patient Details:"+str(fname)+' '+str(lname)+''+'\n You have paid Rs'+ str(fees)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user]
			send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			print(e)
			pass	
		return redirect('doctor_appointment')
	else:
		return render(request,'prescription_by_doctor.html',{'appointments':appointments})

def prescription_by_doctor_patient(request,pk):
	appointments=Appointment.objects.get(pk=pk)
	return render(request,'prescription_by_doctor_patient.html',{'appointments':appointments})

def print_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	patient=appointment.patient
	patient_report=Healthprofile.objects.filter(patient=patient)
	return render(request,'print_appointment.html',{'appointment':appointment,'patient_report':patient_report})

 

def project(request):
	return render(request,'project.html')