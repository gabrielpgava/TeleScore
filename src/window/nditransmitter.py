import time
import threading
import numpy as np
import NDIlib as ndi

# Class to handle NDI video transmission.


class NdiTransmitter():
    # Constructor: Initializes the NDI transmitter with a given tab.
    def __init__(self, tab):
        self._tab = tab
        self._ndi_send = None
        self._video_frame = ndi.VideoFrameV2()  # NDI video frame object.
        self._stop_event = threading.Event()

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

        # Start the thread to update the video frame.
        self._thread = threading.Thread(target=self._update_frame, args=())
        self._thread.daemon = True
        self._thread.start()

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

        while not self._stop_event.is_set():

            # Convert the QWidget to a numpy array.
            img = self._qWidgetConverterToNumpy()
            self._video_frame.data = img
            self._video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
            # Send the video frame via NDI.
            ndi.send_send_video_v2(self._ndi_send, self._video_frame)
            # Sleep for a short period to simulate 60 FPS.
            time.sleep(1/60)

    # Stops the NDI transmission and cleans up resources.
    def stop(self):
        # Signal the thread to stop.
        self._stop_event.set()
        # Wait for the thread to finish.
        self._thread.join()

        # Destroy the NDI sender and finalize the NDI library.
        ndi.send_destroy(self._ndi_send)
        ndi.destroy()
