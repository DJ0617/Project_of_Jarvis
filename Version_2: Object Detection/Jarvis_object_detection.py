# Object Detection using YoloV5 by Daijie Bao
import torch
import cv2

class JarvisDetection:
    """
    The class for Jarvis to perform object recognition on a real-time video source.
    Major Task Support Engine: YoloV5 and OpenCV
    Main Feature:
    1. Using OpenCV process real-time video into frames
    2. Using YoloV5 Machine Vision detection model detect over 80 types of different objects in each Frames

    """

    def __init__(self, source_file, conf: float, iou: float, model_choice: str):
        """
        Parameter:

        source_file: User need to provide real-time video source for detection task, usually is 0 for OpenCV on laptop
        conf: User could self-defined inference threshold for detection task usually 0.4, type: float
        iou: User could self-defined inference IOU threshold for detection task usually 0.3, type: float
        model_choice: User could choice type of model source, either from git clone local source or from pytorch hub

        Return: Void

        """
        self.source_file = source_file
        self.model_choice = model_choice
        self.model = self.load_detect_model()
        self.model.conf = conf
        self.model.iou = iou
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def load_detect_model(self):
        """
        Load the detection model based on users choice either from local or online source

        """
        if self.model_choice == "local":
            model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best.pt')
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        return model

    def input_source_file(self):
        """
        Input real-time video source file from users local machine

        """
        print('Initializing Video Source, Please Wait...... ')
        video_source_file = cv2.VideoCapture(self.source_file)
        print('Video Source Load Successfully! Starting Detect Object......')
        assert video_source_file is not None
        return video_source_file

    def detect_result(self, input_frame):
        """
        Parameter:

        input_frame: frame that need to be detected by YoloV5

        return: Object Detection Result from YoloV5 (Labels, Coordinate for bounding box, and object name)

        """
        self.model.to(self.device)
        results = self.model([input_frame])
        labels = results.xyxyn[0][:, -1].to('cpu').numpy()
        coordinate = results.xyxyn[0][:, :-1].to('cpu').numpy()
        name = results.pandas().xyxy[0]["name"]
        return labels, coordinate, name

    def __call__(self):
        """
        Execute the major detection program

        """

        source = self.input_source_file()
        while source.isOpened():
            ret, frame = source.read()
            cv2.namedWindow("output")
            results = self.detect_result(frame)
            labels, coordinate, name = results
            x_shape, y_shape = frame.shape[1], frame.shape[0]
            for i in range(len(labels)):
                row = coordinate[i]
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y1 - 20), (x2, y1), (0, 255, 0), -1)
                cv2.putText(frame, str(name[0]), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.imshow("output", frame)
            if not ret:
                break
            if cv2.waitKey(1) == ord('e'):
                print("Program End by User")
                break
        source.release()
        cv2.destroyAllWindows()

def detection_assistant():
    """
    Get user input choice for object detection

    """
    print("Hi, I'm Jarvis detection, your virtual detection assistant.")
    input_source = input('Please enter your video source file: ')
    conf_choice = input("Please enter your conf threshold: ")
    iou_choice = input("Please enter your iou threshold: ")
    model_choice = input("please enter your model source choice: ")
    print('Initializing detection assistant......')
    JarvisDetection(input_source, conf_choice, iou_choice, model_choice)

# Start the detection
detection_assistant()









