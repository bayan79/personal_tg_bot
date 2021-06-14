from dataclasses import dataclass

import aiogram.utils.markdown as fmt

from .datamodels import Account, User


@dataclass
class AccountStocksReport:
    account: Account

    def render(self) -> str:
        stocks = self.account.stocks.sum
        balance = self.account.balance.sum
        return fmt.text(
            f"Портфель {self.account.brokerAccountType}:",
            f"\tАкции: ${stocks:.2f}",
            f"\tВалюта: ${balance:.2f}",
            f"\tИТОГО: ${stocks + balance:.2f}",
            sep='\n\t'
        )


@dataclass
class StocksReport:
    user: User

    def render(self):
        return fmt.text(*[
            fmt.text(AccountStocksReport(account=acc).render())
            for acc in self.user.accounts
        ], sep='\n')
