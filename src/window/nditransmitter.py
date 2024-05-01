import numpy as np
import NDIlib as ndi
from PyQt6.QtCore import QTimer

# Class to handle NDI video transmission.


class NdiTransmitter():
    # Constructor: Initializes the NDI transmitter with a given tab.
    def __init__(self, tab):
        self._tab = tab
        self._ndi_send = None
        self._video_frame = ndi.VideoFrameV2()  # NDI video frame object.

        # Initialize NDI. If it fails, raise an exception.
        if not ndi.initialize():
            raise Exception("Could not initialize NDI.")

        # Set up the NDI sending settings.
        self.send_settings = ndi.SendCreate()
        # Name of the NDI source.
        self.send_settings.ndi_name = "TeleScore NDI"

        # Create the NDI sender. If it fails, raise an exception.
        self._ndi_send = ndi.send_create(self.send_settings)
        if self._ndi_send is None:
            raise Exception("Could not create NDI sender.")

        # Timer to update the video frame at a set interval.
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_frame)
        self._timer.start(int(1000 / 60))  # Update at 60 FPS.

    # Converts the QWidget content to a numpy array for NDI transmission.
    def _qWidgetConverterToNumpy(self):
        widget = self._tab
        pixmap = widget.grab()
        qimage = pixmap.toImage()
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(height * width * 4)

        arr = np.array(ptr).reshape(height, width, 4)
        arr = arr.astype(np.uint8)
        arr = arr[..., :3]  # Drop the alpha channel.
        return arr

    # Updates the NDI video frame with the current content of the QWidget.
    def _update_frame(self):
        # Convert the QWidget to numpy array.
        img = self._qWidgetConverterToNumpy()
        self._video_frame.data = img
        self._video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
        # Send the video frame via NDI.
        ndi.send_send_video_v2(self._ndi_send, self._video_frame)

    # Stops the NDI transmission and cleans up resources.
    def stop(self):
        self._timer.stop()
        ndi.send_destroy(self._ndi_send)
        ndi.destroy()
