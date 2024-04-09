import os
from pydicom import dcmwrite
from pynetdicom import AE, evt, StoragePresentationContexts
from pydicom.uid import ExplicitVRLittleEndian
from pynetdicom.sop_class import ComputedRadiographyImageStorage, DigitalXRayImageStorageForPresentation, DigitalXRayImageStorageForProcessing

from typing import Callable

def _on_c_store(event):
    # Save received DICOM file
    filename = f"received_file.dcm"
    filepath = os.path.join('received_files', filename)
    dcmwrite(filepath, event.dataset)


    return 0x0000  # Success

def start_dicom_server(recieve_handler: Callable, host:str = 'localhost', port: str = 11112) -> None:
    ae = AE()

    handlers = [(evt.EVT_C_STORE, recieve_handler)]

    ae.requested_contexts = StoragePresentationContexts
    ae.add_supported_context(ComputedRadiographyImageStorage, ExplicitVRLittleEndian)
    ae.add_supported_context(DigitalXRayImageStorageForPresentation, ExplicitVRLittleEndian)
    ae.add_supported_context(DigitalXRayImageStorageForProcessing, ExplicitVRLittleEndian)

    scp = ae.start_server((host, port), block=True, evt_handlers=handlers)


if __name__ == "__main__":
    host = 'localhost'
    port = 11112  # Change this to any available port
    save_dir = './received_files'  # Directory to save received DICOM files

    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    start_dicom_server( _on_c_store, host, port)
