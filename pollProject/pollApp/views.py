import csv
import io

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import UploadCSVForm, AdmissionNumberLoginForm
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
    try:
        voter = Voters.objects.get(user=user)
        if voter.voted_questions.filter(pk=question_id).exists():
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'You have already voted on this question.'
            })
    except Voters.DoesNotExist:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Voter not found.'
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

        # Mark the user as having voted for this question
        voter.voted_questions.add(question)
        voter.save()

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



def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            return render(request, 'polls/upload_csv.html', {
                'error_message': 'The uploaded file is not a CSV file.'
            })

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        for row in csv.reader(io_string, delimiter=',', quotechar="|"):
            admission_no = row[0]
            name = row[1]
            class_name = row[2]

            user = User.objects.create_user(username=admission_no, password=admission_no)
            Voters.objects.create(
                user=user,
                admission_no=admission_no,
                name=name,
                class_name=class_name
            )

        return HttpResponseRedirect(reverse('polls:index'))

    return render(request, 'polls/upload_csv.html')


def admission_login(request):
    if request.method == 'POST':
        form = AdmissionNumberLoginForm(request.POST)
        if form.is_valid():
            admission_no = form.cleaned_data['admission_no']
            user = authenticate(request, admission_no=admission_no)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse("Invalid Admission Number")
    else:
        form = AdmissionNumberLoginForm()
    return render(request, 'polls/admission_login.html', {'form': form})
