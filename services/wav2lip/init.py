from torch.utils.model_zoo import load_url
from face_detection.detection.sfd.sfd_detector import models_urls

if __name__ == "__main__":
    model_weights = load_url(models_urls['s3fd'])
