
import os

# 🔹 .env нужен ТОЛЬКО локально
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD=os.getenv("DB_ADMIN")
CLIENTS_PASSWORD = os.getenv("DB_CLIENTS")
PASSWORD= os.getenv("DB_MEDIA")
INFORM_PASSWORD= os.getenv("DB_INFORM")
STOCK_PASSWORD= os.getenv("DB_STOCK")
PRISE_PASSWORD=os.getenv("DB_PRISE")
PODII_PASSWORD=os.getenv("DB_PODII")
PRODUCT_PASSWORD=os.getenv("DB_PRODUCT")
NEWPRODUCT_PASSWORD=os.getenv("DB_NEWPRODUCT")
CODE_PASSWORD=os.getenv("DB_CODE")
BTN_PASSWORD=os.getenv("DB_BTN")
MANAGER_PASSWORD=os.getenv("DB_MANAGER")
ORDERS_PASSWORD=os.getenv("DB_ORDERS")




DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "annacos")



DATABASE_URL = os.getenv("DATABASE_URL")



# DATABASE_URL = (
#     f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# )
