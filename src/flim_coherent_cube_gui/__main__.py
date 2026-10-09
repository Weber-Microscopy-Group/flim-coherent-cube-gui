# %%
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
import tkinter as tk
from tkinter import ttk

import coherent_cube as cc


# %%
class State:
    def __init__(self):
        self.port: None | str = None
        self.laser: None | cc.CoherentCube = None
        self._is_emitting: bool = False
        self._analog_control: cc.AnalogControl = cc.AnalogControl.External
        self._operation_mode: cc.OperationMode = (
            cc.OperationMode.Pulsed
        )  # only valid when `_analog_control` is CameraControl.MANUAL
        self._power: float = 0.0
        self._min_power: float = 0.0
        self._nominal_power: float = 0.0

    def connect(self, port: str):
        if self.laser is not None:
            self.laser.close()

        self.port = port
        self.laser = cc.CoherentCube(port)
        self.laser.open()
        self.laser.off()

        self._is_emitting = False
        self._min_power = self.laser.min_power
        self._nominal_power = self.laser.nominal_power

    def disconnect(self):
        if self.laser is not None:
            self.laser.off()
            self.laser.close()

        self.laser = None
        self.port = None
        self._is_emitting = False

    @property
    def emitting(self) -> bool:
        return self._is_emitting

    @emitting.setter
    def emitting(self, value: bool):
        if self.laser is None:
            raise RuntimeError("laser not connected")

        if value:
            self.laser.on()
        else:
            self.laser.off()

        self._is_emitting = value

    @property
    def analog_control(self) -> cc.AnalogControl:
        if self.laser is None:
            raise RuntimeError("laser not connected")

        self._analog_control = self.laser.analog_control
        return self._analog_control

    @analog_control.setter
    def analog_control(self, value: cc.AnalogControl):
        if self.laser is None:
            raise RuntimeError("laser not connected")

        self.laser.analog_control = value
        self._analog_control = value


class UiControl(ttk.Frame):
    def __init__(self, state: State):
        btn_cam = ttk.Button(self, text="Camera").grid(column=0, row=0)
        btn_man = ttk.Button(self, text="Manual").grid(column=1, row=0)

    @property
    def btn_camera(self):
        return self.get


def create_root() -> tk.Tk:
    root = tk.Tk()
    root.title("Coherent Cube | pco flim.X camera")
    root.geometry("600x400")
    return root


def create_control(state: State, parent) -> ttk.Frame:
    frm = ttk.Frame(parent, padding=0)
    frm.grid()

    return frm


def main():
    state = State()
    root = create_root()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    create_control(state, frm)

    root.mainloop()


# %%
if __name__ == "__main__":
    main()
# %%
