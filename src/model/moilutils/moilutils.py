import datetime
import os
import shutil
import cv2
import numpy as np
import pyexiv2
from .moildev import Moildev
import json
from .camera_source import CameraSource
from .camera_parameter import CameraParametersForm
from .camera_type import camera_type

try:
    from PyQt6 import QtWidgets, QtCore, QtGui

    pyqt_version = "pyqt6"

except:
    from PyQt5 import QtWidgets, QtCore, QtGui

    pyqt_version = "pyqt5"

database_camera_parameters = "camera_parameters.json"


def select_type_camera(theme="dark"):
    """
    Generate a dialog for camera selection and return the name of the camera selected.

    Args:
        theme:
            dark mode
    Returns:
        camera name

    .. code-block: python

        type_camera = mutils.select_type_camera()

    """
    camera_name = camera_type(database_camera_parameters, theme)
    return camera_name


def select_source_camera():
    """
    Generate a dialog for usb/web camera source selection and detection.
    You can get available camera sources using the detection button on the dialog.

    Returns:
        Port number for usb cameras or the source link for web cameras

    .. code-block: python

        cam_source = mutils.select_source_camera()
    """
    open_cam_source = QtWidgets.QDialog()
    source_cam = CameraSource(open_cam_source)
    open_cam_source.exec()
    return source_cam.camera_source


def form_camera_parameter():
    """
    Generate a dialog for camera parameters setting.

    """
    open_cam_params = QtWidgets.QDialog()
    CameraParametersForm(open_cam_params, database_camera_parameters)
    open_cam_params.exec()


def show_image_to_label(label, image, width, angle=0, plusIcon=False, scale_content=False):
    """
    Display an image to the label widget on the user interface.

    Args:
        label: destination label
        image: image to show
        width: width for resizing the image while keeps the original aspect ratio
        angle: rotation angle for the image
        plusIcon: whether to show a plus icon at the center of the image
        scale_content: whether to make the image displayed follow the label size

    Returns:
        None. Shows image on the label.

    - Example:

    .. code-block:: python

        MoilUtils.showImageToLabel(label, image, 400, angle=0, plusIcon=False, scale_content=False)
    """
    if scale_content is True:
        label.setScaledContents(True)

    else:
        label.setScaledContents(False)
        height = calculate_height(image, width)
        image = resize_image(image, width)
        label.setMinimumSize(QtCore.QSize(width, height))
        label.setMaximumSize(QtCore.QSize(width, height))

    image = rotate_image(image, angle)
    if plusIcon:
        # draw plus icons on image and show to label
        h, w = image.shape[:2]
        w1 = round((w / 2) - 10)
        h1 = round(h / 2)
        w2 = round((w / 2) + 10)
        h2 = round(h / 2)
        w3 = round(w / 2)
        h3 = round((h / 2) - 10)
        w4 = round(w / 2)
        h4 = round((h / 2)) + 10
        draw_line(image, w1, h1, w2, h2)
        draw_line(image, w3, h3, w4, h4)

    image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                         QtGui.QImage.Format.Format_RGB888).rgbSwapped()
    label.setPixmap(QtGui.QPixmap.fromImage(image))


def connect_to_moildev(type_camera, camera_parameter=None, parent=None):
    """
    Return a Moildev instance for a specific type of camera.

    Args:
        type_camera: name of camera (You can use 'select_type_camera()' to get the name.)
        camera_parameter: parameter of the camera
        parent: None

    Returns:
        Moildev instance

    .. code-block:: python

        c_type = mutils.select_type_camera()
        moildev_camera1 = mutils.connect_to_moildev(type_camera=c_type)
    """
    if camera_parameter is None:
        try:
            moildev = Moildev(database_camera_parameters, type_camera)
        except:
            QtWidgets.QMessageBox.warning(
                parent,
                "Warning!!",
                "The image not support for this application, \n\nPlease contact developer!!")
            print("the image not support for this application, please contact developer!!")
            moildev = None

    else:
        try:
            moildev = Moildev(camera_parameter, type_camera)
        except:
            QtWidgets.QMessageBox.warning(
                parent,
                "Warning!!",
                "The image not support for this application, \n\nPlease contact developer!!")
            print("the image not support for this application, please contact developer!!")
            moildev = None

    return moildev


def check_usb_camera_available():
    """
    Detect the USB camera port available for image/video capture.

    Returns:
            A list of indices of available camera source.
    """
    all_camera_idx_available = []
    for camera_idx in range(5):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            all_camera_idx_available.append(camera_idx)
            cap.release()

    return all_camera_idx_available


def read_image(image_path):
    """
    Load an image from the specified file path (use the cv2.imread function).
    If the image cannot be read (because of missing file, improper permissions, unsupported or invalid format)，
    this method raises an error.

    Args:
        image_path : image file path

    return:
        Image: loaded image in numpy ndarray format

    - Example:

    .. code-block:: python

        image = read_image('image_path')
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("`{}` cannot be loaded".format(image_path))
    return image


def remap_image(image, map_x, map_y):
    """
    Take an image and a pair of X-Y maps generated by a Moildev instance as inputs,
     then return a remapped image using the maps.

    Args:
        image: input image
        map_x: mapping function in the x direction.
        map_y: mapping function in the y direction.

    Returns:
        image: remapped image, typically it would be an anypoint image or a panorama image.

    - Example:

    .. code-block:: python

        image_anypoint = remap_image(image, mapX_anypoint, mapY_anypoint)
    """
    image = cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
    return image


def select_file(parent=None, title="Open file", dir_path=".", file_filter=""):
    """
    Generate a dialog for file selection and return the path of the
    file selected. If no file is selected, an empty string is returned.

    Args:
        parent: parent windows of the dialog
        title: dialog title
        file_filter: filters for specific file types
        dir_path: dialog's working directory

    return:
        path of the file selected.

    - Example:

    .. code-block:: python

        path_img = mutils.select_file(dir_path="./", file_filter='*.jpg')
    """
    if pyqt_version == "pyqt6":
        option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, dir_path,
                                                             file_filter, options=option)
    else:
        options = QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, dir_path,
                                                             file_filter,
                                                             options=options)
    return file_path


def select_directory(parent=None, title='Select Folder'):
    """
    Generate a dialog for directory selection and return the path of the directory
    selected. If no directory is selected, an empty string is returned.


    Returns:
        path of the directory selected

    - Example:

    .. code-block:: python

        path_dir = mutils.select_file()
    """
    if pyqt_version == "pyqt6":
        option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(parent, title, options=option)
    else:
        option = QtWidgets.QFileDialog.DontUseNativeDialog
        directory = QtWidgets.QFileDialog.getExistingDirectory(parent, title, options=option)
    return directory


def copy_directory(src_directory, dst_directory):
    """
    Recursively copy a whole directory to the destination directory.

    Args:
        src_directory: path of the source folder
        dst_directory: path of the destination directory

    Returns:
        None

    - Example:

    .. code-block:: python

        path_source = mutils.select_directory()
        mutils.copy_directory(path_source, '/home')

    """
    directoryName = os.path.basename(src_directory)
    destinationPath = os.path.join(dst_directory, directoryName)
    shutil.copytree(src_directory, destinationPath)


def resize_image(image, width):
    """
    Resize an image to one with a given width while maintaining its original aspect ratio and
    return it.

    Args:
        image: input image
        width: desired image width

    Returns:
        resized image

    """
    h, w = image.shape[:2]
    r = width / float(w)
    hi = round(h * r)
    result = cv2.resize(image, (width, hi),
                        interpolation=cv2.INTER_AREA)
    return result


def rotate_image(src, angle, center=None, scale=1.0):
    """
    Return an image after rotation and scaling(not resizing).
    Args:
        src: input image
        angle: rotation angle
        center: coordinate of the rotation center. By default, it's the image center.
        scale: scaling factor

    Returns:

        rotated image

    - Example:

    .. code-block:: python

        image = mutils.rotate_image(image, 90, center=(20,25))
    """
    h, w = src.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    m = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(src, m, (w, h))
    return rotated


def calculate_height(image, width):
    """
    Return the aspect ratio keeping height for a given image width

    Args:
        image: input image
        width: desired image width

    Returns:
        image height

    - Example:

    .. code-block:: python

        height = calculate_height(image, 140)
    """

    h, w = image.shape[:2]
    r = width / float(w)
    height = round(h * r)
    return height


def draw_polygon(image, mapX, mapY):
    """
    Return image with a drawn polygon indicating the remapped area given an anypoint map pair.

    Args:
        image: input image
        mapX: anypoint mapX
        mapY: anypoint mapY

    return:
        image with a polygon

    - Example:

    .. code-block:: python

        img = mutils.read_image('sample_image.jpg')
        c_type = mutils.select_type_camera()
        m_instance = mutils.connect_to_moildev(type_camera=c_type)
        mx, my = m_instance.maps_anypoint(0, -90, 4)
        img = mutils.draw_polygon(img, mx, my)

    """
    hi, wi = image.shape[:2]
    X1 = []
    Y1 = []
    X2 = []
    Y2 = []
    X3 = []
    Y3 = []
    X4 = []
    Y4 = []

    x = 0
    while x < wi:
        a = mapX[0,]
        b = mapY[0,]
        ee = mapX[-1,]
        f = mapY[-1,]

        if a[x] == 0. or b[x] == 0.:
            pass
        else:
            X1.append(a[x])
            Y1.append(b[x])

        if f[x] == 0. or ee[x] == 0.:
            pass
        else:
            Y3.append(f[x])
            X3.append(ee[x])
        x += 10

    y = 0
    while y < hi:
        c = mapX[:, 0]
        d = mapY[:, 0]
        g = mapX[:, -1]
        h = mapY[:, -1]

        # eliminate the value 0 for map X
        if d[y] == 0. or c[y] == 0.:  # or d[y] and c[y] == 0.0:
            pass
        else:
            Y2.append(d[y])
            X2.append(c[y])

        # eliminate the value 0 for map Y
        if h[y] == 0. or g[y] == 0.:
            pass
        else:
            Y4.append(h[y])
            X4.append(g[y])

        # render every 10 times, it will be like 1, 11, 21 and so on.
        y += 10

    p = np.array([X1, Y1])
    q = np.array([X2, Y2])
    r = np.array([X3, Y3])
    s = np.array([X4, Y4])
    points = p.T.reshape((-1, 1, 2))
    points2 = q.T.reshape((-1, 1, 2))
    points3 = r.T.reshape((-1, 1, 2))
    points4 = s.T.reshape((-1, 1, 2))

    # Draw polyline on original image
    cv2.polylines(image, np.int32([points]), False, (0, 0, 255), 10)
    cv2.polylines(image, np.int32([points2]), False, (255, 0, 0), 10)
    cv2.polylines(image, np.int32([points3]), False, (0, 255, 0), 10)
    cv2.polylines(image, np.int32([points4]), False, (0, 255, 0), 10)
    return image


def write_camera_type(image_file, type_camera):
    """
    Write the camera type into the image's metadata.

    Args:
        image_file: image file path
        type_camera: name of camera

    Returns:
        None

    .. code-block::

        mutils.write_camera_type('sample_image.jpg', 'Camera_name')

    """
    img = pyexiv2.Image(image_file)
    pyexiv2.registerNs('a namespace for image', 'Image')
    img.modify_xmp({'Xmp.Image.cameraName': type_camera})
    img.close()


def read_camera_type(image_file):
    """
    Read the camera type from image's metadata.

    Args:
        image_file: image file path

    Returns:
        camera type

    .. code-block::

        c_type = mutils.read_camera_type('sample_image.jpg')

    """
    img = pyexiv2.Image(image_file)
    try:
        camera_type = img.read_xmp()['Xmp.Image.cameraName']

    except:
        camera_type = None
    img.close()
    return camera_type


def draw_point(image, coordinate_point, radius=5):
    """
    Draw a point in the image and return it.

    Args:
        image: input image
        coordinate_point (): point coordinate (x, y)
        radius: size of the point (scale by radius)

    Returns:
        image with points drawn

    .. code-block::

        img = mutils.read_image('sample_image.jpg')
        img = mutils.draw_point(img, (400, 400), 6)

    """

    if coordinate_point is not None:
        w, h = image.shape[:2]
        if h >= 1000:
            cv2.circle(image, coordinate_point, radius, (200, 5, 200), 30, -1)
        else:
            cv2.circle(image, coordinate_point, radius, (200, 5, 200), -1)
    return image


def save_image(image, dst_directory, type_camera=None):
    """
    Save an image to a directory and write the camera type into its metadata if the type is given.
    The file name would be the date and time when the image is saved.

    Args:
        image: input image
        dst_directory: destination directory path
        type_camera: camera type

    Returns:
        file name

    .. code-block::

        save_image(img, '.', 'camera_1')

    """
    ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
    name = dst_directory + "/" + str(ss) + ".png"
    cv2.imwrite(name, image)
    if type_camera is not None:
        write_camera_type(name, type_camera)
    return ss


def draw_line(image, coordinatePoint_1=None, coordinatePoint_2=None):
    """
    Draw a line on the image from the coordinate given.
    If no coordinate is given, it draws lines on image margins.

    Args:
        image: input image
        coordinatePoint_1: point 1 coordinate (x, y)
        coordinatePoint_2: point 2 coordinate (x, y)

    Returns:
        image with a line drawn

    .. code-block::

        img = mutils.draw_line(img, (300, 300), (300, 400) )

    """
    # draw anypoint line
    if coordinatePoint_1 is None:
        h, w = image.shape[:2]
        if h >= 1000:
            cv2.line(image, (0, 0), (0, h), (255, 0, 0), 10)
            cv2.line(image, (0, 0), (w, 0), (0, 0, 255), 10)
            cv2.line(image, (0, h), (w, h), (0, 255, 0), 10)
            cv2.line(image, (w, 0), (w, h), (0, 255, 0), 10)
        else:
            cv2.line(image, (0, 0), (0, h), (255, 0, 0), 2)
            cv2.line(image, (0, 0), (w, 0), (0, 0, 255), 2)
            cv2.line(image, (0, h), (w, h), (0, 255, 0), 2)
            cv2.line(image, (w, 0), (w, h), (0, 255, 0), 2)
    else:
        # this for draw line on image
        cv2.line(image, coordinatePoint_1, coordinatePoint_2, (0, 255, 0), 1)
    return image


def calculate_ratio_image2label(label, image):
    """
    Calculate the width and height ratio of the image to a label.

    Args:
        label : UI label
        image : input image

    Returns:
        width ratio and height ratio

    .. code-block::

        w_ratio, h_ratio = mutils.calculate_ratio_image2label(label, img)

    """
    h = label.height()
    w = label.width()
    height, width = image.shape[:2]
    ratio_x = width / w
    ratio_y = height / h
    return ratio_x, ratio_y


def cropping_image(image, right, bottom, left, top):
    """
    Crop an image by ratio from every side.

    Args:
        image: input image
        right: ratio of right side (1-0)
        bottom: ratio of bottom side (1-0)
        left: ratio of left side (0-1)
        top: ratio of top side (0-1)

    Returns:
        image has already cropping

    """
    a_right = round(image.shape[1] * right)
    a_bottom = round(image.shape[0] * bottom)
    a_left = round(image.shape[1] * left)
    a_top = round(image.shape[0] * top)
    return image[a_top:a_top + a_bottom, a_left:a_left + a_right]


def draw_list_point_with_text(image, coordinate_point, radius=5):
    """
    Draw points and their indices on the image.

    Args:
        image: input image
        coordinate_point: a list of points' coordinates
        radius: point radius

    Returns:
        image with the point and their sequences drawn.

    .. code-block::

        points_to_draw = [(100, 250), (200, 200), (450, 0)]
        img = mutils.draw_list_point_with_text(img, points_to_draw, radius=3)

    """

    if coordinate_point is not None:
        for i in range(len(coordinate_point)):
            image = cv2.putText(image, str(i + 1), tuple(coordinate_point[i]), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (200, 5, 5), 3, cv2.LINE_AA)
            cv2.circle(image, tuple(coordinate_point[i]), radius, (200, 5, 200), 20, -1)
    return image
