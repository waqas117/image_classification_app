import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import io
import json

def load_model():
    model = models.resnet18(pretrained=True)
    model.eval()
    return model

def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    model = load_model()
    tensor = transform_image(image_bytes)
    outputs = model(tensor)
    _, predicted = torch.max(outputs, 1)
    return predicted.item()

def get_prediction_label(image_bytes):
    with open('imagenet_classes.json') as f:
        labels = json.load(f)
    predicted_class = get_prediction(image_bytes)
    return labels[predicted_class]
