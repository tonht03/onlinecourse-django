# Online Course - Django

Django project gồm app `onlinecourse` với Course, Lesson, Question, Choice, Submission và bài thi trắc nghiệm.

## Chạy project
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- Admin: http://127.0.0.1:8000/admin/
- Trang khóa học: http://127.0.0.1:8000/onlinecourse/

## Các file theo từng Task
| Task | File |
|------|------|
| 1 | `onlinecourse/models.py` |
| 2 | `onlinecourse/admin.py` |
| 3 | `screenshots/03-admin-site.png` |
| 4 | `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | `onlinecourse/views.py` |
| 6 | `onlinecourse/urls.py` |
| 7 | `screenshots/07-final.png` |
