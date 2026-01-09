import os
import requests
import time
import subprocess
import signal
import sys

def test_index_page_served(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Docker Model Runner" in resp.data


def test_static_favicon(client):
    resp = client.get("/static/favicon.ico")
    assert resp.status_code == 200


def test_static_robots(client):
    resp = client.get("/static/robots.txt")
    assert resp.status_code == 200
