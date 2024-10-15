#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
import math

# car parameters
L = 3  # Wheelbase of the car in meters
delta = 0.1  # Initial steering angle
phi = 0.01  # Steering rate
v = 2  # Speed

# state variables
x = 0
y = 0
theta = 0.0  # Heading angle

def compute_position(dt):
    global x, y, theta, delta, v

    # Update model parameters
    x_dot = v * math.cos(theta)
    y_dot = v * math.sin(theta)
    
    theta_dot = (v * math.tan(delta)) / L  # Updated with steering angle
    delta_dot = phi

    # Update states over time
    x += x_dot * dt
    y += y_dot * dt
    theta += theta_dot * dt
    delta += delta_dot * dt

    return x, y, theta

def car_kinematics():
    rospy.init_node('car_kinematics', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    # Create publishers for PoseStamped and Marker messages
    pose_pub = rospy.Publisher('/car_pose', PoseStamped, queue_size=10)
    marker_pub = rospy.Publisher('/car_marker', Marker, queue_size=10)

    t = 0.0
    dt = 0.1  # Time step

    while not rospy.is_shutdown():
        # Compute the new position and heading angle
        x, y, theta = compute_position(dt)

        # Create and publish the PoseStamped message
        pose_msg = PoseStamped()
        pose_msg.header.stamp = rospy.Time.now()
        pose_msg.header.frame_id = "map"

        # Set the position
        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y
        pose_msg.pose.position.z = 0.0  # Assume flat ground

        # Set the orientation (quaternion from theta)
        pose_msg.pose.orientation.z = math.sin(theta / 2.0)
        pose_msg.pose.orientation.w = math.cos(theta / 2.0)

        pose_pub.publish(pose_msg)

        # Create and publish the Marker message for the car visualization
        marker_msg = Marker()
        marker_msg.header.stamp = rospy.Time.now()
        marker_msg.header.frame_id = "map"
        marker_msg.ns = "car"
        marker_msg.id = 0  # Unique ID for this marker

        # Set the marker's type (CUBE, SPHERE, etc.)
        marker_msg.type = Marker.CUBE

        # Set the marker's pose (same as the car's pose)
        marker_msg.pose.position.x = x
        marker_msg.pose.position.y = y
        marker_msg.pose.position.z = 0.0
        marker_msg.pose.orientation.z = math.sin(theta / 2.0)
        marker_msg.pose.orientation.w = math.cos(theta / 2.0)

        # Set the marker's scale (size of the car)
        marker_msg.scale.x = 2.5  # Length of the car
        marker_msg.scale.y = 1.5  # Width of the car
        marker_msg.scale.z = 0.5  # Height of the car

        # Set the marker's color (RGBA)
        marker_msg.color.r = 1.0  # Red car
        marker_msg.color.g = 0.0
        marker_msg.color.b = 0.0
        marker_msg.color.a = 1.0  # Fully opaque

        # Set marker lifetime to never expire
        marker_msg.lifetime = rospy.Duration(0)

        marker_pub.publish(marker_msg)

        # Log the output for debugging, including time
        rospy.loginfo(f"Time: {rospy.Time.now().to_sec():.2f}, x: {x:.2f}, y: {y:.2f}, θ: {theta:.2f}")

        # Update time
        t += dt

        rate.sleep()

if __name__ == '__main__':
    try:
        car_kinematics()
    except rospy.ROSInterruptException:
        pass
