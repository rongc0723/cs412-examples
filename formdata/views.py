from django.shortcuts import render, redirect

# Create your views here.

def show_form(request):
    return render(request, 'formdata/form.html')

def submit(request):
    '''
    Handle the form submission.
    Read out the form data.
    Generate a response.
    '''
    template_name = 'formdata/confirmation.html'
    # read the form data into python variables:
    if request.POST:
        name = request.POST.get('name', 'no name')
        favorite_color = request.POST.get('color', 'no color')
        context = {
            'name': name,
            'favorite_color': favorite_color
        }
        return render(request, template_name, context)
    return redirect('show_form')
    

