from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def calculator(request):
    result = ''
    if request.method == "POST":
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        operation = request.POST.get('operation')

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            result = num1 / num2 if num2 != 0 else "Error: Division by Zero"

    return render(request, 'calculator.html', {'result': result})
