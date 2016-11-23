from django.test import TestCase
from django.conf import settings
from idea.models import Idea, District

from .models import User, UserProfile


class UserProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test_user')
        district = District.objects.create(name='d')
        self.idea = Idea.objects.create(user=self.user, district=district)

    def test_new_user_has_zero_points(self):
        p = self.user.get_profile()
        self.assertEqual(p.approved_ideas_no, 0)
        self.assertEqual(p.votes_no, 0)
        self.assertEqual(p.own_ideas_vote_diff, 0)
        self.assertEqual(p.points, 0)

    def test_idea_author_approved_ideas_no(self):
        self.idea.approve()
        p = self.user.get_profile()
        self.assertEqual(p.approved_ideas_no, 1)
        self.assertEqual(p.points, settings.IDEA_POINT)

    def test_idea_author_votes_no(self):
        p = User.objects.create_user('voter_one').get_profile()
        self.idea.vote_yes(p.user)
        self.assertEqual(p.votes_no, 1)
        self.assertEqual(p.points, settings.VOTE_POINT)

    def test_idea_author_own_ideas_vote_diff(self):
        self.idea.approve()
        p = self.user.get_profile()
        voter_one = User.objects.create_user('voter_one')
        voter_two = User.objects.create_user('voter_two')
        voter_three = User.objects.create_user('voter_three')
        self.idea.vote_yes(self.user)
        self.idea.vote_yes(voter_one)
        self.idea.vote_yes(voter_two)
        self.idea.vote_no(voter_three)
        self.assertEqual(p.own_ideas_vote_diff, 2)
        self.assertEqual(p.points, settings.IDEA_POINT +
            2 * settings.IDEA_VOTE_DIFF_POINT + settings.VOTE_POINT)


class UserProfileManagerTest(TestCase):

    def test_notification_emails(self):
        self.user = User.objects.create_user('test_user')
        self.user.profile.full_name = 'test user'
        self.user.profile.save()
        self.user.emailaddress_set.create(email='a@a.com', verified=True, primary=True)
        self.user.emailaddress_set.create(email='b@b.com', verified=True, primary=False)

        self.user2 = User.objects.create_user('test_user2')
        self.user2.profile.full_name = 'test user two'
        self.user2.profile.receive_notifications = False
        self.user2.profile.save()
        self.user2.emailaddress_set.create(email='c@c.com', verified=True, primary=True)
        with self.assertNumQueries(1):
            l = list(UserProfile.objects.notification_emails)
        self.assertEqual(len(l), 1)
        self.assertTrue(('test user', 'a@a.com') in l)
