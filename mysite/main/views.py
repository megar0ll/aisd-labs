from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import AboutImage
from .forms import ContactForm, AboutImageForm


def home(request):
    return render(request, 'main/home.html')


def about(request):
    images = AboutImage.objects.all()

    if request.method == 'POST':
        form = AboutImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изображение успешно загружено!')
            return redirect('about')
    else:
        form = AboutImageForm()

    return render(request, 'main/about.html', {
        'images': images,
        'form': form
    })


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()

            # Отправка email (для разработки выводится в консоль)
            send_mail(
                f'Новое сообщение от {message.name}',
                message.message,
                message.email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, 'Сообщение успешно отправлено!')
            return redirect('contacts')
    else:
        form = ContactForm()

    return render(request, 'main/contacts.html', {'form': form})