from __future__ import annotations

from random import shuffle
from typing import Literal

from player import Player

# ruff: noqa: E501

STICKERS = {
    "DEFAULT": {
        "h_3": "CAACAgQAAxkBAAIDgmUZ2eeA0OjKd2r2oaEiq1R0h56kAALIDwAC67XQUEkQSivH_ZX9MAQ",
        "h_4": "CAACAgQAAxkBAAIDhGUZ2fdgqjMaziYmFKKZYQpJRg-RAAKxEgACUfTRUIZ6rnSbl6dQMAQ",
        "h_5": "CAACAgQAAxkBAAIDhmUZ2gGio_m25TXkUUg5XGXx5TVtAAK3EAAC45HQUAYf4aU7V2FqMAQ",
        "h_6": "CAACAgQAAxkBAAIDiGUZ2gTdC0D7_M5lRNIYyUO3uhEUAAKNEgACp4fQUPeJ5AuFf-DrMAQ",
        "h_7": "CAACAgQAAxkBAAIDimUZ2gZyS24sh9h3ln2PGIiFESZQAAL0EAAClaDJUBbA3jHpDRPvMAQ",
        "h_8": "CAACAgQAAxkBAAIDjGUZ2glntl0I0cagQav67oayzjDnAALIEgACUH7RUM-n-MZD0nBTMAQ",
        "h_9": "CAACAgQAAxkBAAIDjmUZ2gteOKd3hBQF7fqDG-SrI0YWAAKHEgACqCbRUJbGn_qFOfuWMAQ",
        "h_10": "CAACAgQAAxkBAAIDkGUZ2g32bX0VyTdzAj-S5lk7ja75AALHEgACOi7JUKkzOeyryjVTMAQ",
        "c_3": "CAACAgQAAxkBAAIDcmUZ2Ww7uGkZ3J0PbeQfBSchfRxiAAKoEwACdL7QUALJX2zrVaB7MAQ",
        "c_4": "CAACAgQAAxkBAAIDdGUZ2X4yajpN_A_J1DedfjSlFxSIAAJCEQACvz_RUBcPg5RnVkx4MAQ",
        "c_5": "CAACAgQAAxkBAAIDdmUZ2YHutqh9Cu1rZNno_AYr_xjRAAL0EQACIUPRUJAnoP6Nlky1MAQ",
        "c_6": "CAACAgQAAxkBAAIDeGUZ2YOPXOX_GWRks9aRuL0c77ZwAAIiEgACCErIUDK5D9A34I_WMAQ",
        "c_7": "CAACAgQAAxkBAAIDemUZ2YXhYl8WA3js2e1FwE8dmdkEAAK2FAACzpTJUC2G75QxKSS-MAQ",
        "c_8": "CAACAgQAAxkBAAIDfGUZ2YcOgL8RXm3T8JTQFxEfUynoAAIBDwACuE3RUKG-tPMdJMM6MAQ",
        "c_9": "CAACAgQAAxkBAAIDfmUZ2bmkWeA9mIlAEkM4P8AHviy4AAL_DwACeTrJUHwK9QvmkCfVMAQ",
        "c_10": "CAACAgQAAxkBAAIDgGUZ2buEIVteCky2YuwOK4PoB_kyAAL_EAACliDRUMuVK8ctuYxWMAQ",
        "d_3": "CAACAgQAAxkBAAIDUGUZ1zm8hGgrtig6knIDwgvOfK7JAAImDgACd3XQUGZJHpG2ZEAyMAQ",
        "d_4": "CAACAgQAAxkBAAIDVGUZ2JSDN6nAyNvF1LzRelxCa8hGAAKyEQAChDHRUPgu7wmj3-_hMAQ",
        "d_5": "CAACAgQAAxkBAAIDVmUZ2KnBA_RWmk8MvjfvSnlN4G1_AAJrEAACGx7RUMeZvqAgPZ6pMAQ",
        "d_6": "CAACAgQAAxkBAAIDWGUZ2LXUlE5HUruYLrtliSB4xVrUAAIVEAACjfvQUL-lce085spgMAQ",
        "d_7": "CAACAgQAAxkBAAIDWmUZ2MBbL9Hqy-_qL9iVTLMmVvlFAAJvEgACf7PQUHG6hShJRY2HMAQ",
        "d_8": "CAACAgQAAxkBAAIDXGUZ2Mw5Trm80-bXHg7nIFgU0WUVAAIHFAACxmnJUI2NXIannXFSMAQ",
        "d_9": "CAACAgQAAxkBAAIDXmUZ2NVsc_76iZDwwg4xFY90PlyHAAKhDwACbcvIUArUWFietzxyMAQ",
        "d_10": "CAACAgQAAxkBAAIDYGUZ2OLPizvZl4FJu8Hh8v_yV_6jAALNDwACgPDQUEu4TmKuRgZQMAQ",
        "s_3": "CAACAgQAAxkBAAIDYmUZ2OzLzpmNmYECeEqA78-elnO9AAJUEQACqz7QUAh_TsCPurgoMAQ",
        "s_4": "CAACAgQAAxkBAAIDZGUZ2PtevTIcWcXaRY-CcFI0TSzRAAKoEQACp9jRUKy7ivjSD881MAQ",
        "s_5": "CAACAgQAAxkBAAIDZmUZ2QuATe8-L4tv9vQAAcc5G21tRgAC-g4AAuRryFB44JNX19Er7DAE",
        "s_6": "CAACAgQAAxkBAAIDaGUZ2RQPDHNojrxTTwxRx_8UGn_AAAIEEwACxqbJUDuPghH152awMAQ",
        "s_7": "CAACAgQAAxkBAAIDamUZ2SA-_y3SewtyQvfLQoBq7vUbAAIGFAAC-WTJUGsn4ar_teU1MAQ",
        "s_8": "CAACAgQAAxkBAAIDbGUZ2SygVxOz65Gqo8kaQoQEqkGWAAISDwACRODIUNAUQy1coDNgMAQ",
        "s_9": "CAACAgQAAxkBAAIDbmUZ2TfRsAozzTbDDrstHPsywhOIAAKbEQACzPHJUL7u5Q1RNjXyMAQ",
        "x_21": "CAACAgQAAxkBAAIDkmUZ2lT3Bc7GM8ikKigl_D2m29EAA6MVAAKkMNFQyqxxJnitZd8wBA",
        "x_333": "CAACAgQAAxkBAAIDlGUZ2lZ3NG1KOeTEX3_NN_mKkMNGAAK2EQACGfDRUOZTjMMsjxYiMAQ",
        "x_777": "CAACAgQAAxkBAAIDlmUZ2lizB4_q_j37m5WxPop5HwcGAAKeFAACvhLIUFeyzxBM8B3fMAQ",
        "x_7734": "CAACAgQAAxkBAAIDmGUZ2lqbStK5u2lewiBLlE2g3QGEAAKwEQACaxnJUKcFUmVLJPLrMAQ",
        "x_16": "CAACAgQAAxkBAAIDmmUZ2l0K6rADoAlP5-0stufCHDGSAAJREgACZ93RUIVrLwsVdPYdMAQ",
        "x_0": "CAACAgQAAxkBAAIDcGUZ2U5UAfUMF3u2m2o0snnupDwNAAJ9DgAC3w_JUC-XAoQfGh4hMAQ",
    },
    "OLD": {
        "h_3": "CAACAgQAAxkBAAOzXqbjq88jyiRYK0HCxnuHVAtKL40AAtEAA2FKVA1dSx3Iy3IK3xkE",
        "h_4": "CAACAgQAAxkBAAO5XqbjrcNTX8H3UH19_wNC31XGLh8AAtQAA2FKVA0OOiS308BPOhkE",
        "h_5": "CAACAgQAAxkBAAPBXqbjtC13p5rH_2IwiSvuInaV_nsAAtgAA2FKVA2Lgtx6_jM1NhkE",
        "h_6": "CAACAgQAAxkBAAPJXqbju1Kz8-UX-ytsVYPmgynIMZ4AAtwAA2FKVA3C5Pfy9dX4-xkE",
        "h_7": "CAACAgQAAxkBAAPRXqbjxP3Qxh-wEunyS4pgwm1TSgUAAuAAA2FKVA3rXOVIcwPleBkE",
        "h_8": "CAACAgQAAxkBAAPZXqbjyWKKDEQ1DApejMEz6l_wRfMAAuQAA2FKVA0Trw4HumgfPRkE",
        "h_9": "CAACAgQAAxkBAAPhXqbjzZyczpeVCGk06K_IMYOG_94AAugAA2FKVA3KYooFSMGB7RkE",
        "h_10": "CAACAgQAAxkBAAPpXqbj0oQ05f9Ar3H_09X3sFVKvJoAAuwAA2FKVA3_65EfKjenVBkE",
        "c_3": "CAACAgQAAxkBAAOtXqbjpA1sAStT8uCtGhcSEJtxXJwAAs4AA2FKVA39aBG2r0XL_hkE",
        "c_4": "CAACAgQAAxkBAAO1XqbjrHk4GYylWn5xMkWWQwFrmukAAtIAA2FKVA2hPaFq6AurSRkE",
        "c_5": "CAACAgQAAxkBAAO9XqbjsoPI2GdedcNwaNQuomS4u-cAAtYAA2FKVA13zcXRptFBiBkE",
        "c_6": "CAACAgQAAxkBAAPFXqbjuL5SlCQrb_OeSUnBoSzE5rMAAtoAA2FKVA1rzd9kfh2M_BkE",
        "c_7": "CAACAgQAAxkBAAPNXqbjv3puRGjOIJMmB1sy3L4CjtgAAt4AA2FKVA39w-bYtCjLdRkE",
        "c_8": "CAACAgQAAxkBAAPVXqbjxr4eEDYqCF8jY_s-v-fma_wAAuIAA2FKVA3mbu8th2EhAhkE",
        "c_9": "CAACAgQAAxkBAAPdXqbjy6EPmmRZLpbYDzCvndUVrf0AAuYAA2FKVA2vNZqUMsER_xkE",
        "c_10": "CAACAgQAAxkBAAPlXqbj0O2hfo-nSSXW8Qfqs63xWCgAAuoAA2FKVA1yjlRwq6Zt7hkE",
        "d_3": "CAACAgQAAxkBAAOvXqbjp28wNLAmxxsSJpXilgwwV2gAAs8AA2FKVA2iw15nVG2rtRkE",
        "d_4": "CAACAgQAAxkBAAO3XqbjrVNuIi6ZlOvQ1DYQqrW9HB4AAtMAA2FKVA12zqu3bxhQJBkE",
        "d_5": "CAACAgQAAxkBAAO_XqbjswaKyXPrJynXySiWstQNgv0AAtcAA2FKVA28NhXmJg3BKRkE",
        "d_6": "CAACAgQAAxkBAAPHXqbjuelHyqVPNiZpDmv5C76e_FgAAtsAA2FKVA3FbRkFAhwb5RkE",
        "d_7": "CAACAgQAAxkBAAPPXqbjwj_DDleTmOpKLNW7GTFVxA0AAt8AA2FKVA0437M2GEFBoRkE",
        "d_8": "CAACAgQAAxkBAAPXXqbjxyCAp2X42L-C34B2kLG4rhsAAuMAA2FKVA3NHCgpAiICKhkE",
        "d_9": "CAACAgQAAxkBAAPfXqbjzMo8PsT0Kq3apg7PGBjc5SgAAucAA2FKVA0qpC-x0GJHihkE",
        "d_10": "CAACAgQAAxkBAAPnXqbj0UnjdzWhc87_pM97BFXdDLUAAusAA2FKVA2u-e29eLE3ORkE",
        "s_3": "CAACAgQAAxkBAAOxXqbjqmlh_Xd8hA2oLjI7UwQ9_9IAAtAAA2FKVA1pm0eMORTzLRkE",
        "s_4": "CAACAgQAAxkBAAO7XqbjrjY0VjFsVHHwmMBgfz39br0AAtUAA2FKVA0rN3HXg8KPRhkE",
        "s_5": "CAACAgQAAxkBAAPDXqbjtr_H3dOCL9tpKDcfjCJgpMIAAtkAA2FKVA30DBmF6vkG7RkE",
        "s_6": "CAACAgQAAxkBAAPLXqbjvLAhVBmNy0ACnIbzrvdc5vIAAt0AA2FKVA2JJvqbjb3gWhkE",
        "s_7": "CAACAgQAAxkBAAPTXqbjxfjrMz4qJnEZYHZfKVxuQ4gAAuEAA2FKVA1p2eHNwT4LhxkE",
        "s_8": "CAACAgQAAxkBAAPbXqbjykUPcGREf1CGGUIdiJD06G4AAuUAA2FKVA2I14xWSxqhRxkE",
        "s_9": "CAACAgQAAxkBAAPjXqbjzrYR86ufjQZM_WwQicvDghgAAukAA2FKVA2s71__-M8nghkE",
        "x_21": "CAACAgQAAxkBAAMNXuLPGA6r1loi2c8EPix80dSsRLQAAu4AA2FKVA3qDTAidx882BoE",
        "x_333": "CAACAgQAAxkBAAMPXuLPMo_m6LJtBCoJEKQCZbPK9wcAAu8AA2FKVA2_-eKiP4VxnhoE",
        "x_777": "CAACAgQAAxkBAAMRXuLPUL3O4bkGxyRvO9FDI5ItDiMAAvAAA2FKVA3j7_ZjyANyTBoE",
    },
}


class Card:
    """This class represents a single card instance"""

    def __init__(
        self,
        suit: Literal["h", "s", "c", "d", "x"],
        value: Literal[3, 4, 5, 6, 7, 8, 9, 10, 21, 333, 777, 7734, 16],
        design: Literal["DEFAULT", "GALATIC", "LUXURY", "OLD"] = "DEFAULT",
    ) -> None:
        self.suit: Literal["h", "s", "c", "d", "x"] = suit
        self.icon: Literal["♥️", "♠️", "♣️", "♦️", "*"] = (
            "♥️"
            if suit == "h"
            else "♠️"
            if suit == "s"
            else "♣️"
            if suit == "c"
            else "♦️"
            if suit == "d"
            else "*"
        )
        self.value: Literal[3, 4, 5, 6, 7, 8, 9, 10, 21, 333, 777, 7734, 16] = value
        self.sticker: str = STICKERS[design][f"{self.suit}_{self.value}"]
        self.id = f"{self.suit}_{self.value}"

    def pretty(self) -> str:
        return f"{self.icon}{self.value}"

    @staticmethod
    def is_better_than(card1, card2):
        if card1.suit == "x":
            return True
        if card1.suit == card2.suit:
            return card1.value > card2.value
        return False

    @staticmethod
    def from_id(card_string: str):
        suit, value = card_string.split("_")
        return Card(suit, int(value))  # type: ignore

    def __str__(self) -> str:
        return f"{self.suit}_{self.value}"

    def __eq__(self, c: Card) -> bool:
        return str(object=self.id) == str(c.id)

    def __lt__(self, c: Card) -> bool:
        return self.value < c.value


# ? Test cards - input any set to test with only that set
# ? Do not forget to remove shuffle and
# ? remember the cards are shared from the right to the left
"""
[
    Card(h,3, design), Card(d,7, design), Card(d,6, design), Card(d,8, design),
    Card(d,4, design), Card(d,3, design), Card(h,8, design), Card(h,9, design), Card(h,10, design),
    Card(s,3, design), Card(c,3, design), Card(c,4, design), Card(c,5, design), Card(c,10, design)
]
"""


class Deck:
    """This class represents a shuffled deck of card"""

    def __init__(
        self, design: Literal["DEFAULT", "GALATIC", "LUXURY", "OLD"] = "DEFAULT"
    ):
        self.cards: list[Card] = [
            Card("h", 3, design),
            Card("d", 7, design),
            Card("d", 6, design),
            Card("d", 8, design),
            Card("d", 4, design),
            Card("d", 3, design),
            Card("h", 8, design),
            Card("h", 9, design),
            Card("h", 10, design),
            Card("s", 3, design),
            Card("c", 3, design),
            Card("c", 4, design),
            Card("c", 5, design),
            Card("c", 10, design),
        ]
        """ [
            Card("h", 3, design),
            Card("h", 4, design),
            Card("h", 5, design),
            Card("h", 6, design),
            Card("h", 7, design),
            Card("h", 8, design),
            Card("h", 9, design),
            Card("h", 10, design),
            Card("c", 3, design),
            Card("c", 4, design),
            Card("c", 5, design),
            Card("c", 6, design),
            Card("c", 7, design),
            Card("c", 8, design),
            Card("c", 9, design),
            Card("c", 10, design),
            Card("d", 3, design),
            Card("d", 4, design),
            Card("d", 5, design),
            Card("d", 6, design),
            Card("d", 7, design),
            Card("d", 8, design),
            Card("d", 9, design),
            Card("d", 10, design),
            Card("s", 3, design),
            Card("s", 4, design),
            Card("s", 5, design),
            Card("s", 6, design),
            Card("s", 7, design),
            Card("s", 8, design),
            Card("s", 9, design),
        ].copy() """
        self.design = design

    def shuffle_cards(self):
        shuffle(self.cards)

    def cut_cards(self, player: Player):
        player.hand_of_cards = self.cards[:5]
        del self.cards[:5]
