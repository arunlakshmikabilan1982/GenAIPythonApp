# convert the image into base64 string

1. Encode the image with base64 it will convert image into bytes to convert use the **image_to_bytes.py** file

2. After Encoding that use the String to pass through your post request method in json format as below.

   ```
   json
   ---------------------------------------------
        {
            "image": 'your_base64_string'
        }
   ```
