import datetime
from django.utils.html import escape
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

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
    
    def test_was_published_recently_with_edge_case(self):
  
        time = timezone.now() - datetime.timedelta(days=1)
        edge_case_question = Question(pub_date=time)
        self.assertIs(edge_case_question.was_published_recently(), False)

def create_question(question_text, days):

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
       
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
      
        question = create_question("Past question.", -10)
        create_question("Future question.", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        
        question1 = create_question("Past question 1.", -10)
        question2 = create_question("Past question 2.", -5)
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
       
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):

    def test_future_question(self):
        
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        
        past_question = create_question(question_text="Past Question.", days=-5)
        choice1 = past_question.choice_set.create(choice_text="Option 1", votes=5)
        choice2 = past_question.choice_set.create(choice_text="Option 2", votes=3)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice1.choice_text)
        self.assertContains(response, choice1.votes)
        self.assertContains(response, choice2.choice_text)
        self.assertContains(response, choice2.votes)


class ChoiceModelTests(TestCase):

    def test_choice_is_assigned_to_correct_question(self):
        
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        choice = Choice.objects.create(question=question, choice_text="Option 1", votes=0)
        self.assertEqual(choice.question, question)

    def test_choice_votes_default_to_zero(self):
        
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        choice = Choice.objects.create(question=question, choice_text="Option 1")
        self.assertEqual(choice.votes, 0)

    def test_increase_votes(self):
        
        question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        choice = Choice.objects.create(question=question, choice_text="Option 1", votes=0)
        choice.votes += 1
        choice.save()
        self.assertEqual(choice.votes, 1)

class QuestionVoteViewTests(TestCase):

    def test_vote_valid_choice(self):
       
        question = create_question(question_text="Sample Question", days=-1)
        choice = question.choice_set.create(choice_text="Option 1", votes=0)
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": choice.id})

        self.assertRedirects(response, reverse("polls:results", args=(question.id,)))

        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_invalid_choice(self):
       
        question = create_question(question_text="Sample Question", days=-1)
        url = reverse("polls:vote", args=(question.id,))
        response = self.client.post(url, {"choice": 999})  
        self.assertEqual(response.status_code, 200)
        expected_message = escape("You didn't select a choice.")
        self.assertContains(response, expected_message)

    def test_vote_future_question(self):
       
        future_question = create_question(question_text="Future Question", days=5)
        url = reverse("polls:vote", args=(future_question.id,))
        response = self.client.post(url, {"choice": 1})
        self.assertEqual(response.status_code, 404)
