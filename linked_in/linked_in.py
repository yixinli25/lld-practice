from __future__ import annotations
from typing import List, Dict
from enum import Enum
import datetime
from threading import Lock
import uuid

# User Registration and Authentication:
    # Users should be able to create an account with their professional information, such as name, email, and password.
    # Users should be able to log in and log out of their accounts securely.
# User Profiles:
    # Each user should have a profile with their professional information, such as profile picture, headline, summary, experience, education, and skills.
    # Users should be able to update their profile information.
# Connections:
    # Users should be able to send connection requests to other users.
    # Users should be able to accept or decline connection requests.
    # Users should be able to view their list of connections.
# Messaging:
    # Users should be able to send messages to their connections.
    # Users should be able to view their inbox and sent messages.
# Job Postings:
    # Employers should be able to post job listings with details such as title, description, requirements, and location.
    # Users should be able to view and apply for job postings.
# Search Functionality:
    # Users should be able to search for other users, companies, and job postings based on relevant criteria.
    # Search results should be ranked based on relevance and user preferences.
# Notifications:
    # Users should receive notifications for events such as connection requests, messages, and job postings.
    # Notifications should be delivered in real-time.
# Scalability and Performance:
    # The system should be designed to handle a large number of concurrent users and high traffic load.
    # The system should be scalable and efficient in terms of resource utilization.

class User:
    def __init__(
        self, 
        id: str, 
        name: str, 
        email: str, 
        password: str, 
        profile: Profile, 
        connections: List[Connection], 
        inbox: List[Message], 
        sent_messages: List[Message]
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.connections = connections
        self.inbox = inbox
        self.sent_messages = sent_messages

    def set_profile(self, profile: Profile):
          self.profile = profile


class Profile:
    def __init__(
        self,
        profile_picture: str = "",
        headline: str = "",
        summary: str = "",
        experiences: List[Experience] = [],
        educations: List[Education] = [],
        skills: List[Skill] = []
    ):
        self.profile_picture = profile_picture
        self.headline = headline
        self.summary = summary
        self.experiences = experiences
        self.educations = educations
        self.skills = skills

    def set_summary(self, summary: str):
        self.summary = summary
    
    def set_headline(self, headline: str):
        self.headline = headline

    def add_experience(self, experience: Experience):
        self.experiences.append(experience)

    def add_education(self, education: Education):
        self.educations.append(education)

    def add_skill(self, skill: Skill):
        self.skills.append(skill)


class Experience:
    def __init__(self, title: str, company: str, description: str, start_date: str, end_date: str):
        self.title = title
        self.company = company
        self.description = description
        self.start_date = start_date
        self.end_date = end_date


class Education:
    def __init__(self, school: str, degree: str, field_of_study: str, start_date: str, end_date: str):
        self.school = school
        self.degree = degree
        self.field_of_study = field_of_study
        self.start_date = start_date
        self.end_date = end_date


class Skill:
    def __init__(self, name: str):
        self.name = name


class NotificationType(Enum):
    CONNECTION_REQUEST = "CONNECTION_REQUEST"
    MESSAGE = "MESSAGE"
    JOB_POSTING = "JOB_POSTING"


class Notification:
    def __init__(
        self,
        notification_id: str,
        user: User,
        notification_type: NotificationType,
        content: str,
        timestamp: datetime
    ):
        self._id = notification_id
        self._user = user
        self._type = notification_type
        self._content = content
        self._timestamp = timestamp

    @property
    def id(self):
        return self._id
    
    @property
    def user(self):
        return self._user
    
    @property
    def type(self):
        return self._type
    
    @property
    def content(self):
        return self._content
    
    @property
    def timestamp(self):
        return self._timestamp
    

class Message:
    def __init__(
        self,
        message_id: str,
        sender: User,
        receiver: User,
        content: str,
        timestamp: datetime
    ):
        self._id = message_id
        self._sender = sender
        self._receiver = receiver
        self._content = content
        self._timestamp = timestamp

    @property
    def id(self):
        return self._id
    
    @property
    def sender(self):
        return self._sender
    
    @property
    def receiver(self):
        return self._receiver
    
    @property
    def content(self):
        return self._content
    
    @property
    def timestamp(self):
        return self._timestamp
    

class Connection:
    def __init__(self, sender: User, connection_date: datetime):
        self._user = sender
        self._connection_date = connection_date

    @property
    def user(self):
        return self._user
    
    @property
    def connection_date(self):
        return self._connection_date
    

class JobPosting:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        requirements: List[str],
        location: str,
        post_date: datetime
    ):
        self._id = id
        self._title = title
        self._description = description
        self._requirements = requirements
        self._location = location
        self._post_date = post_date

    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    @property
    def requirements(self):
        return self._requirements
    
    @property
    def location(self):
        return self._location
    
    @property
    def post_date(self):
        return self._post_date
    

class LinkedInService:
    _instance = None
    _lock = Lock()

    users: Dict[str, User] = {}
    job_postings: Dict[str, JobPosting] = {}
    notifications: Dict[str, Notification] = {}
    pending_connection_requests: Dict[str, List[User]] = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is not None:
                cls._instance = super().__new__(cls)
                cls._instance.users = cls.users
                cls._instance.job_postings = cls.job_postings
                cls._instance.notifications = cls.notifications
                cls._pending_connection_requests = cls.pending_connection_requests
            return cls._instance
        
    def register_user(self, user: User):
        self.users[user.id] = user

    def login_user(self, email: str, password: str):
        for user in self.users.values():
            if user.email == email and user.password == password:
                return user
        return None
    
    def update_user_profile(self, user):
        self.users[user.id] = user

    def send_connection_request(self, sender: User, receiver: User):
        connection = Connection(sender, datetime.now())
        sender.connections.append(connection)
        notification = Notification(
            self._generate_notification_id(),
            receiver,
            NotificationType.CONNECTION_REQUEST,
            f"New connection request from {sender.name}",
            datetime.now()
        )
        self._add_notification(receiver.id, notification)

    def accept_connection_request(self, user: User, connection_sender: User):
        # Need to add a pending requests logic
        pass

    def search_user(self, keyword: str):
        return [user for user in self.users.values() if keyword.lower() in user.name.lower()]
    
    def post_job_listing(self, job_posting: JobPosting):
        self.job_postings[job_posting.id] = job_posting
        for user in self.users.values():
            notification = Notification(
                self._generate_notification_id(),
                user,
                NotificationType.JOB_POSTING,
                f"New Job Posting: {job_posting.title}",
                datetime.now()
            )
            self._add_notification(user.id, notification)

    def search_job_posting(self, keyword: str):
        return [job_posting for job_posting in self.job_postings.values() if keyword.lower() in job_posting.description.lower()]
    
    def send_message(self, sender: User, receiver: User, content: str):
        message = Message(self._generate_message_id, sender, receiver, content, datetime.now())
        receiver.inbox.append(message)
        sender.sent_messages.append(message)
        notification = Notification(
            self._generate_notification_id,
            receiver,
            NotificationType.MESSAGE,
            f"New Message from {sender.name}",
            datetime.now()
        )
        self._add_notification(receiver.id, notification)

    def _add_notification(self, user_id: str, notification: Notification):
        if user_id not in self.notifications:
            self.notification[user_id] = []
        self.notification[user_id].append(notification)

    def _generate_notification_id(self):
        return str(uuid.uuid4())
    
    def _generate_message_id(self):
        return str(uuid.uuid4())