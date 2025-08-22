from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from pauses.models import Pause, Feeling, Need
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
)

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'pauses/dashboard.html', {'user': request.user} )

@login_required
def delete_pause(request, pause_id):
    page = request.GET.get("page")

    if request.method == "POST":
        try:
            pause = get_object_or_404(Pause, pk=pause_id)

            if pause.user != request.user:
                messages.error(request, 'Vous ne pouvez pas supprimer cette pause ❌')
            else:
                pause.delete()
                messages.success(request, 'Pause supprimée avec succès ✅')

        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {e}")

        url = reverse('diary')
        if page:
            url += f"?page={page}"
        return redirect(url)
    
    return HttpResponseForbidden("Suppression impossible via GET ❌")

class PauseListView(LoginRequiredMixin, ListView):
    template_name = 'pauses/diary.html'
    model = Pause
    context_object_name = 'pauses'
    paginate_by = 5

    def get_queryset(self):
        return Pause.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for pause in context["pauses"]:
            pause.feelings_with_labels = [
                f.get_label(self.request.user) for f in pause.feelings.all()
            ]
        return context

class PauseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'pauses/observation.html' 
    model = Pause
    fields = ['empty_your_bag', 'observation']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)  
    
    def get_success_url(self):
        return reverse('feelings', kwargs={'pause_id': self.object.pk})
    
class PauseFeelingUpdateView(LoginRequiredMixin, View):
    template_name = "pauses/feelings.html"
    def get_grouped_feelings(self, user):
        grouped_feelings = {}
        for family_code, family_name in Feeling.FeelingFamily.choices:
            feelings = Feeling.objects.filter(feeling_family=family_code).order_by("id")
            for f in feelings:
                f.label = f.get_label(user)
            grouped_feelings[family_name] = feelings
        return grouped_feelings
    
    def get(self, request, pause_id):
        pause = get_object_or_404(Pause, id=pause_id, user=request.user)
        return render(request, self.template_name, {
            "pause": pause,
            "grouped_feelings": self.get_grouped_feelings(request.user),
        })    

    def post(self, request, pause_id):
        pause = get_object_or_404(Pause, id=pause_id, user=request.user)
        selected_ids = request.POST.getlist('feelings')
        if not selected_ids:  
            return render(request, self.template_name, {
                "pause": pause,
                "grouped_feelings": self.get_grouped_feelings(request.user),
                "error_message": "Sélectionne au moins un sentiment."
            })
        pause.feelings.set(selected_ids)  
        return redirect(reverse_lazy('needs', kwargs={'pause_id': pause.id}))
    
class PauseNeedUpdateView(LoginRequiredMixin, View):
    template_name = "pauses/needs.html"

    def get_grouped_needs(self):
        grouped_needs = {}
        for family_code, family_name in Need.NeedFamily.choices:
            needs = Need.objects.filter(need_family=family_code).order_by("id")
            grouped_needs[family_name] = needs
        return grouped_needs

    def get(self, request, pause_id):
        pause = get_object_or_404(Pause, id=pause_id, user=request.user)
        return render(request, self.template_name, {
            "pause": pause,
            "grouped_needs": self.get_grouped_needs(),
        })    

    def post(self, request, pause_id):
        pause = get_object_or_404(Pause, id=pause_id, user=request.user)
        selected_ids = request.POST.getlist('needs')
        print (selected_ids)
        if not selected_ids:  
            return render(request, self.template_name, {
                "pause": pause,
                "grouped_needs": self.get_grouped_needs(),
                "error_message": "Sélectionne au moins un besoin."
            })
        pause.needs.set(selected_ids)  
        return redirect('diary')