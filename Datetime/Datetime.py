#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime

class datetime(object):

    def askTime(self):
        now = datetime.datetime.now()
        time = "Il est {} heure {}".format(now.strftime("%H"), now.strftime("%M"))
        result = requests.get('http://192.168.2.130:5005/Bureau/say/regarde ta montre/fr')
        return time

    def get_askTime_string(self):
        return '{}'.format(self.askTime())

    def askDate(self):
        now = datetime.datetime.now()
        date = "Nous sommes le {} {} {} {}".format(now.strftime("%A"), now.strftime("%d"), now.strftime("%B"), now.strftime("%Y"))
        result = requests.get('http://192.168.2.130:5005/Bureau/say/regarde le calendrier/fr')
        return date

    def get_askDate_string(self):
        return '{}'.format(self.askDate())



