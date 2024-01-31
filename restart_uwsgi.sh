ps -fu siteusr |grep uwsgi |grep Dmtrack2 |awk '{print $2}' | xargs kill -9
sleep 2s
/public/Biosoft/Python-3.8.6/local/bin/uwsgi -x Dmtrack2.xml

