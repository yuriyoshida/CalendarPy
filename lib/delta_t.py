"""
Class for Delta-T calculation.
"""
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import const as lcst


class DeltaT:
    def __init__(self, year, month, utc_tai, dut1):
        """ Initialization

        :param int year
        :param int month
        """
        self.year, self.month = year, month
        self.y = year + (month - 0.5) / 12
        self.utc_tai = utc_tai
        self.dut1 = dut1

    def delta_t(self):
        """ Delta-T calculation """
        try:
            if                         self.year <  -500:
                dt = self.__before_m500()
            elif -500 <= self.year and self.year <   500:
                dt = self.__before_500()
            elif  500 <= self.year and self.year <  1600:
                dt = self.__before_1600()
            elif 1600 <= self.year and self.year <  1700:
                dt = self.__before_1700()
            elif 1700 <= self.year and self.year <  1800:
                dt = self.__before_1800()
            elif 1800 <= self.year and self.year <  1860:
                dt = self.__before_1860()
            elif 1860 <= self.year and self.year <  1900:
                dt = self.__before_1900()
            elif 1900 <= self.year and self.year <  1920:
                dt = self.__before_1920()
            elif 1920 <= self.year and self.year <  1941:
                dt = self.__before_1941()
            elif 1941 <= self.year and self.year <  1961:
                dt = self.__before_1961()
            elif 1961 <= self.year and self.year <  1986:
                dt = self.__before_1986()
            elif 1986 <= self.year and self.year <  2005:
                dt = self.__before_2005()
            elif 2005 <= self.year and self.year <  2050:
                dt = self.__before_2050()
            elif 2050 <= self.year and self.year <= 2150:
                dt = self.__until_2150()
            elif 2150 <  self.year:
                dt = self.__after_2150()
            return dt
        except Exception as e:
            raise

    def __before_m500(self):
        """ year < -500

        :return float
        """
        try:
            t = (self.y - 1820) / 100
            return -20 + 32 * t ** 2
        except Exception as e:
            raise

    def __before_500(self):
        """ -500 <= year and year < 500

        :return float
        """
        t = self.y / 100
        try:
            return 10583.6           \
                + (-1014.41          \
                + (   33.78311       \
                + (   -5.952053      \
                + (   -0.1798452     \
                + (    0.022174192   \
                + (    0.0090316521) \
                * t) * t) * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1600(self):
        """ 500 <= year and year < 1600

        :return float
        """
        t = (self.y - 1000) / 100
        try:
            return 1574.2           \
                + (-556.01          \
                + (  71.23472       \
                + (   0.319781      \
                + (  -0.8503463     \
                + (  -0.005050998   \
                + (   0.0083572073) \
                * t) * t) * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1700(self):
        """ 1600 <= year and year < 1700

        :return float
        """
        t = self.y - 1600
        try:
            return 120           \
                + ( -0.9808      \
                + ( -0.01532     \
                + (  1.0 / 7129) \
                * t) * t) * t
        except Exception as e:
            raise

    def __before_1800(self):
        """ 1700 <= year and year < 1800

        :return float
        """
        t = self.y - 1700
        try:
            return 8.83           \
               + ( 0.1603         \
               + (-0.0059285      \
               + ( 0.00013336     \
               + (-1.0 / 1174000) \
               * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1860(self):
        """ 1800 <= year and year < 1860

        :return float
        """
        t = self.y - 1800
        try:
            return 13.72            \
                + (-0.332447        \
                + ( 0.0068612       \
                + ( 0.0041116       \
                + (-0.00037436      \
                + ( 0.0000121272    \
                + (-0.0000001699    \
                + ( 0.000000000875) \
                * t) * t) * t) * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1900(self):
        """ 1860 <= year and year < 1900

        :return float
        """
        t = self.y - 1860
        try:
            return 7.62          \
               + ( 0.5737        \
               + (-0.251754      \
               + ( 0.01680668    \
               + (-0.0004473624  \
               + ( 1.0 / 233174) \
               * t) * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1920(self):
        """ 1900 <= year and year < 1920

        :return float
        """
        t = self.y - 1900
        try:
            return -2.79      \
                + ( 1.494119  \
                + (-0.0598939 \
                + ( 0.0061966 \
                + (-0.000197) \
                * t) * t) * t) * t
        except Exception as e:
            raise

    def __before_1941(self):
        """ 1920 <= year and year < 1941

        :return float
        """
        t = self.y - 1920
        try:
            return 21.20       \
                + ( 0.84493    \
                + (-0.076100   \
                + ( 0.0020936) \
                * t) * t) * t
        except Exception as e:
            raise

    def __before_1961(self):
        """ 1941 <= year and year < 1961

        :return float
        """
        t = self.y - 1950
        try:
            return 29.07        \
                + ( 0.407       \
                + (-1.0 / 233   \
                + ( 1.0 / 2547) \
                * t) * t) * t
        except Exception as e:
            raise

    def __before_1986(self):
        """ 1961 <= year and year < 1986

        :return float
        """
        utc = datetime(self.year, self.month, 1)
        t = self.y - 1975
        try:
            # うるう秒実施より前は NASA 提供の略算式で
            if self.utc_tai == 0:
                return 45.45       \
                    + ( 1.067      \
                    + (-1.0 / 260  \
                    + (-1.0 / 718) \
                    * t) * t) * t
            else:
                return lcst.TT_TAI - self.utc_tai - self.dut1
        except Exception as e:
            raise

    def __before_2005(self):
        """ 1986 <= year and year < 2005

        :return float
        """
        utc = datetime(self.year, self.month, 1)
        t = self.y - 2000
        try:
            # 以下の7行は NASA 提供の略算式を使用する場合
            #return 63.86           \
            #    + ( 0.3345         \
            #    + (-0.060374       \
            #    + ( 0.0017275      \
            #    + ( 0.000651814    \
            #    + ( 0.00002373599) \
            #    * t) * t) * t) * t) * t
            return lcst.TT_TAI - self.utc_tai - self.dut1
        except Exception as e:
            raise

    def __before_2050(self):
        """ 2005 <= year and year < 2050

        :return float
        """
        utc = datetime(self.year, self.month, 1)
        t = self.y - 2000
        try:
            # うるう秒未定部分は NASA 提供の略算式で
            if self.utc_tai == 0:
                return 62.92      \
                    + ( 0.32217   \
                    + ( 0.005589) \
                    * t) * t
            else:
                return lcst.TT_TAI - self.utc_tai - self.dut1
        except Exception as e:
            raise

    def __until_2150(self):
        """ 2050 <= year and year <= 2150

        :return float
        """
        try:
            return - 20 \
                   + 32 * ((self.y - 1820) / 100) ** 2 \
                   - 0.5628 * (2150 - self.y)
        except Exception as e:
            raise

    def __after_2150(self):
        """ 2150 < year

        :return float
        """
        t = (self.y - 1820) / 100
        try:
            return -20 + 32 * t ** 2
        except Exception as e:
            raise

