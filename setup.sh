
### setup.sh

You can also create a script to automate the installation process:

```bash
#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Install nmap
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y nmap
elif command -v yum &> /dev/null; then
    sudo yum install -y nmap
else
    echo "Please install nmap manually."
fi

# Install john
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y john
elif command -v yum &> /dev/null; then
    sudo yum install -y john
else
    echo "Please install john manually."
fi

# Install python3
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y python3
elif command -v yum &> /dev/null; then
    sudo yum install -y python3
else
    echo "Please install python3 manually."
fi
