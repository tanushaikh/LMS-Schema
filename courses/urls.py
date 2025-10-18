from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseViewSet, MeetingViewSet,CourseEnrollmentViewSet,StudentTotalHoursAPIView,WeeklyStatusTaskViewSet,
                    CoursePDFViewSet,RecentDownloadViewSet,CourseTotalAPIView, CourseAverageScoreAPIView, MentorsViewSet,
                    PDFDownloadView,CourseAverageLearningTimeAPIView, UserStreakAPIView)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'mentors', MentorsViewSet, basename='mentors')
router.register(r'meetings', MeetingViewSet, basename='meeting')
router.register(r'pdfs', CoursePDFViewSet)
router.register(r'downloads', RecentDownloadViewSet)
router.register(r'enrollments', CourseEnrollmentViewSet, basename='courseenrollment')
router.register(r"weekly-tasks", WeeklyStatusTaskViewSet, basename="weekly-tasks")

urlpatterns = [
    path('', include(router.urls)),
    path("total/", CourseTotalAPIView.as_view(), name="course-total"),
    path("average-score/", CourseAverageScoreAPIView.as_view(), name="course-average-score"),
    path("average-learning-time/", CourseAverageLearningTimeAPIView.as_view(), name="course-average-learning-time"),
    path("streak/", UserStreakAPIView.as_view(), name="user-streak"),
    path("total-hours/", StudentTotalHoursAPIView.as_view(), name="student-total-hours"),
    path('courses_pdf/<int:course_id>/pdfs/<int:pdf_id>/download/', PDFDownloadView.as_view(), name='pdf-download'),
    path("weekly-plans/<int:course_id>/users/<int:user_id>/weekly-summary/",
         CourseViewSet.as_view({"get": "user_weekly_summary"}),
         name="user-weekly-summary"),
]
