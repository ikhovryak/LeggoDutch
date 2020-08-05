import torch
import torchvision

print(torch.cuda.is_available)
print(torch.cuda.get_device_properties(0))
print(torch.cuda.get_device_capability(0))