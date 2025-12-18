import os
# Standard Python module (not used in this file, but safe to keep if paths are added later)

from launch import LaunchDescription
# LaunchDescription is the main container that holds all launch actions

from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
# DeclareLaunchArgument: allows parameters to be set from the command line
# IncludeLaunchDescription: allows inclusion of another launch file

from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
# LaunchConfiguration: accesses values of launch arguments at runtime
# PathJoinSubstitution: safely constructs filesystem paths

from launch_ros.substitutions import FindPackageShare
# FindPackageShare: locates the share directory of a ROS 2 package


def generate_launch_description():
    """
    This function is the entry point for the ROS 2 launch system.
    It returns a LaunchDescription object containing all launch actions.
    """

    # Find the share directory of the 'erl1' package
    pkg_erl1 = FindPackageShare('erl1')

    # Construct the default RViz configuration file path:
    # <erl1>/rviz/urdf.rviz
    default_rviz_config_path = PathJoinSubstitution(
        [pkg_erl1, 'rviz', 'urdf.rviz']
    )

    # Declare a launch argument to enable or disable the
    # joint_state_publisher GUI DENNE SOM STARTER RVIZ GREIA
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui'
    )

    # Declare a launch argument for the RViz configuration file
    rviz_arg = DeclareLaunchArgument(
        name='rvizconfig',
        default_value=default_rviz_config_path,
        description='Absolute path to RViz config file'
    )

    # Declare a launch argument specifying which URDF file to load
    # This file is expected to live in:
    # <erl1>/urdf/<model>
    model_arg = DeclareLaunchArgument(
        'model',
        default_value='erl1.urdf',
        description='Name of the URDF description to load'
    )

    # Include the standard URDF display launch file from the
    # 'urdf_launch' package
    #
    # This launch file:
    #  - Loads the URDF
    #  - Starts robot_state_publisher
    #  - Starts joint_state_publisher (optionally with GUI)
    #  - Starts RViz with the provided configuration
    urdf = IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare('urdf_launch'),
            'launch',
            'display.launch.py'
        ]),
        launch_arguments={
            # Name of the package containing the URDF
            'urdf_package': 'erl1',

            # Path to the URDF file inside the package
            'urdf_package_path': PathJoinSubstitution([
                'urdf',
                LaunchConfiguration('model')
            ]),

            # RViz configuration file to use
            'rviz_config': LaunchConfiguration('rvizconfig'),

            # Enable or disable joint_state_publisher_gui
            'jsp_gui': LaunchConfiguration('gui')
        }.items()
    )

    # Create the main LaunchDescription object
    launchDescriptionObject = LaunchDescription()

    # Add all declared launch arguments
    launchDescriptionObject.add_action(gui_arg)
    launchDescriptionObject.add_action(rviz_arg)
    launchDescriptionObject.add_action(model_arg)

    # Add the included URDF + RViz launch file
    launchDescriptionObject.add_action(urdf)

    # Return the complete launch description
    return launchDescriptionObject
