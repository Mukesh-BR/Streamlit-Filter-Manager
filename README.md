# Streamlit Filter Manager

Streamlit Filter Manager is a web application that allows you to edit filters used in production. This README provides instructions on how to install the required dependencies and run the Streamlit app.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mukesh-BR/Streamlit-Filter-Manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Streamlit-Filter-Manager
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. After successfully installing the dependencies, you can run the Streamlit app using the following command:

   ```bash
   streamlit run Alpharoc_Filter_Manager.py
   ```

2. Your default web browser will open, and you'll be able to interact with the Streamlit app to edit filters.

## Features

- **Data Editing**: You can edit the filters in a user-friendly interface provided by Streamlit.

- **Archiving**: The app automatically archives changes, generating timestamped files.

- **Sanity Checks**: The app enforces sanity checks to ensure that data integrity is maintained.

## Additional Information

- The data files are expected to be in the `/Users/mukeshbr/alpharoc_interview/data_editor/data/` directory. Make sure your data files are located there or update the `base_filename` variable in `Alpharoc_Filter_Manager.py` accordingly.

- The metadata is read from `dev_meta.csv`.

- The app allows you to select a filter to edit from the available filters in the specified directory.

- After editing, the changes are saved to the selected filter file, and a timestamped archive is created.

- If any errors occur during the editing process, the app will display an error message and prevent the updates from being saved.

## Feedback

If you encounter any issues or have suggestions for improvements, please feel free to open an issue on the [GitHub repository](https://github.com/Mukesh-BR/Streamlit-Filter-Manager).

## Contributions

Contributions to this project are welcome. Fork the repository, make your changes, and create a pull request. We appreciate your contributions!