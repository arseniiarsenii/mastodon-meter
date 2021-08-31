import os
import typing as tp
from datetime import datetime as dt

import PIL
import matplotlib.pyplot as plt
from loguru import logger

from .Account import Account
from .Metering import Metering


class Plotter:
    """handles drawing plots from the provided meterings"""

    def __init__(self) -> None:
        pass

    @staticmethod
    @logger.catch
    def draw_plot(
        data: tp.Tuple[tp.List[str], tp.List[int]],
        filename: str,
        title: tp.Optional[str] = None,
        subtitle: tp.Optional[str] = None,
        x_label: tp.Optional[str] = None,
        y_label: tp.Optional[str] = None,
    ) -> str:
        """draw a plot with provided data"""
        plt.plot(*data, marker="o")

        if title is not None:
            plt.title(title)

        subtitle_: str = subtitle or f"Generated on {dt.utcnow().strftime('%Y.%m.%d %H:%M')} UTC using Mastodon-meter"
        plt.suptitle(subtitle_)

        if x_label is not None:
            plt.xlabel(x_label)

        if y_label is not None:
            plt.ylabel(y_label)

        dir_: str = "output"
        if not os.path.exists(dir_):
            os.mkdir(dir_)

        filename_: str = f"{dir_}/{filename}"
        plt.savefig(filename_)
        return filename_

    @logger.catch
    def draw_subscribers_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot subscribers"""
        x_data: tp.List[str] = [m.timestamp.strftime("%d.%m") for m in meterings]
        y_data: tp.List[int] = [int(m.subscribers_count) for m in meterings]
        title: str = f"{account.full_address} subscribers"
        x_label: str = "Time"
        y_label: str = "Subscriber count"
        filename: str = f"{account.internal_id}-subscribers-plot-{int(dt.utcnow().timestamp())}.png"
        return self.draw_plot((x_data, y_data), filename, title=title, x_label=x_label, y_label=y_label)

    @logger.catch
    def draw_statuses_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot status count"""
        x_data: tp.List[str] = [m.timestamp.strftime("%d.%m") for m in meterings]
        y_data: tp.List[int] = [int(m.toot_count) for m in meterings]
        title: str = f"{account.full_address} statuses"
        x_label: str = "Time"
        y_label: str = "Statuses count"
        filename: str = f"{account.internal_id}-statuses-plot-{int(dt.utcnow().timestamp())}.png"
        return self.draw_plot((x_data, y_data), filename, title=title, x_label=x_label, y_label=y_label)

    @logger.catch
    def draw_common_plot(self, meterings: tp.List[Metering], account: Account) -> str:
        """plot statuses and subscribers on the same image"""
        subscribers_plot: PIL.Image = PIL.Image.open(self.draw_subscribers_plot(meterings, account))
        statuses_plot: PIL.Image = PIL.Image.open(self.draw_statuses_plot(meterings, account))
        w1, h1 = subscribers_plot.size
        w2, _ = statuses_plot.size
        resulting_image: PIL.Image = PIL.Image.new("RGB", (w1 + w2, h1))
        resulting_image.paste(subscribers_plot, (0, 0))
        resulting_image.paste(statuses_plot, (w2, 0))
        filename: str = f"output/{account.internal_id}-common-plot-{int(dt.utcnow().timestamp())}.png"
        resulting_image.save(filename)
        return filename
