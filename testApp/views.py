from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, TestUpdateForm, TestQuestionInlineFormSet
from .models import Test, Question
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponseBadRequest



def test_create(request):
    context = {}
    form = TestForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.author = request.user 
            obj.save()
            return redirect(obj.get_manage_url())
        form.add_error(None, "Your must be logged in to create products.")
    context['form'] = form
    return render(request, 'create_test.html', context)

def test_list(request):
    object_list = Test.objects.all()
    return render(request, "test_list.html", {"object_list": object_list})



def test_manage_detail(request, slug=None):
    obj = get_object_or_404(Test, slug=slug)
    attachments = Question.objects.filter(test=obj)
    is_manager = False 
    if request.user.is_authenticated:
        is_manager = obj.author == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = TestUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = TestQuestionInlineFormSet(request.POST or None,  request.FILES or None,queryset=attachments)
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
    context['form'] = form
    context['formset'] = formset
    return render(request, 'manage.html', context)

def test_detail(request, slug=None):
    obj = get_object_or_404(Test, slug=slug) 
    if request.user.is_authenticated:
        temp = True # to do
    context = {"object": obj}
    return render(request, './test_detail.html', context)

# def product_attachment_download_view(request, handle=None, pk=None):
#     attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
#     can_download = attachment.is_free or False
#     if request.user.is_authenticated and can_download is False:
#         can_download = request.user.purchase_set.all().filter(product=attachment.product, completed=True).exists()
#     if can_download is False:
#         return HttpResponseBadRequest()
#     file_name = attachment.file.name # .open(mode='rb') # cdn -> S3 object storage
#     file_url = generate_presigned_url(file_name)
#     # filename = attachment.file.name
#     # content_type, _ = mimetypes.guess_type(filename)
#     # response =  FileResponse(file)
#     # response['Content-Type'] = content_type or 'application/octet-stream'
#     # response['Content-Disposition'] = f'attachment;filename={filename}'
#     return HttpResponseRedirect(file_url)




















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
