"""Test the flash age compositor."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Satpy developers
#
# This file is part of satpy.
#
# satpy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# satpy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# satpy.  If not, see <http://www.gnu.org/licenses/>.


import datetime

import numpy as np
import xarray as xr

from satpy.composites.lightning import LightningTimeCompositor


def test_flash_age_compositor():
    """Test the flash_age compsitor by comparing two xarrays object."""
    comp = LightningTimeCompositor("flash_age",prerequisites=["flash_time"],
                                   standard_name="ligtning_time",
                                   time_range=60,
                                   reference_time="end_time")
    attrs_flash_age = {"variable_name": "flash_time","name": "flash_time",
                       "start_time": datetime.datetime(2024, 8, 1, 10, 50, 0),
                       "end_time": datetime.datetime(2024, 8, 1, 11, 0, 0),"reader": "li_l2_nc"}
    flash_age_value = np.array(["2024-08-01T09:00:00",
            "2024-08-01T10:00:00", "2024-08-01T10:30:00","2024-08-01T11:00:00"], dtype="datetime64[ns]")
     #Coordinates data (assuming you have longitude and latitude arrays)
    flash_age = xr.DataArray(
    flash_age_value,
    dims=["y"],
    coords={
        "crs": "8B +proj=longlat +ellps=WGS84 +type=crs"
    },attrs = attrs_flash_age,name="flash_time")
    res = comp([flash_age])
    expected_attrs = {"variable_name": "flash_time","name": "lightning_time",
                       "start_time": datetime.datetime(2024, 8, 1, 10, 50, 0),
                       "end_time": datetime.datetime(2024, 8, 1, 11, 0, 0),"reader": "li_l2_nc",
                       "standard_name": "ligtning_time"
                       }
    expected_array = xr.DataArray(
    np.array([0.0,0.5,1.0]),
    dims=["y"],
    coords={
        "crs": "8B +proj=longlat +ellps=WGS84 +type=crs"
    },attrs = expected_attrs,name="flash_time")
    xr.testing.assert_equal(res,expected_array)
