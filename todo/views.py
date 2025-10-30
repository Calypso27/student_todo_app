from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    
    tasks = Task.objects.all()

    total= tasks.count()
    pending= tasks.filter(is_completed=False).count()
    completed= tasks.filter(is_completed=True).count()

    context = {
        'tasks': tasks,
        'total': total,
        'pending': pending,
        'completed': completed,
    }

    return render(request, 'todo/task_list.html', context)


def task_detail(request, pk):

    task = get_object_or_404(Task, pk=pk)

    context = {
        'task': task,
    }

    return render(request, 'todo/task_detail.html', context)

@login_required
def task_create(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Tâche "{task.title}" créée avec succès!')
            return redirect('task_list')
    else:
        form = TaskForm()

    context = {
        'form': form,
        'title': 'Créer une nouvelle tâche',
    }

    return render(request, 'todo/task_form.html', context)

@login_required
def task_update(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Tâche "{task.title}" mise à jour avec succès!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
        'title': 'Modifier la tâche',
    }

    return render(request, 'todo/task_form.html', context)

@login_required
def task_delete(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Tâche "{task_title}" supprimée avec succès!')
        return redirect('task_list')

    return redirect('task_detail', pk=pk)


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()

    status_text = "complétée" if task.is_completed else "marquée comme incomplète"
    message = f'Tâche "{task.title}" {status_text}!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_completed': task.is_completed,
            'message': message
        })

    messages.success(request, message)
    return redirect('task_list')



