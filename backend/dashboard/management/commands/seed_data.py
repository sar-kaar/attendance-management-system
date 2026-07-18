import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import Student
from courses.models import Course, Enrollment
from attendance.models import Attendance


PROGRAMS = ['BSc.CSIT', 'BIM', 'BCA']
SECTIONS = ['A', 'B', 'C']
STATUS_CHOICES = ['present', 'absent', 'late', 'lp', 'eca']
STATUS_WEIGHTS = [60, 15, 10, 8, 7]

FACULTY_DATA = [
    ('Ram', 'Sharma', 'ram.sharma'),
    ('Sita', 'Adhikari', 'sita.adhikari'),
]

COURSE_DATA = [
    ('Software Engineering', 'CSE 405', 3),
    ('Data Structures', 'CSE 201', 3),
    ('Database Management', 'CSE 301', 3),
    ('Operating Systems', 'CSE 302', 3),
    ('Computer Networks', 'CSE 303', 3),
]

STUDENT_DATA = [
    ('Abhishek', 'Rokaya', 'abhishek.s24'),
    ('Prizma', 'Shrestha', 'prizma.s24'),
    ('Ekata', 'Tamrakar', 'ekata.s24'),
    ('Rahul', 'Thapa', 'rahul.s24'),
    ('Sneha', 'Karki', 'sneha.s24'),
    ('Bikash', 'Gurung', 'bikash.s24'),
    ('Anita', 'Poudel', 'anita.s24'),
    ('Deepak', 'Mishra', 'deepak.s24'),
    ('Sara', 'Lama', 'sara.s24'),
    ('Nabin', ' Rai', 'nabin.s24'),
    ('Priya', 'Gupta', 'priya.s24'),
    ('Karan', 'Bhandari', 'karan.s24'),
    ('Asha', 'Limbu', 'asha.s24'),
    ('Bijay', 'Tamang', 'bijay.s24'),
    ('Chhaya', 'Magar', 'chhaya.s24'),
]


class Command(BaseCommand):
    help = 'Seed database with realistic test data for dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        self.stdout.write('  Creating faculty...')
        faculties = []
        for first, last, username in FACULTY_DATA:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@mitnepal.edu.np',
                    'role': 'faculty',
                },
            )
            if _:
                user.set_password('testpass123')
                user.save()
            faculties.append(user)

        self.stdout.write('  Creating students...')
        students = []
        for i, (first, last, username) in enumerate(STUDENT_DATA):
            program = PROGRAMS[i % len(PROGRAMS)]
            section = SECTIONS[i % len(SECTIONS)]
            student_id = f'MIT-2024-{str(i+1).zfill(3)}'
            student, _ = Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@mitnepal.edu.np',
                    'program': program,
                    'section': section,
                    'phone': f'98{random.randint(10000000, 99999999)}',
                },
            )
            students.append(student)

        self.stdout.write('  Creating courses...')
        courses = []
        for name, code, credits in COURSE_DATA:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'credits': credits,
                    'faculty': random.choice(faculties),
                },
            )
            courses.append(course)

        self.stdout.write('  Enrolling students...')
        for student in students:
            num_courses = random.randint(2, 4)
            enrolled_courses = random.sample(courses, num_courses)
            for course in enrolled_courses:
                Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={'is_active': True},
                )

        self.stdout.write('  Generating attendance (20 class days)...')
        today = date.today()
        attendance_dates = [today - timedelta(days=x) for x in range(1, 21)]

        count = 0
        for course in courses:
            enrollments = Enrollment.objects.filter(course=course, is_active=True)
            for att_date in attendance_dates:
                for enrollment in enrollments:
                    status = random.choices(STATUS_CHOICES, weights=STATUS_WEIGHTS, k=1)[0]
                    Attendance.objects.update_or_create(
                        student=enrollment.student,
                        course=course,
                        date=att_date,
                        defaults={'status': status, 'marked_by': 'seed'},
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {len(faculties)} faculty, {len(students)} students, '
            f'{len(courses)} courses, {count} attendance records.'
        ))
