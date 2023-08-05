from typing import Tuple

import picwriter.components as pc

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.waveguide_template import strip
from gdsfactory.types import ComponentSpec, CrossSectionSpec


@gf.cell
def coupler_adiabatic(
    length1: float = 20.0,
    length2: float = 50.0,
    length3: float = 30.0,
    wg_sep: float = 1.0,
    input_wg_sep: float = 3.0,
    output_wg_sep: float = 3.0,
    dw: float = 0.1,
    port: Tuple[int, int] = (0, 0),
    direction: str = "EAST",
    waveguide_template: ComponentSpec = strip,
    cross_section: CrossSectionSpec = "strip",
    **kwargs
) -> Component:
    """Returns 50/50 adiabatic coupler.

    Design based on asymmetric adiabatic 3dB coupler designs, such as those.

    - https://doi.org/10.1364/CLEO.2010.CThAA2,
    - https://doi.org/10.1364/CLEO_SI.2017.SF1I.5
    - https://doi.org/10.1364/CLEO_SI.2018.STh4B.4

    Has input Bezier curves, with poles set to half of the x-length of the S-bend.

    I is the first half of input S-bend where input widths taper by +dw and -dw
    II is the second half of the S-bend straight with constant, unbalanced widths
    III is the region where the two asymmetric straights gradually come together
    IV  straights taper back to the original width at a fixed distance from one another
    IV is the output S-bend straight.

    Args:
        length1: region that gradually brings the two asymmetric straights together.
            In this region the straight widths gradually change to be different by `dw`.
        length2: coupling region, where asymmetric straights gradually
            become the same width.
        length3: output region where the two straights separate.
        wg_sep: Distance between center-to-center in the coupling region (Region 2).
        input_wg_sep: Separation of the two straights at the input, center-to-center.
        output_wg_sep: Separation of the two straights at the output, center-to-center.
        dw: Change in straight width.
            In Region 1, top arm tapers to width+dw/2.0, bottom taper to width-dw/2.0.
        port: coordinate of the input port (top left).
        direction: for component NORTH, WEST, SOUTH, EAST,or angle in radians.
        waveguide_template: object or function.

    Keyword Args:
       wg_width: in um.
       wg_layer: gf.LAYER.WG[0].
       wg_datatype: gf.LAYER.WG[1].
       clad_layer: gf.LAYER.WGCLAD[0].
       clad_datatype: gf.LAYER.WGCLAD[1].
       bend_radius: in um.
       cladding_offset: in um.
    """
    c = pc.AdiabaticCoupler(
        gf.call_if_func(waveguide_template, **kwargs),
        length1=length1,
        length2=length2,
        length3=length3,
        wg_sep=wg_sep,
        input_wg_sep=input_wg_sep,
        output_wg_sep=output_wg_sep,
        dw=dw,
        port=port,
        direction=direction,
    )

    c = gf.read.from_picwriter(c)

    x = gf.get_cross_section(cross_section)
    if x.add_bbox:
        c = x.add_bbox(c)
    if x.add_pins:
        c = x.add_pins(c)
    return c


if __name__ == "__main__":

    c = coupler_adiabatic(length3=5)
    print(c.ports)
    c.show(show_ports=True)
