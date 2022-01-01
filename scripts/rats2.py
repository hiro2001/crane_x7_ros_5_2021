#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
import time
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Int32


def main():
    rospy.init_node("pose_groupstate_example")
    #sub = rospy.Subscriber('point_x', Int32, callback)
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.75)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)

    print("Group names:")
    print(robot.get_group_names())

    print("Current state:")
    print(robot.get_current_state())

    # アーム初期ポーズを表示
    arm_initial_pose = arm.get_current_pose().pose
    print("Arm initial pose:")
    print(arm_initial_pose)

    # 何かを掴んでいた時のためにハンドを開く
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()

    # SRDFに定義されている"home"の姿勢にする
    def home_pos():
        print("home")
        arm.set_named_target("home")
        arm.go()

    # SRDFに定義されている"vertical"の姿勢にする
    def vertical_pos():
        print("vertical")
        arm.set_named_target("vertical")
        arm.go()

    # ハンドを少し閉じる
    def open_close(per):
        gripper.set_joint_value_target([per,per])
        gripper.go()

    # 手動で姿勢を指定するには以下のように指定
    def set_pos(set_x,set_y,set_z):
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = set_x
        target_pose.position.y = set_y
        target_pose.position.z = set_z
        q = quaternion_from_euler( -3.14, 0.0, -3.14/2.0 )
        target_pose.orientation.x = q[0]
        target_pose.orientation.y = q[1]
        target_pose.orientation.z = q[2]
        target_pose.orientation.w = q[3]
        arm.set_pose_target( target_pose )	# 目標ポーズ設定
        arm.go()				# 実行

    pos_x = 0.30
    pos_y = 0
    pos_z = 0.3

    vertical_pos()

    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()
    time.sleep(5.0)
    gripper.set_joint_value_target([0.3, 0.3])
    gripper.go()
    
    home_pos()
    set_pos(0.33,0,0.3)
    set_pos(0.33,0.2,0.3)

    ax = 400
    ay = 100
    go = 50

    while 1:
        cx = rospy.wait_for_message("point_x", Int32)
        cy = rospy.wait_for_message("point_y", Int32)
        print(cx.data)
        print(cy.data)

        rospy.sleep(1.0)

        if(cx.data <= ax + go )&(cx.data >= ax - go)&(cy.data <= ay + go)&(cy.data > ay - go):
            print("Go")
            pos_y -= 0.04
            pos_x += 0.01
            set_pos(pos_x,pos_y,pos_z)
            print("aaaaaa")
            pos_z = 0.19
            set_pos(pos_x, pos_y, pos_z)
            print("bbbbbb")
            for num in range(10):
                gripper.set_joint_value_target([0.3, 0.3])
                gripper.go()
                pos_y += 0.01
                set_pos(pos_x, pos_y, pos_z)
                print(num)
            pos_z += 0.2
            set_pos(pos_x, pos_y, pos_z)
            break
        elif (cx.data <= ax - go)&(cy.data <= ay - go):
            print("left up")
            pos_x += 0.005
            pos_y -= 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data <= ax - go)&(cy.data >= ay - go)&(cy.data <= ay + go):
            print("left")
            pos_y += 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data < ax - go)&(cy.data > ay + go):
            print("left down")
            pos_x -= 0.005
            pos_y -= 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data >= ax - go)&(cx.data <= ax + go)&(cy.data < ay - go):
            print("up")
            pos_x += 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data > ax + go)&(cy.data < ay - go):
            print("right up")
            pos_x += 0.005
            pos_y += 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data > ax - go)&(cy.data >= ay - go)&(cy.data <= ay + go):
            print("right")
            pos_y -= 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data > ax + go)&(cy.data > ay + go):
            print("right down")
            pos_x -= 0.005
            pos_y += 0.005
            set_pos(pos_x,pos_y,pos_z)
        elif (cx.data >= ax - go)&(cx.data <= ax + go)&(cy.data > ay + go ):
            print("down")
            pos_x -= 0.005
            set_pos(pos_x,pos_y,pos_z)
        else:
            print("break")
            #pos_x -= 0.0445
            #pos_y -= 0.05
            #pos_z -= 0.12
            #set_pos(pos_x,pos_y,pos_z)
            break

    #open_close(0.15)

    vertical_pos()
    
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()

    print("fin")

if __name__ == '__main__':
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
