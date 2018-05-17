#! /usr/local/bin/python3.6
"""
----------------------------------------------------
海上保安庁の天測暦より太陽・月の視位置を計算
（視黄経・視黄緯を含まない）

  date          name            version
  2018.03.28    mk-mode.com     1.00 新規作成

  Copyright(C) 2018 mk-mode.com All Rights Reserved.
----------------------------------------------------
 引数 : JST（日本標準時）
          書式：YYYYMMDD or YYYYMMDDHHMMSS
          無指定なら現在(システム日時)と判断。
----------------------------------------------------
"""
import datetime
import math
import re
import sys
import traceback
import consts as cst


class EphSunMoon:
    JST_UTC = 9  # JST - UTC
    MSG_ERR_1 = "[ERROR] Format: YYYYMMDD or YYYYMMDDHHMMSS"
    MSG_ERR_2 = "[ERROR] It should be between 20080101090000 and 20190101085959."
    MSG_ERR_3 = "[ERROR] Invalid date!"
    DIVS = {
        "SUN_RA":   cst.SUN_RA,
        "SUN_DEC":  cst.SUN_DEC,
        "SUN_DIST": cst.SUN_DIST,
        "MOON_RA":  cst.MOON_RA,
        "MOON_DEC": cst.MOON_DEC,
        "MOON_HP":  cst.MOON_HP,
        "R":        cst.R,
        "EPS":      cst.EPS
    }
    DELTA_T = {
        2008: 65, 2009: 66, 2010: 66, 2011: 67, 2012: 67, 2013: 67,
        2014: 67, 2015: 68, 2016: 68, 2017: 68, 2018: 69
    }

    def __init__(self):
        self.vals = {}    # 所要値格納用dict
        self.__get_arg()  # 引数取得

    def exec(self):
        """ 実行 """
        try:
            self.__calc_t()       # 通日 T の計算
            self.__calc_f()       # 世界時 UT(時・分・秒) の端数計算
            self.__get_delta_t()  # ΔT（世界時 - 地球時）の取得
            self.__calc_tm()      # 計算用時刻引数 tm の計算
            self.__calc()         # 各種計算
            self.__display()      # 結果出力
        except Exception as e:
            raise

    def __get_arg(self):
        """ 引数取得
            * コマンドライン引数を取得して日時の妥当性チェックを行う。
            * コマンドライン引数無指定なら、現在日時とする。
            * JST, UTC をインスタンス変数 jst, utc に格納する。
        """
        try:
            if len(sys.argv) < 2:
                self.jst = datetime.datetime.now()
            else:
                arg = sys.argv[1]
                if re.search(r"^([0-9]{8}|[0-9]{14})$", arg) is None:
                    print(self.MSG_ERR_1)
                    sys.exit()
                arg = arg.ljust(14, "0")
                try:
                    self.jst = datetime.datetime.strptime(arg, "%Y%m%d%H%M%S")
                except ValueError:
                    print(self.MSG_ERR_3)
                    sys.exit(1)
            self.utc = self.jst - datetime.timedelta(hours=self.JST_UTC)
        except Exception as e:
            raise

    def __calc_t(self):
        """ 通日 T の計算
            * 通日 T は1月0日を第0日とした通算日数で、次式により求める。
                T = 30 * P + Q * (S - Y) + P * (1 - Q) + 日
              但し、
                P = 月 - 1, Q = [(月 + 7) / 10]
                Y = [(年 / 4) - [(年 / 4)] + 0.77]
                S = [P * 0.55 - 0.33]
              で、[] は整数部のみを抜き出すことを意味する。
            * 求めた通日 T はインスタンス変数 t に格納する。
        """
        try:
            p = self.utc.month - 1
            q = (self.utc.month + 7) // 10
            y = int(self.utc.year / 4 - self.utc.year // 4 + 0.77)
            s = int(p * 0.55 - 0.33)
            self.t = 30 * p + q * (s - y) + p * (1 - q) + self.utc.day
        except Exception as e:
            raise

    def __calc_f(self):
        """ 世界時 UT(時・分・秒) の端数計算
            * 次式により求め、インスタンス変数 f に格納する。
                F = 時 / 24 + 分 / 1440 + 秒 / 86400
        """
        try:
            self.f = self.utc.hour / 24 \
                   + self.utc.minute / 1440 \
                   + self.utc.second / 86400
        except Exception as e:
            raise

    def __get_delta_t(self):
        """ ΔT（世界時 - 地球時）の取得
            * あらかじめ予測されている ΔT の値を取得し、インスタンス変数 delta_t
              に格納する。
        """
        try:
            self.delta_t = self.DELTA_T[self.utc.year]
        except Exception as e:
            raise

    def __calc_tm(self):
        """ 計算用時刻引数 tm の計算
            * 次式により求め、インスタンス変数 tm, tm_r に格納する。
              (R 計算用は tm_r, その他は tm)
                tm   = T + F + ΔT / 86400
                tm_r = T + F
        """
        try:
            self.tm_r = self.t + self.f
            self.tm   = self.tm_r + self.delta_t / 86400
        except Exception as e:
            raise

    def __calc(self):
        """ 各種計算
            * 各種値を計算し、インスタンス変数 vals に格納する。
        """
        try:
            # 各種係数からの計算
            for div, vals in self.DIVS.items():
                a, b, coeffs = self.__get_coeffs(vals)    # 係数値等の取得
                t = self.tm_r if div == "R" else self.tm  # 計算用時刻引数
                theta = self.__calc_theta(a, b, t)        # θ の計算
                val = self.__calc_ft(theta, coeffs)       # 所要値の計算
                if re.search(r"(_RA|^R)$", div) is not(None):
                    while val >= 24.0:
                        val -= 24.0
                    while val <= 0.0:
                        val += 24.0
                self.vals[div] = val
            # グリニジ時角の計算
            self.vals["SUN_H" ] = self.__calc_h(self.vals["SUN_RA" ])
            self.vals["MOON_H"] = self.__calc_h(self.vals["MOON_RA"])
            # 視半径の計算
            self.vals["SUN_SD" ] = self.__calc_sd_sun()
            self.vals["MOON_SD"] = self.__calc_sd_moon()
        except Exception as e:
            raise

    def __get_coeffs(self, vals):
        """ 係数等の取得
            * 引数の文字列の定数配列から a, b, 係数配列を取得する。

        :param  list vals: 定数名
        :return list: [a, b, 係数配列]
        """
        a, b = 0, 0
        coeffs = []
        try:
            for row in vals:
                if row[0] != self.utc.year:
                    continue
                if row[1][0] <= int(self.tm) and int(self.tm) <= row[1][1]:
                    a, b   = row[1]
                    coeffs = row[2]
                    break
            return [a, b, coeffs]
        except Exception as e:
            raise

    def __calc_theta(self, a, b, t):
        """ θ の計算
            * θ を次式により計算する。
                θ = cos^(-1)((2 * t - (a + b)) / (b - a))
              但し、0°<= θ <= 180°

        :param  int   a
        :param  int   b
        :param  float t
        :return float theta: 単位: °
        """
        try:
            if b < t:  # 年末のΔT秒分も計算可能とするための応急処置
                b = t
            theta = (2 * t - (a + b)) / (b - a)
            theta = math.acos(theta) * 180 / math.pi
            return theta
        except Exception as e:
            raise

    def __calc_ft(self, theta, coeffs):
        """ 所要値の計算
            * θ, 係数配列から次式により所要値を計算する。
                f(t) = C_0 + C_1 * cos(θ) + C_2 * cos(2θ) + ... + C_N * cos(Nθ)

        :param  float theta: θ
        :param  list coeffs: 係数配列
        :return float    ft: 所要値
        """
        ft = 0.0
        try:
            for i, c in enumerate(coeffs):
                ft += c * math.cos(theta * i * math.pi / 180)
            return ft
        except Exception as e:
            raise

    def __calc_h(self, ra):
        """ グリニジ時角の計算
            * 次式によりグリニジ時角を計算する。
                h = E + UT
              (但し、E = R - R.A.)

        :param  float ra: R.A.
        :return float  h: 単位 h
        """
        try:
            e = self.vals["R"] - ra
            h = e + self.f * 24
            return h
        except Exception as e:
            raise

    def __calc_sd_sun(self):
        """ 視半径（太陽）の計算
            * 次式により視半径を計算する。
                S.D.= 16.02 ′/ Dist.

        :return float sd: 単位 ′
        """
        try:
            sd = 16.02 / self.vals["SUN_DIST"]
            return sd
        except Exception as e:
            raise

    def __calc_sd_moon(self):
        """ 視半径（月）の計算
            * 次式により視半径を計算する。
                S.D.= sin^(-1) (0.2725 * sin(H.P.))

        :return float sd: 単位 ′
        """
        try:
            sd = 0.2725 * math.sin(self.vals["MOON_HP"] * math.pi / 180.0)
            sd = math.asin(sd) * 60.0 * 180.0 / math.pi
            return sd
        except Exception as e:
            raise

    def __display(self):
        """ 結果出力 """
        try:
            s  = "[ JST: {},".format(self.jst.strftime("%Y-%m-%d %H:%M:%S"))
            s += "  UTC: {} ]\n".format(self.utc.strftime("%Y-%m-%d %H:%M:%S"))
            s += "  SUN  R.A. = {:12.8f} h".format(self.vals["SUN_RA"])
            s += "  (= {:s})\n".format(self.__hour2hms(self.vals["SUN_RA"]))
            s += "  SUN  DEC. = {:12.8f} °".format(self.vals["SUN_DEC"])
            s += "  (= {:s})\n".format(self.__deg2dms(self.vals["SUN_DEC"]))
            s += "  SUN DIST. = {:12.8f} AU\n".format(self.vals["SUN_DIST"])
            s += "  SUN   hG. = {:12.8f} h".format(self.vals["SUN_H"])
            s += "  (= {:s})\n".format(self.__hour2hms(self.vals["SUN_H"]))
            s += "  SUN  S.D. = {:12.8f} ′".format(self.vals["SUN_SD"])
            s += "  (= {:s})\n".format(self.__deg2dms(self.vals["SUN_SD"] / 60))
            s += "  MOON R.A. = {:12.8f} h".format(self.vals["MOON_RA"])
            s += "  (= {:s})\n".format(self.__hour2hms(self.vals["MOON_RA"]))
            s += "  MOON DEC. = {:12.8f} °".format(self.vals["MOON_DEC"])
            s += "  (= {:s})\n".format(self.__deg2dms(self.vals["MOON_DEC"]))
            s += "  MOON H.P. = {:12.8f} °".format(self.vals["MOON_HP"])
            s += "  (= {:s})\n".format(self.__deg2dms(self.vals["MOON_HP"]))
            s += "  MOON  hG. = {:12.8f} h".format(self.vals["MOON_H"])
            s += "  (= {:s})\n".format(self.__hour2hms(self.vals["MOON_H"]))
            s += "  MOON S.D. = {:12.8f} ′".format(self.vals["MOON_SD"])
            s += "  (= {:s})\n".format(self.__deg2dms(self.vals["MOON_SD"] / 60))
            s += "         R  = {:12.8f} h".format(self.vals["R"])
            s += "  (= {:s})\n".format(self.__hour2hms(self.vals["R"]))
            s += "       EPS. = {:12.8f} °".format(self.vals["EPS"])
            s += "  (= {:s})".format(self.__deg2dms(self.vals["EPS"]))
            print(s)
        except Exception as e:
            raise

    def __hour2hms(self, hour):
        """ 99.999h -> 99h99m99s 変換

        :param float hour
        :return string: 99 h 99 m 99.999 s
        """
        try:
            h   = int(hour)
            h_r = hour - h
            m   = int(h_r * 60)
            m_r = h_r * 60 - m
            s   = m_r * 60
            return " {:02d} h {:02d} m {:06.3f} s".format(h, m, s)
        except Exception as e:
            raise

    def __deg2dms(self, deg):
        """ 99.999° -> 99°99′99″ 変換

        :param float deg
        :return string: 99 ° 99 ′ 99.999 ″
        """
        try:
            pm  = "-" if deg < 0 else " "
            if deg < 0:
                deg *= -1
            d   = int(deg)
            d_r = deg - d
            m   = int(d_r * 60)
            m_r = d_r * 60 - m
            s   = m_r * 60
            return "{:3s} ° {:02d} ′ {:06.3f} ″".format(pm + str(d), m, s)
        except Exception as e:
            raise


if __name__ == '__main__':
    try:
        obj = EphSunMoon()
        obj.exec()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
