from rest_framework import serializers as ss

from poll.models import Poll, Question, Answer, AnswerGiven

class PollSerializer(ss.ModelSerializer):
    questionAwaiting = ss.IntegerField(read_only=True, allow_null=True)   # Вопрос, который ожидает ответа

    def to_representation(self, obj):
        data = super().to_representation(obj)
        """ Выборка неотвеченного вопроса """
        question_list = Question.objects.filter(poll=obj).\
            prefetch_related('answer_list', 'answer_list__answergiven_list')\
            .order_by('id') # Допустим, сортировка по ID есть  
        q_ag_dict = {}
        data['questionAwaiting'] = None
        prev_answer_given = None
        for q in question_list:
            a_g = q.answer_given
            if a_g is None:
                if prev_answer_given and prev_answer_given.answer.question_lead_to == q:
                    data['questionAwaiting'] = q.id
                    break
                if prev_answer_given is None:
                    data['questionAwaiting'] = q.id
                    break
            prev_answer_given = a_g
        return data

    class Meta: 
        model = Poll
        fields = '__all__'
        read_only = ('id', )


class AnswerGivenSerializer(ss.ModelSerializer):
    """ Данный ответ """
    class Meta:
        model = AnswerGiven
        fields = '__all__'


class AnswerSerializer(ss.ModelSerializer):
    isGiven = ss.BooleanField(source='asnwergiven_list', read_only=True)
    """ Ответ """
    def to_representation(self, obj):
        result = super().to_representation(obj)
        result['isGiven'] = obj.answergiven_list.all().exists()
        return result


    class Meta:
        model = Answer 
        fields = '__all__'
        read_only = ('id', )


class QuestionSerializer(ss.ModelSerializer):
    answerList = AnswerSerializer(many=True, source='answer_list')
    class Meta: 
        model = Question
        fields = '__all__'
        