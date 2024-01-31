ps -ef|grep celery|grep Dmtrack2|awk '{print $2}'|xargs kill -9
