import json
import logging
import sys

from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from poll.api_urls import question_by_pk, question_submit_answer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loggingHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(loggingHandler)

class PollTest(TestCase):
    """ Есил вы видите этот тект, то тест в процессе разработки """
    def setUp(self):
        call_command("loaddata", "test.json", verbosity=0)

    def test_loading(self):
        """ Test """
        factory = APIRequestFactory()
        question_id = 3
        request = factory.get(f'/api/question/{question_id}/',)
        response = question_by_pk(request, question_id)
        # logger.debug(response.data)

    def test_get_submit(self):
        factory = APIRequestFactory()
        question_id = 1
        request = factory.get(f'/api/question/{question_id}/',)
        response = question_by_pk(request, question_id)
        # logger.debug(response.data)
        options = dict(response.data).get('answerList')

        self.assertEqual(len(options), 2, 'The options length is equal')
        # logger.debug('The options = ')
        # logger.debug(options)

        # Выбираем 2-й вариант ответа
        chosen_option = next( opt for opt in options if opt.get('id') == 2)

        request = factory.post(f'/api/question/{question_id}/submit-answer/', data={'answerId': chosen_option['id']})
        response = question_submit_answer(request, question_id)
        self.assertEqual(response.status_code, 200)
        new_question_data = response.data
        logger.info(f'The new question data = ')
        logger.info(new_question_data)
        # Запрос на получение вопроса
        request = factory.get(f'/api/question/{question_id}/')
        response = question_by_pk(request, question_id)
        answer_given = next( ans for ans in response.data.get('answerList') if ans['isGiven'])
        self.assertEqual(answer_given.get('id'), 2, f'The AnswerGivenId should be {chosen_option["id"]}')
        # logger.debug(answer_given)
        # logger.debug('The response on submitting answer')
        # logger.debug(response.data)
        
        
    
    
