from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from hs_incidents.forms import HSIncidentForm
from hs_incidents.models import HS_incident, Illness
from django.forms import inlineformset_factory, Select, TextInput
from hs_incidents.models import HS_incident, Injury
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from hs_incidents.simp_functions import create_incident, update_incident


@login_required(login_url='login')
@transaction.atomic
def hs_create_form(request):
    InjuryFormSet = inlineformset_factory(
        HS_incident,
        Injury,
        fields='__all__',
        extra=3,
        widgets={
            'relation_to_business': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
            'severity': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
            'immediate_cause': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
        },
    )
    IllnessFormSet = inlineformset_factory(
        HS_incident,
        Illness,
        fields='__all__',
        extra=3,
        widgets={
            'relation_to_business': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'severity': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'immediate_cause': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'consequence': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'age': TextInput(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'gender': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
        }
    )

    form = HSIncidentForm()
    injury_formset = InjuryFormSet()
    illness_formset = IllnessFormSet()

    if request.method == 'POST':
        form = HSIncidentForm(request.POST)
        injury_formset = InjuryFormSet(request.POST)
        illness_formset = IllnessFormSet(request.POST)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.date_created = timezone.now()
            incident.user = request.user
            incident.save()
            if form.cleaned_data['incident_classification'] == 'Safety' and injury_formset.is_valid():
                for injury_form in injury_formset:
                    if injury_form.cleaned_data != {}:
                        injury = injury_form.save(commit=False)
                        injury.incident = incident
                        injury.save()
            elif form.cleaned_data['incident_classification'] == 'Health' and illness_formset.is_valid():
                for illness_form in illness_formset:
                    if illness_form.cleaned_data != {}:
                        illness = illness_form.save(commit=False)
                        illness.incident = incident
                        illness.save()
            simp_id = create_incident(incident)
            incident.simp_id = simp_id
            incident.save()
            return redirect(reverse('incidents'))

    context = {
        'form': form,
        'injury_formset': injury_formset,
        'illness_formset': illness_formset,
    }

    return render(request, "hs_create_form.html", context)


@login_required(login_url='login')
def hs_edit_form(request, *args, **kwargs):
    InjuryFormSet = inlineformset_factory(
        HS_incident,
        Injury,
        fields='__all__',
        extra=3,
        widgets={
            'relation_to_business': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
            'severity': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
            'immediate_cause': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 200px;'}),
        },
    )
    IllnessFormSet = inlineformset_factory(
        HS_incident,
        Illness,
        fields='__all__',
        extra=3,
        widgets={
            'relation_to_business': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'severity': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'immediate_cause': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'consequence': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'age': TextInput(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
            'gender': Select(attrs={'class': 'rui-combobox__control', 'style': 'width: 300px;'}),
        }
    )

    incident = HS_incident.objects.get(pk=kwargs['id'])
    creation_date = incident.date_created
    form = HSIncidentForm(instance=incident)
    injury_formset = InjuryFormSet(instance=incident)
    illness_formset = IllnessFormSet(instance=incident)

    if request.method == 'POST':
        form = HSIncidentForm(request.POST, instance=incident)
        injury_formset = InjuryFormSet(request.POST, instance=incident)
        illness_formset = IllnessFormSet(request.POST, instance=incident)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.date_created = creation_date
            incident.user = request.user
            incident.save()
            if form.cleaned_data['incident_classification'] == 'Safety' and injury_formset.is_valid():
                for injury_form in injury_formset:
                    if injury_form.cleaned_data != {}:
                        injury_form.save()
            elif form.cleaned_data['incident_classification'] == 'Health' and illness_formset.is_valid():
                for illness_form in illness_formset:
                    if illness_form.cleaned_data != {}:
                        illness_form.save()
            # update_incident(incident)
            return redirect(reverse('incidents'))

    context = {
        'incident': incident,
        'form': form,
        'injury_formset': injury_formset,
        'illness_formset': illness_formset,
    }

    return render(request, "hs_edit_form.html", context)


@login_required(login_url='login')
def incidents(request):
    incidents = HS_incident.objects.filter(user=request.user.id)
    context = {
        'incidents': incidents,
    }

    return render(request, 'main_page.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'jti.trvlscrt@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form": password_reset_form})
