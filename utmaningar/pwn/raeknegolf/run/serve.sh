#!/bin/sh
socat -T600 TCP-LISTEN:3000,reuseaddr,fork EXEC:"./raeknegolf"