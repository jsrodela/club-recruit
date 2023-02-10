from django.shortcuts import render, redirect

from account.base import get_data
from .form_data import form_data
from .models import FormModel


def form(request, clubname):
    data = get_data(request)
    data['form_data'] = form_data

    if request.POST:
        submit = []
        user_id = data['user'].id

        print(request.POST)

        submit_data = dict(request.POST)

        for key in submit_data:

            print(key)

            if key == 'csrfmiddlewaretoken':  # ignore csrf token
                continue

            answer = submit_data[key]  # ["answer"]
            print('answer is ', answer)
            if len(answer) == 1:
                print(answer, 'is', answer[0])
                answer = answer[0]  # "answer"

            submit.append({
                "question": key,
                "answer": answer
            })

        print(submit)
        FormModel(number=user_id, club=clubname, section=submit).save()
        return redirect('/')

    return render(request, 'form/form.html', data)


def example_form(request):
    data = get_data(request)
    data['form_data'] = form_data
    return render(request, 'form/example_form.html', data)
