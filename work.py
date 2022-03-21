import cv2
import mediapipe as mp
import bpy


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.mode_set(mode='EDIT')
with mp_pose.Pose(static_image_mode=False, smooth_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    for n in range(9000):
        success, image = cap.read()
        if not success:
            continue

        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = pose.process(image)

        # Движение
        if results.pose_landmarks:
            bns = results.pose_landmarks.landmark
            scale = 2
            for num in range(0, 33):
                y = (bns[num].z) * 0.5
                x = (0.5 - bns[num].x) * scale
                z = (0.5 - bns[num].y) * scale
                bpy.context.object.data.edit_bones[str(num)].tail = (x, y, z)


            y = ((bns[11].z) * 0.5 + (bns[12].z) * 0.5) / 2
            x = ((0.5 - bns[11].x) * scale + (0.5 - bns[12].x) * scale) / 2
            z = ((0.5 - bns[11].y) * scale + (0.5 - bns[12].y) * scale) / 2
            bpy.context.object.data.edit_bones["Bone"].tail = (x, y, z)

            y = ((bns[23].z) * 0.5 + (bns[24].z) * 0.5) / 2
            x = ((0.5 - bns[23].x) * scale + (0.5 - bns[24].x) * scale) / 2
            z = ((0.5 - bns[23].y) * scale + (0.5 - bns[24].y) * scale) / 2
            bpy.context.object.data.edit_bones["Bone"].head = (x, y, z)
            bpy.context.object.data.edit_bones["23"].head = (x, y, z)
            bpy.context.object.data.edit_bones["24"].head = (x, y, z)


        # Отрисовка
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        image = cv2.flip(image, 1)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        bpy.context.scene.frame_set(n)

    cap.release()
    cv2.destroyAllWindows()