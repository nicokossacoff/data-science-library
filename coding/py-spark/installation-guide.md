# Install JDK
First, install Java Development Kit (JDK). You can install JDK using Homebrew:
```bash
brew install --cask temurin
```
Verify that the installation was successful with the following command:
```bash
java --version
```
Alternatively, you can install JDK using an installer from [Oracle](https://www.oracle.com/java/technologies/downloads/).
# Install Apache Spark
Again, you can install Apache Spark using Homebrew:
```bash
brew install apache-spark
```
You can also download Apache Spark's latest version from this [page](https://spark.apache.org/downloads.html) and extract it to a directory of your choice, e.g., `~/spark`.
# Set-up Environment Variables
This step is very important if we want Python, Apache Spark and Java to interact as intended.
Locate the `~/.zshrc` (or `~/.bash_profile` if you're using bash) and add these variables to the end:
```bash
# Java Home
export JAVA_HOME=$(/usr/libexec/java_home)

# Spark Home - adjust path if you manually installed
export SPARK_HOME=$(brew --prefix apache-spark)/libexec
# OR if manually installed:
# export SPARK_HOME=/path/to/your/spark

# Add Spark to PATH
export PATH=$SPARK_HOME/bin:$PATH

# For PySpark
export PYSPARK_DRIVER_PYTHON=python3
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
```
Then you have to apply those changes running the following command in the terminal:
```bash
source ~/.zshrc
# source ~/.bash_profile
```
# Install PySpark
Install PySpark using your package manager of choice:
```bash
conda install -c conda-forge pyspark
```
Verify the installation by running the following command:
```bash
spark
```
If successful, you'll see the Spark logo and a Python prompt.