#!/bin/zsh

rofi_cmd() {
	rofi \
	    -dmenu -p "WIFI Menu" -config $HOME/.config/rofi/wifi/config.rasi
}

run_rofi() {
	nmcli -t -f "SSID" device wifi list | rofi_cmd
}

connect() {
  # $1 (SSID)
  nmcli device wifi connect $1 2>&1
}

connect_with_password() {
  # $1 (SSID)
  # $2 (PASSWORD)
  nmcli device wifi connect $1 password $2 2>&1
}

ask_to_use_saved_password(){
  rofi -dmenu -p "Use saved password? [Y/n]" -theme "$HOME/.config/rofi/wifi/config.rasi"
}

get_password(){
  rofi -dmenu -p "Password" -password -theme "$HOME/.config/rofi/wifi/config.rasi"
}

# Main
selected_ssid=$(run_rofi)
if [ -z $selected_ssid ]; then
  exit 0
fi

is_saved=$(nmcli -t -f name connection show | grep "^$selected_ssid$")
if [ -n $is_saved ] 
then
  response=$(ask_to_use_saved_password)
  case $response in [yY] | '')
    echo "Using saved connection: $is_saved"
    output_message=$(connect $selected_ssid)
    ;;
    *)
    echo "Enter password for $selected_ssid: "
	  password=$(get_password)
    output_message=$(connect_with_password $selected_ssid $password)
	  ;;
  esac
else
  echo "Enter password for $selected_ssid: "
	password=$(get_password)
  output_message=$(connect_with_password $selected_ssid $password)
fi

# Adapt output message
if [[ $output_message == *"Device"* ]]; then
   output_message="Connected to $selected_ssid"
   notify-send Wi-Fi $output_message
else
   output_message="Failed to connect to $selected_ssid"
   notify-send -u critical Wi-Fi $output_message
fi

