import json

json_command = {
    "id": "waapi.",
    "displayName": "Enable Stream for all the children of the selected items",
    "program": "pythonw",
    "startMode": "MultipleSelectionSingleProcessSpaceSeparated",
    "args": "\"${WwiseUserAddons}/waapi-scripts/_.py\" ${id}",
    "redirectOutputs": "true",
    "contextMenu": {
        "basePath": "WAAPI/Stream",
        "enabledFor": "",
        "visibleFor": ""
      }
    }