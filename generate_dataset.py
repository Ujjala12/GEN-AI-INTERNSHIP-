import csv
import random
import os

categories = {
    "Business": [
        "Stock markets {} after {}",
        "{} announces record {} profits",
        "Oil prices {} due to {}",
        "Small businesses receive {} funding",
        "The central bank {} interest rates",
        "Investors are {} about the upcoming {}",
        "A major merger between {} and {} was announced today",
        "Tech stocks {} significantly amid {} fears",
        "Global trade {} following new {} agreements",
        "Cryptocurrency markets {} over the weekend"
    ],
    "Sports": [
        "{} wins the {} world cup after a thrilling final",
        "The football league season begins {}",
        "Star batsman scores a {} in the tournament",
        "Olympic athletes prepare for {} competition",
        "The national team {} in a stunning {} upset",
        "A controversial penalty decided the {} match",
        "{} announces retirement from professional {}",
        "The grand slam tennis final was {} by {}",
        "A new world record was set in {}",
        "The manager was sacked after {} losses"
    ],
    "Politics": [
        "Parliament passes a new {} reform bill",
        "The prime minister addressed the nation {}",
        "Election campaigns begin across the {}",
        "Government announces a new {} policy",
        "Opposition leaders {} the new {}",
        "A diplomatic summit was held in {}",
        "The local council voted to {} the {}",
        "Voter turnout was unusually {} during the {} election",
        "The president signed the {} act into law",
        "Protests erupted over the proposed {} changes"
    ],
    "Technology": [
        "Apple unveils its latest {} smartphone",
        "Researchers develop a faster {} computing chip",
        "Cybersecurity experts warn about new {} attacks",
        "Software update improves {} performance",
        "A new AI model can {} with unprecedented accuracy",
        "The tech giant faced a massive {} outage",
        "Self-driving cars achieve a new {} milestone",
        "A major vulnerability was found in {}",
        "The latest VR headset promises {} experiences",
        "Space exploration company launches a new {} satellite"
    ],
    "Health": [
        "Scientists discover a promising {} treatment",
        "Doctors recommend regular {} for better health",
        "Hospitals introduce advanced {} surgery",
        "Nutrition experts encourage {} diets",
        "A new study links {} to lower risks of {}",
        "The health ministry launched a {} vaccination drive",
        "Mental health awareness is {} in schools",
        "Researchers warn against the overuse of {}",
        "A rare disease outbreak was reported in {}",
        "New guidelines issued for {} prevention"
    ],
    "Crime": [
        "Police arrest suspects in a {} fraud case",
        "Authorities investigate a major {} network",
        "Court delivers verdict in a high-profile {} case",
        "Security forces prevent a {} attempt",
        "A serial {} was finally caught by detectives",
        "Cyber police busted a massive {} scam",
        "The jury found the defendant {} of all charges",
        "A high-speed chase ended in {} arrests",
        "Detectives are looking for clues in the {} mystery",
        "The judge sentenced the {} to {} years in prison"
    ],
    "Education": [
        "Students prepare for final {} examinations",
        "University launches a new {} learning platform",
        "Teachers attend a national {} conference",
        "Scholarships are announced for {} students",
        "The new curriculum focuses on {} and {}",
        "A school district banned {} in classrooms",
        "College tuition rates are expected to {}",
        "A famous scientist gave a guest lecture on {}",
        "The debate team won the {} championship",
        "New funding was secured for {} research facilities"
    ],
    "Entertainment": [
        "The new {} movie breaks box office records",
        "Popular singer releases a new {} album",
        "Film festival attracts international {}",
        "Award-winning actor signs a new {}",
        "The reality TV show finale sparked {}",
        "A legendary rock band announced a {} tour",
        "Critics are praising the new {} drama series",
        "The celebrity couple announced their {}",
        "A surprise guest appearance shocked the {} audience",
        "The gaming convention showcased highly anticipated {} titles"
    ],
    "Weather": [
        "Heavy rainfall causes {} in several districts",
        "The weather department predicts {} tomorrow",
        "Heatwave conditions continue across the {}",
        "Snowfall disrupts {} in mountain areas",
        "A category 5 hurricane is approaching the {}",
        "Unseasonal {} has damaged local crops",
        "A severe weather warning was issued for {}",
        "Residents are evacuated ahead of the {}",
        "Record-breaking cold temperatures hit the {}",
        "A thick fog blanketed the city causing {} delays"
    ]
}

fillers = {
    "Business": [
        ["rally", "plummet", "surge", "crash"],
        ["strong earnings", "economic uncertainty", "inflation fears", "global tensions"],
        ["tech company", "retail giant", "startup", "conglomerate"],
        ["quarterly", "annual", "surprise", "record"],
        ["surge", "drop", "stabilize", "fluctuate"],
        ["supply constraints", "geopolitical events", "high demand", "OPEC decisions"],
        ["government", "venture capital", "angel investor", "private equity"],
        ["raised", "lowered", "maintained", "paused"],
        ["optimistic", "bearish", "cautious", "bullish"],
        ["merger", "acquisition", "IPO", "earnings report"]
    ],
    "Sports": [
        ["India", "Brazil", "Germany", "Argentina", "Australia"],
        ["cricket", "football", "rugby", "hockey"],
        ["today", "next week", "in a month", "soon"],
        ["century", "hat-trick", "double-double", "record-breaking score"],
        ["international", "regional", "national", "global"],
        ["won", "lost", "drew", "was defeated"],
        ["shocking", "predictable", "historic", "massive"],
        ["championship", "semi-final", "derby", "league"],
        ["tennis", "swimming", "athletics", "basketball"],
        ["won", "dominated", "clinched", "secured"]
    ],
    "Politics": [
        ["education", "healthcare", "tax", "immigration"],
        ["today", "yesterday", "live on television", "during the summit"],
        ["country", "state", "region", "nation"],
        ["economic", "foreign", "domestic", "environmental"],
        ["criticized", "supported", "boycotted", "welcomed"],
        ["legislation", "proposal", "budget", "policy"],
        ["Geneva", "New York", "Paris", "London"],
        ["pass", "reject", "amend", "delay"],
        ["budget", "zoning laws", "funding", "regulations"],
        ["high", "low", "unprecedented", "expected"]
    ],
    "Technology": [
        ["AI-powered", "foldable", "5G", "flagship"],
        ["quantum", "neural", "silicon", "optical"],
        ["malware", "phishing", "ransomware", "DDoS"],
        ["mobile phone", "laptop", "server", "database"],
        ["translate languages", "write code", "generate art", "diagnose diseases"],
        ["cloud", "network", "server", "internet"],
        ["safety", "distance", "efficiency", "autonomous"],
        ["the operating system", "the web browser", "the firmware", "the network protocol"],
        ["immersive", "realistic", "high-resolution", "seamless"],
        ["communications", "weather", "spy", "research"]
    ],
    "Health": [
        ["cancer", "diabetes", "Alzheimer's", "heart disease"],
        ["exercise", "check-ups", "sleep", "meditation"],
        ["robotic", "minimally invasive", "laser", "microsurgery"],
        ["balanced", "plant-based", "low-carb", "Mediterranean"],
        ["poor sleep", "stress", "pollution", "processed food"],
        ["heart disease", "obesity", "hypertension", "diabetes"],
        ["polio", "flu", "COVID", "measles"],
        ["promoted", "discussed", "prioritized", "ignored"],
        ["antibiotics", "painkillers", "vitamins", "supplements"],
        ["Africa", "Asia", "Europe", "South America"]
    ],
    "Crime": [
        ["financial", "corporate", "tax", "insurance"],
        ["cybercrime", "smuggling", "drug", "trafficking"],
        ["murder", "corruption", "embezzlement", "extortion"],
        ["robbery", "hijacking", "kidnapping", "terrorist"],
        ["burglar", "arsonist", "killer", "thief"],
        ["crypto", "investment", "phishing", "lottery"],
        ["guilty", "not guilty", "innocent", "liable"],
        ["multiple", "several", "three", "five"],
        ["murder", "missing person", "heist", "robbery"],
        ["criminal", "defendant", "convict", "perpetrator"]
    ],
    "Education": [
        ["semester", "board", "entrance", "midterm"],
        ["online", "interactive", "distance", "AI-driven"],
        ["education", "teaching", "pedagogy", "STEM"],
        ["deserving", "underprivileged", "meritorious", "minority"],
        ["math", "science", "arts", "humanities"],
        ["technology", "coding", "robotics", "literature"],
        ["smartphones", "calculators", "tablets", "AI tools"],
        ["rise", "fall", "stabilize", "increase"],
        ["astrophysics", "biology", "history", "economics"],
        ["national", "state", "regional", "international"]
    ],
    "Entertainment": [
        ["superhero", "action", "comedy", "horror"],
        ["music", "pop", "rock", "jazz"],
        ["directors", "actors", "producers", "critics"],
        ["project", "movie", "series", "endorsement"],
        ["controversy", "joy", "outrage", "debate"],
        ["world", "national", "farewell", "reunion"],
        ["historical", "sci-fi", "crime", "medical"],
        ["engagement", "breakup", "pregnancy", "marriage"],
        ["live", "studio", "concert", "award show"],
        ["RPG", "FPS", "strategy", "adventure"]
    ],
    "Weather": [
        ["flooding", "landslides", "traffic jams", "power outages"],
        ["thunderstorms", "clear skies", "heavy rain", "strong winds"],
        ["region", "state", "country", "continent"],
        ["transportation", "flights", "trains", "daily life"],
        ["coast", "island", "mainland", "peninsula"],
        ["frost", "rain", "heat", "hail"],
        ["coastal areas", "the valley", "the mountains", "the plains"],
        ["storm", "flood", "wildfire", "tsunami"],
        ["midwest", "northeast", "south", "west coast"],
        ["flight", "traffic", "train", "commute"]
    ]
}


def generate_sentence(category):
    template = random.choice(categories[category])
    num_blanks = template.count("{}")
    
    if num_blanks == 0:
        return template
    
    # Try to fill blanks with random words from fillers
    fills = []
    for i in range(num_blanks):
        # Pick a random list from the category's fillers, then a random word
        filler_list = random.choice(fillers[category])
        fills.append(random.choice(filler_list))
    
    try:
        return template.format(*fills)
    except:
        return template.replace("{}", "something")


# Generate 50 articles per category
dataset = []
for cat in categories.keys():
    for _ in range(55): # generate 55 just to be safe and hit ~495 total
        sentence = generate_sentence(cat)
        dataset.append([sentence, cat])

random.shuffle(dataset)

os.makedirs('C:\\Users\\KIIT0001\\MAHASHANKH INTERNSHIP\\Semantic_Content_Classifier', exist_ok=True)

with open('C:\\Users\\KIIT0001\\MAHASHANKH INTERNSHIP\\Semantic_Content_Classifier\\news_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Text', 'Category'])
    writer.writerows(dataset)

print(f"Generated {len(dataset)} articles across {len(categories)} categories.")
