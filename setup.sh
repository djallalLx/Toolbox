### setup.sh

#!/bin/bash

# Function to install packages on macOS
install_mac() {
    # Install Homebrew if not installed
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Install packages
    brew install nmap john

    # Install Java if needed
    if ! command -v java &> /dev/null
    then
        echo "Java Runtime not found. Installing Java..."
        brew install openjdk
        sudo ln -sfn /usr/local/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
    fi
}

# Function to install packages on Linux
install_linux() {
    # Update package list
    sudo apt update

    # Install packages
    sudo apt install -y nmap john openjdk-11-jdk
}

# Install Python packages
pip3 install --user -r requirements.txt

# Detect the OS and install appropriate packages
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    install_mac
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    install_linux
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Setup completed."
