# -*- coding: utf-8 -*-
# @Time : 3/30/2022 1:58 PM
# @Author : su.xinhai
# @Email : su.xinhai@mech-mind.net
class Contract:
    all_contacts = []

    def __init__(self, name, email):
        self.name = name
        self.email = email
        Contract.all_contacts.append(self)


class MailSender:
    def send_email(self, msg):
        print("send {},to {}".format(msg, self.email))


class test(Contract, MailSender):
    pass


if __name__ == '__main__':
    a = test("1", "xxx@com")
    print(Contract.all_contacts)
    test.send_email("123")
