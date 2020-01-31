#!/bin/sh -e
echo "============================= Welcome to SmartOwn Boat Setup ============================="
echo "Please Enter the Input for following parameters or press Enter to skip entering values."
read -p "Enter Scanner No: " scanner_no
read -p "Enter Scanner Type: " scanner_type
echo "> Creating .env file in root directory"
echo -e "SCANNER=$scanner_no\nSCANNER_TYPE=$scanner_type" > .env
echo "> Installing python modules..."
pip install -r requirements.txt
echo "> Making startup.sh executable"
sudo chmod +x startup.sh
echo "> Creating Crontab on root"
sudo sh -c 'cat <<EOF > /var/spool/cron/crontabs/root
@reboot /home/startup.sh
EOF'
read -p "> Setup complete. Do you want to reboot system? [Y/N]:" choice
case $choice in
    y|Y) echo "Rebooting system..."; reboot; break ;;
    n|N) exit 1 ;;
    *) echo "Sorry, invalid input";;
esac
