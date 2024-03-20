from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, TestUpdateForm, TestQuestionInlineFormSet, QuestionForm, QuestionOptionInlineFormSet
from .models import Test, Question, Option, TestResult
from django.utils.text import slugify
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json


@login_required
def test_create(request):
    user_authenticated = request.user.is_authenticated
    context = {'user_authenticated': user_authenticated}
    
    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.author = request.user 
                obj.save()
                return redirect(obj.get_manage_url())
            form.add_error(None, "You must be logged in to create products.")
    else:
        form = TestForm()   
    
    context['form'] = form
    return render(request, 'test/create_test.html', context)

def test_detail(request, slug=None):
    test = get_object_or_404(Test, slug=slug)
    user_authenticated = request.user.is_authenticated
    context = {'test':test, 'user_authenticated':user_authenticated} 
    return render(request, 'test/test_detail.html', context)

def test_list(request):
    user_authenticated = request.user.is_authenticated
    object_list = Test.objects.all()
    return render(request, "test/test_list.html", {"object_list": object_list,'user_authenticated': user_authenticated})


def delete_test(request, slug):
    user_authenticated = request.user.is_authenticated
    test = get_object_or_404(Test, slug=slug)
    if request.method == 'POST':
        test.delete()
        return redirect('home')   
    return render(request, 'test/delete_test.html', {'test': test, 'user_authenticated': user_authenticated})
       
# It manages specific test
@login_required
def test_manage_detail(request, slug=None):
    user_authenticated = request.user.is_authenticated
    test = get_object_or_404(Test, slug=slug) 
    is_manager = test.author == request.user if user_authenticated else False

    if not is_manager:
        return HttpResponseBadRequest()

    context = {"test": test, 'user_authenticated': user_authenticated}

    if request.method == 'POST':
        form = TestUpdateForm(request.POST, request.FILES, instance=test) 

        if form.is_valid() :
            instance = form.save(commit=False)
            instance.save() 
            return redirect(test.get_manage_url())
    else:
        form = TestUpdateForm(instance=test) 

    context['form'] = form 
    context['test'] = test
    context['is_manager'] = is_manager

    return render(request, 'test/manage.html', context)

# It gets test question form
def get_question(request, id=None):
    user_authenticated = request.user.is_authenticated
    question = get_object_or_404(Question, id=id)
    attachments = Option.objects.filter(question=question)
    # is_manager = question.author == request.user if user_authenticated else False
    is_manager = True

    if not is_manager:
        return HttpResponseBadRequest()

    context = {"object": question, 'user_authenticated': user_authenticated}

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        formset = QuestionOptionInlineFormSet(request.POST, request.FILES, queryset=attachments)

        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.save()
            formset.save(commit=False)
            for _form in formset:
                is_delete = _form.cleaned_data.get("DELETE")
                try:
                    attachment_obj = _form.save(commit=False)
                except:
                    attachment_obj = None
                if is_delete:
                    if attachment_obj is not None:
                        if attachment_obj.pk:
                            attachment_obj.delete()
                else:
                    if attachment_obj is not None:
                        attachment_obj.question  = instance
                        attachment_obj.save()
            return HttpResponse("OK", status=200)

    else:
        form = QuestionForm(instance=question)
        formset = QuestionOptionInlineFormSet(queryset=attachments)

    context['form'] = form
    context['formset'] = formset
    context['question_id'] = question.id

    return render(request, 'test/update_question.html', context)

# Updating all the test questions
def update_test_questions(request, slug=None): 
    user_authenticated = request.user.is_authenticated
    test = get_object_or_404(Test, slug=slug)
    is_manager = test.author == request.user if user_authenticated else False

    if not is_manager:
        return HttpResponseBadRequest()
    questions = test.question_set.all()
    question_ids = [question.id for question in questions]
    return render(request, 'test/update_test_questions.html', {'question_ids': question_ids, 'test': test, 'user_authenticated': user_authenticated})

def add_question(request, slug = None):
    if request.method == 'POST':  
        test = get_object_or_404(Test, slug=slug)
        user_authenticated = request.user.is_authenticated
        is_manager = test.author == request.user if user_authenticated else False

        if not is_manager:
            return HttpResponseBadRequest()
        # print("Hiiiiii")
        new_question = Question.objects.create(
            test=test,                          
            text="",     
            marks=0,    
        ) 
        return JsonResponse({'question_id': new_question.id})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_test_data(request, slug):
    try:
        user_authenticated = request.user.is_authenticated
        test = get_object_or_404(Test, slug=slug)
        
        current_time = timezone.now()
        if test.start_time <= current_time <= test.end_time:
            if request.method == "GET":
                data = retrieve_test_data(test)
                return JsonResponse(data)
            else:
                return JsonResponse({"error": "Unsupported HTTP method"})
        else:
            return JsonResponse({"error": "Test is not currently active",'start_time': test.start_time, 'end_time': test.end_time});
    except Test.DoesNotExist:
        return JsonResponse({"error": "Test not found"}, status=404)

def retrieve_test_data(test):
    questions_data = []
    questions = test.question_set.all()

    for question in questions:
        options = [{'id': option.id, 'text': option.text if question.question_type != 'THEORY' else '', 'is_correct': ''} for option in question.option_set.all()]
        questions_data.append({
            'id': question.id,
            'type': question.question_type,
            'text': question.text,
            'marks': question.marks,
            'options': options,
        })

    data = {
        'test_title': test.title,
        'start_time': test.start_time,
        'end_time': test.end_time,
        'questions': questions_data,
    }
    return data

def retrieve_test_necessary_data(test):
    questions_data = []
    questions = test.question_set.all()

    for question in questions:
        options =  [{'id': option.id, 'text': option.text, 'is_correct': option.is_correct}  for option in question.option_set.filter(is_correct=True)]
        questions_data.append({
            'id': question.id,
            'type': question.question_type, 
            'marks': question.marks,
            'options': options,
        })

    data = {
        'test_title': test.title,
        'start_time': test.start_time,
        'end_time': test.end_time,
        'questions': questions_data,
    }
    return data

def give_test(request, slug=None):
    try:
        test = Test.objects.get(slug=slug)
        context = {
            'test_slug': slug,
            'test_title': test.title,
            'start_time': test.start_time,
            'end_time': test.end_time
        }
        context['user_authenticated'] = request.user.is_authenticated
        return render(request, 'test/give_test.html', context)
    except Test.DoesNotExist:
        return JsonResponse({"error": "Test not found"}, status=404)

def submit_test(request, slug=None):
    test = get_object_or_404(Test, slug=slug)
    testData = retrieve_test_necessary_data(test)
    data = json.loads(request.body)
    data = data['responses'];
    # print((testData['questions']))
    # print((data['questions']))
    testQuestions = testData['questions']
    questions = data['questions']
    totalMarks = 0
    marks = 0 
    for i in (0,len(testData['questions'])-1,1):  
        # print(questions[i]) 
        question_marks = testQuestions[i]['marks']
        totalMarks += question_marks
        if testQuestions[i]['type'] == 'MCQ' or testQuestions[i]['type'] == 'MSQ':
            opt = []
            for option in testQuestions[i]['options']:
                opt.append(option['id'])
            # print(opt)
            if len(testQuestions[i]['options']) == len(questions[i]['options']):
                ind = True
                for option in questions[i]['options']:
                    if option['id'] not in opt:
                        ind = False
                        break
                if ind:
                    marks += question_marks
        else :
            text = testQuestions[i]['options'][0]['text']
            if text == questions[i]['options'][0]['text']:
                marks+=question_marks
            # print(text)
    print(marks, totalMarks)
    
    test_result = TestResult(
        user=request.user,  # Assuming user is logged in
        test=test,
        score_obtained=marks,
        total_score=totalMarks,
        submitted_time=timezone.now()  
    )

    test_result.save() 

    return JsonResponse({'message': 'Test submitted successfully','score':marks, 'totalScore':totalMarks})

def view_score(request, slug=None):
    user_authenticated = request.user.is_authenticated
    if user_authenticated:
        user = request.user 
        test = get_object_or_404(Test, slug=slug)    
        test_result = TestResult.objects.filter(user=user, test=test).first()   
        if((test_result)):
            all_result =  TestResult.objects.filter(test=test)
            # print(all_result)     
            context = {'user': user ,'score': test_result.score_obtained, 'total_score': test_result.total_score, 'user_authenticated':user_authenticated, 'all_result':all_result}
            return render(request, 'test/view_score.html', context)
        else:
            all_result =  TestResult.objects.filter(test=test) 
            context = {'user': user , 'user_authenticated':user_authenticated, 'all_result':all_result}
            return render(request, 'test/view_score.html', context)
    else:
        test = get_object_or_404(Test, slug=slug)   
        all_result =  TestResult.objects.filter(test=test) 
        context = { 'user_authenticated':user_authenticated, 'all_result':all_result}
        return render(request, 'test/view_score.html', context)



(
# def test_manage_detail(request, slug=None):
#     user_authenticated = request.user.is_authenticated
#     obj = get_object_or_404(Test, slug=slug)
#     attachments = Question.objects.filter(test=obj)
#     is_manager = False 
#     if request.user.is_authenticated:
#         is_manager = obj.author == request.user
#     context = {"object": obj,'user_authenticated': user_authenticated}
#     if not is_manager:
#         return HttpResponseBadRequest()
#     form = TestUpdateForm(request.POST, request.FILES or None, request.FILES or None, instance=obj)
#     formset = TestQuestionInlineFormSet(request.POST ,request.FILES or None,queryset=attachments)
#     if form.is_valid() and formset.is_valid():
        # instance = form.save(commit=False)
        # instance.save()
        # formset.save(commit=False)
        # for _form in formset:
        #     is_delete = _form.cleaned_data.get("DELETE")
        #     try:
        #         attachment_obj = _form.save(commit=False)
        #     except:
        #         attachment_obj = None
        #     if is_delete:
        #         if attachment_obj is not None:
        #             if attachment_obj.pk:
        #                 attachment_obj.delete()
        #     else:
        #         if attachment_obj is not None:
        #             attachment_obj.test  = instance
        #             attachment_obj.save()
        # return redirect(obj.get_manage_url())
#     context['form'] = form
#     context['formset'] = formset
#     return render(request, 'test/manage.html', context)


# def test_home(request):
#     tests = Test.objects.all()
#     return render(request, 'test_home.html', {'tests': tests}) 

# def create_test(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         slug = slugify(title)   
#         start_time = request.POST['start_time']
#         duration = request.POST['duration']
#         content = request.POST['content']

#         test = Test.objects.create(
#             title=title,
#             slug=slug,
#             author=request.user,
#             start_time=start_time,
#             duration=duration,
#             content=content
#         )
#         # return redirect(test.get_absolute_url())

#         return redirect('add_question', test_id=test.id)
#     return render(request, 'create_test.html')

# def add_question(request, test_id):
#     test = Test.objects.get(id=test_id)
#     if request.method == 'POST':
#         question = Question.objects.create(
#             test=test,                      
#             question_type=request.POST['question_type'],   
#             text=request.POST['text'],     
#             marks=request.POST['marks'],    
#         ) 
#         return redirect('add_question', test_id=test_id)
#     return render(request, 'add_question.html', {'test': test})

# def test_detail(request, slug):
#     test = Test.objects.get(slug=slug)
#     return render(request, 'test_detail.html', {'test': test})

# def edit_test(request, slug):
#     test = get_object_or_404(Test, slug=slug)
#     if request.method == 'POST':
#         form = TestForm(request.POST, instance=test)
#         if form.is_valid():
#             form.save()
#             return redirect('test_detail', slug=slug)
#     else:
#         form = TestForm(instance=test)
#     return render(request, 'edit_test.html', {'form': form, 'test': test})


# def search_test(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')
#         tests = Test.objects.filter(title__icontains=query)
#         return render(request, 'search_test.html', {'tests': tests, 'query': query})
#     return redirect('home')   

)