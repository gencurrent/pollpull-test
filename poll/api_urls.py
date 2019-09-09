from django.urls import re_path
from poll.api_view import QuestionViewSet, PollViewSet

question_by_pk = QuestionViewSet.as_view({'get': 'get',})
question_submit_answer = QuestionViewSet.as_view({'post': 'submit_answer',})
poll_by_pk = PollViewSet.as_view({'delete': 'delete'})
poll_no_pk = PollViewSet.as_view({'get': 'list'})
poll_result = PollViewSet.as_view({'get': 'get_result'})

urlpatterns = [
    re_path(r'poll/(?P<poll_id>\d+)/$', poll_by_pk, name='poll_by_pk'),
    re_path(r'poll/(?P<poll_id>\d+)/result/$', poll_result, name='poll_result_view'),
    re_path(r'poll/?$', poll_no_pk, name='poll_no_pk'),
    
    re_path(r'question/(?P<question_id>\d+)/submit-answer/$', question_submit_answer, name='question_submit_answer_view'),
    re_path(r'question/(?P<question_id>\d+)/.*', question_by_pk, name='question_by_pk_view'),
]