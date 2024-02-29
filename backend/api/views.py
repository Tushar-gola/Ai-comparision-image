from django.http import JsonResponse
from .models import Images
from .modules import __url__
from urllib.request import urlopen
import numpy as np
import requests
import os.path
import json
import cv2
# from django.contrib.auth.models import User   To get Auth models
def main(request):
    try:
        if request.method == 'GET':   # For Get Request
            id = request.GET.get('id') # To Get params data
            if id is not None:  # To Check id is not None  
                image = Images.objects.filter(id=id).values()
                if image:
                    return JsonResponse(list(image), safe=False)
                else:
                    return  JsonResponse({'error': 'Data not found'}, status=404)
            else:
                images = Images.objects.all().values()
                return JsonResponse(list(images), safe=False)
                
        elif request.method == 'POST':    # For Post Request
            data = json.loads(request.body)
            code = data.get('code')
            name = data.get('name')
            user_id = data.get('user_id')
            image = data.get('image')
            if not all([code, name, user_id, image]):
                missing_fields = [field for field, value in {'code': code, 'name': name, 'user_id': user_id, 'image': image}.items() if value is None]
                return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
            new_image = Images.objects.create(code=code, name=name, user_id=user_id, image=image)
            image_dict = {
                'code': new_image.code,
                'name': new_image.name,
                'user_id': new_image.user_id,
                'image': new_image.image,
            }
            return JsonResponse({'message': 'Data received successfully', 'data': image_dict})
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key in request body: {str(e)}'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
    
    
    


def imageModel(req):
    try:
        if req.method == "POST":
            url = __url__ + 'api/retrieve/all-ImagePath'
            response = requests.get(url)
            data = response.json()
            target_images_paths = [ur for ur in data['data'] if ur != ""]
            # Get the uploaded image
            uploaded_image = req.FILES.get('filterImage')
            if not uploaded_image:
                return JsonResponse({'error': 'No image uploaded'})

            # Read the uploaded image using OpenCV
            nparr = np.frombuffer(uploaded_image.read(), np.uint8)
            uploaded_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Check if the image is loaded successfully
            if uploaded_img is None:
                return JsonResponse({'error': 'Failed to load the uploaded image'})

            # Convert the uploaded image to grayscale
            uploaded_img_gray = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)

            # Initialize the ORB detector
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(uploaded_img_gray, None)

            # Initialize a list to store paths of similar images
            similar_images_paths = []

            for target_image_path in target_images_paths:
                target_img_url = __url__ + 'uploads/' + target_image_path
                extension = os.path.splitext(target_image_path.lower())
                if extension[1] in ('.jpg', '.jpeg', '.png'):
                    target_img_data = urlopen(target_img_url).read()
                    target_img_array = np.frombuffer(target_img_data, np.uint8)
                    target_img = cv2.imdecode(target_img_array, cv2.IMREAD_COLOR)

                    # Check if the target image is loaded successfully
                    if target_img is None:
                        print(f"Failed to load the target image: {target_image_path}")
                        continue

                    target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

                    # Detect keypoints and compute descriptors for the target image
                    kp2, des2 = orb.detectAndCompute(target_img_gray, None)

                    if des2 is not None and des1 is not None:
                        # Initialize the Brute-Force matcher
                        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

                        # Match descriptors
                        matches = bf.match(des1, des2)

                        # Sort matches by distance
                        matches = sorted(matches, key=lambda x: x.distance)
                        # Calculate similarity score
                        similarity_score = len(matches)

                        # Set a threshold for similarity score (you can adjust this)
                        threshold = 110 # Example threshold, adjust as needed
                        # If similarity score is above the threshold, add the image path to the list
                        if similarity_score >= threshold:
                            similar_images_paths.append(target_image_path)
                    else:
                        print(f"Descriptors not found for {target_image_path}")
                else:
                    print(f"Ignoring image with unsupported extension: {target_image_path}")

            return JsonResponse({'similar_images_paths': similar_images_paths})
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An error occurred while processing the request'})

    # Return a default response if the request method is not POST
    return JsonResponse({'error': 'This endpoint only supports POST requests'})




