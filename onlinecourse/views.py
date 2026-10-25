from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .models import Course, Enrollment, Submission


def registration_request(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("onlinecourse:index")
    return render(request, "registration/signup.html", {"form": form})


class CourseListView(generic.ListView):
    template_name = "onlinecourse/course_list_bootstrap.html"
    context_object_name = "course_list"

    def get_queryset(self):
        return Course.objects.order_by("-total_enrollment")[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_details_bootstrap.html"


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course, mode="honor")
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(
        reverse("onlinecourse:course_details", args=(course.id,))
    )


def extract_answers(request):
    """Lấy danh sách id các choice mà học viên đã tick."""
    submitted_answers = []
    for key in request.POST:
        if key.startswith("choice"):
            submitted_answers.append(int(request.POST[key]))
    return submitted_answers


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(extract_answers(request))
    return HttpResponseRedirect(
        reverse("onlinecourse:show_exam_result", args=(course.id, submission.id))
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = [choice.id for choice in submission.choices.all()]

    total_score = 0
    max_score = 0
    results = []
    for question in course.question_set.all():
        max_score += question.grade
        got_score = question.is_get_score(selected_ids)
        if got_score:
            total_score += question.grade
        results.append(
            {
                "question": question,
                "got_score": got_score,
                "choices": [
                    {
                        "choice": c,
                        "selected": c.id in selected_ids,
                    }
                    for c in question.choice_set.all()
                ],
            }
        )

    grade = int(total_score / max_score * 100) if max_score else 0
    context = {
        "course": course,
        "results": results,
        "selected_ids": selected_ids,
        "total_score": total_score,
        "max_score": max_score,
        "grade": grade,
        "passed": grade >= 80,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
