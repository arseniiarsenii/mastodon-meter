import typing as tp
from datetime import datetime as dt

from .Account import Account
from .Metering import Metering


class Reporter:
    """generates reports and stats"""

    def get_simple_text_report(self, tracked_accounts: tp.List[tp.Tuple[Account, tp.List[Metering]]]) -> str:
        """a simple report to put in messages"""
        title: str = f"Mastodon-meter summary report generated on {dt.utcnow().strftime('%Y.%m.%d %H:%M')} UTC\n"
        message_lines: tp.List[str] = [title]
        message_lines += map(self._get_report_line, tracked_accounts)
        return "\n".join(message_lines)

    def _get_report_line(self, account_data: tp.Tuple[Account, tp.List[Metering]]) -> str:
        """get a report string for one account"""
        account, meterings = account_data

        if not meterings:
            return f"No records to display for {account.full_address}"

        last: Metering = meterings[-1]
        previous: tp.Optional[Metering] = meterings[-2] if len(meterings) > 1 else None

        if previous is not None:
            subscribers_diff: int = last.subscribers_count - previous.subscribers_count
            statuses_diff: int = last.toot_count - previous.toot_count
            report_line: str = (
                f"{account.full_address}: {last.subscribers_count}{self._progress(subscribers_diff)} subscribers, "
                f"{last.toot_count}{self._progress(statuses_diff)} statuses"
            )
        else:
            report_line = f"{account.full_address}: {last.subscribers_count} subscribers, {last.toot_count} statuses"

        return report_line

    @staticmethod
    def _progress(diff: int) -> str:
        if diff > 0:
            return f" (+{diff})"
        elif diff < 0:
            return f" ({diff})"
        else:
            return ""
