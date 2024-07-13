import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import UploadCSVForm
from .models import Question, Choice, Voters

# Get questions and display those questions
@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show question and choices
@login_required
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html', {'question': question})

# Get question and display results
@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Vote for a question choice
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    # Check if the user has already voted for this question
    if Choice.objects.filter(question=question, voted_users=user).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You have already voted.'
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.voted_users.add(user)  # Add the user to the voted_users field
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def results_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST' and 'reset_votes' in request.POST:
        for choice in question.choice_set.all():
            choice.votes = 0
            choice.save()
        return HttpResponseRedirect(reverse('polls:results_detail', args=(question.id,)))
    return render(request, 'polls/result_detail.html', {'question': question})


class Voter:
    pass


@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=',')
            next(reader)  # Skip the header row
            for row in reader:
                admission_no = row[0]
                name = row[1]
                class_name = row[2]
                has_voted = row[3].lower() == 'true'
                voter_instance, created = Voters.objects.update_or_create(
                    admission_no=admission_no,
                    defaults={'name': name, 'class_name': class_name, 'has_voted': has_voted}
                )
            return redirect('polls:upload_csv')
    else:
        form = UploadCSVForm()
    return render(request, 'polls/upload_csv.html', {'form': form})
