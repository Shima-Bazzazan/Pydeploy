import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def test_past_question(self):
   
    question = create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(response.context["latest_question_list"], [question])

def test_future_question_and_past_question(self):
    
    question = create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(response.context["latest_question_list"], [question])

def test_two_past_questions(self):
    
    question1 = create_question(question_text="Past question 1.", days=-30)
    question2 = create_question(question_text="Past question 2.", days=-5)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(
        response.context["latest_question_list"],
        [question2, question1],
    )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
   
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
       
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class VoteViewTests(TestCase):
    def test_vote_for_question_without_choices(self):
        
        question = create_question(question_text="Question with no choices.", days=-1)
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 1})
        self.assertEqual(response.status_code, 404)


def test_invalid_choice_vote(self):
       
        question = create_question(question_text="Valid question.", days=-1)
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 9999})  
        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):
    def test_results_future_question(self):
        
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_questions_message(self):
       
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
