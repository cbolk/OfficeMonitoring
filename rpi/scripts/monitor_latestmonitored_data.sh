while change=$(inotifywait -e create,modify --format %w%f -r /home/pi/repository/); do
    sudo  /home/pi/scripts/pushsensors10m.sh
done

