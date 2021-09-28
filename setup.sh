python3 /root/chatBot/srcs/scraping_box_office_revenue.py > /dev/null 2> /dev/null

echo '0 0 * * * python3 /root/chatBot/srcs/scraping_box_office_revenue.py > /dev/null 2> /dev/null' > cron.conf
crontab cron.conf
rm -rf cron.conf

tail -f /dev/null
