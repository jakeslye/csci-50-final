#!/usr/bin/perl

use strict;
use warnings;

my $config_file = 'config.txt';
open(my $fh, '<', $config_file) or die "Cannot open config file: $!";
my %config;
while (my $line = <$fh>) {
   	chomp $line;
   	my ($key, $value) = split('=', $line);
   	$config{$key} = $value;
}
close($fh);

my $cpu = `lscpu | grep "Model name" | awk -F: '{print \$2}' | xargs`;
chomp($cpu);

my $free_output = `free -b | grep Mem: | awk '{print \$2}'`;
chomp($free_output);
my $total_memory_gb = $free_output / 1024 / 1024 / 1024;

print `whoami`;
print "$cpu\n";
print "$total_memory_gb\n";
print "$config{'cpu_threshold'}\n";
print "$config{'memory_threshold'}";