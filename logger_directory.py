"""
Create the LOGGER Objects
for now i.e
Requests Logger , User Logger
"""
import os
from logger import init_logging

# try:
#     os.mkdir(os.path.join(os.getcwd(), 'API_REQUESTS_LOGS'))
#     print("Directory Created")
# except FileExistsError as e_exe:
#     print('Directory already in existance')


def requests_logger():
    """ Returns the Requests Logger Objects """
    return init_logging(log_name='API_REQUESTS_LOGS', log_directory='/home/tejas/complain')


def user_logger():
    """ Returns the User Logger Object"""
    return init_logging(log_name='USER_LOGS', log_directory='/home/tejas/complain')
