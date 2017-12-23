from django import forms
from django.forms import ModelForm, formset_factory
from .models import Choice, Question, QuestionPaper, Submission
from django.forms import formsets, BaseFormSet
from django.core.exceptions import ValidationError



from django import forms

class QuestionPaperForm(ModelForm):
    class Meta:
        model = QuestionPaper
        fields = [ 'title' ]

    def __init__(self, *args, **kwargs):

        questions = kwargs.pop('questions')
        self.questions = questions

        super(QuestionPaperForm, self).__init__(*args, **kwargs)
        if self.questions:
            self.fields['questions'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=[(q.id, q.text ) for q in self.questions]
        )




class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['text', 'is_answer']

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(ChoiceForm, self).__init__(*args, **kwargs)

    def clean_text(self):
        text = self.cleaned_data['text']
        print text.strip()
        if not text.strip():

            raise ValidationError("Can't leave it blank.")
        return text
    def clean_is_answer(self):
        is_answer = self.cleaned_data['is_answer']
        return is_answer

class ChoicesForm(forms.Form):


    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        self.repetitions= kwargs.pop('repetitions')
        super(ChoicesForm, self).__init__(*args, **kwargs)
        for i in range(1,self.repetitions+1):
            self.fields['choice_%d' % i] = forms.CharField(max_length=200)
            self.fields['is_answer_%d' % i] = forms.BooleanField(required=False)

    def save(self):
        print self.question
        data = self.cleaned_data
        li = []
        for i in range(1, 5):
            li.append(Choice(text=data['choice_%d' % i], is_answer=data['is_answer_%d' % i], question=self.question))
        Choice.objects.bulk_create(li)




class BaseChoiceFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        print "form_cleaned"
        for form in self.extra_forms:
            if form.has_changed():
                return
        raise forms.ValidationError("All Choices Required.")

        texts = []
        for form in self.forms:
            text = form.cleaned_data['text']
            if text in texts:
                raise forms.ValidationError("Choices in a set must have distict choice.")

            texts.append(text)

        if len(texts) is not 4:
           raise forms.ValidationError("Insufficient choices.")




class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = [ 'question_paper', 'choices']



class AnswerForm(forms.Form):
    pass

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        self.question = question
        print question
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=[(c.id, c.text) for c in self.question.choices.all()]
        )




#learning forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class BaseChoiceFormSet(BaseFormSet):
    pass



