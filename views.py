from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

tasks = []

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    #priority = forms.IntegerField(label = "Priority", min_value = 1, max_value=5)
# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    tasks = [(index, task) for index, task in enumerate(request.session["tasks"])]

    if request.method == "POST":
        if "task_id" in request.POST:
            task_id = int(request.POST["task_id"])
            if 0 <= task_id < len(request.session["tasks"]):
                del request.session["tasks"][task_id]
                request.session.modified = True  # Save the modified session

    return render(request, "tasks/index.html", {
        "tasks": tasks
    })



def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html",{
        "form": NewTaskForm()
    })