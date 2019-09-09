# import pdb 

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import action

from poll.api_serializers import *
from poll.models import Poll, Question, Answer, AnswerGiven
from poll.queries import get_poll_answers

class PollViewSet(ViewSet):
    """ Страница опросов """
    def list(self, request):
        poll_list = Poll.objects.all()
        serler = PollSerializer(poll_list, many=True)
        return Response(serler.data, status=HTTP_200_OK)
    
    def get(self, request, poll_id):
        try: 
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response('', status=HTTP_404_NOT_FOUND)
        serler = PollSerializer(poll)
        return Response(serler.data, status=HTTP_200_OK)
        
    
    def get_result(self, request, poll_id):
        print('HEreree')
        try: 
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExitst as e: 
            return Response('', status=HTTP_404_NOT_FOUND)
        all_answers = get_poll_answers(poll.id)
        data = {
            'name': poll.name, 
            'score': sum(r['grade'] for r in all_answers),
            'maxScorePossible': len(all_answers) * 100.0,
        }
        
        return Response(data, status=HTTP_200_OK)
    
    def delete(self, request, poll_id):
        try: 
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist as e:
            return Response('', status=HTTP_404_NOT_FOUND)
        poll.delete()
        return Response('', HTTP_200_OK)

class QuestionViewSet(ViewSet):
    def get(self, request, question_id, *args, **kwargs):
        try: 
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist as e: 
            return Response('', status=HTTP_404_NOT_FOUND)
        serler = QuestionSerializer(question)
        return Response(serler.data, status=HTTP_200_OK)

    # @action(method=['post'], detail=True, url_path='submit-answer')
    def submit_answer(self, request, question_id):
        """ Подтвердить (`текущий` или `создать новый`) ответ на вопрос """
        # TODO: Определить удаление всех следующих ответов, если текущий ответ переопределен
        try: 
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist as e: 
            return Response({'question': 'Not found'}, status=HTTP_404_NOT_FOUND)
        try:
            # pdb.set_trace()
            answer_id = int(request.data['answerId'])
        except KeyError as e:
            return Response({'answerId': 'The field is required on submit-answer action'}, status=HTTP_400_BAD_REQUEST)
        except TypeError as e:
            return Response({'answerId': 'Could not convert answerId value to integer'}, status=HTTP_400_BAD_REQUEST)
        try: 
            answer = Answer.objects.get(pk=answer_id, question=question)
        except Answer.DoesNotExist as e:
            return Response({'answer': 'Not found'}, status=HTTP_404_NOT_FOUND)
        # Получение / создание объекта AnswerGiven
        try:
            answer_given = AnswerGiven.objects.get(answer__question=question, poll_id=question.poll_id)
        except Exception as e: 
            answer_given = AnswerGiven(answer=answer, poll_id=question.poll_id)
        # [Пере]запись объекта AnswerGiven
        answer_given.answer = answer
        answer_given.save()
        """ Следующий вопрос """
        next_question = answer.question_lead_to
        if next_question is None: 
            # След. вопрос не найден 
            return Response({'finished': True}, status=HTTP_200_OK)

        serler = QuestionSerializer(next_question)
        return Response(serler.data, status=HTTP_200_OK)
        