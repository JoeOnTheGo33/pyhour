DEV_DIR=$(pwd)
cd ~
if [ ! -d ".pyhour/bin" ]
then
  mkdir .pyhour/bin
fi
echo "Location: ${DEV_DIR}/clock.py"
ln "${DEV_DIR}/clock.py" ".pyhour/bin/clock" || echo "clock already present"
ln "${DEV_DIR}/tally.py" ".pyhour/bin/tally.py" || echo "tally already present"
stat .pyhour/bin/clock
chmod +x .pyhour/bin/clock || exit
clock -h