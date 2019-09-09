from decimal import Decimal

from django.db import models



class Poll(models.Model):
    """ Опрос """

    name = models.CharField('Опрос', max_length=127, default='')

    def __str__(self):
        return f'Опрос #{self.id}:<{self.name}>'

class Question(models.Model):
    """ Вопрос """
    text = models.CharField('Текст', max_length=127, default='')
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, 
        related_name='question_list', 
        verbose_name='Опрос'
    )

    @property
    def answer_given(self):
        answer_list = self.answer_list.all()
        ag_list = []
        for a in answer_list:
            answergiven_list = a.answergiven_list.all()
            ag_list.extend(answergiven_list)
        if len(ag_list) > 1: 
            # Не может быть более одного ответа
            raise Exception(f'The number of given answers is more than 1 in question id:{self.id}')
        if len(ag_list) == 0:
            return None
        return ag_list[0]

    def __str__(self):
        return f'Вопрос #{self.id}:<{self.text}><{self.poll_id}>'

class Answer(models.Model):
    """ Запрограммированный на вопрос """
    text = models.CharField('Текст', max_length=63, default='')
    grade = models.DecimalField('Оценка', max_digits=4, decimal_places=2, default=Decimal(0))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, 
        related_name='answer_list', 
        verbose_name='Относится к вопросы'
    )
    question_lead_to = models.ForeignKey(
        Question, on_delete=models.CASCADE, 
        related_name='answer_leaded_to_list', 
        verbose_name='Направление к вопросу', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f'Ответ #{self.id}:<{self.text}><###>'

class AnswerGiven(models.Model):
    """ Даннные ответ """

    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, 
        related_name='answergiven_list',
        verbose_name='Ответ на вопрос'
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, 
        related_name='answergiven_list', 
        verbose_name='Опрос'
    )

    @property
    def question_text(self):
        return self.answer.question.text

    def __str__(self):
        return f'ДанОтвет #{self.id}:<{self.answer.text}><{self.poll.name}>'
    
    class Meta:
        # unique_together = [('answer', 'user')]    # Как должно быть
        unique_together = [('answer',)]
    