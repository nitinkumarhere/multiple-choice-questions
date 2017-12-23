# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from .models import Question, Choice, QuestionPaper, Candidate, Submission
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AnswerForm, QuestionPaperForm, QuestionForm, ChoiceForm, ContactForm, BaseChoiceFormSet, ChoicesForm
from django.forms import formset_factory
from django.core.urlresolvers import reverse

# Create your views here.


@login_required(login_url="/login/")
def index(request):
    """Finds all question papers"""
    papers = QuestionPaper.objects.all()
    return render(
        request, 'mcq/index.html', {
            'papers': papers
    })



@login_required(login_url="/login/")
def check(request, paper_pk):
    # import pdb;pdb.set_trace()
    paper = get_object_or_404(QuestionPaper, pk=paper_pk)

    submission, created = Submission.objects.get_or_create(
        candidate = request.user.candidate,
        question_paper = paper
    )
    submission.choices.clear()
    for c in request.POST.getlist('choices'):
    #     print c
        submission.choices.add(Choice.objects.get(id=int(c)))
        # print "  ...  " , Choice.objects.get(id=int(c))
    submission.save()
    # print "submitted choices : ", submission.choices.all()

    correctly_answered = {}
    for question in paper.questions.all():
        # print "submitted chioce:", set(submission.choices.filter(question=question))
        correct_choices = [c for c in question.choices.all() if c.is_answer]
        if set(correct_choices) == set(submission.choices.filter(question=question)):
            correctly_answered[question.id] = True
        else:
            correctly_answered[question.id] = False

    submission_choices = submission.choices.all()

    qforms = []
    for question in paper.questions.all():
        qforms.append(AnswerForm(question=question))
    # print correctly_answered

    return render(request, 'mcq/check.html', {
        'paper': paper,
        'question_forms': qforms,
        'correctly_answered': correctly_answered,
        'submission_choices': submission_choices,
    })


def thanks(request):
    return render(request, 'mcq/thanks.html', {'thanks': 'thanks', })

#-----------------------------------------------------------------------------------

@login_required(login_url='/login/')
def create_paper(request):
    questions = Question.objects.all()
    print questions

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST, questions=questions)
        print request.POST
        if form.is_valid():
            paper = form.save()

            for q in request.POST.getlist('questions'):
                paper.questions.add(Question.objects.get(id=int(q)))
            paper.save()
            return HttpResponseRedirect('/mcq/thanks/')

    else:
        form = QuestionPaperForm(questions=questions)


    return render(request, 'mcq/create-paper.html', {'form':form})


@login_required(login_url='/login/')
def create_question(request):

    if request.method == 'POST':
        print request.POST
        #ChoiceFormSet = formset_factory(ChoiceForm, extra=4, formset=BaseChoiceFormSet)

        qform = QuestionForm(request.POST)
        if qform.is_valid():
            question = qform.save()
            cform = ChoicesForm(request.POST, question= question, repetitions=4)
            #formset = ChoiceFormSet(request.POST, form_kwargs={'question': question})

            if cform.is_valid():
                cform.save()


                #for form in cform:
                    #c = form.save(commit=False)
                    #c.question = question
                    #c.save()

                return HttpResponseRedirect('/mcq/thanks/')



    else:
        #ChoiceFormSet = formset_factory(ChoiceForm, extra=4, formset=BaseChoiceFormSet)
        qform = QuestionForm()
        #formset = ChoiceFormSet(form_kwargs={'question': 'question'})
        cform = ChoicesForm( question= 'question', repetitions=4)

    return render(request, 'mcq/create-question.html', {
        'cform': cform,
        'qform': qform,
    })




@login_required(login_url="/login")
def edit_question(request, question_pk):

    if request.method == 'POST':
        ChoiceFormSet = formset_factory(ChoiceForm)
        question= Question.objects.get(pk=question_pk)
        qform = QuestionForm(request.POST, instance=Question.objects.get(pk=question_pk))
        if qform.is_valid():
            question = qform.save()

            formset = ChoiceFormSet(request.POST, form_kwargs={'question': 'question'})
            if formset.is_valid():
                for cform in formset.forms:
                    c = cform.save(commit=False)
                    c.question = question
                    c.save()

                print "thanks"
                return HttpResponseRedirect('/mcq/thanks/')

    else:
        ChoiceFormSet = formset_factory(ChoiceForm)
        question = Question.objects.get(pk=question_pk)
        choiceset = Choice.objects.filter(question=question)
        initial_data = []
        for choice in choiceset:
            initial_data.append({'text': choice.text,
                                 'is_answer': choice.is_answer})
        qform = QuestionForm(instance=question)
        formset = ChoiceFormSet(form_kwargs={'question': 'question'},
                                initial=initial_data)

    return render(request, 'mcq/edit-question.html', {
        'formset': formset,
        'qform': qform,
        'question': question
    })

@login_required(login_url="/login")
def delete_question(request, question_pk):
    Question.objects.filter(id=question_pk).delete()
    questions = Question.objects.all()
    print questions

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST, questions=questions)
        print request.POST
        if form.is_valid():
            paper = form.save()

            for q in request.POST.getlist('questions'):
                paper.questions.add(Question.objects.get(id=int(q)))
            paper.save()
            return HttpResponseRedirect('/mcq/thanks/')

    else:
        form = QuestionPaperForm(questions=questions)

    return render(request, 'mcq/create-paper.html', {'form': form})

@login_required(login_url="/login")
def delete_paper(request, paper_pk):
    QuestionPaper.objects.filter(id=paper_pk).delete()
    papers = QuestionPaper.objects.all()

    return render(request, 'mcq/index.html', {'papers':papers})






@login_required(login_url="/login")
def paper(request, paper_pk):
    """Presents requested question paper by key"""
    paper = QuestionPaper.objects.get(pk=paper_pk)

    qforms = []
    for question in paper.questions.all():
        qforms.append(AnswerForm(question=question))

    return render(request, 'mcq/paper.html', {
        'paper': paper,
        'question_forms': qforms
    })


#learning forms

from django.core.mail import send_mail


def send_mails(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['nitinkumarbnk@gmail.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()
        return render(request, 'mcq/send-mails.html', {'form':form })