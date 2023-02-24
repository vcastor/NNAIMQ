#!/bin/bash
########################################################################
# This bash script write the NNAIMQ code.                              #
# Using the variables about where are the Neural Networks, mean and    #
# std files with the full PATH, and also about the architecture of the #
# computer                                                             #
#                                ✨🌟✨                                #
# This script even install python if your computer does not have it,   #
# however, it cannot install Tensor Flow, since it has many variables  #
# to take into accout and it is not the propouse of this repository    #
#                                                      Victoria Castor #
########################################################################

########################################################################
here=`pwd`
OS=`uname`                                                             # macOS or Linux flavour
if [ "$OS" = 'Darwin' ]; then                                          # macOS (or OSX)
  if ! command -v brew &> /dev/null; then                              # Install Homebrew if it is not installed
    echo "Your computer does not have Homebrew (package manager)"
    echo "I will installed for you because I need it"
    curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
  fi
elif [ "$OS" = 'Linux' ]; then                                         # Linux flavour
  OS=`head -1 /etc/os-release | cut -f2 -d= | cut -f2 -d\"`
fi

########################################################################
# architecture
uname -a | grep x86_64 &> /dev/null
if [ "$?" = "0" ]; then                                                # x86_64
  ssfc="subprocess.check_call([r\"./SSFC.exe\", xyzf, nombre])"
else
  uname -a | grep arm &> /dev/null
  if [ "$?" = "0" ]; then                                              # arm
    ssfc="subprocess.check_call([r\"./SSFC_arm.exe\", xyzf, nombre])"
  else
    arch=`uname -a`
    echo "************************************************************************"
    echo "!                               =ERROR=                                !"
    echo "! You are not using x86_64 or ARM architecture, the executable         !"
    echo "! SSFC.exe will not work                                               !"
    echo "!                                                                      !"
    echo "! Your architecture is:                                                !"
    echo $arch
    echo "! Tensor Flow has not been (and will never be) developed for old       !"
    echo "! architecutres like x86_32.                                           !"
    echo "!                                                                      !"
    echo "! If you have any other trouble, contact:                              !"
    echo "!     Victoria Castor                                                  !"
    echo "!     @vcastor on Twitter                                              !"
    echo "************************************************************************"
    exit
  fi
fi

########################################################################
# the ML was written for python3
# do we have python3?
if ! ( command -v python3 &> /dev/null || command -v python &> /dev/null ); then
  if [ "$OS" = 'Darwin' ]; then                                        # macOS
    brew install python3
    brew postinstall python3
  elif [ "$OS" = 'Ubuntu' ]; then
    sudo apt-get install python3.8
  elif [ "$OS" = 'Debian' ]; then
    sudo apt install python3 -y
  elif [ "$OS" = 'CentOS' ]; then
    sudo yum update -y
    sudo yum install -y python3
  fi
fi                                              # Installed if it wasn't

# Ok, we have it, but where?
if command -v python3 &> /dev/null; then
    interpreter=( $(type python3) )
elif command -v python &> /dev/null; then
    interpreter=( $(type python) )
    echo "************************************************************************"
    echo "!                                WARNING                               !"
    echo "!        Be carfule with the python version that you're using          !"
    python --version
    echo "************************************************************************"
fi

# Do we have pip or pip3?
pip="pip3"
if ! command -v pip3 &> /dev/null; then
    echo "Your computer has python interpreter but with some missings"
    if [ "$OS" = 'Darwin' ]; then
      brew install python3
      brew postinstall python3
    elif [ "$OS" = 'Ubuntu' ]; then
      sudo apt-get install python3-pip
    elif [ "$OS" = 'Debian' ]; then
      sudo apt install python3-pip
    elif [ "$OS" = 'CentOS' ]; then
      sudo yum –y update
      sudo yum install python3-pip
    fi
elif ! command -v pip &> /dev/null; then
    echo "Your computer has python interpreter but with some missings"
    $interpreter -m ensurepip --upgrade
    pip="pip"
    echo "************************************************************************"
    echo "!                                WARNING                               !"
    echo "!        Be carfule with the python version that you're using          !"
    python --version
    echo "************************************************************************"
fi

########################################################################
# Libraries that we need
libraries=( os sys pathlib subprocess numpy pandas seaborn matplotlib random )
for biblioteca in ${libraries[@]}; do
  $interpreter -c "import $biblioteca" &> /dev/null
  if [ "$?" = '1' ]; then
      echo ""
      echo "Installing $biblioteca"
      $pip install $biblioteca
      echo ""
  fi
done

# Tensor Flow 
$interpreter -c 'import tensorflow as tf; print(tf.__version__)' &> /dev/null
if [ "$?" = '1' ]; then
    echo "************************************************************************"
    echo "!                                WARNING                               !"
    echo "!    Tensor Flow is not installed or is deactivated in this session    !"
    echo "!                                                                      !"
    echo "! If you are sure that your computer has Tensor Flow, ignore this      !"
    echo "! warning and activate Tensor Flow before you run the ML program.      !"
    echo "!                                                                      !"
    echo "! If your computer does not have Tensor Flow, please install it        !"
    echo "! Official documentation to do it:                                     !"
    echo "! https://www.tensorflow.org/install                                   !"
    echo "************************************************************************"
    echo ""
fi

########################################################################
# WRITE(*,*)
touch NNAIMQ.py
echo "# -*- coding: UTF-8 -*-  " >> NNAIMQ.py
sed -n '2,166p' raw_code.txt >> NNAIMQ.py
echo "    here = \"${here}/\"" >> NNAIMQ.py
sed -n '168,271p' raw_code.txt >> NNAIMQ.py
echo "        "$ssfc >> NNAIMQ.py
sed -n '273,$p' raw_code.txt >> NNAIMQ.py

# et voilà; danke schön!
echo "------------------------------------------------------------------------"
echo "!                                  NNAIMQ                              !"
echo "!                                                                      !"
echo "! NNAIMQ.py has been written succesfully                               !"
echo "! You can move the program to another directory without troubles       !"
echo "!                                                                      !"
echo "! Run as:                                                              !"
echo "! python3 NNAIMQ.py input                                              !"
echo "!                                                                      !"
echo "------------------------------------------------------------------------"
