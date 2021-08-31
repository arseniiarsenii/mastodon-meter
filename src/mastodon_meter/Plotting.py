from __future__ import annotations

import os
import typing as tp
from datetime import datetime as dt
from functools import reduce

import matplotlib.pyplot as plt
from PIL import Image

from .Account import Account
from .Metering import Metering


class Plotter:
    """handles drawing plots from the provided meterings"""

    @staticmethod
    def _draw_generic_plot(
        data: tp.Tuple[tp.List[str], tp.List[int]], filename: str, title: str, x_label: str, y_label: str
    ) -> str:
        """draw a plot with provided data"""
        plt.plot(*data, marker="o")
        plt.title(title)
        subtitle: str = f"Generated on {dt.utcnow().strftime('%Y.%m.%d %H:%M')} UTC using Mastodon-meter"
        plt.suptitle(subtitle)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        dir_: str = "output"
        if not os.path.exists(dir_):
            os.mkdir(dir_)

        filename = f"{dir_}/{filename}"
        plt.savefig(filename)
        plt.clf()
        return filename

    def draw_subscribers_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot subscribers"""
        x_data: tp.List[str] = [m.timestamp.strftime("%d.%m") for m in meterings]
        y_data: tp.List[int] = [int(m.subscribers_count) for m in meterings]
        title: str = f"{account.full_address} subscribers"
        x_label: str = "Time"
        y_label: str = "Subscriber count"
        filename: str = f"{account.internal_id}-subscribers-plot-{int(dt.utcnow().timestamp())}.png"
        return self._draw_generic_plot((x_data, y_data), filename, title, x_label, y_label)

    def draw_statuses_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot status count"""
        x_data: tp.List[str] = [m.timestamp.strftime("%d.%m") for m in meterings]
        y_data: tp.List[int] = [int(m.toot_count) for m in meterings]
        title: str = f"{account.full_address} statuses"
        x_label: str = "Time"
        y_label: str = "Statuses count"
        filename: str = f"{account.internal_id}-statuses-plot-{int(dt.utcnow().timestamp())}.png"
        return self._draw_generic_plot((x_data, y_data), filename, title, x_label, y_label)

    def draw_common_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot statuses and subscribers on the same image"""
        subscribers_plot: Image = Image.open(self.draw_subscribers_plot(meterings, account))
        statuses_plot: Image = Image.open(self.draw_statuses_plot(meterings, account))
        resulting_image: Image = self._unite_images([subscribers_plot, statuses_plot])
        filename: str = f"output/{account.internal_id}-common-plot-{int(dt.utcnow().timestamp())}.png"
        resulting_image.save(filename)
        return filename

    @staticmethod
    def _unite_images(images: tp.List[Image]) -> Image:
        """make an image that has all the provided images placed on a horizontal line"""

        def _unite_two_images(image_1: Image, image_2: Image) -> Image:
            """place_two images next to each other horizontally"""
            w1, h1 = image_1.size
            w2, h2 = image_2.size
            resulting_image: Image = Image.new("RGB", (w1 + w2, max((h1, h2))))
            resulting_image.paste(image_1, (0, 0))
            resulting_image.paste(image_2, (w1, 0))
            return resulting_image

        result: Image = reduce(_unite_two_images, images)
        return result
