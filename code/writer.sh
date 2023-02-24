#!/bin/bash
########################################################################
#
#                                                      Victoria Castor #
########################################################################
# Paperback Writer

here=`pwd`
OS=`uname`                                      # macOS or Linux flavour
if [ "$OS" = 'Darwin' ]; then                   # macOS (or OSX)
  if ! command -v brew &> /dev/null; then       # Install Homebrew if it is not installed
    echo "Your computer does not have Homebrew (package manager)"
    echo "I will installed for you because I need it"
    curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
  fi
elif [ "$OS" = 'Linux' ]; then                  # Linux flavour
  OS=`head -1 /etc/os-release | cut -f2 -d= | cut -f2 -d\"`
fi

# architecture
uname -a | grep x86_64 &> /dev/null
if [ "$?" = "0" ]; then
  arch="x86_64"
else
  uname -a | grep arm &> /dev/null
  if [ "$?" = "0" ]; then
    arch="arm"
  else
    arch=`uname -a`
  fi
fi

# the ML was written for python3
# do we have it?
if ! ( command -v python3 &> /dev/null || command -v python &> /dev/null ); then
  if [ "$OS" = 'Darwin' ]; then                 # macOS
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
    echo "Be carfule with the python version that you're using"
    python --version
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
    echo "Be carfule with the python version that you're using"
    python --version
fi

########################################################################
# Libraries that we need
lib=( os sys pathlib subprocess numpy pandas seaborn matplotlib random )
for libreria in ${lib[@]}; do
  $interpreter -c "import $libreria" &> /dev/null
  if [ "$?" = '1' ]; then
      echo "Installing $libreria"
      $pip install $libreria &> /dev/null
  fi
done

# Tensor Flow 
$interpreter -c 'import tensorflow as tf; print(tf.__version__)' &> /dev/null
if [ "$?" = '1' ]; then
    echo "**************************************************************************"
    echo "                                WARNING"
    echo "Tensor Flow is not installed or is deactivated in this session"
    echo ""
    echo "If you're sure that your computer has Tensor Flow, ignore this warning and"
    echo "activate Tensor Flow when you run the ML program."
    echo ""
    echo "If you don't have Tensor Flow, please install it"
    echo "Official documentation to do it:"
    echo "https://www.tensorflow.org/install"
    echo "**************************************************************************"
fi

########################################################################
# WRITE(*,*)
touch NNAIMQ.py
sed -n '1,164p' raw_code.txt >> NNAIMQ.py
echo "    here = \"${here}/\"" >> NNAIMQ.py
sed -n '166,269p' raw_code.txt >> NNAIMQ.py
if [ "$arch" = "arm" ]; then
  echo "        subprocess.check_call([r\"./SSFC_arm.exe\", xyzf, nombre])" >> NNAIMQ.py
elif [ "$arch" = "x86_64" ]; then
  echo "        subprocess.check_call([r\"./SSFC.exe\", xyzf, nombre])" >> NNAIMQ.py
else
  echo "**************************************************************************"
  echo "                                WARNING"
  echo "You are not using x86_64 or ARM architecture, the executable SSFC.exe"
  echo "will not work"
  echo ""
  echo "Your architecture:"
  echo "$arch"
  echo "**************************************************************************"
  echo "        subprocess.check_call([r\"./SSFC_uknown_architechture.exe\", xyzf, nombre])" >> NNAIMQ.py
fi
sed -n '271,$p' raw_code.txt >> NNAIMQ.py

# et voilà; danke schön!
echo "**************************************************************************"
echo "                                  NNAIMQ "
echo ""
echo "NNAIMQ.py has been written"
echo "You can move the program to another directory without troubles"
echo ""
echo "Run as:"
echo "python3 NNAIMQ.py input"
echo ""
echo "or"
echo ""
echo "./NNAIMQ.py input"
echo "**************************************************************************"
