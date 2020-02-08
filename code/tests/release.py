# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

# Run this module on each supported MQ version prior to releasing PyMQI.

# stdlib
from uuid import uuid4

# PyMQI
import pymqi
from pymqi import CMQC, CMQCFC

queue_manager = 'MQTEST'
channel = 'CH1'
host = '127.0.0.1'
port = '8887'
conn_info = '{0}({1})'.format(host, port)

queue_name = uuid4().hex
queue_name_bytes = queue_name.encode('ascii')
message = uuid4().hex.encode('ascii')

# Connect ..
with pymqi.connect(queue_manager, channel, conn_info) as qmgr:
    pcf = pymqi.PCFExecute(qmgr)
    
    # .. create a queue ..
    pcf.MQCMD_CREATE_Q({CMQC.MQCA_Q_NAME: queue_name_bytes, CMQC.MQIA_Q_TYPE: CMQC.MQQT_LOCAL})
    
    # .. put a message ..
    with pymqi.Queue(qmgr, queue_name) as queue:
        queue.put(message)
    
    # .. get it back ..
    with pymqi.Queue(qmgr, queue_name) as queue:
        assert queue.get() == message
    
    # .. drop the queue ..
    pcf.MQCMD_DELETE_Q({CMQC.MQCA_Q_NAME: queue_name_bytes, CMQC.MQIA_Q_TYPE: CMQC.MQQT_LOCAL})
    
    # .. and just to be sure, grab some channels as well ..
    result = pcf.MQCMD_INQUIRE_CHANNEL({CMQCFC.MQCACH_CHANNEL_NAME: b'*'})
    assert len(result) > 1
