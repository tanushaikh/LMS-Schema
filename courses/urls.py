from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseViewSet, MeetingViewSet,CourseEnrollmentViewSet,StudentTotalHoursAPIView,
                    CoursePDFViewSet,RecentDownloadViewSet,CourseTotalAPIView, CourseAverageScoreAPIView, 
                    PDFDownloadView,CourseAverageLearningTimeAPIView, UserStreakAPIView)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'meetings', MeetingViewSet, basename='meeting')
router.register(r'pdfs', CoursePDFViewSet)
router.register(r'downloads', RecentDownloadViewSet)
router.register(r'enrollments', CourseEnrollmentViewSet, basename='courseenrollment')

urlpatterns = [
    path('', include(router.urls)),
    path("total/", CourseTotalAPIView.as_view(), name="course-total"),
    path("average-score/", CourseAverageScoreAPIView.as_view(), name="course-average-score"),
    path("average-learning-time/", CourseAverageLearningTimeAPIView.as_view(), name="course-average-learning-time"),
    path("streak/", UserStreakAPIView.as_view(), name="user-streak"),
    path("total-hours/", StudentTotalHoursAPIView.as_view(), name="student-total-hours"),
    path('courses/<int:course_id>/pdfs/<int:pdf_id>/download/', PDFDownloadView.as_view(), name='pdf-download'),

]
