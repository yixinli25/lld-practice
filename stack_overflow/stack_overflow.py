from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime

# Users can post questions, answer questions, and comment on questions and answers.
# Users can vote on questions and answers.
# Questions should have tags associated with them.
# Users can search for questions based on keywords, tags, or user profiles.
# The system should assign reputation score to users based on their activity and the quality of their contributions.
# The system should handle concurrent access and ensure data consistency.

class Votable(ABC):
    @abstractmethod
    def vote(self, user, value):
        pass

    @abstractmethod
    def get_vote_count(self):
        pass

class Commentable(ABC):
    @abstractmethod
    def add_comment(self, user, content):
        pass

    def get_comment_count(self):
        pass

class User:
    def __init__(self, id, user_name, email):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.reputation = 0
        self.questions = []
        self.answers = []
        self.comments = []

    def ask_question(self, title, content, tags):
        question = Question(self, title, content, tags)
        self.questions.append(question)
        return question
    
    def answer_question(self, question, content):
        answer = Answer(self, question, content)
        self.answers.append(answer)
        question.add_answer(answer)
        return answer
    
    def comment_on(self, item, content):
        comment = Comment(self, content)
        self.comments.append(comment)
        item.add_comment(comment)
        return comment
    
    def update_reputation(self, value):
        self.reputation += value
        self.reputation = max(0, self.reputation)

    def get_questions(self):
        return self.questions


class Question(Votable, Commentable):
    def __init__(self, author, title, content, tags):
        self.id = id(self)
        self.author = author
        self.title = title
        self.content = content
        self.tags = [Tag(name) for name in tags]
        self.created_at = datetime.now()
        self.answers = []
        self.votes = defaultdict(int)
        self.comments = []

    def add_answer(self, answer):
        if answer in self.answers:
            raise Exception("Answer already added!")
        self.answers.append(answer)

    def vote(self, user, value):
        if value not in [-1, 1]:
            raise Exception("Invalid vote value!")
        self.votes[user] = value

    def get_vote_count(self):
        return sum(v for _, v in self.votes.items())
    
    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments


class Answer(Votable, Commentable):
    def __init__(self, author, question, content):
        self.id = id(self)
        self.author = author
        self.question = question
        self.content = content
        self.votes = defaultdict(int)
        self.comments = []
        self.is_accepted = False

    def vote(self, user, value):
        if value not in [-1, 1]:
            raise Exception("Invalid vote value!")
        self.votes[user] = value

    def get_vote_count(self):
        return sum(v for _, v in self.votes.items())
    
    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

    def accept(self, user):
        if self.is_accepted:
            raise Exception("Answer already accepted!")

        if user != self.question.author:
            raise Exception("Only question author can accept answer!")
        
        self.is_accepted = True
        self.author.update_reputation(15)


class Tag:
    def __init__(self, name):
        self.id = id(self)
        self.name = name

    def get_name(self):
        return self.name

class Vote:
    def __init__(self, user, value):
        self.user = user
        self.value = value

class Comment:
    def __init__(self, author, content):
        self.id = id(self)
        self.author = author
        self.content = content
        self.created_at = datetime.now()

# Central Class to handle all the operations:
class StackOverflow:
    def __init__(self):
        self.users = {}
        self.questions = {}
        self.answers = {}
        self.tags = {}

    def create_user(self, user_name, email):
        user_id = len(self.users) + 1
        user = User(user_id, user_name, email)
        self.users[user_id] = user
        return user
    
    def ask_question(self, user, title, content, tags):
        question = user.ask_question(title, content, tags)
        self.questions[question.id] = question
        for tag in tags:
            self.tags[Tag(tag).get_name()] = tag
        return question
    
    def answer_question(self, user, question, content):
        answer = user.answer_question(question, content)
        self.answers[answer.id] = answer
        return answer
    
    def add_comment(self, user, item, content):
        return user.comment_on(item, content)
    
    def vote_question(self, user, question, value):
        question.vote(user, value)

    def vote_answer(self, user, answer, value):
        answer.vote(user, value)

    def accept_answer(self, user, answer):
        answer.accept(user)

    def search_question(self, query):
        return [q for q in self.questions.values() if
                query.lower() in q.title.lower()
                or query.lower() in q.content.lower()
                or any(query.lower() == tag.name.lower() for tag in q.tags)]
    
    def get_questions_by_user(self, user):
        return user.get_questions()
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_question(self, question_id):
        return self.questions.get(question_id)
    
    def get_answer(self, answer_id):
        return self.answers.get(answer_id)
    
    def get_tags(self, tag_name):
        return self.tags.get(tag_name)


class StackOverflowDemo:
    @staticmethod
    def run():
        stack_overflow = StackOverflow()

        john = stack_overflow.create_user("John Doe", "jdoe@gmail.com")
        bob = stack_overflow.create_user("Bob Smith", "bsmith@gmail.com")
        jack = stack_overflow.create_user("Jack Black", "jblack@gmail.com")

        question1 = stack_overflow.ask_question(
            john,
            "How to create a Python dictionary?",
            "I am trying to create a dictionary in Python. Can someone help me?",
            ["python", "dictionary"]    
        )

        answer1 = stack_overflow.answer_question(
            bob,
            question1,
            "You can create a dictionary using the dict() constructor."
        )

        comment1 = stack_overflow.add_comment(
            jack,
            question1,
            "Agreed! You can also use the {} syntax."
        )

        vote1 = stack_overflow.vote_answer(jack, answer1, 1)

        print(f"Question1: {question1.title}")
        print(f"Answer1: {answer1.content}")
        print(f"Comment1: {comment1.content}")
        print(f"Votes: {answer1.get_vote_count()}")

if __name__ == "__main__":
    StackOverflowDemo.run()