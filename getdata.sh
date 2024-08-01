cpu=$(top -b -n1 | grep "Cpu(s)" | awk '{print $2 + $4}')
mem=$(free | grep Mem | awk '{print $3/$2 * 100.0}')

printf $cpu
printf "\n"
printf $mem