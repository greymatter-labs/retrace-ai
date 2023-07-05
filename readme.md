# Retrace

Retrace is an open-source Mac application that allows you to search everything you've ever done on your computer.

## Features

- **Screenshot Capture**: Retrace periodically captures screenshots of your computer screen, storing them in the "history" folder.
- **Text Detection**: The captured screenshots are processed to detect text within them using Optical Character Recognition (OCR) techniques.
- **ChromaDB Integration**: The detected text and corresponding file paths are stored in a ChromaDB collection called "user-activity".
- **Natural Language Description**: Retrace prompts an AI model to generate natural language descriptions of the detected activities for better understanding.
- **User Interface**: Retrace provides a simple user interface where you can search for a specific activity description.

## Dependencies

Retrace depends on the following libraries:

- PIL: Python Imaging Library for capturing and processing screenshots.
- PyAutoGUI: Provides cross-platform capabilities to control the mouse and keyboard, required for taking screenshots.
- Quartz: Enables interaction with the Mac operating system and working with images.
- Vision: Provides powerful image analysis capabilities on macOS.
- ChromaDB: A database library for managing and querying activity data.
- Anthropyc: An AI-powered library for generating natural language descriptions.
- PyScreeze: Enables capturing screenshots in a cross-platform manner.
- DearPyGUI: A modern GUI framework for creating user interfaces.
- pynput: Allows detecting and interacting with keyboard events.

## Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage

1. Run the application by executing the following command:

```
python retrace.py
```

2. The application will start capturing screenshots and detecting activities in the background.

3. Use the provided user interface to search for specific activity descriptions.

4. Retrace will retrieve the corresponding file paths, allowing you to view the saved information easily.

5. Press the "Quit" button or the escape key to stop the application.

## Configuration

You can modify the following settings in the code (retrace.py) to customize the behavior of the application:

- `max_tokens_to_sample`: The maximum number of tokens to sample when generating natural language descriptions. Adjust this value based on your desired description length.
- `persist_directory`: The directory where ChromaDB will store the activity data. By default, it is set to a folder named "chroma" in the current directory.

## Contributions

Contributions to Retrace are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

Retrace is licensed under the APACHE 2.0 License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

Retrace was designed by Grey Matter Labs, inspired by the functionalities provided by Rewind AI. Special thanks to all the contributors and maintainers of the libraries used in this project.

## Disclaimer

Retrace is an open-source alternative to Rewind AI and is not affiliated with or endorsed by Rewind AI or any related organizations.
