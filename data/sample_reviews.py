"""Generate a sample review dataset for demonstration."""
import pandas as pd
import random

REVIEWS = [
    # Positive
    ("The battery life on this phone is absolutely incredible. Lasts two full days!", 5, "electronics"),
    ("Camera quality is stunning. Photos come out crisp and vibrant even in low light.", 5, "electronics"),
    ("Setup was super easy and the interface is very intuitive.", 4, "electronics"),
    ("Fast delivery and the packaging was secure. Product works perfectly.", 5, "electronics"),
    ("Sound quality on these headphones is phenomenal. Deep bass, clear highs.", 5, "electronics"),
    ("The screen resolution is gorgeous. Colors are vivid and sharp.", 4, "electronics"),
    ("Customer support was incredibly helpful and resolved my issue quickly.", 5, "electronics"),
    ("Build quality feels premium. Solid and durable construction.", 4, "electronics"),
    ("The app integration works seamlessly with all my devices.", 4, "electronics"),
    ("Great value for the price. Performs as well as much more expensive models.", 5, "electronics"),
    # Negative
    ("Battery drains within 4 hours. Completely unusable for a full day.", 1, "electronics"),
    ("The charging port broke after just two weeks of normal use.", 1, "electronics"),
    ("Camera is blurry and washed out. Terrible in any lighting condition.", 2, "electronics"),
    ("Customer service was rude and unhelpful. Refused to honor the warranty.", 1, "electronics"),
    ("Device overheats constantly during normal usage. Gets dangerously hot.", 1, "electronics"),
    ("Screen cracked after a minor drop. Very fragile build quality.", 2, "electronics"),
    ("Software crashes multiple times a day. Completely unreliable.", 1, "electronics"),
    ("Bluetooth keeps disconnecting every few minutes. Very frustrating.", 2, "electronics"),
    ("The product stopped working after one month. Total waste of money.", 1, "electronics"),
    ("Volume buttons are unresponsive. Had to return the product.", 2, "electronics"),
    # Mixed
    ("Great camera but the battery life is disappointing for the price.", 3, "electronics"),
    ("Sound quality is excellent but the build feels cheap and plasticky.", 3, "electronics"),
    ("Fast performance overall but the software has some annoying bugs.", 3, "electronics"),
    ("Love the design but the charging takes forever. Over 3 hours.", 3, "electronics"),
    ("Display is beautiful but the device runs very hot under load.", 3, "electronics"),
    ("Easy to set up but customer support was slow to respond.", 3, "electronics"),
    ("Good value but the packaging was damaged on arrival.", 3, "electronics"),
    ("Excellent features but the instruction manual is confusing.", 3, "electronics"),
    ("Works well most of the time but occasionally freezes randomly.", 3, "electronics"),
    ("Nice design and good performance but the price is a bit high.", 3, "electronics"),
    # More variety
    ("Absolutely love this product! Best purchase I've made this year.", 5, "electronics"),
    ("Returned it immediately. Nothing worked as advertised.", 1, "electronics"),
    ("The WiFi connectivity is spotty and drops frequently.", 2, "electronics"),
    ("Impressive performance for the price point. Highly recommend.", 4, "electronics"),
    ("The touchscreen is unresponsive in cold weather. Major design flaw.", 2, "electronics"),
    ("Noise cancellation is top notch. Perfect for working from home.", 5, "electronics"),
    ("Arrived with a scratch on the screen. Disappointed with QC.", 2, "electronics"),
    ("Battery charges quickly and holds charge well. Very satisfied.", 4, "electronics"),
    ("The microphone picks up too much background noise during calls.", 2, "electronics"),
    ("Lightweight and comfortable to wear for long periods.", 4, "electronics"),
    ("The app crashes every time I try to sync data.", 1, "electronics"),
    ("Excellent build quality. Feels like it will last for years.", 5, "electronics"),
    ("Speaker quality is mediocre at best. Tinny and distorted at high volume.", 2, "electronics"),
    ("Very intuitive controls. No learning curve at all.", 4, "electronics"),
    ("The product description was misleading. Not what I expected.", 2, "electronics"),
    ("Waterproofing works great. Survived a full submersion.", 5, "electronics"),
    ("Buttons are stiff and hard to press. Poor ergonomics.", 2, "electronics"),
    ("Seamless pairing with all my devices. Works every time.", 4, "electronics"),
    ("The warranty process was a nightmare. Took 6 weeks to resolve.", 1, "electronics"),
    ("Incredible value. Outperforms products twice the price.", 5, "electronics"),
]

def generate_dataset(n: int = 500) -> pd.DataFrame:
    """Generate a dataset by sampling and augmenting the base reviews."""
    random.seed(42)
    rows = []
    for i in range(n):
        text, rating, category = random.choice(REVIEWS)
        # Slight variation to simulate real diversity
        rows.append({
            "review_id": i + 1,
            "text": text,
            "rating": rating,
            "category": category,
            "label": "positive" if rating >= 4 else ("negative" if rating <= 2 else "neutral"),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset(500)
    df.to_csv("reviews.csv", index=False)
    print(df["label"].value_counts())
