# -*- coding: utf-8 -*-

"""
Geospatial utilities to interleave and deinterleave co-ordinates.
"""

from __future__ import division

from collections import namedtuple
import math

from morton import deinterleave_64, interleave_64, UINT32

_LonLat = namedtuple('_LonLat', ['lon', 'lat'])
class LonLat(_LonLat):
    """
    LonLat namedtuple allowing you to refer co-ordinates as x or y too.

    In the Global Co-ordinates System, the longitude range is [-180, 180]
    which we'll transpose as [0, 360].
    Likewise, for latitudes, we refer to the [-90, 90] range as [0, 180]
    """
    MIN_LON = 0
    MAX_LON = 360

    MIN_LAT = 0
    MAX_LAT = 180

    @property
    def x(self):
        return self.lon

    @property
    def y(self):
        return self.lat

    @property
    def interleaved(self):
        """
        Returns a 64-bit interleaved integer of the co-ordinates.
        """
        lon_range = int(math.ceil(self.MAX_LON - self.MIN_LON))
        lat_range = int(math.ceil(self.MAX_LAT - self.MIN_LAT))

        # Preventing ourselves from exceeding the range.
        # These will be between [0..1]
        indexed_lon = min(
            self.MAX_LON,
            max(self.MIN_LON,
                (self.lon + (lon_range / 2)) / lon_range)
        )
        indexed_lat = min(
            self.MAX_LAT,
            max(self.MIN_LAT,
                (self.lat + (lat_range / 2)) / lat_range
            )
        )

        return interleave_64(int(indexed_lon * UINT32),
                             int(indexed_lat * UINT32))

    @classmethod
    def deinterleave(cls, coordinates):
        lon_range = int(math.ceil(cls.MAX_LON - cls.MIN_LON))
        lat_range = int(math.ceil(cls.MAX_LAT - cls.MIN_LAT))

        lon, lat = deinterleave_64(coordinates)

        # UINT32 here is because it is what we used to interleave
        deranged_lon = lon * lon_range / UINT32 - lon_range / 2
        deranged_lat = lat * lat_range / UINT32 - lat_range / 2

        return cls(lon=deranged_lon, lat=deranged_lat)


class MercatorLonLat(LonLat):
    """
    For Auxiliary Spheroid, ESRI says:
    Xmin: -20037507.0671618  - 180°W
    Ymin: -19971868.8804086  - 85°S
    Xmax: 20037507.0671618   - 180°E
    Ymax: 19971868.8804086   - 85°N

    For the Google/Bing projection, we say:
    Xmin: -20037508.342789244  - 180°W
    Ymin: -19971868.880408563  - 85°S
    Xmax: 20037508.342789244   - 180°E
    Ymax: 19971868.88040853    - 85°N

    Ref.: http://alastaira.wordpress.com/2011/01/23/the-google-maps-bing-maps-spherical-mercator-projection/
    """

    # The constant 6378137 is the major axis of the spheroid used by
    # the Web Mercator projection (EPSG 3785).
    HALF_CIRCUMFERENCE = math.pi * 6378137

    MIN_LON = 0.0
    MAX_LON = 40075016.68557849

    MIN_LAT = 0.0
    MAX_LAT = 39943737.76081706

    @classmethod
    def deproject(cls, projected_lonlat):
        """
        Deprojects a projected LonLat point.

        Beware that this will fail if the resulting latitude is between
        [-90, -85) or (85, 90].
        """
        deproj_lon = projected_lonlat.lon / cls.HALF_CIRCUMFERENCE * 180

        deproj_lat = projected_lonlat.lat / cls.HALF_CIRCUMFERENCE * 180
        adjusted_lat = 180 / math.pi * \
            (2 * math.atan(math.exp(deproj_lat * math.pi / 180)) - math.pi / 2)

        return LonLat(lon=deproj_lon, lat=adjusted_lat)

    @classmethod
    def project(cls, lonlat):
        """
        Projects a LonLat point.

        Beware that this will fail if the latitude is between [-90, -85)
        or (85, 90].
        """
        proj_lon = lonlat.lon * cls.HALF_CIRCUMFERENCE / 180


        proj_lat = math.log(math.tan((90 + lonlat.lat) * math.pi / 360)) / \
                   (math.pi / 180)
        proj_lat *= cls.HALF_CIRCUMFERENCE / 180

        return cls(lon=proj_lon, lat=proj_lat)
