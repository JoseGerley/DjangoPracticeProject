import datetime
from time import time
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    
    def setUp(self):
        self.question=Question(question_text="What's up?", pub_date=timezone.now())
    
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)    
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the past for more than one day
        """
        time = timezone.now() + datetime.timedelta(days=1, minutes=5)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=55)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse(('polls:index')))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])
        
    def test_no_question_with_future_question(self):
        """
        Even if no questions exist, if a future question exists, an appropriate message is displayed.
        """
        Question.objects.create(question_text="Future question.", pub_date = timezone.now() + datetime.timedelta(days=30))
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])
    
    def test_question_with_two_future_questions(self):
        """
        If two future questions exist, an appropriate message is displayed.
        """
        Question.objects.create(question_text="Future question 1.", pub_date = timezone.now() + datetime.timedelta(days=30))
        Question.objects.create(question_text="Future question 2.", pub_date = timezone.now() + datetime.timedelta(days=10))
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])
    
    def test_question_with_past_question_and_future(self):
        """
        If even a past question exists, Only display the past question.
        """
        q1 = Question.objects.create(question_text="Past question.", pub_date = timezone.now() - datetime.timedelta(days=30))
        Question.objects.create(question_text="Future question.", pub_date = timezone.now() + datetime.timedelta(days=30))
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question.")
        self.assertNotContains(response, "Future question.")
        self.assertEqual(response.context['lastest_question_list'].count(), 1)
        self.assertQuerysetEqual(response.context['lastest_question_list'], [repr(q1)])
        
    def test_question_with_past_and_actual_question(self):
        """
        Exist only past and actual question. Show all questions.
        """
        q1 = Question.objects.create(question_text="Past question.", pub_date = timezone.now() - datetime.timedelta(days=30))
        a1 = Question.objects.create(question_text="Actual question.", pub_date = timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past question.")
        self.assertContains(response, "Actual question.")
        self.assertEqual(response.context['lastest_question_list'].count(), 2)
        self.assertQuerysetEqual(response.context['lastest_question_list'], [repr(a1),repr(q1)])

class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)