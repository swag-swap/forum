from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, TestUpdateForm, TestQuestionInlineFormSet
from .models import Test, Question
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponseBadRequest


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


def test_list(request):
    user_authenticated = request.user.is_authenticated
    object_list = Test.objects.all()
    return render(request, "test/test_list.html", {"object_list": object_list,'user_authenticated': user_authenticated})





def test_manage_detail(request, slug=None):
    user_authenticated = request.user.is_authenticated
    obj = get_object_or_404(Test, slug=slug)
    attachments = Question.objects.filter(test=obj)
    is_manager = obj.author == request.user if user_authenticated else False

    if not is_manager:
        return HttpResponseBadRequest()

    context = {"object": obj, 'user_authenticated': user_authenticated}

    if request.method == 'POST':
        form = TestUpdateForm(request.POST, request.FILES, instance=obj)
        formset = TestQuestionInlineFormSet(request.POST, request.FILES, queryset=attachments)

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
                        attachment_obj.test  = instance
                        attachment_obj.save()
            return redirect(obj.get_manage_url())
    else:
        form = TestUpdateForm(instance=obj)
        formset = TestQuestionInlineFormSet(queryset=attachments)

    context['form'] = form
    context['formset'] = formset

    return render(request, 'test/manage.html', context)


def test_detail(request, slug=None): 
    user_authenticated = request.user.is_authenticated 
    obj = get_object_or_404(Test, slug=slug) 
    questions = Question.objects.filter(test=obj) 
    if user_authenticated: 
        can_manage_test = obj.author == request.user 
    context = {
        "object": obj,                   
        "user_authenticated": user_authenticated,   
        "questions": questions,       
        "can_manage_test": can_manage_test   
    } 
    return render(request, 'test/test_detail.html', context)













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

# def delete_test(request, slug):
#     test = get_object_or_404(Test, slug=slug)
#     if request.method == 'POST':
#         test.delete()
#         return redirect('home')   
#     return render(request, 'delete_test.html', {'test': test})

# def search_test(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')
#         tests = Test.objects.filter(title__icontains=query)
#         return render(request, 'search_test.html', {'tests': tests, 'query': query})
#     return redirect('home')   