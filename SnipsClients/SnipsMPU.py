#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

from hermes_python.hermes import Hermes
from hermes_python.ontology import *

class SnipsMPU(object):
    def __init__(self, i18n, mqtt_addr, site_id, datetime):
        self.THRESHOLD_INTENT_CONFSCORE_DROP = 0.3
        self.THRESHOLD_INTENT_CONFSCORE_TAKE = 0.6

        self.__i18n = i18n
        self.__site_id = site_id
        self.__datetime = datetime
        self.__mqtt_addr = mqtt_addr

    def check_site_id(handler):
        @functools.wraps(handler)
        def wrapper(self, hermes, intent_message):
            if intent_message.site_id != self.__site_id:
                return None
            else:
                return handler(self, hermes, intent_message)
        return wrapper

    def check_confidence_score(handler):
        @functools.wraps(handler)
        def wrapper(self, hermes, intent_message):
            if handler is None:
                return None
            if intent_message.intent.confidence_score < self.THRESHOLD_INTENT_CONFSCORE_DROP:
                hermes.publish_end_session(
                    intent_message.session_id,
                    ''
                )
                return None
            elif intent_message.intent.confidence_score <= self.THRESHOLD_INTENT_CONFSCORE_TAKE:
                hermes.publish_end_session(
                    intent_message.session_id,
                    self.__i18n.get('error.doNotUnderstand')
                )
                return None
            return handler(self, hermes, intent_message)
        return wrapper

    @check_confidence_score
    @check_site_id
    def handler_ask_time(self, hermes, intent_message):
        print("Ask Time")
        #resp_texte = self.__datetime.get_askTime_string()
        resp_texte = "Snips MPU"
        hermes.publish_end_session(
            intent_message.session_id,
            self.__i18n.get('askTime', {"Time": resp_texte})
        )

    @check_confidence_score
    @check_site_id
    def handler_ask_date(self, hermes, intent_message):
        print("Ask Date")
        resp_texte = self.__datetime.get_askDate_string()
        hermes.publish_end_session(
            intent_message.session_id,
            self.__i18n.get('askDate', {"Date": resp_texte})
        )

    def start_block(self):
        with Hermes(self.__mqtt_addr) as h:
            h.subscribe_intent(
                'askTime',
                self.handler_ask_time
            ) \
             .subscribe_intent(
                'askDate',
                self.handler_ask_date
            ) \
             .start()