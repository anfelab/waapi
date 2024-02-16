# WAAPI Scripts

Some scripts to improve the workflow in Wwise using WAAPI.

Included:
-Switch Assigner: Automatically assings a Random Container for every switch in a Switch group for every Switch Container selected. It will also assign any object that matches the name of the Switch.
-Rename with indexing: A quick way to rename multiple objects with the same name and add the indexing automatically
-Rename with Clipboard contents: Get the names from Excel or other text editor and rename the selected containers
-Parent creator: Creates a parent container (of any type) for every group of items with similar names (without indexing)

More in the works
## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a Windows machine. The instructions are tailored for Windows users.
- You have permission to install software on your computer.

## Installing Python

Follow these steps to install Python and set up the necessary environment variables:

1. **Download Python**: Visit the [official Python website](https://www.python.org/downloads/) and download the latest version of Python for Windows.

2. **Run the Installer**: Open the downloaded file to start the installation process. Ensure you check the box that says **Add Python X.X to PATH** before clicking **Install Now**, where X.X corresponds to the version you're installing.

   ![Add Python to PATH](![image](https://github.com/anfelab/waapi/assets/57996654/76ca4a1a-5e9f-49f1-801d-c050ab798e94)


3. **Verify Installation**: Open a command prompt and type `python --version`. If Python is installed correctly and added to your PATH, you should see the Python version printed in the terminal.

## Setting Up Your Environment

After installing Python, you need to set up your project environment:

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`, followed by the URL to this repository.

2. **Navigate to the Project Directory**: Use the command prompt to navigate to the directory where you cloned the repository.

3. **Running the Batch File**: Locate the batch file provided in the repository. Right-click and select **Run as administrator** to execute the batch file. This file will set up the necessary folders and copy the required files to the correct locations.

   If you encounter any permission issues, ensure you have administrative rights to run batch files on your system.

## Additional Configuration

If you want to set the port or the IP for WAAPI manually go to __init__.py in the wwise_helpers folder. Change the IP or port in the set_client() function.

## Using the Project

The scripts will be added in Wwise as commands, you can access them by right-clicking an item or a selection of items.
They are roghly categorized. If you want any changes contact me.

## Contributing to Project Name

To contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contributors

Thanks to the following people who have contributed to this project:

- Myself (@anfelab)

