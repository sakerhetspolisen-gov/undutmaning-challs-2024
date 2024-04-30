#!/bin/sh
socat -T600 TCP-LISTEN:3001,reuseaddr,fork SYSTEM:"cat|./allmant_underligt_extraordinart_verktyg"
