from django.test import TestCase
from django.contrib.auth.models import User
from .models import Idea, IdeaVote, District


class IdeaVoteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser')
        self.user2 = User.objects.create_user('testuser2')
        self.user3 = User.objects.create_user('testuser3')
        district = District.objects.create(name='d')
        self.idea = Idea.objects.create(district=district, user=self.user)

    def test_vote_yes(self):
        self.idea.vote_yes(self.user)
        self.assertEqual(IdeaVote.objects.get(user=self.user,
            idea=self.idea).state, True)

    def test_vote_no(self):
        self.idea.vote_no(self.user)
        self.assertEqual(IdeaVote.objects.get(user=self.user,
            idea=self.idea).state, False)

    def test_vote_yes_than_no_has_one_record(self):
        self.idea.vote_yes(self.user)
        self.idea.vote_no(self.user)
        self.assertEqual(IdeaVote.objects.filter(user=self.user,
            idea=self.idea).count(), 1)

    def test_vote_count_when_single_vote_change(self):
        self.idea.vote_yes(self.user)
        self.assertEqual(self.idea.vote_yes_count, 1)
        self.assertEqual(self.idea.vote_no_count, 0)
        self.idea.vote_no(self.user)
        self.assertEqual(self.idea.vote_yes_count, 0)
        self.assertEqual(self.idea.vote_no_count, 1)

    def test_vote_count_overall(self):
        self.idea.vote_yes(self.user)
        self.idea.vote_yes(self.user2)
        self.idea.vote_no(self.user3)
        self.assertEqual(self.idea.vote_yes_count, 2)
        self.assertEqual(self.idea.vote_no_count, 1)
