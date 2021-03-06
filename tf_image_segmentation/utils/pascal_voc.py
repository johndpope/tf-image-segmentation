import skimage.io as io
import numpy as np
import os


def pascal_segmentation_lut():
    """Return look-up table with number and correspondng class names
    for PASCAL VOC segmentation dataset. Two special classes are: 0 -
    background and 255 - ambigious region. All others are numerated from
    1 to 20.
    
    Returns
    -------
    classes_lut : dict
        look-up table with number and correspondng class names
    """

    class_names = ['background', 'aeroplane', 'bicycle', 'bird', 'boat',
                   'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
                   'dog', 'horse', 'motorbike', 'person', 'potted-plant',
                   'sheep', 'sofa', 'train', 'tv/monitor', 'ambigious']
    
    enumerated_array = enumerate(class_names[:-1])
    
    classes_lut = list(enumerated_array)
    
    # Add a special class representing ambigious regions
    # which has index 255.
    classes_lut.append((255, class_names[-1]))
    
    classes_lut = dict(classes_lut)

    return classes_lut


def get_pascal_segmentation_images_lists_txts(pascal_root):
    """Return full paths to files in PASCAL VOC with train and val image name lists.
    This function returns full paths to files which contain names of images
    and respective annotations for the segmentation in PASCAL VOC.
    
    Parameters
    ----------
    pascal_root : string
        Full path to the root of PASCAL VOC dataset.
    
    Returns
    -------
    full_filenames_txts : [string, string, string]
        Array that contains paths for train/val/trainval txts with images names.
    """
    
    segmentation_images_lists_relative_folder = 'ImageSets/Segmentation'
    
    segmentation_images_lists_folder = os.path.join(pascal_root,
                                                    segmentation_images_lists_relative_folder)
    
    pascal_train_list_filename = os.path.join(segmentation_images_lists_folder,
                                              'train.txt')

    pascal_validation_list_filename = os.path.join(segmentation_images_lists_folder,
                                                   'val.txt')
    
    pascal_trainval_list_filname = os.path.join(segmentation_images_lists_folder,
                                                'trainval.txt')
    
    return [
            pascal_train_list_filename,
            pascal_validation_list_filename,
            pascal_trainval_list_filname
           ]


def readlines_with_strip(filename):
    """Reads lines from specified file with whitespaced removed on both sides.
    The function reads each line in the specified file and applies string.strip()
    function to each line which results in removing all whitespaces on both ends
    of each string. Also removes the newline symbol which is usually present
    after the lines wre read using readlines() function.
    
    Parameters
    ----------
    filename : string
        Full path to the root of PASCAL VOC dataset.
    
    Returns
    -------
    clean_lines : array of strings
        Strings that were read from the file and cleaned up.
    """
    
    # Get raw filnames from the file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Clean filenames from whitespaces and newline symbols
    clean_lines = map(lambda x: x.strip(), lines)
    
    return clean_lines


def readlines_with_strip_array_version(filenames_array):
    """The function that is similar to readlines_with_strip() but for array of filenames.
    Takes array of filenames as an input and applies readlines_with_strip() to each element.
    
    Parameters
    ----------
    array of filenams : array of strings
        Array of strings. Each specifies a path to a file.
    
    Returns
    -------
    clean_lines : array of (array of strings)
        Strings that were read from the file and cleaned up.
    """
    
    multiple_files_clean_lines = map(readlines_with_strip, filenames_array)
    
    return multiple_files_clean_lines


def add_full_path_and_extention_to_filenames(filenames_array, full_path, extention):
    """Concatenates full path to the left of the image and file extention to the right.
    The function accepts array of filenames without fullpath and extention like 'cat'
    and adds specified full path and extetion to each of the filenames in the array like
    'full/path/to/somewhere/cat.jpg.
    Parameters
    ----------
    filenames_array : array of strings
        Array of strings representing filenames
    full_path : string
        Full path string to be added on the left to each filename
    extention : string
        Extention string to be added on the right to each filename
    Returns
    -------
    full_filenames : array of strings
        updated array with filenames
    """
    full_filenames = map(lambda x: os.path.join(full_path, x) + '.' + extention, filenames_array)
    
    return full_filenames


def add_full_path_and_extention_to_filenames_array_version(filenames_array_array, full_path, extention):
    """Array version of the add_full_path_and_extention_to_filenames() function.
    Applies add_full_path_and_extention_to_filenames() to each element of array.
    Parameters
    ----------
    filenames_array_array : array of array of strings
        Array of strings representing filenames
    full_path : string
        Full path string to be added on the left to each filename
    extention : string
        Extention string to be added on the right to each filename
    Returns
    -------
    full_filenames : array of array of strings
        updated array of array with filenames
    """
    result = map(lambda x: add_full_path_and_extention_to_filenames(x, full_path, extention),
                 filenames_array_array)
    
    return result


def get_pascal_segmentation_image_annotation_filenames_pairs(pascal_root):
    """Return (image, annotation) filenames pairs from PASCAL VOC segmentation dataset.
    Returns three dimensional array where first dimension represents the type
    of the dataset: train, val or trainval in the respective order. Second
    dimension represents the a pair of images in that belongs to a particular
    dataset. And third one is responsible for the first or second element in the
    dataset.
    Parameters
    ----------
    pascal_root : string
        Path to the PASCAL VOC dataset root that is usually named 'VOC2012'
        after being extracted from tar file.
    Returns
    -------
    image_annotation_filename_pairs : 
        Array with filename pairs.
    """
    
    pascal_relative_images_folder = 'JPEGImages'
    pascal_relative_class_annotations_folder = 'SegmentationClass'
    
    images_extention = 'jpg'
    annotations_extention = 'png'
    
    pascal_images_folder = os.path.join(pascal_root, pascal_relative_images_folder)
    pascal_class_annotations_folder = os.path.join(pascal_root, pascal_relative_class_annotations_folder)
    
    pascal_images_lists_txts = get_pascal_segmentation_images_lists_txts(pascal_root)
    
    pascal_image_names = readlines_with_strip_array_version(pascal_images_lists_txts)
    
    images_full_names = add_full_path_and_extention_to_filenames_array_version(pascal_image_names,
                                                                               pascal_images_folder,
                                                                               images_extention)
    
    annotations_full_names = add_full_path_and_extention_to_filenames_array_version(pascal_image_names,
                                                                                    pascal_class_annotations_folder,
                                                                                    annotations_extention)
    
    # Combine so that we have [(images full filenames, annotation full names), .. ]
    # where each element in the array represent train, val, trainval sets.
    # Overall, we have 3 elements in the array.
    temp = zip(images_full_names, annotations_full_names)
    
    # Now we should combine the elements of images full filenames annotation full names
    # so that we have pairs of respective image plus annotation
    # [[(pair_1), (pair_1), ..], [(pair_1), (pair_2), ..] ..]
    # Overall, we have 3 elements -- representing train/val/trainval datasets
    image_annotation_filename_pairs = map(lambda x: zip(*x), temp)
    
    return image_annotation_filename_pairs