python3 web_crawler.py
pidof web_crawler.py
while [ $? -ne 0 ]
do
        echo "Process exits with errors! Sleep 2m!"
        sleep 2m
        echo "Restarting.."
        python3 web_crawler.py
done
echo "Process ends"