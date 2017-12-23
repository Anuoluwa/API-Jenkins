import requests
import jenkins
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# server = jenkins.Jenkins('http://localhost:8080', username='myuser', password='mypassword')
# user = server.get_whoami()
# version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))

def connectToJenkins(url, username, password):
    server = jenkins.Jenkins(url, username=username, password=password)
    return server

def initializeDb():
    db = create_engine('sqlite:///apis.db', echo = False)
    #db = false
    session = sessionmaker(bind=db)()
    Base.metadata.create_all(db)
    return session

def addJob(session, job_list):
    for job in job_list:
        session.add(job)
    session.commit()

def getLastJobId(session, name):
    job = session.query(Jobs).filter_by(name=name).order_by(Jobs.jen_id.desc()).first()
    if (job != None):
        return job.jen_id

class Jobs(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, primary_key = True)
    jen_id = Column(Integer)
    name = Column(String)
    building = Column(String)
    result = Column(String)
    timeStamp = Column(DateTime)


def createJob(first, lastBuildNumber, jobName):
    jobList = []
    for i in range(first + 1, lastBuildNumber + 1):
        last = server.get_build_info(jobName, i)
        lastJobs = Jobs()
        lastJobs.jen_id = last['id']
        lastJobs.building = last['building']
        lastJobs.name = jobName
        lastJobs.result = current['result']
        lastJobs.timeStamp = datetime.datetime.fromtimestamp(long(current['timestamp'])*0.001)
        jobList.append(lastJobs)
    return jobList


url = 'http://localhost:8080'
username = raw_input('Enter username: ')
password = raw_input('Enter password: ')
server = connectToJenkins(url, username, password)


if authenticated:
    session = initializeDb()
    """
     get list of jobs
    """

    jobs = server.get_all_jobs()
    for j in jobs:
        jobName = j['name']
        lastJobId = getLastJobId(session, jobName) # get last locally stored job of this name
        lastBuildNumber = server.get_job_info(jobName)['lastBuild']['number']  # get last build number from Jenkins for this job

        if lastJobId == None:
            start = 0
        else:
            start = lastJobId

        jlist = createJobList(start, lastBuildNumber, jobName)
        addJob(session, jlist)
    else:
        authenticated = false
        print ('Authentication error')
