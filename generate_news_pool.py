import json
import random

# دسته‌بندی‌های اخبار
categories = {
    "stocks": ["Tech_Stocks", "Pharma_Stocks", "Auto_Stocks", "Retail_Stocks", "Banking_Stocks", 
               "Energy_Stocks", "Airline_Stocks", "Mining_Stocks", "Real_Estate_Stocks"],
    "commodities": ["Gold", "Silver", "Oil", "Natural_Gas", "Copper", "Wheat", "Corn", "Coffee", 
                   "Sugar", "Cocoa", "Cotton", "Platinum", "Palladium"],
    "currencies": ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY"],
    "crypto": ["Bitcoin", "Ethereum", "Crypto_General"],
    "indices": ["SP500", "NASDAQ", "DOW", "FTSE", "DAX", "NIKKEI"]
}

normal_news_templates = [
    {
        "title_fa": "تحلیلگران {action} {percent}% در {sector} پیش‌بینی می‌کنند",
        "desc_fa": "تحلیلگران بازار انتظار دارند {sector} در {timeframe} آینده تغییرات قابل توجهی را تجربه کند.",
        "actions": ["رشد", "کاهش", "نوسان", "ثبات"],
        "timeframes": ["فصل", "ماه", "هفته", "سه‌ماهه"],
        "min_impact": 0.5,
        "max_impact": 10
    }
]

major_news_templates = [
    {
        "title_fa": "{event} بزرگ در {location} رخ داد",
        "desc_fa": "رویدادی بزرگ رخ داده که می‌تواند اثرات گسترده‌ای بر بازارها داشته باشد.",
        "events": ["جنگ تجاری", "بحران مالی", "انقلاب", "کودتا", "جنگ"],
        "locations": ["خاورمیانه", "آسیا", "اروپا", "آمریکا"],
        "min_impact": 5,
        "max_impact": 90
    }
]

companies = ["TechCorp", "GlobalBank", "MegaRetail"]

def generate_normal_news():
    news_list = []
    for news_id in range(1, 321):
        template = normal_news_templates[0]
        category = random.choice(list(categories.keys()))
        sector = random.choice(categories[category])
        
        impact_value = round(random.uniform(template['min_impact'], template['max_impact']), 1)
        if random.choice([True, False]) and impact_value > 0:
            impact_value = -impact_value
        
        title = template['title_fa'].replace('{action}', random.choice(template['actions']))
        title = title.replace('{percent}', str(abs(round(impact_value))))
        title = title.replace('{sector}', sector)
        
        desc = template['desc_fa'].replace('{sector}', sector)
        desc = desc.replace('{timeframe}', random.choice(template['timeframes']))
        
        news = {
            "id": f"n{news_id:03d}",
            "title": title,
            "description": desc,
            "impact": {
                sector: {
                    "min": round(impact_value * 0.8, 1),
                    "max": round(impact_value * 1.2, 1)
                }
            }
        }
        
        news_list.append(news)
    
    return news_list

def generate_major_news():
    news_list = []
    for news_id in range(1, 161):
        template = major_news_templates[0]
        impact_value = round(random.uniform(template['min_impact'], template['max_impact']), 1)
        if random.choice([True, False]):
            impact_value = -abs(impact_value)
        else:
            impact_value = abs(impact_value)
        
        title = template['title_fa'].replace('{event}', random.choice(template['events']))
        title = title.replace('{location}', random.choice(template['locations']))
        
        affected_sectors = []
        for _ in range(random.randint(2, 5)):
            category = random.choice(list(categories.keys()))
            sector = random.choice(categories[category])
            if sector not in affected_sectors:
                affected_sectors.append(sector)
        
        news = {
            "id": f"m{news_id:03d}",
            "title": title,
            "description": template['desc_fa'],
            "severity": "major",
            "impact": {}
        }
        
        for idx, sector in enumerate(affected_sectors):
            if idx == 0:
                news["impact"][sector] = {
                    "min": round(impact_value * 0.9, 1),
                    "max": round(impact_value * 1.1, 1)
                }
            else:
                secondary_impact = impact_value * random.uniform(0.3, 0.7)
                news["impact"][sector] = {
                    "min": round(secondary_impact * 0.9, 1),
                    "max": round(secondary_impact * 1.1, 1)
                }
        
        news_list.append(news)
    
    return news_list

normal_news = generate_normal_news()
major_news = generate_major_news()

news_pool = {
    "normalNews": normal_news,
    "majorNews": major_news,
    "scheduledEvents": [
        {
            "id": "se001",
            "title": "انتخابات ریاست جمهوری آمریکا",
            "description": "انتخابات مهم ریاست جمهوری که می‌تواند سیاست‌های اقتصادی را تغییر دهد.",
            "triggerDay": 90,
            "impact": {
                "USD": {"min": -15, "max": 20},
                "Stocks_General": {"min": -10, "max": 15}
            }
        }
    ]
}

with open('/workspace/data/news/news-pool.json', 'w', encoding='utf-8') as f:
    json.dump(news_pool, f, ensure_ascii=False, indent=2)

print(f"✅ تولید {len(normal_news)} خبر معمولی")
print(f"✅ تولید {len(major_news)} خبر مهم")
print(f"✅ مجموع: {len(normal_news) + len(major_news)} خبر")
