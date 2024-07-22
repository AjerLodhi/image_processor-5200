Image Processor 
Overview
A comprehensive image processing tool. This project leverages Python with the pillow library to provide a robust set of image manipulation features, including flipping, rotating, resizing, and converting images to grayscale. The application is built with a modular architecture, ensuring extensibility and maintainability. The image processing system follows a Pipe and Filter architecture, where data flows through a series of processing components sequentially. Each component performs a specific image processing operation, and the system is designed to be modular and extensible.
 
Components:
1) User Interface: Responsible for accepting user input, uploading images, and displaying processed images.
2) Backend Server: Handles HTTP requests from the user interface and coordinates the image processing operations.
3) Image Processing Components: A set of individual components responsible for performing specific image processing operations highlighted below.

API:

The API is designed to use RPC, where the client sends the image along with a list of
 operations to be performed in a single request. This ensures that only one round-trip to the
 server is required, regardless of the number of image operations requested.
 API Endpoint:
 1) POST/process-image: Accepts an image file along with a JSON payload specifying the operations to be performed. In this case, the image flips vertically, rotated by 90 degrees, and converted to grayscale. It then returns the processed image file.
 2) Sample JSON Payload:
  {
 "image": "<base64_encoded_image_data>",
 "operations": [
 {"operation": "flip_vertical"},
 {"operation": "rotate", "angle": 90},
 {"operation": "convert_to_grayscale"}
 ]
 The expected response:
 {
 "status": "success",
 "processed_image": "<base64_encoded_processed_image_data>",
 "message": "Image processed successfully."

Features:
1) Flip Images: Horizontally and vertically.
2) Rotate Images: Rotate images by any degree.
3) Grayscale Conversion: Convert images to grayscale.
4) Resize Images: Resize images to specified dimensions.
5) Thumbnail Generation: Create thumbnails of images.
6) Rotate Left/Right: Rotate images left or right by 90 degrees.

Prerequisites:
1) .NET 5.0 or higher
2) Visual Studio 2019 or higher

Installation:
1) Clone the repository: git clone https://github.com/AjerLodhi/image_processor-5200.git
2)  Open the solution file image_processor.sln in Visual Studio.
3)   Build the solution to restore the necessary packages and dependencies.

Usage:
1) Run the application from Visual Studio.
2) Use the GUI to upload an image and apply the desired transformations.
3) Save the processed image to your local machine.

Code Structure:
1) Controllers: Handles the user interface and interaction.
2) Services: Contains the business logic for image processing.
3) Utilities: Helper functions for common tasks.
4) Models: Data models representing images and their properties.

Contribution: 
Contributions are welcome! Please fork the repository and create a pull request with your changes.

Contact: 
For any inquiries or feedback, please contact Ajer Lodhi at [your email].
