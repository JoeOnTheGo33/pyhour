DEV_DIR=$(pwd)
cd ~
if [ ! -d ".pyhour/bin" ]
then
  mkdir .pyhour/bin
fi
echo "Location: ${DEV_DIR}/clock.py"
cp "${DEV_DIR}/clock.py" ".pyhour/bin/clock" || exit
stat .pyhour/bin/clock
chmod +x .pyhour/bin/clock || exit