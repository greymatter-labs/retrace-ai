import random
import threading
import time
from typing import List, Optional
import PIL
import pyautogui
import objc
import time

import Quartz
from Cocoa import NSURL
from Foundation import NSDictionary
from PIL import Image
import Vision
import chromadb
from chromadb.config import Settings
import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import pyscreeze
import dearpygui.dearpygui as dpg
from pynput import keyboard


__PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
os.environ["TOKENIZERS_PARALLELISM"] = "false"
pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION

def call_anthropic(prompt):
    prompt = f"{prompt}\nReturn a natural language description of what the user is working on or doing. Use the format: 'The user is working on...''"
    anthropic = Anthropic(api_key="ENTER_YOUR_KEY")
    completion = anthropic.completions.create(
        model="claude-instant-v1",
        max_tokens_to_sample=300,
        prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
    )
    return completion.completion

# Set up the Chroma client
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="chroma" # Optional, defaults to .chromadb/ in the current directory
))

activity = client.get_or_create_collection(name="user-activity")

def get_file_path(description):
    # Query the collection with a description to get corresponding file path
    results = activity.query(query_texts=[description], n_results=1)
    return results["ids"][0]  # Return file path

def take_screenshot(path):
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    screenshot = screenshot.crop((0, height * 0.05, width, height * 0.95))
    screenshot.save(path)
    return path

def detect_text(img_path: str, orientation: Optional[int] = None) -> List:
    # Code for text detection from images
    with objc.autorelease_pool():
        input_url = NSURL.fileURLWithPath_(img_path)
        input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)
        vision_options = NSDictionary.dictionaryWithDictionary_({})

        vision_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(input_image, vision_options) if orientation is None else Vision.VNImageRequestHandler.alloc().initWithCIImage_orientation_options_(input_image, orientation, vision_options)

        results = []
        handler = make_request_handler(results)
        vision_request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(handler)
        vision_handler.performRequests_error_([vision_request], None)

        vision_request.dealloc()
        vision_handler.dealloc()

        for result in results:
            result[0] = str(result[0])

        return results 

def make_request_handler(results):
    # Code for creating request handler
    def handler(request, error):
        if error:
            print(f"Error! {error}")
        else:
            observations = request.results()
            for text_observation in observations:
                recognized_text = text_observation.topCandidates_(1)[0]
                results.append([recognized_text.string(), recognized_text.confidence()])

    return handler
should_continue = threading.Event()
should_continue.set()
def main_loop():
    while should_continue.is_set():
        print("NEW ITERATION")
        datetime = time.strftime("%Y%m%d-%H%M%S")
        image_path = take_screenshot("history/"+datetime + ".png")
        text_boxes = detect_text(image_path)
        if text_boxes:
            text = "".join([box[0] + "<split>" for box in text_boxes])
            chunks = text.split("<split>")
            length = len(chunks)
            chunks = [chunks[i:i+int(length/6)] for i in range(0, length, int(length/6))]

            full_response = ""
            for chunk in chunks:
                input_text = " ".join(chunk)
                response = input_text
                full_response += response + "\n"
            full_response = call_anthropic(full_response)
            activity.add(documents=[full_response], ids=[image_path])

def get_path():
    # Perform a search based on user input in the UI
    description = dpg.get_value("SearchInput")
    file_path = get_file_path(description)
    return file_path[0]
def setup_ui():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.toggle_viewport_fullscreen()

    def update_image(path):
        # Load the image
        width, height, channels, data = dpg.load_image(path)

        # Generate a unique tag for this texture
        texture_tag = f"texture_{path}"

        # Add the image to the texture registry if it does not exist already
        if not dpg.does_item_exist(texture_tag):
            with dpg.texture_registry():
                dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_tag)

        # Clear the child window before adding a new image
        dpg.delete_item("image_holder", children_only=True)

        # Create a new image widget with the new texture
        image_tag = f"image_{time.time()}"
        dpg.add_image(texture_tag, parent="image_holder", tag=image_tag)

    with dpg.window(label="Main Window") as main_window:
        dpg.add_input_text(label="Search Description", tag="SearchInput")
        dpg.add_button(label="Search", callback=lambda: update_image(get_path()))
        dpg.add_text("Search Result:")
        dpg.add_text(default_value="", tag="SearchOutput")
        dpg.add_child_window(parent=main_window, tag="image_holder")
        dpg.add_button(label="Quit", callback=dpg.stop_dearpygui)
    #takes screenshot to get screen size
    datetime = time.strftime("%Y%m%d-%H%M%S")
    image_path = take_screenshot("history/"+datetime + ".png")
    screen_width, screen_height, channels, data = dpg.load_image(image_path)
    
    print(f"Screen width: {screen_width}, Screen height: {screen_height}")

    dpg.configure_item(main_window, width=screen_width, height=screen_height)
    dpg.show_viewport()
    dpg.start_dearpygui()

    while dpg.is_dearpygui_running():
        time.sleep(0.01)

    dpg.destroy_context()

def on_key_release(key):
    if key == keyboard.Key.esc:
        dpg.stop_dearpygui()

def main():
    # Start the main loop in a separate thread
    main_thread = threading.Thread(target=main_loop, daemon=True)
    main_thread.start()

    # Create a listener for the escape key
    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()

    # Set up UI
    setup_ui()

if __name__ == "__main__":
    main()
