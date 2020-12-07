from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import *

# Create your views here.

def principal(request):
    return render(request,'funcionario.html')
'''
def authentication(request):
    if request.user.is_authenticated:
        return sucessful_login(request)
    elif request.method == 'POST':
        post = request.POST
        username = post.get('usuario', default=None)
        password = post.get('senha', default=None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return sucessful_login(request)
        else:
            return failed_login(request)
    else:
        return failed_login(request)
'''
def sucessful_login(request):
    return redirect('principal')

def failed_login(request):
    return render(request,'login_page.html')



'''
@login_required
@transaction.atomic
def update_funcionario(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        funcionario_form = funcionarioForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and funcionario_form.is_valid():
            user_form.save()
            funcionario_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        funcionario_form = funcionarioForm(instance=request.user.profile)
    return render(request, 'update_funcionario.html', {
        'user_form': user_form,
        'funcionario_form': funcionario_form
    })

from django.contrib.auth.models import User
from rango.models import UserProfile
from rango.models import UserForm, UserProfileForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from tango_with_django_project.settings import MEDIA_ROOT

def register(request):
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
                uform = UserForm(data = request.POST)
                pform = UserProfileForm(data = request.POST)
                if uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        profile = pform.save(commit = False)
                        profile.user = user
                        profile.save()
                        save_file(request.FILES['picture'])
                        registered = True
                else:
                        print uform.errors, pform.errors
        else:
                uform = UserForm()
                pform = UserProfileForm()

        return render_to_response('rango/register.html', {'uform': uform, 'pform': pform, 'registered': registered }, context)


def save_file(file, path=''):
        filename = file._get_name()
        fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb' )
        for chunk in file.chunks():
                fd.write(chunk)
        fd.close()
'''

from .forms import funcionarioForm, UserForm
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm




def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        funcionario_form = funcionarioForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and funcionario_form.is_valid():
            # Save the user's form data to the database.
            usuario = user_form.save()
            
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            usuario.email = user_form.cleaned_data.get('email')
            usuario.username = user_form.cleaned_data.get('username')
            #usuario.set_password(usuario.password)
            usuario.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = funcionario_form.save(commit=False)
            profile.usuario = usuario
            '''
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
               if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            '''
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            print('ooooi')
            return redirect('login')
            #{'user_form': user_form, 'funcionario_form': funcionario_form, 'registered': registered}
            #)
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print('oi')

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        funcionario_form =funcionarioForm()

    # Render the template depending on the context.
    return render(request,
            'register.html',
            {'user_form': user_form, 'funcionario_form': funcionario_form, 'registered': registered}
            )




def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('user')
        print(username)
        password = request.POST.get('senha')
        print(password)

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                #return redirect(register)
                return redirect('register')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.all()
            print(users)
            for userl in users:
                print(userl.get_username(), userl.password)
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login_page.html', {})

