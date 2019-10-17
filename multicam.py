import pyrealsense2 as rs
import numpy as np
import cv2
import logging


# Configure depth and color streams...
# from Camera 1
# print("pipeline1")
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device('123456789012') # add your serial number
# if you use USB2.0 keep in mind the right resolution: https://www.intelrealsense.com/usb2-support-for-intel-realsense-technology/
config_1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# from Camera 2
# print("pipeline2")
pipeline_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device('123456789012') # add your serial number
config_2.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config_2.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)


# Start streaming from both cameras
pipeline_1.start(config_1)
pipeline_2.start(config_2)

try:

    # Skip 35 first frames to give the Auto-Exposure time to adjust
    for x in range(35):
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipeline_1.wait_for_frames()
        frames_2 = pipeline_2.wait_for_frames()

    #print("config_camera1")
    # Camera 1

    # Store next frameset for later processing, otherwise underexpose image
    frames_1 = pipeline_1.wait_for_frames()
    frames_2 = pipeline_2.wait_for_frames()

    depth_frame_1 = frames_1.get_depth_frame()
    color_frame_1 = frames_1.get_color_frame()

    # Convert images to numpy arrays
    depth_image_1 = np.asanyarray(depth_frame_1.get_data())
    color_image_1 = np.asanyarray(color_frame_1.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.5), cv2.COLORMAP_JET)

    #print("config_camera2")
    # Camera 2

    depth_frame_2 = frames_2.get_depth_frame()
    color_frame_2 = frames_2.get_color_frame()

    # Convert images to numpy arrays
    depth_image_2 = np.asanyarray(depth_frame_2.get_data())
    color_image_2 = np.asanyarray(color_frame_2.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.5), cv2.COLORMAP_JET)

    # Stack all images horizontally
    images = np.hstack((color_image_1, depth_colormap_1,color_image_2, depth_colormap_2))

    #print("save images")
    # write images
    cv2.imwrite("my_image_1.jpg",color_image_1)
    cv2.imwrite("my_depth_1.jpg",depth_colormap_1)
    cv2.imwrite("my_image_2.jpg",color_image_2)
    cv2.imwrite("my_depth_2.jpg",depth_colormap_2)
    print ("imges stored")


finally:

    # Stop streaming
    pipeline_1.stop()
    pipeline_2.stop()
