from flask import Flask, jsonify, send_file
import os
import io
import zipfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Directory containing your images
IMAGE_GLOBAL_DIR = 'pictures'

@app.route('/get_images/<filename>', methods=['GET'])
def get_images(filename):
    # Create a bytes buffer to hold the zip file
    zip_buffer = io.BytesIO()
    image_dir = os.path.join(IMAGE_GLOBAL_DIR, filename)
    # Create a zip file in the buffer
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename in os.listdir(image_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):  # Adjust file types as needed
                zip_file.write(os.path.join(image_dir, filename), arcname=filename)
    
    zip_buffer.seek(0)  # Go to the start of the BytesIO buffer
    zip_size_kb = len(zip_buffer.getvalue()) / 1024
    print(f"Size of the zip file: {zip_size_kb:.2f} KB")
    # Save the zip file locally
    with open('images.zip', 'wb') as f:
        f.write(zip_buffer.getvalue())
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='images.zip')


# @app.route('/images/<filename>', methods=['GET'])
# def get_images(filename):
#     # List to store image paths
#     image_paths = []

#     image_dir = os.path.join(IMAGE_DIR, filename)
#     # Collect all image file names
#     for image in os.listdir(image_dir):
#         if image.endswith(('.jpg')):  # Adjust as needed
#             image_paths.append(os.path.join(image_dir, image))

#     # Return JSON response with image paths
#     return jsonify(image_paths)

# @app.route('/image/<filename>', methods=['GET'])
# def get_images(filename):
#     return send_file(os.path.join(IMAGE_DIR, filename), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
