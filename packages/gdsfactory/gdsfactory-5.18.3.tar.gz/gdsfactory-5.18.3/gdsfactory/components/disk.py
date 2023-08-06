from typing import Tuple

import numpy as np
import picwriter.components as pc

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.waveguide_template import strip
from gdsfactory.types import ComponentSpec


@gf.cell
def disk(
    radius: float = 10.0,
    gap: float = 0.2,
    wrap_angle_deg: float = 180.0,
    parity: int = 1,
    port: Tuple[int, int] = (0, 0),
    direction: str = "EAST",
    waveguide_template: ComponentSpec = strip,
    **kwargs
) -> Component:
    """Disk Resonator.

    Args:
       radius: disk resonator radius.
       gap: Distance between the bus straight and resonator.
       wrap_angle_deg: Angle in degrees between 0 and 180.
        determines how much the bus straight wraps along the resonator.
        0 corresponds to a straight bus straight.
        180 corresponds to a bus straight wrapped around half of the resonator.
       parity (1 or -1): 1, resonator left from bus straight, -1 resonator to the right.
       port: Cartesian coordinate of the input port (x1, y1).
       direction: of component 'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'.
       waveguide_template: Picwriter WaveguideTemplate object.

    Keyword Args:
       wg_width: 0.5.
       wg_layer: gf.LAYER.WG[0].
       wg_datatype: gf.LAYER.WG[1].
       clad_layer: gf.LAYER.WGCLAD[0].
       clad_datatype: gf.LAYER.WGCLAD[1].
       bend_radius: 10.
       cladding_offset: 3.
    """
    c = pc.Disk(
        gf.call_if_func(waveguide_template, **kwargs),
        radius=radius,
        coupling_gap=gap,
        wrap_angle=wrap_angle_deg * np.pi / 180,
        parity=parity,
        port=port,
        direction=direction,
    )

    return gf.read.from_picwriter(c)


if __name__ == "__main__":

    c = disk(wrap_angle_deg=30)
    c.show(show_ports=True)
