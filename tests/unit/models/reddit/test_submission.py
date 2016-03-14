import pickle

import pytest
from praw.models import Submission

from ... import UnitTest


class TestSubmission(UnitTest):
    def test_equality(self):
        submission1 = Submission(self.reddit, _data={'id': 'dummy1', 'n': 1})
        submission2 = Submission(self.reddit, _data={'id': 'dummy1', 'n': 2})
        submission3 = Submission(self.reddit, _data={'id': 'dummy3', 'n': 2})
        assert submission1 == submission1
        assert submission2 == submission2
        assert submission3 == submission3
        assert submission1 == submission2
        assert submission2 != submission3
        assert submission1 != submission3

    def test_fullname(self):
        submission = Submission(self.reddit, _data={'id': 'dummy'})
        assert submission.fullname == 't3_dummy'

    def test_hash(self):
        submission1 = Submission(self.reddit, _data={'id': 'dummy1', 'n': 1})
        submission2 = Submission(self.reddit, _data={'id': 'dummy1', 'n': 2})
        submission3 = Submission(self.reddit, _data={'id': 'dummy3', 'n': 2})
        assert hash(submission1) == hash(submission1)
        assert hash(submission2) == hash(submission2)
        assert hash(submission3) == hash(submission3)
        assert hash(submission1) == hash(submission2)
        assert hash(submission2) != hash(submission3)
        assert hash(submission1) != hash(submission3)

    def test_id_from_url(self):
        urls = ['http://my.it/2gmzqe',
                'https://redd.it/2gmzqe',
                'http://reddit.com/comments/2gmzqe',
                'https://www.reddit.com/r/redditdev/comments/2gmzqe/'
                'praw_https_enabled_praw_testing_needed/']
        for url in urls:
            assert Submission.id_from_url(url) == '2gmzqe', url

    def test_id_from_url__invalid_urls(self):
        urls = ['', '1', '/', 'my.it/2gmzqe',
                'http://my.it/_',
                'https://redd.it/_/',
                'http://reddit.com/comments/_/2gmzqe']
        for url in urls:
            with pytest.raises(AttributeError):
                Submission.id_from_url(url)

    def test_pickle(self):
        submission = Submission(self.reddit, _data={'id': 'dummy'})
        for level in range(pickle.HIGHEST_PROTOCOL + 1):
            other = pickle.loads(pickle.dumps(submission, protocol=level))
            assert submission == other
