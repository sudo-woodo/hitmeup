from django.shortcuts import render


def csrf_failure(request, reason=''):
    return render(request, 'csrf.jinja', {
        'reason': reason
    })
