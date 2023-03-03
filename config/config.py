"""Configuration file"""
import os

from dotenv import load_dotenv

load_dotenv()

"""DB settings"""
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

"""Path to csv file"""

PATH_TO_CSV = os.getenv('PATH_TO_CSV')