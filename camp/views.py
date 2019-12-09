from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm, StudentForm, ParentForm
from .models import Parent, Student, User
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .decorators import *
import os
import io
from camp_reg import settings
from .pdf_generator import PdfGenerate as pdf
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape
from django.http import FileResponse


def welcome(request):
    return render(request, 'camp/welcome.html', {})


def base_signup(request):
    if request.method == 'POST':

        post_values = request.POST.copy()
        user_type = post_values.get('user_type')
        if user_type == 'parent':
            post_values['is_parent'] = True
            post_values['is_staff'] = False
        elif user_type == 'staff':
            post_values['is_parent'] = False
            post_values['is_staff'] = True
        form = UserForm(post_values)

        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user_name, password=password)
            auth_login(request, user)
            return redirect(f'/login?user={user_type}')
        else:
            messages.error(request, form.errors)
    else:
        form = UserForm()
    return render(request, 'camp/base_signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                user_type = request.POST.get('user_type')
                page = None
                if user_type == 'parent':
                    page = '/home'
                elif user_type == 'staff':
                    page = '/list'
                return HttpResponseRedirect(page)
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            messages.error(request, ('Invalid login details given!'))
            return HttpResponseRedirect(request.path_info)

    else:
        user = request.GET.get('user')
        id = "lg"
        if user == "parent" or user == "staff":
            id = ""
        return render(request, 'camp/login.html', {'user': request.GET.get('user'), 'id': id})


@login_required(login_url="/login")
@staff_required
def list(request):
    students = None
    camp = None
    if request.method == "POST":
        all_list = False
        try:
            camp = request.POST.get('camp')
            students = Student.objects.filter(camp=camp).prefetch_related('parent')
            if not students:
                messages.success(request, ('No Students in this camp!'))
                students = None
        except Exception as e:
            messages.error(request, (e.__str__()))
            students = None
        if 'pdf' in request.POST or 'print' in request.POST:

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0)

            _pdf = pdf()
            _pdf.AddLogo()
            _pdf.AddTable(students, camp)

            doc.build(_pdf.story)

            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)

            as_attachment = True
            if 'print' in request.POST:
                as_attachment = False
            return FileResponse(buffer, as_attachment=as_attachment, filename=f'Students_{camp}.pdf')
    else:
        all_list = True

    return render(request, 'camp/list.html', {'students': students, 'camp': camp, 'all_list': all_list})


@login_required(login_url="/login")
@staff_required
def download_all(request):
    camps = []
    students = []
    try:
        students = Student.objects.all()
        camps = students.values_list('camp', flat=True).distinct()
    except Exception as e:
        messages.error(request, (e.__str__()))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0)

    _pdf = pdf()
    _pdf.AddLogo()
    for camp in camps:
        camp_st = students.filter(camp=camp)
        _pdf.AddTable(camp_st, camp)

    doc.build(_pdf.story)

    if 'pdf' in request.POST:
        as_attachment = True
    elif 'print' in request.POST:
        as_attachment = False
    else:
        as_attachment = False

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=as_attachment, filename=f'All Students.pdf')


@login_required(login_url="/login")
@parent_required
def register(request):
    print(request.POST)
    p_id = None
    student = None
    try:
        parent = Parent.objects.get(user=request.user.id)
        p_id = parent.id
    except Exception as e:
        messages.error(request, ('Parent details are missing. Please add your details first.'))

    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['parent'] = p_id
        try:
            st = get_object_or_404(Student, pk=request.POST.get('st_id'))
        except:
            st = None
        form = StudentForm(post_values, request.FILES, instance=st)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, ('Child Details Added Successfully!'))
            except Exception as e:
                print(e.__str__())

            return HttpResponseRedirect('/home')
        else:
            messages.error(request, form.errors)
    else:
        child_id = request.GET.get('child')

        if child_id:
            student = Student.objects.get(pk=child_id)

    return render(request, 'camp/register.html', {'child': student})


@login_required(login_url="/login")
@staff_required
def download_resume(request):
    print(request.POST.get('student_id'))
    if request.method == 'POST':
        try:
            student = Student.objects.select_related('parent').get(pk=request.POST.get('student_id'))
        except:
            student = None
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0)

        _pdf = pdf()
        _pdf.AddLogo()
        _pdf.AddResume(student)
        doc.build(_pdf.story)

        buffer.seek(0)
        as_attachment = False
        if 'pdf' in request.POST:
            as_attachment = True
        return FileResponse(buffer, as_attachment=as_attachment, filename=f'Student_{student.name}.pdf')


@login_required(login_url="/login")
@parent_required
def home(request):
    return render(request, 'camp/home.html', {})


@login_required(login_url="/login")
@parent_required
def parent_details(request):

    try:
        parent = get_object_or_404(Parent, user=request.user.id)
        if parent.user_id != request.user.id:
            return HttpResponseForbidden()
    except:
        parent = None

    post_values = None
    if request.method == 'POST':
        post_values = request.POST.copy()
        post_values['user'] = request.user.id

    form = ParentForm(post_values, instance=parent)

    if request.method == 'POST':

        if form.is_valid():
            try:
                form.save()
                messages.success(request, ('Details Added Successfully!'))
            except Exception as e:
                messages.error(request, (e.__str__()))

            return HttpResponseRedirect('/home')
        else:
            messages.error(request, form.errors)

    return render(request, 'camp/parent_details.html', {'form': form})


@login_required(login_url="/login")
@parent_required
def view(request):
    p_id = None
    try:
        parent = Parent.objects.get(user=request.user.id)
        p_id = parent.id
    except Exception as e:
        messages.error(request, ('No children added!'))

    if request.method == "POST":
        if "edit" in request.POST:
            ch_id = request.POST.get('child')
            st = Student.objects.get(pk=ch_id)
            print(st)
            return HttpResponseRedirect(f'/register?child={st.id}')
        elif "delete" in request.POST:
            ch_id = request.POST.get('child')
            Student.objects.filter(pk=ch_id).delete()

    students = Student.objects.filter(parent=p_id)
    return render(request, 'camp/view.html', {'children': students})


@login_required(login_url="/login")
@parent_required
def edit_student(request):
    return render(request, 'camp/edit_student.html', {})


@login_required(login_url="/login")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url="/login")
def router(request):
    try:
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        if user.is_parent == True and user.is_staff == False:
            page = '/home'
        elif user.is_staff == True and user.is_parent == False:
            page = '/list'
        else:
            logout(request)

        return HttpResponseRedirect(page)
    except Exception as e:
        messages.error(request, '(Something went wrong!)')


@login_required(login_url='/login')
def student(request):
    student = None
    try:
        st_id = request.GET.get('id')
        student = Student.objects.select_related('parent').get(pk=st_id)
    except Exception as e:
        messages.error(request, (e.__str__()))

    try:
        user = User.objects.get(pk=request.user.id)
        if user.is_parent and not user.is_staff:
            type = 'parent'
        elif user.is_staff and not user.is_parent:
            type = 'staff'
        else:
            type = None
    except Exception as e:
        messages.error(request, (e.__str__()))
        type = None

    print(student.parent.user.username)

    return render(request, 'camp/student_resume.html', {'student': student, 'type': type})


def reset(request):
    return render(request, 'camp/reset.html', {})



