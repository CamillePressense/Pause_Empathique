from user_agents import parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseForbidden
from pauses.models import Pause, Feeling, Need
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView


@login_required
def dashboard(request):
    user_pauses = Pause.objects.filter(user=request.user).order_by("-updated_at")

    paginator = Paginator(user_pauses, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for pause in page_obj:
        pause.feelings_with_labels = [
            f.get_label(request.user) for f in pause.feelings.all()
        ]

    context = {
        "user": request.user,
        "pauses": page_obj,
        "page_obj": page_obj,
    }
    return render(request, "pauses/dashboard.html", context)


@login_required
def delete_pause(request, pk):
    try:
        page = max(1, int(request.GET.get("page", 1)))
    except ValueError:
        page = 1

    if request.method == "POST":
        user_agent = parse(request.META.get("HTTP_USER_AGENT", ""))
        try:
            pause = get_object_or_404(Pause, pk=pk, user=request.user)
            pause.delete()
            messages.success(request, "Pause supprimée avec succès ✅")

            user_pauses = Pause.objects.filter(user=request.user)
            paginator = Paginator(user_pauses, 5)
            if page > paginator.num_pages and paginator.num_pages > 0:
                page = paginator.num_pages

            if user_agent.is_mobile:
                return redirect("diary")
            else:
                return redirect(f"{reverse('dashboard')}?page={page}")

        except Http404:
            messages.error(
                request, "Cette pause n'existe pas ou ne vous appartient pas ❌"
            )
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {e}")

        return redirect(f"{reverse('diary')}?page={page}")

    return HttpResponseForbidden("Suppression impossible via GET ❌")


class PauseListView(LoginRequiredMixin, ListView):
    template_name = "pauses/diary.html"
    model = Pause
    context_object_name = "pauses"
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


class PauseDetailView(LoginRequiredMixin, DetailView):
    model = Pause
    template_name = "pauses/pause_detail.html"
    context_object_name = "pause"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pause"].feelings_with_labels = [
            feeling.get_label(self.request.user)
            for feeling in context["pause"].feelings.all()
        ]
        return context


class PauseCreateView(LoginRequiredMixin, CreateView):
    template_name = "pauses/observation.html"
    model = Pause
    fields = ["title", "empty_your_bag", "observation"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("feelings", kwargs={"pk": self.object.pk})


class PauseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "pauses/pause_update.html"
    model = Pause
    fields = ["title", "empty_your_bag", "observation"]

    def get_queryset(self):
        return Pause.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("update_feelings", kwargs={"pk": self.object.pk})


class PauseFeelingCreateView(LoginRequiredMixin, View):
    template_name = "pauses/feelings.html"

    def get_grouped_feelings(self, user):
        grouped_feelings = {}
        for family_code, family_name in Feeling.FeelingFamily.choices:
            feelings = Feeling.objects.filter(feeling_family=family_code).order_by("id")
            for feeling in feelings:
                feeling.label = feeling.get_label(user)
            grouped_feelings[family_name] = feelings
        return grouped_feelings

    def get(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        return render(
            request,
            self.template_name,
            {
                "pause": pause,
                "grouped_feelings": self.get_grouped_feelings(request.user),
            },
        )

    def post(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        selected_ids = request.POST.getlist("feelings")
        if not selected_ids:
            return render(
                request,
                self.template_name,
                {
                    "pause": pause,
                    "grouped_feelings": self.get_grouped_feelings(request.user),
                    "error_message": "Sélectionne au moins un sentiment.",
                },
            )
        pause.feelings.set(selected_ids)
        return redirect("needs", pk=pk)


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

    def get_context(self, pause, user, error_message=None):
        selected_feelings_ids = list(pause.feelings.values_list("id", flat=True))
        context = {
            "pause": pause,
            "grouped_feelings": self.get_grouped_feelings(user),
            "selected_feelings": selected_feelings_ids,
        }
        if error_message:
            context["error_message"] = error_message
        return context

    def get(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        return render(
            request, self.template_name, self.get_context(pause, request.user)
        )

    def post(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        selected_ids = request.POST.getlist("feelings")

        if not selected_ids:
            return render(
                request,
                self.template_name,
                self.get_context(
                    pause, request.user, "Sélectionne au moins un sentiment."
                ),
            )

        pause.feelings.set(selected_ids)
        return redirect("update_needs", pk=pk)


class PauseNeedCreateView(LoginRequiredMixin, View):
    template_name = "pauses/needs.html"

    def get_grouped_needs(self):
        grouped_needs = {}
        for family_code, family_name in Need.NeedFamily.choices:
            needs = Need.objects.filter(need_family=family_code).order_by("id")
            grouped_needs[family_name] = needs
        return grouped_needs

    def get_context(self, pause, error_message=None):
        context = {
            "pause": pause,
            "grouped_needs": self.get_grouped_needs(),
        }
        if error_message:
            context["error_message"] = error_message
        return context

    def get(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        return render(request, self.template_name, self.get_context(pause))

    def post(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        selected_ids = request.POST.getlist("needs")
        if not selected_ids:
            return render(
                request,
                self.template_name,
                self.get_context(pause, "Sélectionne au moins un besoin."),
            )
        pause.needs.set(selected_ids)

        user_agent = parse(request.META.get("HTTP_USER_AGENT", ""))
        if user_agent.is_mobile:
            return redirect("diary")
        else:
            return redirect("dashboard")


class PauseNeedUpdateView(LoginRequiredMixin, View):
    template_name = "pauses/needs.html"

    def get_grouped_needs(self):
        grouped_needs = {}
        for family_code, family_name in Need.NeedFamily.choices:
            needs = Need.objects.filter(need_family=family_code).order_by("id")
            grouped_needs[family_name] = needs
        return grouped_needs

    def get_context(self, pause, error_message=None):
        selected_needs_ids = list(pause.needs.values_list("id", flat=True))
        context = {
            "pause": pause,
            "grouped_needs": self.get_grouped_needs(),
            "selected_needs": selected_needs_ids,
        }
        if error_message:
            context["error_message"] = error_message
        return context

    def get(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        return render(request, self.template_name, self.get_context(pause))

    def post(self, request, pk):
        pause = get_object_or_404(Pause, id=pk, user=request.user)
        selected_ids = request.POST.getlist("needs")
        if not selected_ids:
            return render(
                request,
                self.template_name,
                self.get_context(pause, "Sélectionne au moins un besoin."),
            )
        pause.needs.set(selected_ids)

        user_agent = parse(request.META.get("HTTP_USER_AGENT", ""))
        if user_agent.is_mobile:
            return redirect("diary")
        else:
            return redirect("dashboard")
