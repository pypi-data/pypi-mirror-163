# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-05/2021 : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, jerome.carnis@esrf.fr
"""Functions related to BCDI data preprocessing, before phase retrieval."""

try:
    import hdf5plugin  # for P10, should be imported before h5py or PyTables
except ModuleNotFoundError:
    pass

import logging
import pathlib
from numbers import Real
from operator import mul
from typing import Any, Dict, List, Optional, Tuple, Union, no_type_check

import matplotlib.pyplot as plt
import numpy as np
import xrayutilities as xu
from scipy.interpolate import interp1d
from scipy.ndimage.measurements import center_of_mass

from bcdi.experiment import loader
from bcdi.graph import graph_utils as gu
from bcdi.utils import utilities as util
from bcdi.utils import validation as valid

module_logger = logging.getLogger(__name__)


def center_fft(
    data,
    mask,
    detector,
    frames_logical,
    centering="max",
    fft_option="crop_asymmetric_ZYX",
    **kwargs,
):
    """
    Center and crop/pad the dataset depending on user parameters.

    :param data: the 3D data array
    :param mask: the 3D mask array
    :param detector: an instance of the class Detector
    :param frames_logical: array of initial length the number of measured frames.
     In case of padding the length changes. A frame whose index is set to 1 means
     that it is used, 0 means not used, -1 means padded (added) frame.
    :param centering: method used to determine the location of the Bragg peak: 'max',
     'com' (center of mass), or 'max_com' (max along the first axis, center of mass in
     the detector plane)
    :param fft_option:
     - 'crop_sym_ZYX': crop the array for FFT requirements, Bragg peak centered
     - 'crop_asym_ZYX': crop the array for FFT requirements without centering the
       Brag peak
     - 'pad_sym_Z_crop_sym_YX': crop detector images (Bragg peak centered) and pad
       the rocking angle based on 'pad_size' (Bragg peak centered)
     - 'pad_sym_Z_crop_asym_YX': pad rocking angle based on 'pad_size'
       (Bragg peak centered) and crop detector (Bragg peak non-centered)
     - 'pad_asym_Z_crop_sym_YX': crop detector images (Bragg peak centered),
       pad the rocking angle without centering the Brag peak
     - 'pad_asym_Z_crop_asym_YX': pad rocking angle and crop detector without centering
       the Bragg peak
     - 'pad_sym_Z': keep detector size and pad/center the rocking angle based on
       'pad_size', Bragg peak centered
     - 'pad_asym_Z': keep detector size and pad the rocking angle without centering
       the Brag peak
     - 'pad_sym_ZYX': pad all dimensions based on 'pad_size', Brag peak centered
     - 'pad_asym_ZYX': pad all dimensions based on 'pad_size' without centering
       the Brag peak
     - 'skip': keep the full dataset or crop it to the size defined by fix_size

    :param kwargs:
     - 'fix_bragg': user-defined position in pixels of the Bragg peak
       [z_bragg, y_bragg, x_bragg]
     - 'fix_size': user defined output array size
       [zstart, zstop, ystart, ystop, xstart, xstop]
     - 'pad_size': user defined output array size [nbz, nby, nbx]
     - 'q_values': [qx, qz, qy], each component being a 1D array
     - 'logger': an optional logger

    :return:
     - updated data, mask (and q_values if provided, [] otherwise)
     - pad_width = [z0, z1, y0, y1, x0, x1] number of pixels added at each end of the
       original data
     - updated frames_logical

    """
    logger = kwargs.get("logger", module_logger)

    valid.valid_ndarray(arrays=(data, mask), ndim=3)
    # check and load kwargs
    valid.valid_kwargs(
        kwargs=kwargs,
        allowed_kwargs={"fix_bragg", "fix_size", "logger", "pad_size", "q_values"},
        name="kwargs",
    )
    fix_bragg = kwargs.get("fix_bragg")
    fix_size = kwargs.get("fix_size")
    pad_size = kwargs.get("pad_size", [])
    q_values = kwargs.get("q_values", [])

    if q_values:  # len(q_values) != 0
        qx = q_values[0]  # axis=0, z downstream, qx in reciprocal space
        qz = q_values[1]  # axis=1, y vertical, qz in reciprocal space
        qy = q_values[2]  # axis=2, x outboard, qy in reciprocal space
    else:
        qx = []
        qy = []
        qz = []

    if centering == "max":
        z0, y0, x0 = np.unravel_index(abs(data).argmax(), data.shape)
        if q_values:
            logger.info(
                f"Max at (qx, qz, qy): {qx[z0]:.5f}, {qz[y0]:.5f}, {qy[x0]:.5f}"
            )
        else:
            logger.info(f"Max at pixel (Z, Y, X): ({z0, y0, x0})")
    elif centering == "com":
        z0, y0, x0 = center_of_mass(data)
        if q_values:
            logger.info(
                "Center of mass at (qx, qz, qy): "
                f"{qx[z0]:.5f}, {qz[y0]:.5f}, {qy[x0]:.5f}"
            )
        else:
            logger.info(f"Center of mass at pixel (Z, Y, X): ({z0, y0, x0})")
    else:  # 'max_com'
        position = list(np.unravel_index(abs(data).argmax(), data.shape))
        position[1:] = center_of_mass(data[position[0], :, :])
        z0, y0, x0 = tuple(map(lambda x: int(np.rint(x)), position))

    if fix_bragg:
        if len(fix_bragg) != 3:
            raise ValueError("fix_bragg should be a list of 3 integers")
        z0, y0, x0 = fix_bragg
        logger.info(
            "Peak intensity position defined by user on the full detector: "
            f"({z0, y0, x0})"
        )
        y0 = (y0 - detector.roi[0]) / detector.binning[1]
        x0 = (x0 - detector.roi[2]) / detector.binning[2]
        logger.info(
            "Peak intensity position with detector ROI and binning in detector plane: "
            f"({z0, y0, x0})"
        )
    iz0, iy0, ix0 = int(round(z0)), int(round(y0)), int(round(x0))
    logger.info(f"Data peak value = {data[iz0, iy0, ix0]:.1f}")

    # Max symmetrical box around center of mass
    nbz, nby, nbx = np.shape(data)
    max_nz = abs(2 * min(iz0, nbz - iz0))
    max_ny = 2 * min(iy0, nby - iy0)
    max_nx = abs(2 * min(ix0, nbx - ix0))
    if fft_option != "skip":
        logger.info(f"Max symmetrical box (qx, qz, qy): ({max_nz, max_ny, max_nx})")
    if any(val == 0 for val in (max_nz, max_ny, max_nx)):
        logger.info(
            "Empty images or presence of hotpixel at the border,"
            ' defaulting fft_option to "skip"!'
        )
        fft_option = "skip"

    # Crop/pad data to fulfill FFT size and user requirements
    if fft_option == "crop_sym_ZYX":
        # crop rocking angle and detector, Bragg peak centered
        nz1, ny1, nx1 = util.smaller_primes(
            (max_nz, max_ny, max_nx), maxprime=7, required_dividers=(2,)
        )
        pad_width = np.zeros(6, dtype=int)

        data = data[
            iz0 - nz1 // 2 : iz0 + nz1 // 2,
            iy0 - ny1 // 2 : iy0 + ny1 // 2,
            ix0 - nx1 // 2 : ix0 + nx1 // 2,
        ]
        mask = mask[
            iz0 - nz1 // 2 : iz0 + nz1 // 2,
            iy0 - ny1 // 2 : iy0 + ny1 // 2,
            ix0 - nx1 // 2 : ix0 + nx1 // 2,
        ]
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        if (iz0 - nz1 // 2) > 0:  # if 0, the first frame is used
            frames_logical[0 : iz0 - nz1 // 2] = 0
        if (iz0 + nz1 // 2) < nbz:  # if nbz, the last frame is used
            frames_logical[iz0 + nz1 // 2 :] = 0

        if len(q_values) != 0:
            qx = qx[iz0 - nz1 // 2 : iz0 + nz1 // 2]
            qy = qy[ix0 - nx1 // 2 : ix0 + nx1 // 2]
            qz = qz[iy0 - ny1 // 2 : iy0 + ny1 // 2]

    elif fft_option == "crop_asym_ZYX":
        # crop rocking angle and detector without centering the Bragg peak
        nz1, ny1, nx1 = util.smaller_primes(
            (nbz, nby, nbx), maxprime=7, required_dividers=(2,)
        )
        pad_width = np.zeros(6, dtype=int)

        data = data[
            nbz // 2 - nz1 // 2 : nbz // 2 + nz1 // 2,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        mask = mask[
            nbz // 2 - nz1 // 2 : nbz // 2 + nz1 // 2,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        if (nbz // 2 - nz1 // 2) > 0:  # if 0, the first frame is used
            frames_logical[0 : nbz // 2 - nz1 // 2] = 0
        if (nbz // 2 + nz1 // 2) < nbz:  # if nbz, the last frame is used
            frames_logical[nbz // 2 + nz1 // 2 :] = 0

        if len(q_values) != 0:
            qx = qx[nbz // 2 - nz1 // 2 : nbz // 2 + nz1 // 2]
            qy = qy[nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2]
            qz = qz[nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2]

    elif fft_option == "pad_sym_Z_crop_sym_YX":
        # pad rocking angle based on 'pad_size' (Bragg peak centered)
        # and crop detector (Bragg peak centered)
        if len(pad_size) != 3:
            raise ValueError("pad_size should be a list of three elements")
        if pad_size[0] != util.higher_primes(
            pad_size[0], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[0], "does not meet FFT requirements")
        ny1, nx1 = util.smaller_primes(
            (max_ny, max_nx), maxprime=7, required_dividers=(2,)
        )

        data = data[:, iy0 - ny1 // 2 : iy0 + ny1 // 2, ix0 - nx1 // 2 : ix0 + nx1 // 2]
        mask = mask[:, iy0 - ny1 // 2 : iy0 + ny1 // 2, ix0 - nx1 // 2 : ix0 + nx1 // 2]
        pad_width = np.array(
            [
                int(min(pad_size[0] / 2 - iz0, pad_size[0] - nbz)),
                int(min(pad_size[0] / 2 - nbz + iz0, pad_size[0] - nbz)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0]) * dqx
            qy = qy[ix0 - nx1 // 2 : ix0 + nx1 // 2]
            qz = qz[iy0 - ny1 // 2 : iy0 + ny1 // 2]

    elif fft_option == "pad_sym_Z_crop_asym_YX":
        # pad rocking angle based on 'pad_size' (Bragg peak centered)
        # and crop detector (Bragg peak non-centered)
        if len(pad_size) != 3:
            raise ValueError("pad_size should be a list of three elements")
        logger.info(f"pad_size for 1st axis before binning: {pad_size[0]}")
        if pad_size[0] != util.higher_primes(
            pad_size[0], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[0], "does not meet FFT requirements")
        ny1, nx1 = util.smaller_primes(
            (max_ny, max_nx), maxprime=7, required_dividers=(2,)
        )

        data = data[
            :,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        mask = mask[
            :,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        pad_width = np.array(
            [
                int(min(pad_size[0] / 2 - iz0, pad_size[0] - nbz)),
                int(min(pad_size[0] / 2 - nbz + iz0, pad_size[0] - nbz)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0]) * dqx
            qy = qy[nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2]
            qz = qz[nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2]

    elif fft_option == "pad_asym_Z_crop_sym_YX":
        # pad rocking angle without centering the Bragg peak
        # and crop detector (Bragg peak centered)
        ny1, nx1 = util.smaller_primes(
            (max_ny, max_nx), maxprime=7, required_dividers=(2,)
        )
        nz1 = util.higher_primes(nbz, maxprime=7, required_dividers=(2,))

        data = data[:, iy0 - ny1 // 2 : iy0 + ny1 // 2, ix0 - nx1 // 2 : ix0 + nx1 // 2]
        mask = mask[:, iy0 - ny1 // 2 : iy0 + ny1 // 2, ix0 - nx1 // 2 : ix0 + nx1 // 2]
        pad_width = np.array(
            [
                int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2),
                int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1) * dqx
            qy = qy[ix0 - nx1 // 2 : ix0 + nx1 // 2]
            qz = qz[iy0 - ny1 // 2 : iy0 + ny1 // 2]

    elif fft_option == "pad_asym_Z_crop_asym_YX":
        # pad rocking angle and crop detector without centering the Bragg peak
        ny1, nx1 = util.smaller_primes((nby, nbx), maxprime=7, required_dividers=(2,))
        nz1 = util.higher_primes(nbz, maxprime=7, required_dividers=(2,))

        data = data[
            :,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        mask = mask[
            :,
            nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2,
            nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2,
        ]
        pad_width = np.array(
            [
                int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2),
                int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1) * dqx
            qy = qy[nbx // 2 - nx1 // 2 : nbx // 2 + nx1 // 2]
            qz = qz[nby // 2 - ny1 // 2 : nby // 2 + ny1 // 2]

    elif fft_option == "pad_sym_Z":
        # pad rocking angle based on 'pad_size'(Bragg peak centered)
        # and keep detector size
        if len(pad_size) != 3:
            raise ValueError("pad_size should be a list of three elements")
        logger.info(f"pad_size for 1st axis before binning: {pad_size[0]}")
        if pad_size[0] != util.higher_primes(
            pad_size[0], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[0], "does not meet FFT requirements")

        pad_width = np.array(
            [
                int(min(pad_size[0] / 2 - iz0, pad_size[0] - nbz)),
                int(min(pad_size[0] / 2 - nbz + iz0, pad_size[0] - nbz)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(pad_size[0]) * dqx

    elif fft_option == "pad_asym_Z":
        # pad rocking angle without centering the Bragg peak, keep detector size
        nz1 = util.higher_primes(nbz, maxprime=7, required_dividers=(2,))

        pad_width = np.array(
            [
                int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2),
                int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                0,
                0,
                0,
                0,
            ],
            dtype=int,
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qx = qx0 + np.arange(nz1) * dqx

    elif fft_option == "pad_sym_ZYX":
        # pad both dimensions based on 'pad_size' (Bragg peak centered)
        if len(pad_size) != 3:
            raise ValueError("pad_size should be a list of 3 integers")
        logger.info(f"pad_size: {pad_size}")
        logger.info(
            "The 1st axis (stacking dimension) is padded before binning,"
            " detector plane after binning."
        )
        if pad_size[0] != util.higher_primes(
            pad_size[0], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[0], "does not meet FFT requirements")
        if pad_size[1] != util.higher_primes(
            pad_size[1], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[1], "does not meet FFT requirements")
        if pad_size[2] != util.higher_primes(
            pad_size[2], maxprime=7, required_dividers=(2,)
        ):
            raise ValueError(pad_size[2], "does not meet FFT requirements")

        pad_width = [
            int(min(pad_size[0] / 2 - iz0, pad_size[0] - nbz)),
            int(min(pad_size[0] / 2 - nbz + iz0, pad_size[0] - nbz)),
            int(min(pad_size[1] / 2 - iy0, pad_size[1] - nby)),
            int(min(pad_size[1] / 2 - nby + iy0, pad_size[1] - nby)),
            int(min(pad_size[2] / 2 - ix0, pad_size[2] - nbx)),
            int(min(pad_size[2] / 2 - nbx + ix0, pad_size[2] - nbx)),
        ]
        pad_width = np.array(
            list((map(lambda value: max(value, 0), pad_width))), dtype=int
        )  # remove negative numbers
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels
        logger.info(f"FFT box (qx, qz, qy): {data.shape}")

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            dqy = qy[1] - qy[0]
            dqz = qz[1] - qz[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qy0 = qy[0] - pad_width[2] * dqy
            qz0 = qz[0] - pad_width[1] * dqz
            qx = qx0 + np.arange(pad_size[0]) * dqx
            qy = qy0 + np.arange(pad_size[2]) * dqy
            qz = qz0 + np.arange(pad_size[1]) * dqz

    elif fft_option == "pad_asym_ZYX":
        # pad both dimensions without centering the Bragg peak
        nz1, ny1, nx1 = [
            util.higher_primes(nbz, maxprime=7, required_dividers=(2,)),
            util.higher_primes(nby, maxprime=7, required_dividers=(2,)),
            util.higher_primes(nbx, maxprime=7, required_dividers=(2,)),
        ]

        pad_width = np.array(
            [
                int((nz1 - nbz + ((nz1 - nbz) % 2)) / 2),
                int((nz1 - nbz + 1) / 2 - ((nz1 - nbz) % 2)),
                int((ny1 - nby + ((pad_size[1] - nby) % 2)) / 2),
                int((ny1 - nby + 1) / 2 - ((ny1 - nby) % 2)),
                int((nx1 - nbx + ((nx1 - nbx) % 2)) / 2),
                int((nx1 - nbx + 1) / 2 - ((nx1 - nbx) % 2)),
            ]
        )
        data = zero_pad(data, padding_width=pad_width, mask_flag=False)
        mask = zero_pad(
            mask, padding_width=pad_width, mask_flag=True
        )  # mask padded pixels

        temp_frames = -1 * np.ones(data.shape[0])
        temp_frames[pad_width[0] : pad_width[0] + nbz] = frames_logical
        frames_logical = temp_frames

        if len(q_values) != 0:
            dqx = qx[1] - qx[0]
            dqy = qy[1] - qy[0]
            dqz = qz[1] - qz[0]
            qx0 = qx[0] - pad_width[0] * dqx
            qy0 = qy[0] - pad_width[2] * dqy
            qz0 = qz[0] - pad_width[1] * dqz
            qx = qx0 + np.arange(nz1) * dqx
            qy = qy0 + np.arange(nx1) * dqy
            qz = qz0 + np.arange(ny1) * dqz

    elif fft_option == "skip":
        # keep the full dataset or use 'fix_size' parameter
        pad_width = np.zeros(
            6, dtype=int
        )  # do nothing or crop the data, starting_frame should be 0
        if fix_size:
            if len(fix_size) != 6:
                raise ValueError("fix_bragg should be a list of 3 integers")

            # take binning into account
            fix_size[2] = int(fix_size[2] // detector.binning[1])
            fix_size[3] = int(fix_size[3] // detector.binning[1])
            fix_size[4] = int(fix_size[4] // detector.binning[2])
            fix_size[5] = int(fix_size[5] // detector.binning[2])
            # size of output array defined
            nbz, nby, nbx = np.shape(data)
            z_span = fix_size[1] - fix_size[0]
            y_span = fix_size[3] - fix_size[2]
            x_span = fix_size[5] - fix_size[4]
            if (
                z_span > nbz
                or y_span > nby
                or x_span > nbx
                or fix_size[1] > nbz
                or fix_size[3] > nby
                or fix_size[5] > nbx
            ):
                raise ValueError("Predefined fix_size uncorrect")
            data = data[
                fix_size[0] : fix_size[1],
                fix_size[2] : fix_size[3],
                fix_size[4] : fix_size[5],
            ]
            mask = mask[
                fix_size[0] : fix_size[1],
                fix_size[2] : fix_size[3],
                fix_size[4] : fix_size[5],
            ]

            if fix_size[0] > 0:  # if 0, the first frame is used
                frames_logical[0 : fix_size[0]] = 0
            if fix_size[1] < nbz:  # if nbz, the last frame is used
                frames_logical[fix_size[1] :] = 0

            if len(q_values) != 0:
                qx = qx[fix_size[0] : fix_size[1]]
                qy = qy[fix_size[4] : fix_size[5]]
                qz = qz[fix_size[2] : fix_size[3]]
    else:
        raise ValueError("Incorrect value for 'fft_option'")

    if len(q_values) != 0:
        q_values = list(q_values)
        q_values[0] = qx
        q_values[1] = qz
        q_values[2] = qy
    return data, mask, pad_width, q_values, frames_logical


@no_type_check  # https://github.com/python/mypy/issues/6697
def find_bragg(
    data: np.ndarray,
    roi: Optional[Tuple[int, int, int, int]] = None,
    binning: Optional[Union[Tuple[int, ...], List[int]]] = None,
    savedir: Optional[str] = None,
    **kwargs,
) -> Dict[str, Tuple[int, int, int]]:
    """
    Find the Bragg peak position in data based on various peak finding methods.

    It compensates for a ROI in the detector and an eventual binning.

    :param data: 2D or 3D array. If complex, Bragg peak position is calculated for
     abs(array)
    :param roi: tuple of integers of length 4, region of interest used to generate data
     from the full sized detector.
    :param binning: tuple of integers of length data.ndim, binning applied to the data
     in each dimension.
    :param savedir: path to the saving directory
    :param kwargs:

     - 'logger': an optional logger

    :return: the Bragg peak positions in the unbinned, full size detector as a tuple of
     data.ndim elements
    """
    logger = kwargs.get("logger", module_logger)
    # check parameters
    valid.valid_ndarray(arrays=data, ndim=3)
    valid.valid_container(
        roi,
        container_types=(tuple, list, np.ndarray),
        item_types=int,
        length=4,
        allow_none=True,
        name="roi",
    )
    valid.valid_container(
        binning,
        container_types=(tuple, list, np.ndarray),
        item_types=int,
        length=data.ndim,
        allow_none=True,
        name="binning",
    )

    logger.info(
        f"Finding Bragg peak position:"
        f"\n\tInput data shape {data.shape}"
        f"\n\tBinning: {binning}"
        f"\n\tRoi: {roi}"
    )
    position_max = np.unravel_index(abs(data).argmax(), data.shape)
    logger.info(f"Max at: {position_max}, value = {int(data[position_max])}")

    position_com = center_of_mass(data)
    position_com = tuple(map(lambda x: int(np.rint(x)), position_com))
    logger.info(f"Center of mass at: {position_com}, value = {int(data[position_com])}")

    position_max_com = list(np.unravel_index(abs(data).argmax(), data.shape))
    position_max_com[1:] = center_of_mass(data[position_max_com[0], :, :])
    position_max_com = tuple(map(lambda x: int(np.rint(x)), position_max_com))
    logger.info(
        f"MaxCom at (z, y, x): {position_max_com}, "
        f"value = {int(data[position_max_com])}"
    )

    # unbin
    if binning is not None:
        position_max = [a * b for a, b in zip(position_max, binning)]
        position_com = [a * b for a, b in zip(position_com, binning)]
        position_max_com = [a * b for a, b in zip(position_max_com, binning)]

    # add the offset due to the region of interest
    # the roi is defined as [y_start, y_stop, x_start, x_stop]
    if roi is not None:
        position_max = list(position_max)
        position_max[-1] = position_max[-1] + roi[2]
        position_max[-2] = position_max[-2] + roi[0]

        position_com = list(position_com)
        position_com[-1] = position_com[-1] + roi[2]
        position_com[-2] = position_com[-2] + roi[0]

        position_max_com = list(position_max_com)
        position_max_com[-1] = position_max_com[-1] + roi[2]
        position_max_com[-2] = position_max_com[-2] + roi[0]

    plt.ion()
    methods = {
        "max": (position_max, "k"),
        "com": (position_com, "g"),
        "max_com": (position_max_com, "b"),
    }
    indices = {0: [2, 1], 1: [2, 0], 2: [1, 0]}
    fig, axes, _ = gu.multislices_plot(
        data,
        sum_frames=True,
        scale="log",
        plot_colorbar=True,
        vmin=0,
        vmax=6,
        title="data",
    )
    for ax, ind in indices.items():
        for method, values in methods.items():
            axes[ax].scatter(
                values[0][ind[0]],
                values[0][ind[1]],
                color=values[1],
                marker="1",
                alpha=0.7,
                linewidth=2,
                label=method,
            )
        axes[ax].legend()
    plt.pause(0.1)
    if savedir is not None:
        fig.savefig(savedir + "centering_method.png")
    return {
        "max": tuple(position_max),
        "com": tuple(position_com),
        "max_com": tuple(position_max_com),
    }


def grid_bcdi_labframe(
    data,
    mask,
    detector,
    setup,
    align_q=False,
    reference_axis=(0, 1, 0),
    debugging=False,
    **kwargs,
):
    """
    Interpolate BCDI reciprocal space data using a linearized transformation matrix.

    The resulting (qx, qy, qz) are in the laboratory frame (qx downstrean,
    qz vertical up, qy outboard).

    :param data: the 3D data, already binned in the detector frame
    :param mask: the corresponding 3D mask
    :param detector: an instance of the class Detector
    :param setup: instance of the Class experiment_utils.Setup()
    :param align_q: boolean, if True the data will be rotated such that q is along
     reference_axis, and q values will be calculated in the pseudo crystal frame.
    :param reference_axis: 3D vector along which q will be aligned, expressed in an
     orthonormal frame x y z
    :param debugging: set to True to see plots
    :param kwargs:

     - 'cmap': str, name of the colormap
     - 'fill_value': tuple of two real numbers, fill values to use for pixels outside
       of the interpolation range. The first value is for the data, the second for the
       mask. Default is (0, 0)
     - 'logger': an optional logger

    :return:

     - the data interpolated in the laboratory frame
     - the mask interpolated in the laboratory frame
     - a tuple of three 1D vectors of q values (qx, qz, qy)
     - a numpy array of shape (3, 3): transformation matrix from the detector
       frame to the laboratory/crystal frame

    """
    logger = kwargs.get("logger", module_logger)
    valid.valid_ndarray(arrays=(data, mask), ndim=3)
    # check and load kwargs
    valid.valid_kwargs(
        kwargs=kwargs,
        allowed_kwargs={"cmap", "fill_value", "logger", "reference_axis"},
        name="kwargs",
    )
    cmap = kwargs.get("cmap", "turbo")
    fill_value = kwargs.get("fill_value", (0, 0))
    valid.valid_container(
        fill_value,
        container_types=(tuple, list, np.ndarray),
        length=2,
        item_types=Real,
        name="fill_value",
    )

    # check some parameters
    if setup.rocking_angle == "energy":
        raise NotImplementedError(
            "Geometric transformation not yet implemented for energy scans"
        )
    valid.valid_item(align_q, allowed_types=bool, name="align_q")
    valid.valid_container(
        reference_axis,
        container_types=(tuple, list, np.ndarray),
        length=3,
        item_types=Real,
        name="reference_axis",
    )
    reference_axis = np.array(reference_axis)

    # grid the data
    logger.info(
        "Gridding the data using the linearized matrix, "
        "the result will be in the laboratory frame"
    )
    string = "linmat_reciprocal_space_"
    (interp_data, interp_mask), q_values, transfer_matrix = setup.ortho_reciprocal(
        arrays=(data, mask),
        verbose=True,
        debugging=debugging,
        fill_value=fill_value,
        align_q=align_q,
        reference_axis=reference_axis,
        scale=("log", "linear"),
        title=("data", "mask"),
    )
    qx, qz, qy = q_values

    # check for Nan
    interp_mask[np.isnan(interp_data)] = 1
    interp_data[np.isnan(interp_data)] = 0
    interp_mask[np.isnan(interp_mask)] = 1
    # set the mask as an array of integers, 0 or 1
    interp_mask[np.nonzero(interp_mask)] = 1
    interp_mask = interp_mask.astype(int)

    # apply the mask to the data
    interp_data[np.nonzero(interp_mask)] = 0

    # save plots of the gridded data
    final_binning = (
        detector.preprocessing_binning[0] * detector.binning[0],
        detector.preprocessing_binning[1] * detector.binning[1],
        detector.preprocessing_binning[2] * detector.binning[2],
    )

    numz, numy, numx = interp_data.shape
    plot_comment = (
        f"_{numz}_{numy}_{numx}_"
        f"{final_binning[0]}_{final_binning[1]}_{final_binning[2]}.png"
    )

    max_z = interp_data.sum(axis=0).max()
    fig, _, _ = gu.contour_slices(
        interp_data,
        (qx, qz, qy),
        sum_frames=True,
        title="Regridded data",
        levels=np.linspace(0, np.ceil(np.log10(max_z)), 150, endpoint=True),
        plot_colorbar=True,
        scale="log",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(detector.savedir + string + "sum" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.contour_slices(
        interp_data,
        (qx, qz, qy),
        sum_frames=False,
        title="Regridded data",
        levels=np.linspace(0, np.ceil(np.log10(interp_data.max())), 150, endpoint=True),
        plot_colorbar=True,
        scale="log",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(detector.savedir + string + "central" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.multislices_plot(
        interp_data,
        sum_frames=True,
        scale="log",
        plot_colorbar=True,
        vmin=0,
        title="Regridded data",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(detector.savedir + string + "sum_pix" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.multislices_plot(
        interp_data,
        sum_frames=False,
        scale="log",
        plot_colorbar=True,
        vmin=0,
        title="Regridded data",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(detector.savedir + string + "central_pix" + plot_comment)
    plt.close(fig)
    if debugging:
        gu.multislices_plot(
            interp_mask,
            sum_frames=False,
            scale="linear",
            plot_colorbar=True,
            vmin=0,
            title="Regridded mask",
            is_orthogonal=True,
            reciprocal_space=True,
            cmap=cmap,
        )

    return interp_data, interp_mask, q_values, transfer_matrix


def grid_bcdi_xrayutil(
    data, mask, scan_number, setup, frames_logical, hxrd, debugging=False, **kwargs
):
    """
    Interpolate BCDI reciprocal space data using xrayutilities package.

    The resulting (qx, qy, qz) are in the crystal frame (qz vertical).

    :param data: the 3D data, already binned in the detector frame
    :param mask: the corresponding 3D mask
    :param scan_number: the scan number to load
    :param setup: instance of the Class experiment_utils.Setup()
    :param frames_logical: array of initial length the number of measured frames.
     In case of padding the length changes. A frame whose index is set to 1 means
     that it is used, 0 means not used, -1 means padded (added) frame.
    :param hxrd: an initialized xrayutilities HXRD object used for the orthogonalization
     of the dataset
    :param debugging: set to True to see plots
    :param kwargs:

     - 'cmap': str, name of the colormap
     - 'logger': an optional logger

    :return: the data and mask interpolated in the crystal frame, q values
     (downstream, vertical up, outboard). q values are in inverse angstroms.
    """
    logger = kwargs.get("logger", module_logger)
    valid.valid_ndarray(arrays=(data, mask), ndim=3)
    cmap = kwargs.get("cmap", "turbo")
    numz, numy, numx = data.shape
    logger.info(
        "Gridding the data using xrayutilities package, "
        "the result will be in the crystal frame"
    )
    string = "xrutil_reciprocal_space_"
    if setup.filtered_data:
        logger.info(
            "Trying to orthogonalize a filtered data, "
            "the corresponding detector ROI should be provided "
            "otherwise q values will be wrong."
        )
    qx, qz, qy, frames_logical = setup.calc_qvalues_xrutils(
        hxrd=hxrd,
        nb_frames=numz,
        scan_number=scan_number,
        frames_logical=frames_logical,
    )

    maxbins: List[int] = []
    for dim in (qx, qy, qz):
        maxstep = max((abs(np.diff(dim, axis=j)).max() for j in range(3)))
        maxbins.append(int(abs(dim.max() - dim.min()) / maxstep))
    logger.info(f"Maximum number of bins based on the sampling in q: {maxbins}")
    maxbins = util.smaller_primes(maxbins, maxprime=7, required_dividers=(2,))
    logger.info(
        f"Maximum number of bins based on the shape requirements for FFT: {maxbins}"
    )
    # only rectangular cuboidal voxels are supported in xrayutilities FuzzyGridder3D
    gridder = xu.FuzzyGridder3D(*maxbins)
    #
    # define the width of data points (rectangular datapoints, xrayutilities use half
    # of these values but there are artefacts sometimes)
    wx = (qx.max() - qx.min()) / maxbins[0]
    wy = (qy.max() - qy.min()) / maxbins[1]
    wz = (qz.max() - qz.min()) / maxbins[2]
    # convert mask to rectangular grid in reciprocal space
    gridder(
        qx, qz, qy, mask, width=(wx, wz, wy)
    )  # qx downstream, qz vertical up, qy outboard
    interp_mask = np.copy(gridder.data)
    # convert data to rectangular grid in reciprocal space
    gridder(
        qx, qz, qy, data, width=(wx, wz, wy)
    )  # qx downstream, qz vertical up, qy outboard
    interp_data = gridder.data

    qx, qz, qy = [
        gridder.xaxis,
        gridder.yaxis,
        gridder.zaxis,
    ]  # downstream, vertical up, outboard
    # q values are 1D arrays

    # check for Nan
    interp_mask[np.isnan(interp_data)] = 1
    interp_data[np.isnan(interp_data)] = 0
    interp_mask[np.isnan(interp_mask)] = 1
    interp_mask = interp_mask.astype(int)

    # apply the mask to the data
    interp_data[np.nonzero(interp_mask)] = 0

    # plot the gridded data
    final_binning = (
        setup.detector.preprocessing_binning[0] * setup.detector.binning[0],
        setup.detector.preprocessing_binning[1] * setup.detector.binning[1],
        setup.detector.preprocessing_binning[2] * setup.detector.binning[2],
    )

    numz, numy, numx = interp_data.shape
    plot_comment = (
        f"_{numz}_{numy}_{numx}"
        f"_{final_binning[0]}_{final_binning[1]}_{final_binning[2]}.png"
    )

    max_z = interp_data.sum(axis=0).max()
    fig, _, _ = gu.contour_slices(
        interp_data,
        (qx, qz, qy),
        sum_frames=True,
        title="Regridded data",
        levels=np.linspace(0, np.ceil(np.log10(max_z)), 150, endpoint=True),
        plot_colorbar=True,
        scale="log",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(setup.detector.savedir + string + "sum" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.contour_slices(
        interp_data,
        (qx, qz, qy),
        sum_frames=False,
        title="Regridded data",
        levels=np.linspace(0, np.ceil(np.log10(interp_data.max())), 150, endpoint=True),
        plot_colorbar=True,
        scale="log",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(setup.detector.savedir + string + "central" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.multislices_plot(
        interp_data,
        sum_frames=True,
        scale="log",
        plot_colorbar=True,
        vmin=0,
        title="Regridded data",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(setup.detector.savedir + string + "sum_pix" + plot_comment)
    plt.close(fig)

    fig, _, _ = gu.multislices_plot(
        interp_data,
        sum_frames=False,
        scale="log",
        plot_colorbar=True,
        vmin=0,
        title="Regridded data",
        is_orthogonal=True,
        reciprocal_space=True,
        cmap=cmap,
    )
    fig.savefig(setup.detector.savedir + string + "central_pix" + plot_comment)
    plt.close(fig)
    if debugging:
        gu.multislices_plot(
            interp_mask,
            sum_frames=False,
            scale="linear",
            plot_colorbar=True,
            vmin=0,
            title="Regridded mask",
            is_orthogonal=True,
            reciprocal_space=True,
            cmap=cmap,
        )

    return interp_data, interp_mask, (qx, qz, qy), frames_logical


def load_bcdi_data(
    scan_number,
    setup,
    bin_during_loading=False,
    flatfield=None,
    hotpixels=None,
    background=None,
    normalize="skip",
    debugging=False,
    **kwargs,
):
    """
    Load Bragg CDI data, apply optional threshold, normalization and binning.

    :param scan_number: the scan number to load
    :param setup: an instance of the class Setup
    :param bin_during_loading: True to bin the data during loading (faster)
    :param flatfield: the 2D flatfield array
    :param hotpixels: the 2D hotpixels array. 1 for a hotpixel, 0 for normal pixels.
    :param background: the 2D background array to subtract to the data
    :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
     return a monitor based on the integrated intensity in the region of interest
     defined by detector.sum_roi, 'skip' to do nothing
    :param debugging:  set to True to see plots
    :param kwargs:

     - 'photon_threshold': float, photon threshold to apply before binning
     - 'frames_pattern': 1D array of int, of length data.shape[0]. If
       frames_pattern is 0 at index, the frame at data[index] will be skipped,
       if 1 the frame will added to the stack.
     - 'logger': an optional logger

    :return:
     - the 3D data and mask arrays
     - frames_logical: array of initial length the number of measured frames.
       In case of padding the length changes. A frame whose index is set to 1 means
       that it is used, 0 means not used, -1 means padded (added) frame.
     - the monitor values used for the intensity normalization

    """
    logger = kwargs.get("logger", module_logger)

    # check and load kwargs
    valid.valid_kwargs(
        kwargs=kwargs,
        allowed_kwargs={"photon_threshold", "frames_pattern", "logger"},
        name="kwargs",
    )
    photon_threshold = kwargs.get("photon_threshold", 0)
    valid.valid_item(
        photon_threshold,
        allowed_types=Real,
        min_included=0,
        name="photon_threshold",
    )
    frames_pattern = kwargs.get("frames_pattern")
    valid.valid_1d_array(
        frames_pattern, allow_none=True, allowed_values={0, 1}, name="frames_pattern"
    )

    rawdata, rawmask, monitor, frames_logical = setup.loader.load_check_dataset(
        scan_number=scan_number,
        setup=setup,
        frames_pattern=frames_pattern,
        bin_during_loading=bin_during_loading,
        flatfield=flatfield,
        hotpixels=hotpixels,
        background=background,
        normalize=normalize,
        debugging=debugging,
    )

    #####################################################
    # apply an optional photon threshold before binning #
    #####################################################
    if photon_threshold != 0:
        rawmask[rawdata < photon_threshold] = 1
        rawdata[rawdata < photon_threshold] = 0
        logger.info(f"Applying photon threshold before binning: < {photon_threshold}")

    ####################################################################################
    # bin data and mask in the detector plane if not already done during loading       #
    # binning in the stacking dimension is done at the very end of the data processing #
    ####################################################################################
    if not bin_during_loading and (
        (setup.detector.binning[1] != 1) or (setup.detector.binning[2] != 1)
    ):
        logger.info(
            f"Binning the data: detector vertical axis by {setup.detector.binning[1]}, "
            f"detector horizontal axis by {setup.detector.binning[2]}"
        )
        rawdata = util.bin_data(
            rawdata,
            (1, setup.detector.binning[1], setup.detector.binning[2]),
            debugging=False,
        )
        rawmask = util.bin_data(
            rawmask,
            (1, setup.detector.binning[1], setup.detector.binning[2]),
            debugging=False,
        )
        rawmask[np.nonzero(rawmask)] = 1

    # update the current binning factor
    setup.detector.current_binning = list(
        map(
            mul,
            setup.detector.current_binning,
            (1, setup.detector.binning[1], setup.detector.binning[2]),
        )
    )
    ################################################
    # pad the data to the shape defined by the ROI #
    ################################################
    rawdata, rawmask = util.pad_from_roi(
        arrays=(rawdata, rawmask),
        roi=setup.detector.roi,
        binning=setup.detector.binning[1:],
        pad_value=(0, 1),
    )

    return rawdata, rawmask, frames_logical, monitor


def reload_bcdi_data(
    data,
    mask,
    scan_number,
    setup,
    normalize=False,
    debugging=False,
    **kwargs,
):
    """
    Reload BCDI data, apply optional threshold, normalization and binning.

    :param data: the 3D data array
    :param mask: the 3D mask array
    :param scan_number: the scan number to load
    :param setup: an instance of the class Setup
    :param normalize: set to "monitor" to normalize by the default monitor of
     the beamline, otherwise set to "skip"
    :param debugging:  set to True to see plots
    :parama kwargs:

     - 'photon_threshold' = float, photon threshold to apply before binning
     - 'logger': an optional logger

    :return:
     - the updated 3D data and mask arrays
     - the monitor values used for the intensity normalization

    """
    logger = kwargs.get("logger", module_logger)
    valid.valid_ndarray(arrays=(data, mask), ndim=3)
    # check and load kwargs
    valid.valid_kwargs(
        kwargs=kwargs,
        allowed_kwargs={"logger", "photon_threshold"},
        name="kwargs",
    )
    photon_threshold = kwargs.get("photon_threshold", 0)
    valid.valid_item(
        photon_threshold,
        allowed_types=Real,
        min_included=0,
        name="photon_threshold",
    )

    nbz, nby, nbx = data.shape
    frames_logical = np.ones(nbz)

    logger.info(f"{(data < 0).sum()} negative data points masked")
    # can happen when subtracting a background
    mask[data < 0] = 1
    data[data < 0] = 0

    # normalize by the incident X-ray beam intensity
    if normalize == "skip":
        logger.info("Skip intensity normalization")
        monitor = []
    else:  # use the default monitor of the beamline
        monitor = setup.loader.read_monitor(
            scan_number=scan_number,
            setup=setup,
        )

        logger.info(f"Intensity normalization using {normalize}")
        data, monitor = loader.normalize_dataset(
            array=data,
            monitor=monitor,
            norm_to_min=True,
            savedir=setup.detector.savedir,
            debugging=True,
            logger=logger,
        )

    # pad the data to the shape defined by the ROI
    if (
        setup.detector.roi[1] - setup.detector.roi[0] > nby
        or setup.detector.roi[3] - setup.detector.roi[2] > nbx
    ):
        start = (np.nan, min(0, setup.detector.roi[0]), min(0, setup.detector.roi[2]))
        logger.info("Paddind the data to the shape defined by the ROI")
        data = util.crop_pad(
            array=data,
            pad_start=start,
            output_shape=(
                data.shape[0],
                setup.detector.roi[1] - setup.detector.roi[0],
                setup.detector.roi[3] - setup.detector.roi[2],
            ),
        )
        mask = util.crop_pad(
            array=mask,
            pad_value=1,
            pad_start=start,
            output_shape=(
                mask.shape[0],
                setup.detector.roi[1] - setup.detector.roi[0],
                setup.detector.roi[3] - setup.detector.roi[2],
            ),
        )

    # apply optional photon threshold before binning
    if photon_threshold != 0:
        mask[data < photon_threshold] = 1
        data[data < photon_threshold] = 0
        logger.info(f"Applying photon threshold before binning: < {photon_threshold}")

    # bin data and mask in the detector plane if needed
    # binning in the stacking dimension is done at the very end of the data processing
    if (setup.detector.binning[1] != 1) or (setup.detector.binning[2] != 1):
        logger.info(
            "Binning the data: setup.detector vertical axis by "
            f"{setup.detector.binning[1]}, setup.detector horizontal axis by "
            f"{setup.detector.binning[2]}"
        )
        data = util.bin_data(
            data,
            (1, setup.detector.binning[1], setup.detector.binning[2]),
            debugging=debugging,
        )
        mask = util.bin_data(
            mask,
            (1, setup.detector.binning[1], setup.detector.binning[2]),
            debugging=debugging,
        )
        mask[np.nonzero(mask)] = 1
        setup.detector.current_binning = list(
            map(
                mul,
                setup.detector.current_binning,
                (1, setup.detector.binning[1], setup.detector.binning[2]),
            )
        )

    return data, mask, frames_logical, monitor


def show_rocking_curve(
    data: np.ndarray,
    peaks: Dict[str, Optional[Tuple[int, int, int]]],
    peak_method: str,
    detector_roi: Union[Tuple[int, int, int, int], List[int]],
    binning: Union[Tuple[int, int, int], List[int]],
    window_width: Optional[Union[Tuple[int, int], List[int]]] = (100, 100),
    tilt_values: Optional[Union[List[float], np.ndarray]] = None,
    savedir: Optional[str] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Calculate the integrated intensity along a rocking curve and plot it.

    The data is expected to be stacked, the first axis corresponding to the rocking
    angle and axes 1 and 2 to the detector plane (vertical, horizontal).

    :param data: the stacked rocking curve data
    :param peaks: a dictionary containing the peak-finding method as key and the peak
     position as value
    :param peak_method: the user-defined peak method
    :param detector_roi: roi used when loading the detector data
    :param binning: binning factor used when loading the detector data
    :param window_width: width in pixels of the window use to integrate the intensity
     for the rocking curve line plot and to plot the detector slice at the peak position
    :param tilt_values: the angular values along the rocking curve
    :param savedir: path to the saving directory
    :param kwargs:

     - 'logger': an optional logger

    :return: a dictionary containing the output metadata
    """
    logger = kwargs.get("logger", module_logger)

    # check parameters
    allowed_methods = {"max", "com", "max_com", "user", "skip"}
    if peak_method not in allowed_methods:
        raise ValueError(f"allowed peak methods {allowed_methods}, got {peak_method}")

    valid.valid_ndarray(data, ndim=3, name="data")
    nb_frames = data.shape[0]

    valid.valid_container(
        window_width,
        container_types=(tuple, list),
        length=2,
        item_types=int,
        allow_none=True,
        name="integration_roi",
    )
    if window_width is None:
        window_width = (data.shape[1], data.shape[2])
    elif window_width[0] > data.shape[1] or window_width[1] > data.shape[2]:
        logger.info(
            f"window_width {window_width} larger than the frame size {data.shape[1:3]},"
            " using the full frame instead"
        )
        window_width = (data.shape[1], data.shape[2])

    valid.valid_container(
        tilt_values,
        container_types=(tuple, list, np.ndarray),
        length=nb_frames,
        item_types=Real,
        allow_none=True,
        name="tilt_values",
    )
    tilt_values = np.array(tilt_values)
    if tilt_values is None:
        tilt_values = np.arange(nb_frames)
        x_label = "Frame number"
    else:
        x_label = "Rocking angle (deg)"

    valid.valid_container(savedir, container_types=str, allow_none=True, name="savedir")
    if savedir is not None:
        pathlib.Path(savedir).mkdir(parents=True, exist_ok=True)
    bragg_peak = peaks[peak_method]
    if bragg_peak is None:
        raise ValueError(f"Bragg peak not detected with method {peak_method}")
    roi_center = (
        bragg_peak[0],
        (bragg_peak[1] - detector_roi[0]) // binning[1],
        (bragg_peak[2] - detector_roi[2]) // binning[2],
    )

    # calculate the offset indices due to the window_width (need to compensate the
    # peak positions for that offset in plots)
    offset_indices = [
        np.clip(roi_center[1] - window_width[0] // 2, 0, data.shape[1]),
        np.clip(roi_center[1] + window_width[0] // 2, 0, data.shape[1]),
        np.clip(roi_center[2] - window_width[1] // 2, 0, data.shape[2]),
        np.clip(roi_center[2] + window_width[1] // 2, 0, data.shape[2]),
    ]
    rocking_curve = data[
        :,
        offset_indices[0] : offset_indices[1],
        offset_indices[2] : offset_indices[3],
    ].sum(axis=(1, 2))

    interpolation = interp1d(tilt_values, rocking_curve, kind="cubic")
    interp_points = 5 * nb_frames
    interp_tilt = np.linspace(tilt_values.min(), tilt_values.max(), interp_points)
    interp_curve = interpolation(interp_tilt)
    interp_fwhm = (
        len(np.argwhere(interp_curve >= interp_curve.max() / 2))
        * (tilt_values.max() - tilt_values.min())
        / (interp_points - 1)
    )
    logger.info(f"FWHM by interpolation: {interp_fwhm:.3f} deg")

    plt.ion()
    fig, (ax0, ax1) = plt.subplots(2, 1, sharex="col", figsize=(10, 5))
    ax0.plot(tilt_values, rocking_curve, ".")
    ax0.plot(interp_tilt, interp_curve)
    ax0.axvline(tilt_values[roi_center[0]], color="r", alpha=0.7, linewidth=1)
    ax0.set_ylabel("Integrated intensity")
    ax0.legend(("data", "interpolation"))
    ax0.set_title(f"Rocking curve in a {window_width[0]}x{window_width[1]} roi")
    ax1.plot(tilt_values, np.log10(rocking_curve), ".")
    ax1.plot(interp_tilt, np.log10(interp_curve))
    ax1.axvline(tilt_values[roi_center[0]], color="r", alpha=0.7, linewidth=1)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel("Log(integrated intensity)")
    ax0.legend(("data", "interpolation"))
    plt.pause(0.1)
    if savedir is not None:
        fig.savefig(savedir + "rocking_curve.png")
    plt.close(fig)

    fig, _ = plt.subplots(1, 1, figsize=(10, 5))
    plt.imshow(
        np.log10(
            abs(
                data[
                    roi_center[0],
                    offset_indices[0] : offset_indices[1],
                    offset_indices[2] : offset_indices[3],
                ]
            )
        ),
        vmin=0,
        vmax=5,
    )
    colors = ["k", "g", "b", "r"]
    idx = 0
    for key, peak in peaks.items():
        if peak is not None:
            detected_peak = (
                peak[0],
                (peak[1] - detector_roi[0]) // binning[1] - offset_indices[0],
                (peak[2] - detector_roi[2]) // binning[2] - offset_indices[2],
            )

            plt.scatter(
                detected_peak[2],
                detected_peak[1],
                color=colors[idx],
                marker="1",
                alpha=0.7,
                linewidth=2,
                label=f"{key}={peak}",
            )
            idx += 1
    plt.title(f"User_defined method '{peak_method}'")
    plt.colorbar()
    plt.legend()
    plt.pause(0.1)
    if savedir is not None:
        fig.savefig(savedir + "central_slice.png")
    plt.close(fig)
    plt.ioff()

    metadata = {
        "tilt_values": tilt_values,
        "rocking_curve": rocking_curve,
        "interp_tilt_values": interp_tilt,
        "interp_rocking_curve": interp_curve,
        "interp_fwhm": interp_fwhm,
        "tilt_value_at_peak": tilt_values[roi_center[0]],
        "detector_data_at_peak": data[roi_center[0], :, :],
    }

    return metadata


def zero_pad(array, padding_width=np.zeros(6), mask_flag=False, debugging=False):
    """
    Pad obj with zeros.

    :param array: 3D array to be padded
    :param padding_width: number of zero pixels to padd on each side
    :param mask_flag: set to True to pad with 1, False to pad with 0
    :type mask_flag: bool
    :param debugging: set to True to see plots
    :type debugging: bool
    :return: obj padded with zeros
    """
    valid.valid_ndarray(arrays=array, ndim=3)
    nbz, nby, nbx = array.shape

    if debugging:
        gu.multislices_plot(
            array=array,
            sum_frames=False,
            plot_colorbar=True,
            vmin=0,
            vmax=1,
            title="Array before padding",
        )

    if mask_flag:
        newobj = np.ones(
            (
                nbz + padding_width[0] + padding_width[1],
                nby + padding_width[2] + padding_width[3],
                nbx + padding_width[4] + padding_width[5],
            )
        )
    else:
        newobj = np.zeros(
            (
                nbz + padding_width[0] + padding_width[1],
                nby + padding_width[2] + padding_width[3],
                nbx + padding_width[4] + padding_width[5],
            )
        )

    newobj[
        padding_width[0] : padding_width[0] + nbz,
        padding_width[2] : padding_width[2] + nby,
        padding_width[4] : padding_width[4] + nbx,
    ] = array

    if debugging:
        gu.multislices_plot(
            array=newobj,
            sum_frames=False,
            plot_colorbar=True,
            vmin=0,
            vmax=1,
            title="Array after padding",
        )
    return newobj
