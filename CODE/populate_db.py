#! /usr/bin/env python
# populate_db.py
# Gina Schmalzle
# 20140723, works

"""Database populating tools for Million Song Database."""

import os
import sqlite3
import ast
import time
import shutil
import glob
import unicodedata

def retrieve_user_files(path='../DATA/DOWNLOADS/'):
    """Get list of user files in a given directory."""
    file_list = glob.glob(path+'*.dict')
    return file_list

def retrieve_all_user_data_as_dict(files=retrieve_user_files()):
    """ Retrieve user information from file.  """
    contents_dict = {}
    for file in files:
      user = file[18:36]
      with open(file, 'r') as f:
        contents = f.read()
      contents_dict[user] = ast.literal_eval(contents)
    return contents_dict

def retrieve_all_user_data_as_list_of_tuples(files=retrieve_user_files()):
    """ Retrieve user information from file.  """
    contents_list = []
    contents_dict = retrieve_all_user_data_as_dict(files)
    for user in contents_dict:
      user_id = user
      for i in range(0, len(contents_dict[user])):
        selection_number = i
        try:
          artist_id = contents_dict[user][i]['artist_id'].encode('utf8')
          artist_name = contents_dict[user][i]['artist_name'].encode('utf8')
          date_added = contents_dict[user][i]['date_added'].encode('utf8')
          foreign_id = contents_dict[user][i]['foreign_id'].encode('utf8')
          last_modified = contents_dict[user][i]['last_modified'].encode('utf8')
          song_id = contents_dict[user][i]['song_id'].encode('utf8')
          song_name = contents_dict[user][i]['song_name'].encode('utf8')
          contents_list.append((user_id,selection_number,artist_id,
          artist_name, date_added, foreign_id, last_modified, song_id,
          song_name))
        except KeyError:
          artist_id = contents_dict[user][i]['artist_id'].encode('utf8')
          artist_name = contents_dict[user][i]['artist_name'].encode('utf8')
          date_added = contents_dict[user][i]['date_added'].encode('utf8')
          foreign_id = contents_dict[user][i]['foreign_id'].encode('utf8')
          last_modified = contents_dict[user][i]['last_modified'].encode('utf8')
          song_id = contents_dict[user][i]['song_id'].encode('utf8')
          song_name = 'NA'
          contents_list.append((user_id,selection_number,artist_id,
          artist_name, date_added, foreign_id, last_modified, song_id,
          song_name))
          print ("No song name for user ", user_id, "song number", i)
          continue
    return contents_list

def populate_db_w_users(to_print=None, db='music_user.db'):
    """Populate database with contents of site list."""
    list_of_users = retrieve_all_user_data_as_list_of_tuples()
    connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
    with connection:
        cursor = connection.cursor()
        i = 0
        for user in list_of_users:
            i = i + 1
            mytuple = (i,user[0],user[1],user[2],user[3],user[4],user[5],user[6],user[7],user[8])
            print ('mytuple', mytuple)
            if user == ['']:
                print('\n    Empty tuple found; skipping.\n')
                continue
            if to_print:
                print(str(mytuple))
            try:
                cursor.execute(
                    '''INSERT INTO users VALUES''' +
                    str(tuple(mytuple)) )
            except:
                continue
