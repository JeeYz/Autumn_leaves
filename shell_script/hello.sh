#!/bin/bash

echo "hello, world~!!"

language="Korean"

echo "i speak $language"


function print(){
  echo $1
}

print "I can speak Korean"


function learn(){
  local learn_language="English"
  echo "i am learning $learn_language"
}

learn


temp_filepath=$PWD

echo $temp_filepath
echo ${temp_filepath%/*}
echo ${temp_filepath#/*}

