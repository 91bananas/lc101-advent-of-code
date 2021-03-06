from collections import namedtuple
from wtforms import StringField, TextAreaField, SelectField
from .forms import SubmitChallenge

# We want a namedtuple, but with default parameters and non-standard
# behavior at initialization-time. So we're making a class that
# immediately inherits from the one produced by namedtuple, and tacking
# on some additional logic.
all_challenges = []

class Challenge(namedtuple(
    'ChallengeParent',
    ['day', 'title', 'form'])):
    def __new__(self, day, title, form=None, answers=None):
        if form is None:
            # You don't want a custom form? that's cool, we can make you a
            # standard one if you tell us what the acceptable_answers are.
            assert answers is not None, "must pass either 'form' or 'answers'"
            class form(SubmitChallenge):
                acceptable_answers = answers

        return super(Challenge, self).__new__(self, day, title, form)

class BoxableChallenge(SubmitChallenge):
    answer = SelectField('answer', choices=[('boxable', 'Boxable'), ('unboxable', 'Unboxable')])
    acceptable_answers = ['unboxable']

all_challenges.append(Challenge(
    day=1,
    title='well-wrapped presents',
    form=BoxableChallenge))
all_challenges.append(Challenge(
    day=2,
    title='conserving candles',
    answers=['66', '66%', '0.66']))
all_challenges.append(Challenge(
    day=3,
    title='wishlist snooping',
    answers=[
        'dear santa i would like a toy pup a toy kitten a toy bunny and a toy horse and also a small plane that i could ride in i would like a coloring book too',
        'dear santa i would like a toy pup a toy kitten a toy bunny and a toy horse and also a small plane that i could ride in i would like a coloring book too'.replace(' ', '')]))

def get_challenge(day):
    challenge = all_challenges[day - 1]
    assert challenge.day == day, "We got out-of-order challenges over here!"
    return challenge
