from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm
from .models import Test

def test_home(request):
    tests = Test.objects.all()
    return render(request, 'test_home.html', {'tests': tests})

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        print(form)
        if form.is_valid():
            test = form.save(commit=False)
            test.slug = Test.create_unique_slug(test)
            test.author = request.user  
            test.save()
            return redirect('test_detail', slug=test.slug)
    else:
        form = TestForm() 
    return render(request, 'create_test.html', {'form': form})

def test_detail(request, slug):
    test = get_object_or_404(Test, slug=slug)
    return render(request, 'test_detail.html', {'test': test})

def edit_test(request, slug):
    test = get_object_or_404(Test, slug=slug)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('test_detail', slug=slug)
    else:
        form = TestForm(instance=test)
    return render(request, 'edit_test.html', {'form': form, 'test': test})

def delete_test(request, slug):
    test = get_object_or_404(Test, slug=slug)
    if request.method == 'POST':
        test.delete()
        return redirect('home')   
    return render(request, 'delete_test.html', {'test': test})

def search_test(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        tests = Test.objects.filter(title__icontains=query)
        return render(request, 'search_test.html', {'tests': tests, 'query': query})
    return redirect('home')   
