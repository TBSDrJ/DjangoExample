from django.shortcuts import render
from django.http import HttpResponse
from .htmlCompletions import htmlHead, htmlBody, Row, Column

def index(request):
    httpStr = htmlHead("This is Dr. J's Twit Page")
    blankCol = Column(2)
    actualCol = Column(10, "This is Dr. J's Twit Page", bgColor='light', textColor='primary')
    testColumns = [blankCol, actualCol]
    testRow = Row(testColumns)
    rows = [testRow]
    httpStr += htmlBody(rows)
    return HttpResponse(httpStr)
