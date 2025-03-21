docs available here: 

https://doc.divoom-gz.com/web/#/12?page_id=536

example:

? (192.168.68.104) at 64:e8:33:48:98:70 [ether] on wlp0s20f3


test url:

http://appin.divoom-gz.com/Device/ReturnCurrentDate?test=0

returns:

{"ReturnCode":0,"ReturnMessage":"","DispData":"2025-03-22 06:10:58"}


export DIVOOM_TIMES_GATE_IP=192.168.68.104

[nix-shell:~/src/divoom-times-gate]$ poetry run python ./src/brightness.py 
2025-03-21 15:29:59,115 - DEBUG - Starting new HTTP connection (1): 192.168.68.104:80
2025-03-21 15:29:59,344 - DEBUG - http://192.168.68.104:80 "POST /post HTTP/1.1" 200 None
2025-03-21 15:29:59,345 - INFO - Successfully sent command: Channel/SetBrightness
Brightness set to 50%: {'error_code': 0}
2025-03-21 15:30:09,354 - DEBUG - Starting new HTTP connection (1): 192.168.68.104:80
2025-03-21 15:30:09,505 - DEBUG - http://192.168.68.104:80 "POST /post HTTP/1.1" 200 None
2025-03-21 15:30:09,506 - INFO - Successfully sent command: Channel/SetBrightness
Brightness set to 100%: {'error_code': 0}


the json return body for the external call:
{"ReturnCode":0,"ReturnMessage":"","DispData":"blah"}

