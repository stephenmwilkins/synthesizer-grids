"""
Download the Maraston2013 SPS model and convert to HDF5 synthesizer grid.
"""

import os

import numpy as np
from synthesizer.conversions import llam_to_lnu
from synthesizer_grids.grid_io import GridFile
from synthesizer_grids.parser import Parser
from unyt import Angstrom, erg, s, yr


def make_grid(model, imf, input_dir, grid_dir):
    """Main function to convert Maraston 2013 and
    produce grids used by synthesizer
    Args:
        model (dict):
            dictionary containing model parameters
        imf (string):
            Initial mass function, Salpeter or
            Kroupa
        input_dir (string):
            directory where the raw Maraston+13 files are read from
        grid_dir (string):
            directory where the grids are created.
        grid_dir (string):
            directory where the grids are created.
    Returns:
        fname (string):
            output filename
    """

    # define output
    out_filename = f"{grid_dir}/{sps_name}_{imf}.hdf5"
    out_filename = f"{grid_dir}/{sps_name}_{imf}.hdf5"

    metallicity = np.array(
        [0.001, 0.01, 0.02, 0.04]
    )  # array of available metallicities

    if imf == "kroupa100":
        metallicity = np.array([0.02])

    metallicity_code = {
        0.001: "0001",
        0.01: "001",
        0.02: "002",
        0.04: "004",
    }  # codes for converting metallicty

    # open first raw data file to get age
    fn = (
        f"{input_dir}/sed_M13.{imf_code[imf]}"
        f"z{metallicity_code[metallicity[0]]}"
    )

    age_, _, lam_, llam_ = np.loadtxt(fn).T  # llam is in (ergs /s /AA /Msun)

    age_Gyr = np.sort(np.array(list(set(age_))))  # Gyr
    age = age_Gyr * 1e9 * yr
    log10age = np.log10(age)

    lam = lam_[age_ == age_[0]] * Angstrom

    spec = np.zeros((len(age), len(metallicity), len(lam)))

    # Create the GridFile ready to take outputs
    out_grid = GridFile(out_filename, mode="w", overwrite=True)

    # at each point in spec convert the units
    for iZ, Z in enumerate(metallicity):
        for ia, a_Gyr in enumerate(age_Gyr):
            fn = (
                f"{input_dir}/sed_M13.{imf_code[imf]}"
                f"z{metallicity_code[Z]}"
            )
            print(iZ, ia, fn)
            age_, _, lam_, llam_ = np.loadtxt(fn).T

            llam = llam_[age_ == a_Gyr] * erg / s / Angstrom
            lnu = llam_to_lnu(lam, llam)
            spec[ia, iZ] = lnu

    # Write everything out thats common to all models
    out_grid.write_grid_common(
        model=model,
        axes={"log10age": log10age, "metallicity": metallicity},
        wavelength=lam,
        spectra={"incident": spec},  # check this unit
        alt_axes=("log10age", "metallicity"),
    )

    # Include the specific ionising photon luminosity
    out_grid.add_specific_ionising_lum()


if __name__ == "__main__":
    # Set up the command line arguments
    parser = Parser(description="Maraston+13 download and grid creation")

    args = parser.parse_args()

    grid_dir = args.grid_dir

    # Define the model metadata
    sps_name = "maraston13"
    imfs = ["salpeter", "kroupa"]
    imf_code = {"salpeter": "ss", "kroupa": "kr", "kroupa100": "100kr"}
    model = {
        "sps_name": sps_name,
        "sps_version": False,
        "alpha": False,
    }

    input_dir = args.input_dir
    input_dir += f"/{sps_name}"

    # create directory to store downloaded output if it doesn't exist
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)

    # run the single kroupa100 model
    imf = "kroupa100"
    make_grid(model, imf, input_dir, grid_dir)

    # then run the rest
    for imf in imfs:
        make_grid(model, imf, input_dir, grid_dir)
