import pytest
from flask import Flask, request

from app.enums import ParserKey, InputLocation
from app.errors import ParsingError
from app.models.quest import Quest
from app.request_management.parser.parser import Parser