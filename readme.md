# Retrace

Retrace is an open-source Mac application that allows you to search everything you've ever done on your computer.

## Features

- **Screenshot Capture**: Retrace periodically captures screenshots of your computer screen, storing them in the "history" folder.
- **Text Detection**: The captured screenshots are processed to detect text within them using Optical Character Recognition (OCR) techniques.
- **ChromaDB Integration**: The detected text and corresponding file paths are stored in a ChromaDB collection called "user-activity".
- **Natural Language Description**: Retrace prompts an AI model to generate natural language descriptions of the detected activities for better understanding.
- **User Interface**: Retrace provides a simple user interface where you can search for a specific activity description.

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

4. Press `command + tab` to switch out of search and click the minimized window to switch in.

5. Press the escape key to stop the application.

## Roadmap
Use a compressed video instead of images.

## Contributions

Contributions to Retrace are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

Retrace is licensed under the APACHE 2.0 License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

Retrace was designed by Grey Matter Labs, inspired by the functionalities provided by Rewind AI. Special thanks to all the contributors and maintainers of the libraries used in this project.

## Disclaimer

Retrace is an open-source alternative to Rewind AI and is not affiliated with or endorsed by Rewind AI or any related organizations.
