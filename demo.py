from pygrok import Grok
text = '2018-08-30 17:12:28.846066 [PID 4789] [485ms] [UID R0BOH] [ERROR] /login Error on line 920 at login_handler.py. Logtrace below. Error name: ValueError'
pattern = '%{TIMESTAMP_ISO8601:timestamp}%{SPACE}(\[%{WORD:pid}%{SPACE}%{POSINT:pid}])%{SPACE}(\[%{NUMBER:responsetime}?ms])%{SPACE}(\[%{WORD:uid}\s+%{WORD:uidname}])%{SPACE}(\[%{LOGLEVEL:loglevel}])%{SPACE}(%{URIPATHPARAM:request})%{SPACE}%{GREEDYDATA:syslog_message}'
grok = Grok(pattern)
print grok.match(text)