import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    '''任意の質問名 / 日時でQuestionオブジェクトを作成'''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_no_qiestopms(self):
        '''questionを作らず、No polls are availableが表示されるかを確認'''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        # latest_question_listが空になっているかを確認
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_past_question(self):
        '''過去の日付で検証'''
        question = create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
    
    def test_future_question(self):
        '''未来の日付で検証'''
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_question_and_past_question(self):
        '''過去と未来の質問があった場合、過去のみが表示されるか検証'''
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
    
    def test_two_past_question(self):
        '''過去日付の質問が2つあった場合両方表示されるか検証'''
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
        
    def test_was_published_recently_with_future_question(self):
        '''未来の日付に対してFalseを返すかどうか'''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        '''1日以内ならTrueを返す'''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''未来の日付の質問は404を返す'''
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        '''過去の日付の質問が表示されるかを確認'''
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)