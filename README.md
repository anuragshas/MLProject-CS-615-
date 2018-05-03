## Requirements
 - tensorflow-gpu==1.3
 - keras==2.0.8
 - imgaug
 - opencv-python
 - h5py
 - pyqt==5.6
 - pickle
 - tqdm


## For Training and Validation
#####   Open Yolo.ipynb in jupyter notebook and follow below instruction

+ Initialization
    + Download COCO detection data from http://cocodataset.org/#download
        + http://images.cocodataset.org/zips/train2014.zip <= train images
        + http://images.cocodataset.org/zips/val2014.zip <= validation images
        + http://images.cocodataset.org/annotations/annotations_trainval2014.zip <= train and validation annotations
    + Run this script in terminal to convert annotations in COCO format to VOC format
        + ```python coco2pascal.py```
    + Download pre-trained weights from https://drive.google.com/file/d/1yUW7b1gAp0GecJf1NH8KvcXaRL0ZmaFN/view?usp=sharing
    + Specify the directory of train annotations (train_annot_folder) and train images (train_image_folder)
    + Specify the directory of validation annotations (valid_annot_folder) and validation images (valid_image_folder)
    + Specity the path of pre-trained weights by setting variable *wt_path*
+ Load the pretrained weights
+ Perform training 


## For Application
 - Download file of trained weights with 9 classes(person, bicycle, car, motorcycle, bus, train, truck, traffic light, stop sign)
https://drive.google.com/file/d/1aAqhRy4OnaQgNP8HausSyPZmF-8E57Vj/view?usp=sharing

 - run this in terminal for the application
```python obj2.py```



##### Note:: Some Sample images and videos included for testing in ```images``` folder

For any issues email at anuragsingh@iiitdmj.ac.in