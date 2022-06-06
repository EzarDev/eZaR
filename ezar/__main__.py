from ezar.backend.config.constants import Config
from ezar.utils.ezar import Ezar


bot = Ezar()

bot.run(Config.main_token if not bot.beta else Config.beta_token)
