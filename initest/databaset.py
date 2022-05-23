# -*- coding: utf-8 -*-
# @Time : 3/29/2022 3:09 PM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net

class Database:

    def pr(self):
        print(1)


database = None

def initialize_database():
    global database
    database = Database()
