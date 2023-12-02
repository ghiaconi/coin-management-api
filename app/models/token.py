from .base import db, Base
from config import Config


class Token(Base):
    id = db.Column(db.String(60), primary_key=True)
    symbol = db.Column(db.String(10))
    name = db.Column(db.String(100))
    image = db.Column(db.String(255))
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.BigInteger)
    market_cap_rank = db.Column(db.Integer)
    fully_diluted_valuation = db.Column(db.BigInteger)
    total_volume = db.Column(db.BigInteger)
    high_24h = db.Column(db.Float)
    low_24h = db.Column(db.Float)
    price_change_24h = db.Column(db.Float)
    price_change_percentage_24h = db.Column(db.Float)
    market_cap_change_24h = db.Column(db.BigInteger)
    market_cap_change_percentage_24h = db.Column(db.Float)
    circulating_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    max_supply = db.Column(db.Float)
    ath = db.Column(db.Float)
    ath_change_percentage = db.Column(db.Float)
    ath_date = db.Column(db.String(30))
    atl = db.Column(db.Float)
    atl_change_percentage = db.Column(db.Float)
    atl_date = db.Column(db.String(30))
    roi = db.Column(db.JSON)
    last_updated = db.Column(db.String(30))
    sparkline_in_7d = db.Column(db.JSON)
    price_change_percentage_1h_in_currency = db.Column(db.Float)
    price_change_percentage_24h_in_currency = db.Column(db.Float)
    price_change_percentage_7d_in_currency = db.Column(db.Float)

    def serialize(self):
        return {
            'key': self.id,
            'data': {
                'key': self.id,
                'symbol': self.symbol,
                'name': self.name,
                'image': self.image,
                'current_price': self.current_price,
                'market_cap': self.market_cap,
                'market_cap_rank': self.market_cap_rank,
                'fully_diluted_valuation': self.fully_diluted_valuation,
                'total_volume': self.total_volume,
                'high_24h': self.high_24h,
                'low_24h': self.low_24h,
                'price_change_24h': self.price_change_24h,
                'price_change_percentage_24h': self.price_change_percentage_24h,
                'market_cap_change_24h': self.market_cap_change_24h,
                'market_cap_change_percentage_24h': self.market_cap_change_percentage_24h,
                'circulating_supply': self.circulating_supply,
                'total_supply': self.total_supply,
                'max_supply': self.max_supply,
                'ath': self.ath,
                'ath_change_percentage': self.ath_change_percentage,
                'ath_date': self.ath_date,
                'atl': self.atl,
                'atl_change_percentage': self.atl_change_percentage,
                'atl_date': self.atl_date,
                'roi': self.roi,
                'last_updated': self.last_updated,
                'sparkline_in_7d': self.sparkline_in_7d,
                'price_change_percentage_1h_in_currency': self.price_change_percentage_1h_in_currency,
                'price_change_percentage_24h_in_currency': self.price_change_percentage_24h_in_currency,
                'price_change_percentage_7d_in_currency': self.price_change_percentage_7d_in_currency
            }
        }

    def __repr__(self):
        return f'<Token {self.id}>'
